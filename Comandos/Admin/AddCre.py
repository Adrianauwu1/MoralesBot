from aiogram import Router, types, Bot
from aiogram.filters import Command
from Prefijos import PrefijosComandos
from SegPo.FuncionBan import *
from SegPo.FuncionNiveles import *
from SegPo.FuncionRegister import *
from SegPo.Plantillas import MoralesPlantillas
from DB import *
from dotenv import load_dotenv
import os

load_dotenv(override=True)

router = Router()

@router.message(Command("addcre", prefix=PrefijosComandos))
async def add_creditos(message: types.Message):
    verfreg = await Register.verificar_registro(message.from_user.id)
    if not verfreg:
        return await message.reply(MoralesPlantillas.unregister())

    valor, razon = await BanUser.verificar_ban(message.from_user.id)
    if valor:
        return await message.reply(MoralesPlantillas.ban_user(razon))

    verfniv = await Privilegios.verificar_nivel(message.from_user.id, 0)
    if not verfniv:
        return await message.reply(MoralesPlantillas.nivel_restringido())

    try:
        data = message.text.split(" ", 3)
        if len(data) < 3:
            return await message.reply('<b> Uso correcto del comando: <code>$addcred id credits</code></b>')

        ide = data[1]
        try:
            creditos = int(data[2])
        except ValueError:
            return await message.reply('<b> The amount of credits provided is invalid.</b>')

        if creditos <= 0:
            return await message.reply('<b> The amount of credits provided is invalid.</b>')

        usuario = await User.get_or_none(userid=ide)
        if not usuario:
            return await message.reply(MoralesPlantillas.unregister())

        old_credits = usuario.credits 
        nuevo_credito = old_credits + creditos

        actualizado = await User.filter(userid=ide).update(credits=nuevo_credito)

        if actualizado:
            mensaje_cred = MoralesPlantillas.add_cred(message.from_user.username, message.from_user.id, creditos, usuario.username, ide)
            await message.reply(mensaje_cred)
            await message.bot.send_message(chat_id=ide, text=mensaje_cred)
            return await message.bot.send_message(chat_id=os.getenv('LOGS_CHANNEL'), text=mensaje_cred)
        else:
            return await message.reply(f"<b>Error when assigning the credits to the user:</b> <code>{ide}</code>")
    except Exception as e:
        print(e)
        return await message.reply(f"<b>Error when assigning the credits to the user:</b> <code>{ide}</code>")
