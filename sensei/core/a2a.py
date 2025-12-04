from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Callable, Awaitable
import uuid
import time
import asyncio

@dataclass
class AgentMessage:
    sender: str
    recipient: str  # "broadcast" or specific Agent ID
    message_type: str  # "request", "response", "event"
    content: Dict[str, Any]
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: float = field(default_factory=time.time)

class AgentBus:
    """
    Central Message Bus for Agent-to-Agent (A2A) communication.
    Acts as a router for messages between agents.
    """
    def __init__(self):
        # Map agent_id -> callback function
        self._subscribers: Dict[str, Callable[[AgentMessage], Awaitable[None]]] = {}
        self._history: List[AgentMessage] = []

    def register(self, agent_id: str, callback: Callable[[AgentMessage], Awaitable[None]]):
        """Registers an agent on the bus."""
        self._subscribers[agent_id] = callback
        print(f"[Bus] Agent registered: {agent_id}")

    async def send(self, message: AgentMessage):
        """Routes a message to its recipient."""
        self._history.append(message)
        
        if message.recipient == "broadcast":
            # Send to everyone except sender
            tasks = []
            for aid, callback in self._subscribers.items():
                if aid != message.sender:
                    tasks.append(callback(message))
            if tasks:
                await asyncio.gather(*tasks)
        
        elif message.recipient in self._subscribers:
            # Point-to-Point
            await self._subscribers[message.recipient](message)
        else:
            print(f"[Bus] Warning: Recipient '{message.recipient}' not found.")

# Global instance for simplicity in this V2 prototype
bus = AgentBus()
