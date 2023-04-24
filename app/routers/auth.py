from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import database, models, schemas, utils, oauth2


router = APIRouter(tags=['Authentication'])
@router.post('/login', response_model=schemas.Token)
def login(user_credintials:OAuth2PasswordRequestForm = Depends(), db:Session=Depends(database.get_db)):

    user = db.query(models.User).filter(models.User.email==user_credintials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"invalid credintials")
    
    if not utils.verify(user_credintials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"invalid credintials")
    
#create a token
#return token

    access_token=oauth2.create_access_token(data={"user_id":user.id})
    return {"access_token":access_token, "token_type":"Bearer"}
