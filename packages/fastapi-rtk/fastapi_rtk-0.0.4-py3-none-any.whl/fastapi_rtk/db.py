import contextlib
import json
from abc import ABC, abstractmethod
from typing import Any, AsyncIterator, Literal

from fastapi import Depends, HTTPException
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy import Select, func, select
from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import selectinload

from .filters import BaseFilter
from .model import metadata, metadatas
from .models import Model, OAuthAccount, User
from .schemas import PRIMARY_KEY, FilterSchema


class UserDatabase(SQLAlchemyUserDatabase):
    def get_by_username(self, username: str) -> User | None:
        statement = select(self.user_table).where(
            func.lower(self.user_table.username) == func.lower(username)
        )
        return self._get_user(statement)


class BaseQueryManager(ABC):
    """
    Abstract base class for query managers.

    This class defines the interface for query managers that interact with the database.

    Attributes:
        None

    Methods:
        add_options(db: AsyncSession, **kwargs):
            Adds options for pagination and ordering to the query.

        join(column: str):
            Abstract method to join a column in the query.

        page(page: int, page_size: int):
            Abstract method to paginate the query results.

        order_by(column: str, direction: str):
            Abstract method to order the query results by a specific column.

        where(column: str, value: Any):
            Abstract method to filter the query results based on a specific column and value.

        where_in(column: str, values: list[Any]):
            Abstract method to filter the query results based on a specific column and a list of values.

        where_id(id: PRIMARY_KEY):
            Abstract method to filter the query results based on the primary key.

        where_id_in(ids: list[PRIMARY_KEY]):
            Abstract method to filter the query results based on a list of primary keys.

        filter(db: AsyncSession, filter: FilterSchema):
            Abstract method to apply a filter to the query.

        filter_class(col: str, filter_class: BaseFilter, value: Any):
            Abstract method to apply a filter class to the query.

        count(db: AsyncSession, filters: list[FilterSchema] = [], filter_classes: list[tuple[str, BaseFilter, Any]] = []) -> int:
            Abstract method to count the number of query results.

        execute(db: AsyncSession, many=True) -> Model | list[Model] | None:
            Abstract method to execute the query and return the results.

        yield_per(db: AsyncSession, page_size: int):
            Abstract method to yield query results in batches.

        _init_query():
            Abstract method to initialize the query.

    """

    async def add_options(
        self,
        db: AsyncSession,
        *,
        join_columns: list[str] = [],
        page: int | None = None,
        page_size: int | None = None,
        order_column: str | None = None,
        order_direction: str | None = None,
        where: tuple[str, Any] | None = None,
        where_in: tuple[str, list[Any]] | None = None,
        where_id: PRIMARY_KEY | None = None,
        where_id_in: list[PRIMARY_KEY] | None = None,
        filters: list[FilterSchema] = [],
        filter_classes: list[tuple[str, BaseFilter, Any]] = [],
    ):
        """
        Adds options for pagination and ordering to the query.

        Args:
            db (AsyncSession): The async db object for the database connection.
            join_columns (list[str], optional): The list of columns to join. Use attribute from the model itself. Defaults to [].
            page (int): The page number. If None, no pagination is applied. Defaults to None.
            page_size (int): The number of items per page. If None, no pagination is applied. Defaults to None.
            order_column (str | None): The column to order by. If None, no ordering is applied. Defaults to None.
            order_direction (str | None): The direction of the ordering. If None, no ordering is applied. Defaults to None.
            where (tuple[str, Any], optional): The column name and value to apply the WHERE clause on. Defaults to None.
            where_in (tuple[str, list[Any]], optional): The column name and list of values to apply the WHERE IN clause on. Defaults to None.
            where_id (PRIMARY_KEY, optional): The primary key value to apply the WHERE clause on. Defaults to None.
            where_id_in (list[PRIMARY_KEY], optional): The list of primary key values to apply the WHERE IN clause on. Defaults to None.
            filters (list[FilterSchema], optional): The list of filters to apply to the query. Defaults to [].
            filter_classes (list[tuple[str, BaseFilter, Any]], optional): The list of filter classes to apply to the query. Defaults to [].
        """
        for col in join_columns:
            self.join(col)
        if page is not None and page_size is not None:
            self.page(page, page_size)
        if order_column and order_direction:
            self.order_by(order_column, order_direction)
        if where:
            self.where(*where)
        if where_in:
            self.where_in(*where_in)
        if where_id:
            self.where_id(where_id)
        if where_id_in:
            self.where_id_in(where_id_in)
        for filter in filters:
            await self.filter(db, filter)
        for col, filter_class, value in filter_classes:
            self.filter_class(col, filter_class, value)

    @abstractmethod
    def page(self, page: int, page_size: int):
        pass

    @abstractmethod
    def order_by(self, column: str, direction: str):
        pass

    @abstractmethod
    def join(self, column: str):
        pass

    @abstractmethod
    def where(self, column: str, value: Any):
        pass

    @abstractmethod
    def where_in(self, column: str, values: list[Any]):
        pass

    @abstractmethod
    def where_id(self, id: PRIMARY_KEY):
        pass

    @abstractmethod
    def where_id_in(self, ids: list[PRIMARY_KEY]):
        pass

    @abstractmethod
    async def filter(self, db: AsyncSession, filter: FilterSchema):
        pass

    @abstractmethod
    def filter_class(self, col: str, filter_class: BaseFilter, value: Any):
        pass

    @abstractmethod
    async def count(
        self,
        db: AsyncSession,
        filters: list[FilterSchema] = [],
        filter_classes: list[tuple[str, BaseFilter, Any]] = [],
    ) -> int:
        pass

    @abstractmethod
    async def execute(self, db: AsyncSession, many=True) -> Model | list[Model] | None:
        pass

    @abstractmethod
    async def yield_per(self, db: AsyncSession, page_size: int):
        pass

    @abstractmethod
    def _init_query(self):
        pass


class QueryManager(BaseQueryManager):
    """
    A class to manage database queries. It provides methods to add options for pagination, ordering, and filtering to the query.

    Raises:
        e: If an error occurs during query execution.
    """

    datamodel: Any
    stmt: Select
    _joined_columns: list[Model] = []

    def __init__(self, datamodel: Any) -> None:
        self.datamodel = datamodel
        self._init_query()

    def join(self, column: str):
        """
        Joins a column in the query.

        Args:
            column (str): The column to join.

        Returns:
            None
        """
        col = getattr(self.datamodel.obj, column)
        self.stmt = self.stmt.options(selectinload(col))

    def page(self, page: int, page_size: int):
        """
        Paginates the query results.

        Args:
            page (int): The page number.
            page_size (int): The number of items per page.

        Returns:
            None
        """
        self.stmt = self.stmt.offset(page * page_size).limit(page_size)

    def order_by(self, column: str, direction: str):
        """
        Orders the query results by a specific column.

        Args:
            column (str): The column to order by.
            direction (str): The direction of the ordering.

        Returns:
            None
        """
        col = column

        #! If the order column comes from a request, it will be in the format ClassName.column_name
        if col.startswith(self.datamodel.obj.__class__.__name__):
            col = col.split(".", 1)[1]

        # if there is . in the column name, it means it is a relation column
        if "." in col:
            rel, col = col.split(".")
            rel_obj = self.datamodel.get_related_model(rel)
            col = getattr(rel_obj, col)
        else:
            col = getattr(self.datamodel.obj, col)
        if direction == "asc":
            self.stmt = self.stmt.order_by(col)
        else:
            self.stmt = self.stmt.order_by(col.desc())

    def where(self, column: str, value: Any):
        """
        Apply a WHERE clause to the query.

        Args:
            column (str): The column name to apply the WHERE clause on.
            value (Any): The value to compare against in the WHERE clause.
        """
        column = getattr(self.datamodel.obj, column)
        self.stmt = self.stmt.where(column == value)

    def where_in(self, column: str, values: list[Any]):
        """
        Apply a WHERE IN clause to the query.

        Args:
            column (str): The column name to apply the WHERE IN clause on.
            values (list[Any]): The list of values to compare against in the WHERE IN clause.
        """
        column = getattr(self.datamodel.obj, column)
        self.stmt = self.stmt.where(column.in_(values))

    def where_id(self, id: PRIMARY_KEY):
        """
        Adds a WHERE clause to the query based on the primary key.

        Parameters:
        - id: The primary key value to filter on.
        """
        pk_dict = self._convert_id_into_dict(id)
        for col, val in pk_dict.items():
            self.where(col, val)

    def where_id_in(self, ids: list[PRIMARY_KEY]):
        """
        Filters the query by a list of primary key values.

        Args:
            ids (list): A list of primary key values.

        Returns:
            None
        """
        to_apply_dict = {}
        for id in self.datamodel.get_pk_attrs():
            to_apply_dict[id] = []

        pk_dicts = [self._convert_id_into_dict(id) for id in ids]
        for pk_dict in pk_dicts:
            for col, val in pk_dict.items():
                to_apply_dict[col].append(val)

        for col, vals in to_apply_dict.items():
            self.where_in(col, vals)

    async def filter(self, db: AsyncSession, filter: FilterSchema):
        """
        Apply a filter to the query.

        Args:
            db (AsyncSession): The async db object for the database connection.
            filter (FilterSchema): The filter to apply to the query.
        """
        filter_classes = self.datamodel._filters.get(filter.col)
        filter_class = None
        for f in filter_classes:
            if f.arg_name == filter.opr:
                filter_class = f
                break
        if not filter_class:
            raise HTTPException(
                status_code=400, detail=f"Invalid filter opr: {filter.opr}"
            )

        col = getattr(self.datamodel.obj, filter.col)
        value = filter.value

        # If it is a relation column, we need to join the relation
        if self.datamodel.is_relation(filter.col):
            rel_interface = self.datamodel.get_related_interface(filter.col)
            if self.datamodel.is_relation_one_to_one(
                filter.col
            ) or self.datamodel.is_relation_many_to_one(filter.col):
                query = QueryManager(rel_interface)
                query.where_id(value)
                value = await query.execute(db, many=False)
            else:
                query.where_id_in(value)
                value = await query.execute(db)

        self.stmt = filter_class.apply(self.stmt, col, value)

    def filter_class(self, col: str, filter_class: BaseFilter, value: Any):
        """
        Apply a filter class to the query.

        Args:
            col (str): The column to apply the filter class on.
            filter_class (BaseFilter): The filter class to apply to the query.
            value (Any): The value to compare against in the filter class.
        """
        # If there is . in the column name, it means it should filter on a related table
        if "." in col:
            rel, col = col.split(".")
            rel_obj = self.datamodel.get_related_model(rel)
            if rel_obj not in self._joined_columns:
                self.stmt = self.stmt.join(rel_obj)
                self._joined_columns.append(rel_obj)
            col = getattr(rel_obj, col)
        else:
            col = getattr(self.datamodel.obj, col)

        self.stmt = filter_class.apply(self.stmt, col, value)

    async def count(
        self,
        db: AsyncSession,
        filters: list[FilterSchema] = [],
        filter_classes: list[tuple[str, BaseFilter, Any]] = [],
    ) -> int:
        """
        Counts the number of records in the database table.
        The query is reset before and after execution.

        Args:
            db (AsyncSession): The async db object for the database connection.
            filters (list[FilterSchema], optional): The list of filters to apply to the query. Defaults to [].
            filter_classes (list[tuple[str, BaseFilter, Any]], optional): The list of filter classes to apply to the query. Defaults to [].

        Returns:
            int: The number of records in the table.
        """
        try:
            self._init_query()
            for filter in filters:
                await self.filter(db, filter)
            for col, filter_class, value in filter_classes:
                self.filter_class(col, filter_class, value)
            stmt = select(func.count()).select_from(self.stmt.subquery())
            result = await db.execute(stmt)
            return result.scalar() or 0
        finally:
            self._init_query()

    async def execute(self, db: AsyncSession, many=True) -> Model | list[Model] | None:
        """
        Executes the database query using the provided db.
        After execution, the query is reset to its initial state.

        Args:
            db (AsyncSession): The async db object for the database connection.
            many (bool, optional): Indicates whether the query should return multiple results or just the first result. Defaults to True.

        Returns:
            Model | list[Model] | None: The result of the query.

        Raises:
            Exception: If an error occurs during query execution.
        """
        try:
            result = await db.execute(self.stmt)
            if many:
                return result.scalars().all()

            return result.scalars().first()
        except Exception as e:
            await db.rollback()
            raise e
        finally:
            self._init_query()

    async def yield_per(self, db: AsyncSession, page_size: int):
        """
        Executes the database query using the provided db and yields results in batches of the specified size.
        After execution, the query is reset to its initial state.

        Note: PLEASE ALWAYS CLOSE THE DB AFTER USING THIS METHOD

        Args:
            db (AsyncSession): The async db object for the database connection.
            page_size (int): The number of items to yield per batch.

        Returns:
            Generator[Sequence, None, None]: A generator that yields results in batches of the specified size.
        """
        try:
            self.stmt = self.stmt.execution_options(stream_results=True)
            result = await db.stream(self.stmt)
            while True:
                chunk = await result.scalars().fetchmany(page_size)
                if not chunk:
                    break
                yield chunk
        finally:
            self._init_query()

    def _init_query(self):
        self.stmt = select(self.datamodel.obj)
        self._joined_columns = []

    def _convert_id_into_dict(self, id: PRIMARY_KEY) -> dict[str, Any]:
        """
        Converts the given ID into a dictionary format.

        Args:
            id (PRIMARY_KEY): The ID to be converted.

        Returns:
            dict[str, Any]: The converted ID in dictionary format.

        Raises:
            HTTPException: If the ID is invalid.
        """
        pk_dict = {}
        if self.datamodel.is_pk_composite():
            try:
                # Assume the ID is a JSON string
                id = json.loads(id) if isinstance(id, str) else id
                for col, val in id.items():
                    pk_dict[col] = val
            except Exception:
                raise HTTPException(status_code=400, detail="Invalid ID")
        else:
            pk_dict[self.datamodel.get_pk_attr()] = id

        return pk_dict


class BaseDatabaseSessionManager(ABC):
    """
    Abstract base class for database session managers.

    This class defines the interface for managing database sessions and connections.

    Attributes:
        None

    Methods:
        init_db(url: str, binds: dict[str, str] | None = None):
            Abstract method to initialize the database engine and session maker.

        close():
            Abstract method to close the database engine and session maker.

        connect() -> AsyncIterator[AsyncConnection]:
            Abstract method to establish a connection to the database.

        session() -> AsyncIterator[AsyncSession]:
            Abstract method to provide a database session for performing database operations.

        create_all(connection: AsyncConnection):
            Abstract method to create all tables in the database.

        drop_all(connection: AsyncConnection):
            Abstract method to drop all tables in the database.
    """

    @abstractmethod
    def init_db(self, url: str, binds: dict[str, str] | None = None):
        pass

    @abstractmethod
    async def close(self):
        pass

    @abstractmethod
    async def connect(self, bind: str | None = None) -> AsyncIterator[AsyncConnection]:
        pass

    @abstractmethod
    async def session(self, bind: str | None = None) -> AsyncIterator[AsyncSession]:
        pass

    @abstractmethod
    async def create_all(self, binds: list[str] | Literal["all"] | None = "all"):
        pass

    @abstractmethod
    async def drop_all(self, binds: list[str] | Literal["all"] | None = "all"):
        pass


class DatabaseSessionManager(BaseDatabaseSessionManager):

    _engine: AsyncEngine | None = None
    _async_sessionmaker: async_sessionmaker[AsyncSession] | None = None
    _engine_dict: dict[str, AsyncEngine] = None
    _async_sessionmaker_dict: dict[str, async_sessionmaker[AsyncSession]] = None

    def init_db(self, url: str, binds: dict[str, str] | None = None):
        """
        Initializes the database engine and session maker.

        Args:
            url (str): The URL of the database.
            binds (dict[str, str] | None, optional): Additional database URLs to bind to. Defaults to None.
        """
        self._engine = create_async_engine(url)
        self._async_sessionmaker = async_sessionmaker(
            bind=self._engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

        if binds:
            self._engine_dict = {}
            self._async_sessionmaker_dict = {}
            for key, value in binds.items():
                self._engine_dict[key] = create_async_engine(value)
                self._async_sessionmaker_dict[key] = async_sessionmaker(
                    bind=self._engine_dict[key],
                    class_=AsyncSession,
                    expire_on_commit=False,
                )

    async def close(self):
        """
        Closes the database engine and session maker.

        Raises:
            Exception: If the database engine is not initialized.

        Returns:
            None
        """
        if not self._engine:
            raise Exception("Database engine is not initialized")
        await self._engine.dispose()
        self._engine = None
        self._async_sessionmaker = None

        if self._engine_dict:
            for engine in self._engine_dict.values():
                await engine.dispose()
            self._engine_dict = None
            self._async_sessionmaker_dict = None

    @contextlib.asynccontextmanager
    async def connect(self, bind: str | None = None) -> AsyncIterator[AsyncConnection]:
        """
        Establishes a connection to the database.

        Args:
            bind (str, optional): The database URL to bind to. If none, the default database is used. Defaults to None.

        Raises:
            Exception: If the DatabaseSessionManager is not initialized.

        Yields:
            AsyncConnection: The database connection.

        Returns:
            None
        """
        if bind:
            if self._engine_dict is None:
                raise Exception("DatabaseSessionManager is not initialized")
            async with self._engine_dict[bind].begin() as connection:
                try:
                    yield connection
                except Exception:
                    await connection.rollback()
                    raise
        else:
            if self._engine is None:
                raise Exception("DatabaseSessionManager is not initialized")
            async with self._engine.begin() as connection:
                try:
                    yield connection
                except Exception:
                    await connection.rollback()
                    raise

    @contextlib.asynccontextmanager
    async def session(self, bind: str | None = None) -> AsyncIterator[AsyncSession]:
        """
        Provides a database session for performing database operations.

        Args:
            bind (str, optional): The database URL to bind to. If none, the default database is used. Defaults to None.

        Raises:
            Exception: If the DatabaseSessionManager is not initialized.

        Yields:
            AsyncSession: The database session.

        Returns:
            None
        """
        if bind:
            if self._async_sessionmaker_dict is None:
                raise Exception("DatabaseSessionManager is not initialized")
            session = self._async_sessionmaker_dict[bind]()
            try:
                yield session
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()
        else:
            if self._async_sessionmaker is None:
                raise Exception("DatabaseSessionManager is not initialized")
            session = self._async_sessionmaker()
            try:
                yield session
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()

    # Used for testing
    async def create_all(self, binds: list[str] | Literal["all"] | None = "all"):
        """
        Creates all tables in the database.

        Args:
            binds (list[str] | Literal["all"] | None, optional): The database URLs to create tables in. Defaults to "all".
        """
        async with self.connect() as connection:
            await connection.run_sync(metadata.create_all)

        if not self._engine_dict or not binds:
            return

        bind_keys = self._engine_dict.keys() if binds == "all" else binds
        for key in bind_keys:
            async with self.connect(key) as connection:
                await connection.run_sync(metadatas[key].create_all)

    async def drop_all(self, binds: list[str] | Literal["all"] | None = "all"):
        """
        Drops all tables in the database.

        Args:
            binds (list[str] | Literal["all"] | None, optional): The database URLs to drop tables in. Defaults to "all".
        """
        async with self.connect() as connection:
            await connection.run_sync(metadata.drop_all)

        if not self._engine_dict or not binds:
            return

        bind_keys = self._engine_dict.keys() if binds == "all" else binds
        for key in bind_keys:
            async with self.connect(key) as connection:
                await connection.run_sync(metadatas[key].drop_all)


session_manager = DatabaseSessionManager()


def get_db(bind: str | None = None):
    """
    A coroutine function that returns a function that yields a database session.

    Can be used as a dependency in FastAPI routes.

    Args:
        bind (str, optional): The database URL to bind to. If None, the default database is used. Defaults to None.

    Returns:
        AsyncIterator[AsyncSession]: An async generator that yields a database session.

    Usage:
    ```python
        async with get_db()() as session:
            # Use the session to interact with the database

        # or

        @app.get("/items/")
        async def read_items(session: AsyncSession = Depends(get_db())):
            # Use the session to interact with the database
    ```
    """

    async def get_db_dependency():
        async with session_manager.session(bind) as session:
            yield session

    return get_db_dependency


async def get_user_db(db: AsyncSession = Depends(get_db(User.__bind_key__))):
    """
    A dependency for FAST API to get the UserDatabase instance.

    Parameters:
    - db: The async db object for the database connection.

    Yields:
    - UserDatabase: An instance of the UserDatabase class.

    """
    yield UserDatabase(db, User, OAuthAccount)
