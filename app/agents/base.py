from abc import ABC, abstractmethod
from ..core.llm import GeminiClient
from ..core.a2a import bus, AgentMessage
import uuid

class BaseAgent(ABC):
    def __init__(self, client: GeminiClient, agent_id: str = None):
        self.client = client
        self.id = agent_id or f"{self.__class__.__name__}-{str(uuid.uuid4())[:8]}"
        self.bus = bus
        
        # Register to the bus
        self.bus.register(self.id, self.receive_message)

    async def send_message(self, recipient_id: str, content: dict, msg_type: str = "request"):
        """Sends a message via the A2A bus."""
        msg = AgentMessage(
            sender=self.id,
            recipient=recipient_id,
            message_type=msg_type,
            content=content
        )
        await self.bus.send(msg)

    async def receive_message(self, message: AgentMessage):
        """Callback when a message is received from the bus."""
        # Default behavior: log or ignore. subclasses should override.
        pass

    @abstractmethod
    async def process(self, input_text: str) -> str:
        """Main processing logic for the agent."""
        pass