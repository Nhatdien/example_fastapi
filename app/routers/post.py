from .. import database, models, schemas, oauth2
from fastapi import Response, status, HTTPException, Depends, APIRouter
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func


router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.get("/", response_model=List[schemas.PostOut])
def get_post(db: Session = Depends(database.get_db),
             current_user: models.User = Depends(oauth2.get_current_user),
             limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # cursor.execute("""SELECT * from posts WHERE id = %s""", (id,))
    # test_post = cursor.fetchone()
    test_post = db.query(models.Post).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip).all()
    result = db.query(models.Post,
                        func.count(models.Vote.user_id).label("votes")
                      ).join(models.Vote, models.Vote.post_id == models.Post.id,
                             full=True, isouter=False).group_by(models.Post.id).group_by(models.Post.owner_id).all()
    print(result)
    if not test_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return result


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate,
                db: Session = Depends(database.get_db),
                current_user: models.User = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title, content, published)
    # VALUES (%(title)s, %(content)s, %(published)s)
    # RETURNING *""",
    #                {"title":new_post.title, "content":new_post.content, 'published':new_post.published})
    # created_post = cursor.fetchall()
    # conn.commit()
    created_post = models.Post(owner_id=current_user.id,
                               **post.dict())

    db.add(created_post)
    db.commit()
    db.refresh(created_post)
    return created_post


@router.get("/{id}", response_model=schemas.Post)
def get_posts(id: int, db: Session = Depends(database.get_db),
              current_user: models.User = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).filter(models.Post.id == id).first()
    return posts


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(database.get_db),
                current_user: models.User = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (id,))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post witd id {id} doesn't exist")

    if post.first().owner_id != current_user.id:  # type: ignore
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"cannot delete post witd id {id}. Youre not the owner")

    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate,
                db: Session = Depends(database.get_db),
                current_user: models.User = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s
    # RETURNING *""",
    #                (post.title, post.content, post.published, id))

    # updated_post = cursor.fetchone()
    post_update_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_update_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post witd id {id} doesn't exist")

    if post.owner_id != current_user.id:  # type: ignore
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"cannot update post witd id {id}. Youre not the owner")

    post_update_query.update(
        updated_post.dict(), synchronize_session=False)  # type: ignore

    db.commit()
    return post_update_query.first()
