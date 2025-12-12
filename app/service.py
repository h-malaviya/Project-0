import asyncio
from typing import Optional,List
from bson import ObjectId
from pymongo.errors import DuplicateKeyError
from app.database import db
from app.schemas import UserCreate,UserDelete,UserOut,UserUpdate

user_coll = db.get_collection('users')

def doc_to_userout(doc:dict) -> Optional[UserOut]:
    """
    converts dictionary to userOut

    :param doc: dictionary contains user details 
    """
    id_str = str(doc.get("_id")) if doc.get("_id") is not None else doc.get("id")

    payload = {
        "id": id_str,
        "email": doc.get("email"),
    }

    # if "password" in UserOut.__fields__:
    #     payload["password"] = doc.get("password")

    return UserOut(**payload)

def create_user(user: UserCreate) -> Optional[UserOut]:
    """
    Add a new user,
    :param user : user details
    """
    doc = {'email':user.email,'password':user.password}
    try:
        res= user_coll.insert_one(doc)
    except DuplicateKeyError:
        raise
    created = user_coll.find_one({'_id':res.inserted_id})
    return doc_to_userout(created)

def get_user(user_id : str) -> Optional[UserOut]:
    """
    get user details using user id
    
    :param user_id: user's unique id
    return User details or None
    """
    try:
        oid = ObjectId(user_id)
    except Exception:
        return None
    res = user_coll.find_one({'_id':oid})
    print(res)
    return doc_to_userout(res)

def list_users() -> List[UserOut]:
    """
    Get all user list,
    returns list of all users
    """
    cur = user_coll.find()
    return [doc_to_userout(u) for u in cur]

def update_password(user : UserUpdate) -> Optional[UserOut]:
    """
    change user password,
    :param user : user details
    """
    try :
        oid = ObjectId(user.id)
    except Exception:
        return None
    doc =user_coll.find_one_and_update(        
        {'_id':oid},
        {'$set':{'password':user.password}},
        return_document=True
    )
    return doc_to_userout(doc)

def delete_user(user : UserDelete) -> bool:
    """
    delete user,
    :param user : user details
    """
    try:
        oid = ObjectId(user.id)
    except Exception:
        return None
    res = user_coll.delete_one({'_id':oid})
    return res.deleted_count==1   