"""
MongoDB database connection and utilities.
"""
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure
from .config import get_settings


class Database:
    """MongoDB database manager."""
    
    client: AsyncIOMotorClient | None = None
    db = None
    
    @classmethod
    async def connect(cls) -> None:
        """Establish connection to MongoDB."""
        settings = get_settings()
        cls.client = AsyncIOMotorClient(
            settings.mongodb_url,
            serverSelectionTimeoutMS=5000,
        )
        cls.db = cls.client[settings.mongodb_db_name]
        
        # Verify connection
        try:
            await cls.client.admin.command("ping")
        except ConnectionFailure as e:
            raise ConnectionFailure(f"MongoDB connection failed: {e}") from e
    
    @classmethod
    async def disconnect(cls) -> None:
        """Close MongoDB connection."""
        if cls.client:
            cls.client.close()
            cls.client = None
            cls.db = None
    
    @classmethod
    def get_db(cls):
        """Get database instance."""
        if cls.db is None:
            raise RuntimeError("Database not connected. Call connect() first.")
        return cls.db
