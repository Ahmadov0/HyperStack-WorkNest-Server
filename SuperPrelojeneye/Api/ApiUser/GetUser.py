from fastapi import APIRouter, HTTPException
from SuperPrelojeneye.schemasi.SchemasUser import Auth, Login
from SuperPrelojeneye.DataBase.database import sessionDeb, engine
from SuperPrelojeneye.DataBase.model import UserModel, PostModel, Base
from sqlalchemy import select
from sqlalchemy.orm import selectinload


router = APIRouter()

@router.post("/auth",
             tags=["User"],
             summary="Auth User",
             )
async def add_user(user: Auth, db: sessionDeb):

    q = select(UserModel).where(UserModel.username == user.username)
    result = await db.execute(q)
    UserF = result.scalar_one_or_none()

    if UserF:
        raise HTTPException(status_code=400, detail="name Usera Pohoje")

    new_user = UserModel(username=user.username, password=user.password)
    db.add(new_user)

    await db.commit()
    await db.refresh(new_user)

    return {"success": True,
            "username": user.username,
            "id": new_user.id}

@router.post("/login",
             tags=["User"],
            summary="Login User",)
async def login_user(user: Login, db: sessionDeb):
    q = select(UserModel).where(
        UserModel.username == user.username,
        UserModel.password == user.password,
    )
    result = await db.execute(q)
    res = result.scalar_one_or_none()

    if not res:
        raise HTTPException(status_code=404, detail="Name or password incorrect")
    return {"success": True,
            "username": res.username,
            "id": res.id}

@router.put("/author/{id}",
            tags=["User"],
            summary="upd User",)
async def update_user(id: int, user: Login, db: sessionDeb):
    q = select(UserModel).where(
        UserModel.id == id,
    )
    result = await db.execute(q)
    res = result.scalar_one_or_none()

    if not res:
        raise HTTPException(status_code=404, detail="User not found")

    res.username = user.username
    res.password = user.password

    await db.commit()
    await db.refresh(res)

    return {"success": True,
            "message": "User updated",
            "username": res.username,
            "password": res.password,}

@router.delete("/author/{id}",
               tags=["User"],
               summary="Delete User",)
async def delete_user(id: int, db: sessionDeb):
    q = select(UserModel).where(UserModel.id == id)

    result = await db.execute(q)
    res = result.scalar_one_or_none()

    if not res:
        raise HTTPException(status_code=404, detail="User not found")

    qu = select(PostModel).options(selectinload(PostModel.author)).where(PostModel.Author_id == id)
    resu = await db.execute(qu)

    post = resu.scalars().all()
    if post:
        for items in post:
            await db.delete(items)

        await db.delete(res)
        await db.commit()

        return {"success": True}
    else:
        await db.delete(res)
        await db.commit()

        return {"success": True}

