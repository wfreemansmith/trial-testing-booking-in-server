from fastapi import Query, Depends
from fastapi.exceptions import HTTPException
from src.db import get_db
from sqlalchemy.orm import Session, joinedload
from src.models import User, CentreContact
import hashlib
from datetime import date, timedelta

def verify_token_get_user(raw_token: str, db: Session) -> User:
    hashed_token = hashlib.sha256(raw_token.encode()).hexdigest()
    return (db.query(User)
        .filter(User.token_hash == hashed_token, User.is_active == True)
        .options(
            joinedload(User.role),
            joinedload(User.centre_contact).joinedload(CentreContact.centre),
            joinedload(User.marking_window))
        .first()
    )

async def require_permission(permission: str) -> User:
    """
    Wrapper for retrieving user & checking their role has permission for the given action.
    
    :param action: Action to check permission for e.g. "upload:write"
    :type action: str
    """
    def dependency(q: str = Query(...), db: Session = Depends(get_db)):
        user = verify_token_get_user(q, db)
        if user is None:
            raise HTTPException(status_code=401, detail="Invalid or inactive token")
        if user.marking_window and date.today() > (user.marking_window.window_end  + timedelta(days=7)):
            raise HTTPException(status_code=403, detail="Marking window has closed")
        if permission not in user.role.permissions:
            raise HTTPException(status_code=403, detail="User has insufficient permissions")
        return user
        
    return dependency


async def require_centre_permission(action: str) -> User:
    """
    Centre-specific wrapper for retrieving user & checking their role has permission for the given action.
    Checks that User has required fields 'centre_id' and 'marking_window_id'.
    
    :param action: Action to check permission for e.g. "upload:write"
    :type action: str
    """
    def dependency(q: str = Query(...), db: Session = Depends(get_db)):
        user = verify_token_get_user(q, db)
        if user is None:
            raise HTTPException(status_code=401, detail="Invalid or inactive token")
        if user.centre_contact is None:
            raise HTTPException(status_code=403, detail="No centre associated with this account")
        if user.marking_window and date.today() > (user.marking_window.window_end  + timedelta(days=7)):
            raise HTTPException(status_code=403, detail="Marking window has closed")
        if action not in user.role.permissions:
            raise HTTPException(status_code=403, detail="User has insufficient permissions")
        return user
        
    return dependency