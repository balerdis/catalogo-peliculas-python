
import logging
import time


from app.core.database.connection import db_connection
from app.config.config import config
from app.api.v1.schemas.generic import TokenInfo

logging.basicConfig(level=config.LOG_LEVEL)


logging.basicConfig(level=config.LOG_LEVEL)
logger = logging.getLogger(__name__)



class TokenHandler:
    def __init__ (self):
        self.active_tokens: dict[str, TokenInfo] = {}

    def is_token_forced_valid(self, token: str, client_key: str) -> bool:
        """
            Toma el token y el clientKey y se fija si existe en las variables de entorno, con el fin de permitir
            Acceso sin autenticación desde el otro backend en laravel
        """        
        return (
            config.FORCED_VALID_TOKEN is not None and
            config.FORCED_CLIENT_KEY is not None and
            token == config.FORCED_VALID_TOKEN and
            client_key == config.FORCED_CLIENT_KEY
        )


    def verify_token(self, token:str, client_key: str) -> bool:
        """
            Toma el token y el clientKey y se fija si existe en la base de datos si el token es uno vigente    
            TODO: hay que acceder a la base de datos y verificar estos datos contra la DB de charcot usuarios_sessions
        """        
        if self.is_token_forced_valid(token, client_key):
            return True
        if self.is_token_cached(token, client_key):
            logger.info(f"Token found in cache: {self.active_tokens[f'{token}:{client_key}']}")
            return True
        try:
            self.active_tokens[f"{token}:{client_key}"] = {"time": time.time(), "id":1, "email":'xxx@sss.com'}
            return True
        except Exception as e:
            logger.error(f"Error verify_token al intentar verificar el token en la base de datos: {e}")
        return False
    
    def decode_token(self, token: str, client_key: str) -> dict:
        """El decodifica el token desde el X-Authorization, tambien contampla el hecho de que el 
        el token y el client-key sean validos por variables de entorno

        Args:
            token (str)
            client_key (str)

        Returns:
            dict: devuelve el token decodificado
        """
        logger.info(f"Decoding token: {token}")
        try:
            if self.is_token_forced_valid(token, client_key):
                # el token es valido por variables de entorno
                self.active_tokens[f"{token}:{client_key}"] = {"time": time.time(), "id":config.FORCED_VALID_TOKEN, "email":config.FORCED_CLIENT_KEY}
                logger.info(f"Token decoded: {self.active_tokens[f'{token}:{client_key}']} and saved in cache")
                return self.active_tokens[f"{token}:{client_key}"]
            if self.is_token_cached(token, client_key):
                logger.info(f"Token found in cache: {self.active_tokens[f'{token}:{client_key}']}")
                return self.active_tokens[f"{token}:{client_key}"]

            self.active_tokens[f"{token}:{client_key}"] = {"time": time.time(), "id":1, "email":'xxx@sss.com'}
            logger.info(f"Token decoded: {self.active_tokens[f"{token}:{client_key}"]} and saved in cache")
            return self.active_tokens[f"{token}:{client_key}"]
        except Exception as e:
            logger.error(f"Error decode_token al intentar verificar el token en la base de datos: {e}")
        return False
    
    def is_token_cached(self, token: str, client_key: str) -> bool:
        cache_key = f"{token}:{client_key}"
        if(cache_key in self.active_tokens):
            # se verifica si el token está en caché, se considera valido en cache durante 20 minutos (1200 segundos)
            if(time.time() - self.active_tokens[cache_key]["time"] < 1200):
                return True
            else:
                del self.active_tokens[cache_key]    
        return False

