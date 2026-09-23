from fastapi import APIRouter, HTTPException
from SuperPrelojeneye.schemasi.SchemasPost import AddPost, UpdatePost, Post
from SuperPrelojeneye.DataBase.database import sessionDeb
from SuperPrelojeneye.DataBase.model import UserModel, PostModel
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from SuperPrelojeneye.Api.ApiUser.GetUser import router

main_router = APIRouter()
main_router.include_router(router)

@main_router.post("/post", tags=["Post"], summary="Add a post")
async def add_post(post: AddPost, db: sessionDeb):
    user_query = select(UserModel).where(UserModel.id == post.Author_id)
    user_res = await db.execute(user_query)
    user_base = user_res.scalar_one_or_none()

    if not user_base:
        raise HTTPException(status_code=404, detail="User not found")

    new_post = PostModel(
        title=post.title, content=post.content, Author_id=post.Author_id, private=post.private, body=post.body
    )
    db.add(new_post)
    await db.commit()
    await db.refresh(new_post)

    stmt = select(PostModel).options(selectinload(PostModel.author)).where(PostModel.id == new_post.id)
    result = await db.execute(stmt)
    refreshed_post = result.scalar_one()

    return {"success": True,
            "title": refreshed_post.title,
            "content": refreshed_post.content,
            "body": refreshed_post.body,
            "author_id": refreshed_post.Author_id}

@main_router.get("/getAllPosts", tags=["Post"], summary="get all posts", response_model=list[Post])
async def get_all_posts(db: sessionDeb):

    s = select(PostModel).options(selectinload(PostModel.author)).where(PostModel.private == False)
    result = await db.execute(s)

    posts = result.scalars().all()

    if not posts:
        raise HTTPException(status_code=404, detail="Posts not found")

    return posts

@main_router.get("/getmyposts/{id}", tags=["Post"], summary="get my posts", response_model=list[Post])
async def get_my_posts(db: sessionDeb, id: int):
    q = select(PostModel).options(selectinload(PostModel.author)).where(PostModel.Author_id == id)
    result = await db.execute(q)

    posts = result.scalars().all()

    if not posts:
        raise HTTPException(status_code=404, detail="Posts not found")
    return posts

@main_router.put("/post/{post_id}", tags=["Post"], summary="Update a post")
async def update_post(post_id: int, post_data: UpdatePost, user_id: int, db: sessionDeb):
    query = select(PostModel).options(selectinload(PostModel.author)).where(PostModel.id == post_id)
    result = await db.execute(query)
    post = result.scalar_one_or_none()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    if post.Author_id != user_id:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to edit this post"
        )

    post.title = post_data.title
    post.content = post_data.content
    post.body = post_data.body
    post.private = post_data.private

    await db.commit()
    await db.refresh(post)

    return {
        "success": True,
        "message": "Post updated successfully",
        "post": post
    }

@main_router.delete("/post/{post_id}", tags=["Post"], summary="Delete a post")
async def delete_post(post_id: int, user_id: int, db: sessionDeb):
    query = select(PostModel).where(PostModel.id == post_id)
    result = await db.execute(query)
    post = result.scalar_one_or_none()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    if post.Author_id != user_id:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to delete this post"
        )

    await db.delete(post)
    await db.commit()

    return {
        "success": True,
        "message": f"Post with id {post_id} has been deleted successfully"
    }