from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from tortoise.exceptions import DoesNotExist
from DB import KeyUser, User
from SegPo.FuncionBan import *
from SegPo.FuncionNiveles import *
from SegPo.FuncionRegister import *
from SegPo.Plantillas import MoralesPlantillas
from Prefijos import PrefijosComandos
from datetime import datetime, timedelta
import os

router = Router()

@router.message(Command("claim", prefix=PrefijosComandos))
async def claim(message: Message):
    try:

        user_id = message.from_user.id
        first_name = message.from_user.first_name
        chat_id = message.chat.id

        if not await Register.verificar_registro(user_id):
            return await message.reply(MoralesPlantillas.unregister())

        valor, razon = await BanUser.verificar_ban(user_id)
        if valor:
            return await message.reply(MoralesPlantillas.ban_user(razon))

        args = message.text.split()
        if len(args) < 2:
            return await message.reply("""<b> Usar <code>/claim Morales-xxx-xxx</code></b>""")

        key = args[1]

        try:
            key_info = await KeyUser.get(key_gen=key)
        except DoesNotExist:
            return await message.reply("""<b> Key inválida.</b>""")

        if key_info.key_status == "CL" or key_info.expiry < 0:
            return await message.reply(MoralesPlantillas.key_claimed(key, first_name))

        try:
            target_user = await User.get(userid=user_id)
        except DoesNotExist:
            return await message.reply("""<b>No tienes una cuenta registrada.</b>""")

        fecha_actual = datetime.now()
        rango = key_info.status
        
        if target_user.role == "Free User" or not target_user.DFinal:
            nueva_fecha_expiracion = fecha_actual + timedelta(days=key_info.expiry)
            target_user.DInicio = fecha_actual.strftime("%d-%m-%Y %H:%M:%S")
        else:
            try:
                fecha_expiracion_actual = datetime.strptime(target_user.DFinal, "%d-%m-%Y %H:%M:%S")
            except ValueError:
                return await message.reply("<b>Error: Formato de fecha inválido en la base de datos.</b>")

            nueva_fecha_expiracion = fecha_expiracion_actual + timedelta(days=key_info.expiry)

        target_user.role = rango
        target_user.antispam = 16
        target_user.DFinal = nueva_fecha_expiracion.strftime("%d-%m-%Y %H:%M:%S")
        await target_user.save()

        key_info.key_status = "CL"
        key_info.userid = user_id
        await key_info.save()

        mensaje_exito = MoralesPlantillas.key_success(key, first_name, user_id, key_info.expiry, 20, fecha_actual.strftime("%d-%m-%Y %H:%M:%S"), rango)
        await message.reply(mensaje_exito)
        await message.bot.send_message(user_id, MoralesPlantillas.msg_succes(user_id, key_info.expiry, fecha_actual.strftime("%d-%m-%Y %H:%M:%S"), rango))
        await message.bot.send_message(os.getenv("LOGS_CHANNEL"), mensaje_exito)

    except Exception as e:
        print(f"Error en el comando /claim: {e}")
        await message.reply(f"<b>Error al reclamar la key: </b> <code>{key}</code>")
