from aiogram import Router, types
from aiogram.filters import Command
from datetime import datetime
from Prefijos import PrefijosComandos
from SegPo.FuncionBan import *
from SegPo.FuncionNiveles import *
from SegPo.FuncionRegister import *
from SegPo.Plantillas import MoralesPlantillas

from DB import Tool
from dotenv import load_dotenv
import os

load_dotenv(override=True)

router = Router()

@router.message(Command("addtool", prefix=PrefijosComandos))
async def add_tool(message: types.Message):
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
        if len(data) < 4:
            return await message.reply('<b> Usar <code>/addtool nombre comando tipo(free, paid)</code></b>')
        
        name, comand, tipo = data[1:4]
        date1 = datetime.now().strftime('%d-%m-%Y')
        
        addt = await Tool.create(
            name=name, comand=comand, status=1, type=tipo, review=date1
        )
        
        if addt:
            mensaje_tool = MoralesPlantillas.addtool(name, tipo, comand, date1)
            await message.reply(mensaje_tool)
            return await message.bot.send_message(os.getenv('LOGS_CHANNEL'), mensaje_tool)
        else:
            return await message.reply(f"<b>Error al añadir la tool => </b> <code>{name}</code>")
    except Exception as e:
        print(f"Error en la línea {e.__traceback__.tb_lineno}: {e}")
        return await message.reply(f"<b>Error al añadir la tool => </b> <code>{name}</code>")
