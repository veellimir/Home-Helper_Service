import asyncio
from collections import defaultdict
from collections.abc import AsyncGenerator


class SSEManager:
    def __init__(self) -> None:
        self._connections: dict[
            int,
            set[asyncio.Queue[str]],
        ] = defaultdict(set)
        self._admin_connections: set[asyncio.Queue[str]] = set()

    async def connect(
        self,
        user_id: int,
    ) -> AsyncGenerator[str, None]:
        queue: asyncio.Queue[str] = asyncio.Queue()

        self._connections[user_id].add(queue)

        try:
            while True:
                event = await queue.get()
                yield event

        finally:
            self._connections[user_id].discard(queue)

            if not self._connections[user_id]:
                del self._connections[user_id]

    async def connect_admin(
        self,
    ) -> AsyncGenerator[str, None]:
        queue: asyncio.Queue[str] = asyncio.Queue()

        self._admin_connections.add(queue)

        try:
            while True:
                event = await queue.get()
                yield event

        finally:
            self._admin_connections.discard(queue)

    async def send_to_user(
        self,
        user_id: int,
        event: str,
    ) -> None:
        """Отправляет событие конкретному пользователю."""

        queues = self._connections.get(user_id)

        if not queues:
            return

        for queue in queues:
            await queue.put(event)

    async def send_to_admins(
        self,
        event: str,
    ) -> None:
        """Отправляет событие всем подключённым администраторам."""

        for queue in self._admin_connections:
            await queue.put(event)


sse_manager = SSEManager()