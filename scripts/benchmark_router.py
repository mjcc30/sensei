import asyncio
import json
import os
import yaml
from app.core.llm import GeminiClient
from app.agents.router import RouterAgent

# Test Cases
TEST_CASES = [
    ("how to pwn wifi", "RED"),
    ("what is a firewall", "NOVICE"),
    ("scan 192.168.1.1", "ACTION"),
    ("hello sensei", "CASUAL"),
    ("decrypt this md5 hash", "CRYPTO"),
    ("aws s3 bucket public exploit", "CLOUD"), # Should be CLOUD or RED
    ("why podman is failing", "SYSTEM")
]

async def run_benchmark():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ ERROR: GEMINI_API_KEY not set.")
        return

    client = GeminiClient(api_key)

    # 1. Load V1 Prompt (Default from Code)
    router_v1 = RouterAgent(client) # Uses DEFAULT_PROMPT inside class
    
    # 2. Load V2 Prompt (From prompts.yaml)
    try:
        with open("prompts.yaml", "r") as f:
            config = yaml.safe_load(f)
            prompt_v2_text = config["agents"]["router"]["prompt"]
            router_v2 = RouterAgent(client, prompt_template=prompt_v2_text)
            print("✅ Loaded V2 Prompt from prompts.yaml")
    except Exception as e:
        print(f"⚠️ Could not load prompts.yaml ({e}). Using V1 only.")
        router_v2 = None

    print("\n" + "="*100)
    print(f"{ 'QUERY':<30} | {'EXPECTED':<8} | {'V1 CAT':<8} | {'V2 CAT':<8} | {'V2 REPHRASE (Snippet)'}")
    print("="*100)

    for query, expected in TEST_CASES:
        # Run V1
        res1 = await router_v1.process(query)
        cat1 = res1.get("category", "ERR")
        
        # Run V2
        cat2 = "N/A"
        rephrase2 = ""
        if router_v2:
            res2 = await router_v2.process(query)
            cat2 = res2.get("category", "ERR")
            rephrase2 = res2.get("enhanced_query", "")

        # Scoring
        mark1 = "✅" if cat1 == expected else "❌"
        mark2 = "✅" if cat2 == expected else "❌"
        
        # Special check for overlapping categories (RED/CLOUD)
        if expected == "CLOUD" and cat2 == "RED": mark2 = "✅ (RED)"

        print(f"{query:<30} | {expected:<8} | {mark1} {cat1:<6} | {mark2} {cat2:<6} | {rephrase2[:40]}...")

    print("="*100)

if __name__ == "__main__":
    asyncio.run(run_benchmark())
