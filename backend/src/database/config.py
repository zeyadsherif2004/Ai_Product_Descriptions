# backend/src/database/config.py
"""
Database configuration
"""

import os
from typing import Optional
from dataclasses import dataclass


@dataclass
class DatabaseConfig:
    """Database configuration settings"""
    
    # Database connection
    url: str
    echo: bool = False
    pool_size: int = 5
    max_overflow: int = 10
    pool_timeout: int = 30
    pool_recycle: int = 3600
    
    # Migration settings
    migration_dir: str = "migrations"
    
    # SSL settings for production
    ssl_mode: Optional[str] = None
    ssl_cert: Optional[str] = None
    ssl_key: Optional[str] = None
    ssl_root_cert: Optional[str] = None


def get_database_url() -> str:
    """Get database URL from environment variables"""
    
    # Check for explicit DATABASE_URL first
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        # Ensure SSL mode is set for PostgreSQL (required by Render and most cloud providers)
        if 'postgresql' in database_url and 'sslmode' not in database_url:
            if '?' in database_url:
                database_url += '&sslmode=require'
            else:
                database_url += '?sslmode=require'
        return database_url
    
    # Build URL from individual components
    db_type = os.getenv("DB_TYPE", "postgresql")
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "5432")
    db_name = os.getenv("DB_NAME", "ai_descriptions")
    db_user = os.getenv("DB_USER", "postgres")
    db_password = os.getenv("DB_PASSWORD", "")
    
    # Handle different database types
    if db_type == "postgresql":
        if db_password:
            url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        else:
            url = f"postgresql://{db_user}@{db_host}:{db_port}/{db_name}"
        # Add SSL mode for non-localhost PostgreSQL
        if db_host != "localhost" and db_host != "127.0.0.1":
            url += "?sslmode=require"
        return url
    elif db_type == "sqlite":
        return f"sqlite:///{db_name}.db"
    elif db_type == "mysql":
        if db_password:
            return f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        else:
            return f"mysql+pymysql://{db_user}@{db_host}:{db_port}/{db_name}"
    else:
        raise ValueError(f"Unsupported database type: {db_type}")


def get_database_config() -> DatabaseConfig:
    """Get database configuration from environment"""
    
    url = get_database_url()
    echo = os.getenv("DB_ECHO", "false").lower() == "true"
    pool_size = int(os.getenv("DB_POOL_SIZE", "5"))
    max_overflow = int(os.getenv("DB_MAX_OVERFLOW", "10"))
    pool_timeout = int(os.getenv("DB_POOL_TIMEOUT", "30"))
    pool_recycle = int(os.getenv("DB_POOL_RECYCLE", "3600"))
    
    # SSL settings
    ssl_mode = os.getenv("DB_SSL_MODE")
    ssl_cert = os.getenv("DB_SSL_CERT")
    ssl_key = os.getenv("DB_SSL_KEY")
    ssl_root_cert = os.getenv("DB_SSL_ROOT_CERT")
    
    return DatabaseConfig(
        url=url,
        echo=echo,
        pool_size=pool_size,
        max_overflow=max_overflow,
        pool_timeout=pool_timeout,
        pool_recycle=pool_recycle,
        ssl_mode=ssl_mode,
        ssl_cert=ssl_cert,
        ssl_key=ssl_key,
        ssl_root_cert=ssl_root_cert
    )

