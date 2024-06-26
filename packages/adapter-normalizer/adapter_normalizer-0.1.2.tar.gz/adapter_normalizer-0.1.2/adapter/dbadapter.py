from typing import Any

from sqlalchemy import UUID, insert, select, update
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from adapter.models.tags import Tag


class DBAdapter:
    def __init__(self, url: str) -> None:
        self.url = url
        engine = create_async_engine(
            url,
            echo=False,
            connect_args={"server_settings": {"jit": "off"}},
        )
        self.async_session_factory = async_sessionmaker(engine, expire_on_commit=False)

    async def get_labels(self) -> list[Tag]:
        async with self.async_session_factory() as session:
            stmt = select(Tag)
            result = await session.execute(stmt)
            return result.scalars().all()

    async def get_label(self, label_id: UUID) -> Tag:
        async with self.async_session_factory() as session:
            stmt = select(Tag).where(Tag.id == label_id)
            result = await session.execute(stmt)
            return result.scalars().first()

    async def edit_label(
        self,
        label_id: UUID,
        labels: list[dict[str, Any]] | None = None,
        groups: list[dict[str, Any]] | None = None,
    ) -> None:
        values = {}
        if labels:
            values["labels"] = labels
        if groups:
            values["groups"] = groups

        async with self.async_session_factory() as session:
            stmt = update(Tag).where(Tag.id == label_id).values(**values)
            await session.execute(stmt)
            await session.commit()

        return None

    async def create_label(
        self, labels: list[dict[str, Any]], groups: list[dict[str, Any]]
    ) -> Tag:
        async with self.async_session_factory() as session:
            stmt = insert(Tag).values(labels=labels, groups=groups).returning(Tag)
            result = await session.execute(stmt)
            await session.commit()

        return result.scalars().first()
