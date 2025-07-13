from datetime import datetime, timedelta

from jose import JWTError, jwt

from infrastructure.auth.jwt_processor_interface import JwtProcessorInterface
from infrastructure.auth.jwt_settings import JwtSettings, get_jwt_settings


class JwtProcessor(JwtProcessorInterface):
    def __init__(self, jwt_settings: JwtSettings) -> None:
        self.jwt_settings = jwt_settings

    def validate_token(self, token: str) -> dict | None:
        if token is None:
            return None

        try:
            payload = jwt.decode(token, self.jwt_settings.secret_key, algorithms=[self.jwt_settings.algorithm])
            return payload
        except JWTError:
            return None

    def create_token(self, data: dict, hours = None) -> str:
        if hours is None:
            exp = datetime.utcnow() + timedelta(hours=self.jwt_settings.expires_in)
        else:
            exp = datetime.utcnow() + timedelta(hours=hours)

        data.update({"exp": exp})

        return jwt.encode(data, self.jwt_settings.secret_key, algorithm=self.jwt_settings.algorithm)


def get_jwt_processor(settings: JwtSettings = get_jwt_settings()) -> JwtProcessor:
    return JwtProcessor(jwt_settings=settings)
