from api.config import config as cfg
from api.crud.users import UserCrud
from api.models import User
from api.schemas.user import UserCreateSchema, SpecificUserSchema, UserUpdateSchema


class UserService:
    def __init__(self, crud: UserCrud):
        self.crud = crud
        self.cfg = cfg

    async def get_user(self, user_id: int):
        return await self.crud.get_user(user_id=user_id)

    async def del_user(self, user_id: int):
        return await self.crud.delete_user(user_id=user_id)

    async def get_specific_user(self, user_id: int):
        user = await self.crud.get_user(user_id=user_id)
        bosses = await self.crud.get_user_notify(user_id)
        return SpecificUserSchema(
            chat_id=user.chat_id,
            push1=user.push1,
            push5=user.push5,
            push10=user.push10,
            push30=user.push30,
            bosses=bosses
        )

    async def get_all_users(self):
        return await self.crud.get_users()

    async def add_user(self, user: UserCreateSchema):
        return await self.crud.add_user(user=User(**user.model_dump()))

    async def update_user(self, user: User, user_update: UserUpdateSchema):
        return await self.crud.update_user(user=user, user_update=user_update)
