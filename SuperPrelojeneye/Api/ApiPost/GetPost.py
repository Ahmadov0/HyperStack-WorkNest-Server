from fastapi import APIRouter, HTTPException
from SuperPrelojeneye.schemasi.SchemasPost import AddPost, UpdatePost, PostResponse
from SuperPrelojeneye.DataBase.database import sessionDeb
from SuperPrelojeneye.DataBase.model import UserModel, PostModel, LikeModel, CommentModel
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from SuperPrelojeneye.Api.ApiUser.GetUser import router
from SuperPrelojeneye.schemasi.SchemasLikeComment import AddComment, Comment

man_router = APIRouter()
man_router.include_router(router)

@man_router.post("/post", tags=["Post"], summary="Add a post")
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


@man_router.get("/getAllPosts", tags=["Post"], summary="get all posts")
async def get_all_posts(db: sessionDeb):

    s = select(PostModel).options(
        selectinload(PostModel.author),
        selectinload(PostModel.likes)
    ).where(PostModel.private == False)

    result = await db.execute(s)
    posts = result.scalars().all()

    if not posts:
        raise HTTPException(status_code=404, detail="Posts not found")

    posts_list = []
    for p in posts:
        posts_list.append({
            "id": p.id,
            "title": p.title,
            "content": p.content,
            "body": p.body,
            "private": p.private,
            "author": {"id": p.author.id, "username": p.author.username} if p.author else None,
            "likes_count": len(p.likes) if p.likes else 0,
            "likes_users": [like.user_id for like in p.likes] if p.likes else []
        })

    return posts_list


@man_router.get("/getmyposts/{id}", tags=["Post"], summary="get my posts")
async def get_my_posts(db: sessionDeb, id: int):
    q = select(PostModel).options(
        selectinload(PostModel.author),
        selectinload(PostModel.likes)
    ).where(PostModel.Author_id == id)

    result = await db.execute(q)
    posts = result.scalars().all()

    if not posts:
        raise HTTPException(status_code=404, detail="Posts not found")

    posts_list = []
    for p in posts:
        posts_list.append({
            "id": p.id,
            "title": p.title,
            "content": p.content,
            "body": p.body,
            "private": p.private,
            "author": {"id": p.author.id, "username": p.author.username} if p.author else None,
            "likes_count": len(p.likes) if p.likes else 0,
            "likes_users": [like.user_id for like in p.likes] if p.likes else []
        })

    return posts_list

@man_router.put("/post/{post_id}", tags=["Post"], summary="Update a post")
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

@man_router.delete("/post/{post_id}", tags=["Post"], summary="Delete a post")
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

    likes_query = select(LikeModel).where(LikeModel.post_id == post_id)
    likes_res = await db.execute(likes_query)
    for like in likes_res.scalars().all():
        await db.delete(like)

    comments_query = select(CommentModel).where(CommentModel.post_id == post_id)
    comments_res = await db.execute(comments_query)
    for comment in comments_res.scalars().all():
        await db.delete(comment)

    await db.delete(post)
    await db.commit()

    return {
        "success": True,
        "message": f"Post with id {post_id} and all related data has been deleted successfully"
    }

@man_router.get("/serch", response_model=list[PostResponse])
async def serch(post_title: str, db: sessionDeb):
    q = select(PostModel).options(selectinload(PostModel.author), selectinload(PostModel.likes)).where(PostModel.title.ilike(f"%{post_title}%"), PostModel.private == False)
    respost = await db.execute(q)
    post = respost.scalars().all()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    posts_list = []
    for p in post:
        posts_list.append({
            "id": p.id,
            "title": p.title,
            "content": p.content,
            "body": p.body,
            "private": p.private,
            "author": {"id": p.author.id, "username": p.author.username} if p.author else None,
            "likes_count": len(p.likes) if p.likes else 0,
            "likes_users": [like.user_id for like in p.likes] if p.likes else []
        })

    return posts_list


@man_router.post("/post/{post_id}/like", tags=["Post"], summary="Toggle like on a post")
async def toggle_like(post_id: int, user_id: int, db: sessionDeb):
    post_query = select(PostModel).where(PostModel.id == post_id)
    post_res = await db.execute(post_query)
    post = post_res.scalar_one_or_none()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    if post.Author_id == user_id:
        raise HTTPException(
            status_code=400,
            detail="Te Cho like samomu sebe stavish"
        )

    like_query = select(LikeModel).where(LikeModel.post_id == post_id, LikeModel.user_id == user_id)
    like_res = await db.execute(like_query)
    existing_like = like_res.scalar_one_or_none()

    if existing_like:
        await db.delete(existing_like)
        await db.commit()
        action = "unliked"
    else:

        new_like = LikeModel(user_id=user_id, post_id=post_id)
        db.add(new_like)
        await db.commit()
        action = "liked"

    count_query = select(LikeModel).where(LikeModel.post_id == post_id)
    count_res = await db.execute(count_query)
    likes_count = len(count_res.scalars().all())

    return {
        "success": True,
        "action": action,
        "likes_count": likes_count
    }

@man_router.post("/post/{post_id}/comment", tags=["Comment"], summary="Add a comment to a post")
async def add_comment(post_id: int, user_id: int, comment_data: AddComment, db: sessionDeb):

    post_query = select(PostModel).where(PostModel.id == post_id)
    post_res = await db.execute(post_query)
    post = post_res.scalar_one_or_none()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    user_query = select(UserModel).where(UserModel.id == user_id)
    user_res = await db.execute(user_query)
    user = user_res.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    new_comment = CommentModel(
        text=comment_data.text,
        user_id=user_id,
        post_id=post_id
    )
    db.add(new_comment)
    await db.commit()
    await db.refresh(new_comment)

    return {
        "success": True,
        "message": "Comment added successfully",
        "comment": {
            "id": new_comment.id,
            "text": new_comment.text,
            "user_id": new_comment.user_id,
            "author": user.username
        }
    }

@man_router.get("/post/{post_id}/comments", tags=["Comment"], summary="Get comments for a post", response_model=list[Comment])
async def get_comments(post_id: int, db: sessionDeb):

    query = select(CommentModel).options(selectinload(CommentModel.user)).where(CommentModel.post_id == post_id)
    result = await db.execute(query)
    comments = result.scalars().all()

    comments_list = [
        {
            "id": c.id,
            "text": c.text,
            "author": c.user.username if c.user else "Unknown"
        }
        for c in comments
    ]

    return comments_list

@man_router.delete("/comment/{comment_id}", tags=["Comment"], summary="Delete a comment")
async def delete_comment(comment_id: int, user_id: int, db: sessionDeb):
    query = select(CommentModel).where(CommentModel.id == comment_id)
    result = await db.execute(query)
    comment = result.scalar_one_or_none()

    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    if comment.user_id != user_id:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to delete this comment"
        )

    await db.delete(comment)
    await db.commit()

    return {
        "success": True,
        "message": f"Comment with id {comment_id} has been deleted successfully"
    }