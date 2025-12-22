from app.config.config import config

DATABASE_URL = (
    f"mysql+pymysql://{config.DB_USER}:"
    f"{config.DB_PASSWORD}@"
    f"{config.DB_HOST}:"
    f"{config.DB_PORT}/"
    f"{config.DB_NAME}?charset=utf8mb4"
)