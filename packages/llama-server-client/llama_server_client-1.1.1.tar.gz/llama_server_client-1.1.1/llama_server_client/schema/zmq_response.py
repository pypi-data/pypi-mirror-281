from dataclasses import dataclass

from llama_server_client.schema import Base
from llama_server_client.schema import ZmqMessageHeader


@dataclass
class ZmqResponse(Base):
    header: ZmqMessageHeader
    body: Base
