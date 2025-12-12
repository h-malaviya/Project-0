import uuid
from typing import Optional, List
from contextlib import contextmanager
from sqlalchemy import Column, String, Table, select, update, delete
from sqlalchemy import UniqueConstraint
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.orm import mapped_column, registry
from pymongo.errors import DuplicateKeyError
from app.database2 import Base, get_db, engine
from app.schemas import UserCreate, UserOut,UserUpdate,UserDelete

mapper_registry = registry()

class UserORM(Base):
    
    __tablename__ = "users"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, nullable=False, unique=True, index=True)
    password = Column(String, nullable=False)

def ensure_tables():
    """Creates tables if not there is database2"""
    Base.metadata.create_all(bind=engine)

def _orm_to_userout(orm: Optional[UserORM]) -> Optional[UserOut]:
    """
    converts Userorm object to userOut
    """
    if not orm:
        return None
    return UserOut(id=str(orm.id), email=orm.email)

@contextmanager
def _db_session():
    """
    Manages db sessions
    """
    db = get_db()
    try:
        yield db
        db.commit()
    except:
        db.rollback()
        raise
    finally:
        db.close()

def create_user(user: UserCreate) -> Optional[UserOut]:
    """
    Add a new user,
    :param user : user details
    """
    new_id = str(uuid.uuid4())
    with _db_session() as db:
        user_obj = UserORM(id=new_id, email=user.email, password=user.password)
        db.add(user_obj)
        try:
            db.flush()  
        except IntegrityError as e:          
            raise DuplicateKeyError("duplicate key error collection: users email") from e
        return _orm_to_userout(user_obj)

def get_user(user_id: str) -> Optional[UserOut]:
    """
    get user details using user id
    
    :param user_id: user's unique id
    return User details or None
    """
    with _db_session() as db:
        stmt = select(UserORM).where(UserORM.id == user_id)
        res = db.execute(stmt).scalars().first()
        return _orm_to_userout(res)

def list_users() -> List[UserOut]:
    """
    Get all user list,
    returns list of all users
    """
    with _db_session() as db:
        stmt = select(UserORM)
        results = db.execute(stmt).scalars().all()
        return [_orm_to_userout(r) for r in results]

def update_password(user:UserUpdate) -> Optional[UserOut]:
    """
    change user password,
    :param user : user details
    """
    with _db_session() as db:
        stmt = select(UserORM).where(UserORM.id == user.id)
        orm = db.execute(stmt).scalars().first()
        if not orm:
            return None
        orm.password = user.password
        db.add(orm)
        db.flush()
        return _orm_to_userout(orm)

def delete_user(user:UserDelete) -> bool:
    """
    delete user,
    :param user : user details
    """
    with _db_session() as db:
        stmt = select(UserORM).where(UserORM.id == user.id)
        orm = db.execute(stmt).scalars().first()
        if not orm:
            return False
        db.delete(orm)
        db.flush()
        return True
