# backend/src/database/connection.py
"""
Database connection management
"""

import logging
from contextlib import contextmanager
from typing import Generator, Optional

from sqlalchemy import create_engine, Engine, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

from .config import get_database_config
from ..models.payment_models import Base

logger = logging.getLogger(__name__)

# Global engine and session factory
_engine: Optional[Engine] = None
_session_factory: Optional[sessionmaker] = None


def get_engine() -> Engine:
    """Get or create database engine"""
    global _engine
    
    if _engine is None:
        config = get_database_config()
        
        # Engine configuration
        engine_kwargs = {
            "echo": config.echo,
            "pool_size": config.pool_size,
            "max_overflow": config.max_overflow,
            "pool_timeout": config.pool_timeout,
            "pool_recycle": config.pool_recycle,
            "pool_pre_ping": True,  # Verify connections before using
        }
        
        # SQLite specific configuration
        if config.url.startswith("sqlite"):
            engine_kwargs = {
                "echo": config.echo,
                "poolclass": StaticPool,
                "connect_args": {"check_same_thread": False}
            }
        
        # PostgreSQL specific configuration
        elif config.url.startswith("postgresql"):
            # Always add SSL mode for cloud databases
            connect_args = {
                "connect_timeout": 10,  # 10 second connection timeout
            }
            # Add SSL args if specified in config
            if config.ssl_mode:
                connect_args["sslmode"] = config.ssl_mode
            if config.ssl_cert:
                connect_args["sslcert"] = config.ssl_cert
            if config.ssl_key:
                connect_args["sslkey"] = config.ssl_key
            if config.ssl_root_cert:
                connect_args["sslrootcert"] = config.ssl_root_cert
            
            engine_kwargs["connect_args"] = connect_args
        
        _engine = create_engine(config.url, **engine_kwargs)
        logger.info(f"Database engine created for: {config.url.split('@')[-1] if '@' in config.url else config.url}")
    
    return _engine


def get_session_factory() -> sessionmaker:
    """Get or create session factory"""
    global _session_factory
    
    if _session_factory is None:
        engine = get_engine()
        _session_factory = sessionmaker(bind=engine, autocommit=False, autoflush=False)
        logger.info("Session factory created")
    
    return _session_factory


@contextmanager
def get_session() -> Generator[Session, None, None]:
    """Get database session with automatic cleanup"""
    session_factory = get_session_factory()
    session = session_factory()
    
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        logger.error(f"Database session error: {str(e)}")
        raise
    finally:
        session.close()


def init_database() -> None:
    """Initialize database tables"""
    try:
        engine = get_engine()
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
        
    except Exception as e:
        logger.error(f"Failed to initialize database: {str(e)}")
        raise


def drop_database() -> None:
    """Drop all database tables (use with caution!)"""
    try:
        engine = get_engine()
        Base.metadata.drop_all(bind=engine)
        logger.warning("All database tables dropped")
        
    except Exception as e:
        logger.error(f"Failed to drop database: {str(e)}")
        raise


def check_database_connection() -> bool:
    """Check if database connection is working"""
    try:
        engine = get_engine()
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("Database connection successful")
        return True
        
    except Exception as e:
        logger.error(f"Database connection failed: {str(e)}")
        return False


def get_database_info() -> dict:
    """Get database information"""
    try:
        engine = get_engine()
        config = get_database_config()
        
        with engine.connect() as conn:
            # Get database version
            if config.url.startswith("postgresql"):
                result = conn.execute(text("SELECT version()"))
                version = result.scalar()
            elif config.url.startswith("sqlite"):
                result = conn.execute(text("SELECT sqlite_version()"))
                version = result.scalar()
            elif config.url.startswith("mysql"):
                result = conn.execute(text("SELECT VERSION()"))
                version = result.scalar()
            else:
                version = "Unknown"
        
        return {
            "url": config.url.split('@')[-1] if '@' in config.url else config.url,
            "version": version,
            "pool_size": config.pool_size,
            "max_overflow": config.max_overflow,
            "echo": config.echo
        }
        
    except Exception as e:
        logger.error(f"Failed to get database info: {str(e)}")
        return {"error": str(e)}
