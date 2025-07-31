from aiogram import Router, types
from aiogram.filters import Command
from Prefijos import PrefijosComandos
from DB import User
from SegPo.Plantillas import MoralesPlantillas

router = Router() 

@router.message(Command("chatid", prefix=PrefijosComandos))
async def chatid(message: types.Message):
    user_id = message.from_user.id
    result = await User.get_or_none(userid=user_id)
    if not result:
        return await message.reply(MoralesPlantillas.unregister())
    if not message.chat.id:
        return await message.reply("No se pudo obtener el ID del chat.")
    if not message.from_user.id:
        return await message.reply("No se pudo obtener el ID del usuario.")

    if result:
        return await message.reply(
            f"Tu ID de chat es: <code>{message.chat.id}</code>\n"
            f"Tu ID de usuario es: <code>{message.from_user.id}</code>"
        )

