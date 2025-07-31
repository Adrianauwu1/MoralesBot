from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from tortoise.exceptions import DoesNotExist
from DB import User
from SegPo.FuncionBan import *
from SegPo.FuncionNiveles import *
from SegPo.FuncionRegister import *
from SegPo.Plantillas import MoralesPlantillas
from Prefijos import PrefijosComandos

router = Router()

@router.message(Command("deldb", prefix=PrefijosComandos))
async def demote_user(message: Message):
    try:
        user_id = message.from_user.id

        # Verificar registro
        if not await Register.verificar_registro(user_id):
            return await message.reply(MoralesPlantillas.unregister())

        # Verificar si está baneado
        is_banned, reason = await BanUser.verificar_ban(user_id)
        if is_banned:
            return await message.reply(MoralesPlantillas.ban_user(reason))

        # Verificar privilegios (nivel 0 requerido)
        if not await Privilegios.verificar_nivel(user_id, 0):
            return await message.reply(MoralesPlantillas.nivel_restringido())

        # Validar parámetros
        args = message.text.split(" ", 1)
        if len(args) < 2:
            return await message.reply("""<b> Usar <code>/demote</code> id</b>""")

        try:
            target_id = int(args[1].strip())
        except ValueError:
            return await message.reply("""<b> El ID debe ser un número válido.</b>""")

        # Buscar usuario por ID
        try:
            target_user = await User.get(userid=target_id)
        except DoesNotExist:
            return await message.reply(f"""<b> El usuario no está registrado => <code>{target_id}</code></b>""")

        role = target_user.role

        # Quitar privilegios VIP (asumimos que el rol de usuario normal es "USER")
        target_user.role = "Free User"
        target_user.antispam = "70"
        target_user.credits = 0
        target_user.DInicio = None
        target_user.DFinal = None
        target_user.apodo = None
        target_user.nivel = None
        await target_user.save()

        await message.reply(f"""<b> Se le quitaron los privilegios de {role} al usuario => <code>{target_id}</code></b>""")

    except Exception as e:
        print(f"Error en demote: {e} ")
        await message.reply("<b>Ocurrió un error inesperado. Contacta al administrador.</b>")
