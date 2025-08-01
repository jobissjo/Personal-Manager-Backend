from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.log_repository import LogRepository
from app.schemas.log_schema import LogCreate, LogRead


class LogService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_log(self, log_data: LogCreate)-> LogRead:
        """
        Create a new log entry.
        :param log_data: Dictionary containing log data.
        :return: Created log entry.
        """
        return await LogRepository.create_log(self.session, log_data)
    
    async def get_user_logs(self, user_id: int)-> list[LogRead]:
        """
        Retrieve all logs for a specific user.
        :param user_id: ID of the user whose logs are to be retrieved.
        :return: List of log entries for the user.
        """
        return await LogRepository.get_user_logs(self.session, user_id)