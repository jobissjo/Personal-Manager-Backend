import asyncio
import typer
from app.core.db_config import get_db
from app.models import User, Profile
from app.models.enums import UserRole
from sqlalchemy import select
from app.core.security import hash_password

def run(
    email: str = typer.Option(..., prompt="Enter email"),
    password: str = typer.Option(..., prompt="Enter password"),
    first_name: str = typer.Option("Admin", prompt="Enter first name"),
    last_name: str = typer.Option(..., prompt="Enter last name"),
):
    async def create_user():
        async for session in get_db():
            stmt = select(User).where(User.email == email)
            result = await session.execute(stmt)
            user = result.scalars().first()
            if user:
                typer.echo(f"User with email {email} already exists.")
                return
            hashed_password = await hash_password(password)
            user = User(
                email=email,
                password=hashed_password,
                first_name=first_name,
                last_name=last_name,
                role=UserRole.ADMIN,
                is_superuser=True,
            )
            session.add(user)
            await session.flush()

            profile = Profile(user_id=user.id, bio="", profile_picture_url="")
            session.add(profile)
            await session.commit()
            typer.echo("Super Admin created successfully🔥🔥")
        
    asyncio.run(create_user())

