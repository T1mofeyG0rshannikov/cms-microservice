from datetime import datetime, timedelta

from jose import JWTError, jwt

from infrastructure.auth.jwt_processor_interface import JwtProcessorInterface
from infrastructure.auth.jwt_settings import JwtSettings, get_jwt_settings


class JwtProcessor(JwtProcessorInterface):
    def __init__(self, jwt_settings: JwtSettings) -> None:
        self.jwt_settings = jwt_settings

    def create_set_password_token(self, user_id: int) -> str:
        expires = datetime.utcnow() + timedelta(hours=int(self.jwt_settings.expires_in))
        encode = {"id": user_id, "exp": expires}

        return jwt.encode(encode, self.jwt_settings.secret_key, algorithm=self.jwt_settings.algorithm)

    def create_access_token(self, username: str, user_id: int) -> str:
        encode = {"sub": username, "id": user_id}
        expires = datetime.utcnow() + timedelta(hours=int(self.jwt_settings.expires_in))
        encode.update({"exp": expires})
        return jwt.encode(encode, self.jwt_settings.secret_key, algorithm=self.jwt_settings.algorithm)

    def validate_token(self, token: str) -> dict | None:
        if token is None:
            return None

        try:
            payload = jwt.decode(token, self.jwt_settings.secret_key, algorithms=[self.jwt_settings.algorithm])
            return payload
        except JWTError:
            return None

    def create_confirm_email_token(self, user_id: int) -> str:
        payload = {
            "user_id": user_id,
            "exp": datetime.utcnow() + timedelta(hours=self.jwt_settings.expires_in),
        }

        return jwt.encode(payload, self.jwt_settings.secret_key, algorithm=self.jwt_settings.algorithm)


def get_jwt_processor(settings: JwtSettings = get_jwt_settings()) -> JwtProcessor:
    return JwtProcessor(jwt_settings=settings)
