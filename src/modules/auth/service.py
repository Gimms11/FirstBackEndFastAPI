from src.modules.auth.models import User, UserRole
from src.modules.auth.schemas import UserCreateModel
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from src.modules.auth.utils import hash_password


def _resolve_role_from_email(email: str) -> UserRole:
    """
    Asigna el rol del usuario según el dominio de su correo:
      - @admin.com   → ADMIN
      - @pro_user.com → PRO_USER
      - cualquier otro → USER (por defecto)
    """
    domain = email.split("@")[-1].lower()
    role_map = {
        "admin.com": UserRole.ADMIN,
        "pro_user.com": UserRole.PRO_USER,
    }
    return role_map.get(domain, UserRole.USER)


class UserService:
    async def get_user_by_email(self, email: str, session: AsyncSession):
        statement = select(User).where(User.email == email)
        result = await session.exec(statement)
        return result.first()

    async def get_user_by_username(self, username: str, session: AsyncSession):
        statement = select(User).where(User.username == username)
        result = await session.exec(statement)
        return result.first()

    async def create_user(self, user_data: UserCreateModel, session: AsyncSession):
        user_data_dict = user_data.model_dump()
        new_user = User(**user_data_dict)
        new_user.password_hash = hash_password(user_data_dict["password"])
        new_user.role = _resolve_role_from_email(user_data_dict["email"])
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user
