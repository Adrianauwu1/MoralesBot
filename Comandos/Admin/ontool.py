from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from tortoise.exceptions import DoesNotExist
from SegPo.FuncionBan import *
from SegPo.FuncionNiveles import *
from SegPo.FuncionRegister import *
from DB import Tool
from SegPo.Plantillas import MoralesPlantillas
from Prefijos import PrefijosComandos

router = Router()

@router.message(Command("ontool", prefix=PrefijosComandos))
async def on_tool(message: Message):
    try:
        user_id = message.from_user.id

        # Verificar registro
        if not await Register.verificar_registro(user_id):
            return await message.reply(MoralesPlantillas.unregister())

        # Verificar si está baneado
        valor, razon = await BanUser.verificar_ban(user_id)
        if valor:
            return await message.reply(MoralesPlantillas.ban_user(razon))

        # Verificar privilegios (nivel 2 requerido)
        if not await Privilegios.verificar_nivel(user_id, 2):
            return await message.reply(MoralesPlantillas.nivel_restringido())

        # Validar parámetros
        args = message.text.split(" ", 2)
        if len(args) < 2:
            return await message.reply(""" Usar <code>/ontool Nombre</code>""")

        name = args[1]
        razon = args[2] if len(args) > 2 else "No especificado"

        # Buscar la herramienta en la base de datos
        try:
            tool = await Tool.get(name=name)
        except DoesNotExist:
            return await message.reply(f""" Tool <code>{name}</code> no existe""")

        # Verificar si ya está encendida
        if tool.status == 1:
            return await message.reply(f""" Tool <code>{name}</code> ya está encendido""")

        # Actualizar el estado de la herramienta
        tool.status = 1
        tool.razon = razon
        await tool.save()

        await message.reply(f""" Tool <code>{name}</code> encendido""")

    except Exception as e:
        print(f"Error en el comando /ontool: {e}")
        await message.reply("Ocurrió un error inesperado. Contacta al administrador.")
