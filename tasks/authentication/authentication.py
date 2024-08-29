from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from fastapi.security import APIKeyHeader, OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status

from tasks.database.models import User, AccessToken
from tasks.database.database import get_database_session
from tasks.authentication.password import verify_password, generate_token

api_key_token = APIKeyHeader(name='Token')
auth_schema = OAuth2PasswordBearer(tokenUrl='/token')


def verify_access_token(token: str = Depends(api_key_token),
                        db: Session = Depends(get_database_session)):
    access_token = db.query(AccessToken).join(User).filter(AccessToken.access_token == token).first()

    if access_token is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Token invalid')

    if datetime.now() > access_token.expiration_date:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Token expired')

    return access_token.user


def verify_access_token_auth_schema(token: str = Depends(auth_schema),
                                    db: Session = Depends(get_database_session)):
    access_token = db.query(AccessToken).join(User).filter(AccessToken.access_token == token).first()

    if access_token is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Token expired')

    if datetime.now() > access_token.expiration_date:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Token expired')

    return access_token.user


def authenticate(email: str, password: str, db: Session) -> User | None:
    user_db = db.query(User).filter(User.email == email).first()
    if user_db is None:
        return None

    if not verify_password(password, user_db.hashed_password):
        return None

    return user_db


def create_access_token(user: User, db: Session) -> AccessToken:
    access_token = db.query(AccessToken).filter(AccessToken.user_id == user.id).first()
    if access_token is not None:
        if datetime.now() > access_token.expiration_date:
            db.delete(access_token)
        else:
            return access_token

    tomorrow = datetime.now() + timedelta(days=1)
    access_token = AccessToken(
        user_id=user.id,
        expiration_date=tomorrow,
        access_token=generate_token()
    )

    db.add(access_token)
    db.commit()
    db.refresh(access_token)

    return access_token


def logout(token: str = Depends(api_key_token), db: Session = Depends(get_database_session)):
    access_token = db.query(AccessToken).filter(AccessToken.access_token == token).first()

    if access_token is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    db.delete(access_token)
    db.commit()
