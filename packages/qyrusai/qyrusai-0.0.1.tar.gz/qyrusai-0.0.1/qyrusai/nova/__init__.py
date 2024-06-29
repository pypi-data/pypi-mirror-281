# from nova.nova import AsyncNovaJira, AsyncNovaUserDescription
# from nova.nova import AsyncNovaJira, AsyncNovaUserDescription
from typing import Optional
from .nova import AsyncNovaJira, AsyncNovaUserDescription, SyncNovaJira, SyncNovaUserDescription


class AsyncNova:
    # def __init__(self, api_key: str, base_url: Optional[str] = None) -> None:
    def __init__(self, api_key: str) -> None:
        self.from_jira = AsyncNovaJira(api_key)
        self.from_description = AsyncNovaUserDescription(api_key)
        
class SyncNova:
    # def __init__(self, api_key: str, base_url: Optional[str] = None) -> None:
    def __init__(self, api_key: str) -> None:
        self.from_jira = SyncNovaJira(api_key)
        self.from_description = SyncNovaUserDescription(api_key)
