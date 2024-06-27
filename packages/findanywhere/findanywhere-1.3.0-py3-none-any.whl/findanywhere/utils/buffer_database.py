from collections.abc import Sequence
from dataclasses import asdict, dataclass
from functools import partial
from operator import itemgetter, attrgetter
from pathlib import Path
from typing import TypeVar, Generic, Protocol, ClassVar, Any

from dacite import from_dict
from sqlalchemy import Integer, String, JSON, Engine, create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker, mapped_column, Mapped
from toolz import compose


class Base(DeclarativeBase):
    pass


class Position(Base):
    __tablename__ = 'position'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    path: Mapped[str] = mapped_column(String)
    data: Mapped[JSON] = mapped_column(JSON)


class _Dataclass(Protocol):
    __dataclass_fields__: ClassVar[dict[str, Any]]


_T = TypeVar('_T', bound=_Dataclass)


class BufferDatabase(Generic[_T]):

    def __init__(self, path: Path, data_type: type[_T]):
        self._db_url: str = path.joinpath(
            'buffer.sqlite'
        ).absolute().as_uri().replace('file://', 'sqlite:///')
        self._engine: Engine = create_engine(self._db_url)
        self._create_session: sessionmaker = sessionmaker(self._engine)
        self._counter: int = 0
        self._type: type[_T] = data_type
        Base.metadata.create_all(self._engine, checkfirst=True)


    def add_entry(self, path: str, entry: _T):
        with self._create_session() as session:
            session.add(Position(id=self._counter, path=path, data=asdict(entry)))
            session.commit()
        self._counter += 1

    def get_unique_paths(self) -> Sequence[str]:
        with self._create_session() as session:
            return sorted(map(itemgetter(0), session.query(Position.path.distinct())))

    def get_all_with_path(self, path: str) -> Sequence[_T]:

        with self._create_session() as session:
            return list(
                map(
                    compose(partial(from_dict, self._type), attrgetter('data')),
                    session.query(Position).filter(Position.path == path).order_by(Position.id)
                )
            )
