from aiogram import Router, types
from aiogram.filters import Command
from SegPo.FuncionBan import *
from SegPo.FuncionNiveles import *
from SegPo.FuncionRegister import *
from SegPo.Plantillas import MoralesPlantillas
from Prefijos import PrefijosComandos
from DB import User
from dotenv import load_dotenv
import os

load_dotenv(override=True)

router = Router()

@router.message(Command("ban", prefix=PrefijosComandos))
async def ban_user(message: types.Message):
    try:
        user_id = message.from_user.id

        if not await Register.verificar_registro(user_id):
            return await message.reply(MoralesPlantillas.unregister())

        valor, razon = await BanUser.verificar_ban(user_id)
        if valor:
            return await message.reply(MoralesPlantillas.ban_user(razon))

        if not await Privilegios.verificar_nivel(user_id, 1):
            return await message.reply(MoralesPlantillas.nivel_restringido())

        data = message.text.split(" ", 2)

        if not message.reply_to_message and len(data) < 2:
            return await message.reply('<b> Usar <code>/ban ID razon</code></b>')

        if message.reply_to_message:
            target_id = message.reply_to_message.from_user.id
            razon = data[1] if len(data) > 1 else "No especificado"
        else:
            target_id = data[1]
            razon = data[2] if len(data) > 2 else "No especificado"

        if str(target_id) == str(os.getenv('OWNER')):
            return await message.reply("<b> No puedes banear a mi creador</b>")

        user = await User.filter(userid=target_id).first()

        if user:
            if user.baned:
                return await message.reply(f"<b> Usuario ya baneado => <code>{target_id}</code></b>")
            await User.filter(userid=target_id).update(baned=1)
        else:
            await User.create(userid=target_id, baned=1)


        
        await message.reply(MoralesPlantillas.ban_user(razon))

        await message.bot.send_message(os.getenv('LOGS_CHANNEL'), MoralesPlantillas.ban_user2(razon, message.from_user.username, message.from_user.id,user.username, target_id))

    except Exception as e:
        print(f"Error en la línea {e.__traceback__.tb_lineno}: {e}")
        return await message.reply("<b>Error interno al ejecutar el comando de ban.</b>")
