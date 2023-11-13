import logging

from aiopg.sa import create_engine
from sqlalchemy.dialects.postgresql import insert

from src.infrastructure.sql_client.exceptions import DbEngineNotInitialized
from src.infrastructure.sql_client.upsert_command import UpsertCommand

logger = logging.getLogger(__name__)


class SqlClient:
    def __init__(self, connection_parameters: dict):
        self.connection_parameters = connection_parameters
        self.db_engine = None

    async def start(self):
        logger.info(
            'Initializing database engine with params: %s', self.connection_parameters
        )
        self.db_engine = await create_engine(**self.connection_parameters)
        async with self.db_engine.acquire() as conn:
            await conn.execute("select 1")
        logger.info(
            'Successfully initialized database engine and verified that it is working'
        )

    async def stop(self):
        self.db_engine.close()
        await self.db_engine.wait_closed()
        logger.info('Closed database engine')

    async def _execute(self, statement, get_result=None):
        self._verify_engine()

        async with self.db_engine.acquire() as connection:
            try:
                result = await connection.execute(statement)
                if get_result:
                    return await get_result(result)
            except Exception as e:
                raise e

    async def execute_statement(self, sql_statement):
        self._verify_engine()
        await self._execute(statement=sql_statement)

    async def fetch_one(self, query: str):
        self._verify_engine()
        return await self._execute(
            statement=query,
            get_result=self._fetchone,
        )

    async def fetch_all(self, query):
        self._verify_engine()
        return await self._execute(
            statement=query,
            get_result=self._fetchall,
        )

    async def upsert(self, command: UpsertCommand):
        insert_statement = insert(command.table).values(command.rows)
        on_conflict_statement = insert_statement.on_conflict_do_update(
            index_elements=command.index_elements,
            set_={
                col: getattr(insert_statement.excluded, col)
                for col in command.columns_to_update
            },
        )
        await self.execute_statement(on_conflict_statement)

    def _verify_engine(self):
        if self.db_engine is None:
            raise DbEngineNotInitialized('DB engine not initialized')

    @staticmethod
    async def _fetchone(result):
        return await result.fetchone()

    @staticmethod
    async def _fetchall(result):
        return await result.fetchall()


__all__ = ['SqlClient']
