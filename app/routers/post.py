from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from sqlalchemy import func
from .. import models, schemas, oauth2
from ..database import  get_db
from typing import List, Optional



router = APIRouter(
    prefix="/posts",
    tags = ['Posts']
)
 
@router.get("/", response_model=List[schemas.PostOut])
def root(db:Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user), Limit:int=5, skip:int=0, search:Optional[str]=""):
    #cursor.execute("""SELECT * FROM posts""")
    #posts = cursor.fetchall()
    """
    #only receiving logged in user post
    posts = db.query(models.Post).filter(models.Post.owner_id==current_user.id).all()
    """
    #print(Limit)
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(Limit).offset(skip).all()

    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id==models.Post.id, isouter = True).group_by(models.Post.id).filter(
        models.Post.title.contains(search)).limit(Limit).offset(skip).all()
    res = []
    for each in results:
        dct = {}
        dct['post'] = each[0].__dict__
        dct['votes'] = each[1]
        res.append(dct)
    return res


@router.post("/", status_code = status.HTTP_201_CREATED, response_model=schemas.Posts)
def new(new_post : schemas.PostCreate, db:Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)):
    #cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (new_post.title, new_post.content, new_post.published))
    #new = cursor.fetchall()
    #conn.commit()

    #print(current_user.email)
    
    new_posts = models.Post(owner_id=current_user.id, **new_post.dict())
    db.add(new_posts)
    db.commit()
    db.refresh(new_posts)
    return new_posts


"""@router.get("/posts/latest")
def latest_post():
    new_var = my_post[len(my_post)-3]
    print(new_var)
    return new_var"""


#@router.get("/{id}", response_model=schemas.Posts)
@router.get("/{id}", response_model= schemas.PostOut)
def get_one_post(id:int, db:Session = Depends(get_db), current_user:int=Depends(oauth2.get_current_user)):
    #cursor.execute(""" SELECT * FROM posts where id = %s""",(str(id)))
    #one_post = cursor.fetchone()
    #conn.commit()
    #one_post = db.query(models.Post).filter(models.Post.id==id).first()

    one_post = db.query(models.Post, func.count(models.Vote.post_id)).join(
        models.Vote, models.Vote.post_id==models.Post.id, isouter = True).group_by(models.Post.id).filter(models.Post.id==id).first()
    

    if not one_post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post {id} not found")
    
    dct = {}
    dct['post'] = one_post[0].__dict__
    dct['votes'] = one_post[1]

    """ 
    #only receiving logged in user post
    if one_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"not authorized user")"""
    
    #return one_post
    return dct

@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db:Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)):
    #cursor.execute(""" DELETE FROM posts WHERE id=%s RETURNING *""", (str(id)))
    #delete_one = cursor.fetchone()
    #conn.commit()
    delete_one_query = db.query(models.Post).filter(models.Post.id==id)

    delete_one = delete_one_query.first()

    if delete_one == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post not exist")
    
    if delete_one.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"not authorized user")
    
    delete_one_query.delete(synchronize_session= False)
    db.commit()
    
    return Response(status_code = status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.Posts)
def update_post(id:str , updated_post:schemas.PostUpdate, db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)):
    #cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, (str(id))))
    #update_one = cursor.fetchone()
    #conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id==id)
    var = post_query.first()
    if var == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"post not exist")
    
    if var.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"not authorized")
    
    item = jsonable_encoder(updated_post)
    post_query.update(item, synchronize_session=False)
    db.commit()
    return post_query.first()