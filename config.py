from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_HOST:str
    DATABASE_PORT:str
    DATABASE_NAME:str
    DATABASE_USER:str
    DATABASE_PASSWORD:str

    secret_key:str
    algorithm:str
    access_token_expire_minutes:int

    class Config():
        env_file=".env"

settings=Settings()
