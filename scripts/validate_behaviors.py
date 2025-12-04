import asyncio
import sys
from unittest.mock import MagicMock, patch

# Add project root to path
sys.path.append(".")

from app.agents.orchestrator import Orchestrator
from app.core.llm import GeminiClient

# Mock Responses for the Router to force classification
ROUTER_MOCKS = {
    "hello": '{"category": "CASUAL", "enhanced_query": "hello"}',
    "hack wifi": '{"category": "RED", "enhanced_query": "audit wifi security"}',
    "scan localhost": '{"category": "ACTION", "enhanced_query": "scan localhost"}',
    "podman status": '{"category": "SYSTEM", "enhanced_query": "check podman status"}',
    "explain dns": '{"category": "NOVICE", "enhanced_query": "explain dns"}',
    "analyze malware": '{"category": "BLUE", "enhanced_query": "analyze malware"}',
    "aws buckets": '{"category": "CLOUD", "enhanced_query": "audit aws buckets"}',
    "decrypt md5": '{"category": "CRYPTO", "enhanced_query": "crack md5"}'
}

async def mock_generate(user_input, system_prompt=None, *args, **kwargs):
    # GeminiClient.generate signature is (text, system_prompt, ...)
    # Check if this is a Router call (system_prompt contains classification instructions)
    
    if system_prompt and "Classify it into" in system_prompt:
        user_input_lower = user_input.lower()
        for key, json_resp in ROUTER_MOCKS.items():
            if key in user_input_lower:
                return json_resp
        return '{"category": "CASUAL", "enhanced_query": "default"}'
    
    # Agent Response
    return "I am the Agent responding."

async def run_validation():
    print("🧪 Starting Behavior Validation...\n")
    
    # Mock the LLM Client
    with patch("app.agents.orchestrator.GeminiClient") as MockClient:
        mock_client_instance = MockClient.return_value
        mock_client_instance.generate.side_effect = mock_generate
        
        # Mock System Tools to avoid real execution
        with patch("app.tools.system.SystemTool.run", return_value="[System Tool Output]"):
            with patch("app.tools.nmap.NmapTool.run", return_value="[Nmap Output]"):
                
                orch = Orchestrator("dummy_key")
                
                scenarios = [
                    ("Greeting", "Hello Sensei", "CASUAL"),
                    ("Offensive", "How to hack wifi", "RED"),
                    ("Action", "Scan localhost", "ACTION"),
                    ("System", "Check podman status", "SYSTEM"),
                    ("Education", "Explain DNS", "NOVICE"),
                    ("Defensive", "Analyze malware", "BLUE"),
                    ("Cloud", "Check AWS buckets", "CLOUD"),
                    ("Crypto", "Decrypt MD5", "CRYPTO"),
                ]

                for name, query, expected_agent_key in scenarios:
                    print(f"► Testing Scenario: {name} ('{query}')")
                    
                    # Spy on the router process to see what it returns
                    # But since we mocked generate, we rely on the orchestrator's internal state or logs?
                    # Actually, let's just run it and see if it crashes, and maybe inspect which agent was called.
                    # To do that strictly, we'd need to spy on specific agents.
                    
                    response = await orch.handle_request(query)
                    
                    # Check if the response tag matches the expected agent ID pattern
                    # The Orchestrator returns "[Agent-ID] Response"
                    # Our Agent IDs in Orchestrator are like "Novice-1", "RedTeam-1", "Action-1", etc.
                    
                    expected_id_part = expected_agent_key.title() 
                    if expected_agent_key == "RED": expected_id_part = "RedTeam"
                    if expected_agent_key == "BLUE": expected_id_part = "BlueTeam"
                    
                    # Special case mappings in Orchestrator dict
                    # "RED" -> RedTeam-1
                    # "BLUE" -> BlueTeam-1
                    # "CLOUD" -> Cloud-1
                    # "CRYPTO" -> Crypto-1
                    # "OSINT" -> Osint-1
                    # "SYSTEM" -> System-1
                    # "ACTION" -> Action-1
                    # "NOVICE" -> Novice-1
                    # "CASUAL" -> Casual-1
                    
                    if expected_id_part.upper() in response.upper():
                         print(f"  ✅ Routed to {expected_agent_key} Correctly. Response: {response[:50]}...")
                    else:
                         print(f"  ❌ Wrong Route! Expected {expected_agent_key}, got response: {response}")

    print("\n✨ Validation Complete.")

if __name__ == "__main__":
    asyncio.run(run_validation())
