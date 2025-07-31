from aiogram import Router, types
from aiogram.filters import Command
from datetime import datetime
from DB import User
from SegPo.Plantillas import MoralesPlantillas
from Prefijos import PrefijosComandos

router = Router()

@router.message(Command("register", prefix=PrefijosComandos))
async def register(message: types.Message):
    # Determinar el usuario objetivo: si es una respuesta, el autor del mensaje original; si no, el que ejecuta el comando.
    if message.reply_to_message:
        target_user = message.reply_to_message.from_user
    else:
        target_user = message.from_user

    user_id = target_user.id
    username = target_user.username
    first_name = target_user.first_name or "User"

    result = await User.get_or_none(userid=user_id)

    if result:
        # Aquí puedes decidir si el mensaje de "ya registrado" debe ser para el usuario objetivo
        # o para quien intentó registrarlo. En este caso, lo hacemos para el usuario objetivo.
        return await message.reply(MoralesPlantillas.yaregistrado())

    fecha_hora_actual = datetime.now()
    fecha_actual = fecha_hora_actual.strftime("%d-%m-%Y")
    hora_actual = fecha_hora_actual.strftime("%H:%M:%S")
    now = f"{fecha_actual} {hora_actual}"

    await User.create(
            userid=user_id,
            username=username,
            role="Free User",
            credits=0,
            antispam=70,
            DInicio=None,
            DFinal=None,
            DRegistro=now,
            last_message="2000-01-01 00:00:00",
            firstname=first_name,
            baned=0,
            apodo="",
            razon="",
            total_messages=0,
            nivel=None,
            cc_count=0,
            cc_count_limit=10,
            language="es"
        )
    # El mensaje de confirmación debe indicar a quién se registró.
    return await message.reply(MoralesPlantillas.register(user_id))