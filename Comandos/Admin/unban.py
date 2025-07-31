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
from dotenv import load_dotenv
import os

load_dotenv(override=True)

router = Router()

@router.message(Command("unban", prefix=PrefijosComandos))
async def unban_user(message: Message):
    try:
        user_id = message.from_user.id

        # Verificar registro
        if not await Register.verificar_registro(user_id):
            return await message.reply(MoralesPlantillas.unregister())

        # Verificar si está baneado el que ejecuta el comando
        valor, razon = await BanUser.verificar_ban(user_id)
        if valor:
            return await message.reply(MoralesPlantillas.ban_user(razon))

        # Verificar privilegios (nivel 0 requerido)
        if not await Privilegios.verificar_nivel(user_id, 0):
            return await message.reply(MoralesPlantillas.nivel_restringido())

        # Validar parámetros
        args = message.text.split(" ", 2)

        if message.reply_to_message:
            target_id = message.reply_to_message.from_user.id
            razon = args[1] if len(args) > 1 else "No especificado"
        else:
            if len(args) < 2:
                return await message.reply("""<b> Usar <code>/unban id razon</code></b>""")

            try:
                target_id = int(args[1])
            except ValueError:
                return await message.reply("<b>El ID debe ser un número válido.</b>")

        # Buscar usuario en la base de datos
        try:
            target_user = await User.get(userid=target_id)
        except DoesNotExist:
            return await message.reply(f"""<b> Error: Usuario no encontrado en mi DB => <code>{target_id}</code></b>""")

        # Verificar si ya está desbaneado
        if target_user.baned == 0:
            return await message.reply(f"""<b> Usuario ya está desbaneado => <code>{target_id}</code></b>""")

        # Desbanear al usuario
        target_user.baned = 0
        await target_user.save()

        # Plantilla de confirmación
        confirmacion = MoralesPlantillas.unban_user(message.from_user.username, user_id, target_user.username, target_id)

        # Responder en el chat, al usuario y enviar a logs
        await message.reply(confirmacion)
        await message.bot.send_message(target_id, confirmacion)
        await message.bot.send_message(os.getenv('LOGS_CHANNEL'), confirmacion)

    except Exception as e:
        print(f"Error en el comando /unban: {e}")
        await message.reply("<b>Ocurrió un error inesperado. Contacta al administrador.</b>")
