from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from datetime import datetime
from SegPo.FuncionBan import *
from SegPo.FuncionNiveles import *
from SegPo.FuncionRegister import *
from SegPo.Plantillas import MoralesPlantillas
from Prefijos import PrefijosComandos
import time


START_TIME = datetime.now()

router = Router()

@router.message(Command("uptime", prefix=PrefijosComandos))
async def uptime(message: Message):
    try:
        user_id = message.from_user.id

        # Verificar registro
        if not await Register.verificar_registro(user_id):
            return await message.reply(MoralesPlantillas.unregister())

        # Verificar si está baneado
        valor, razon = await BanUser.verificar_ban(user_id)
        if valor:
            return await message.reply(MoralesPlantillas.ban_user(razon))

        # Verificar privilegios (nivel 0 requerido)
        if not await Privilegios.verificar_nivel(user_id, 0):
            return await message.reply(MoralesPlantillas.nivel_restringido())

        # Calcular tiempo de actividad (uptime)
        now = datetime.now()
        uptime_duration = now - START_TIME

        # Medir latencia (ping)
        start_time = time.time()
        sent_message = await message.reply("Ping!")
        latency = round(time.time() - start_time, 2)

        # Formatear respuesta
        uptime_text = f"Pong!: {latency}s\n"
        uptime_text += f"Uptime: {uptime_duration.days}d, {uptime_duration.seconds // 3600}h, "
        uptime_text += f"{(uptime_duration.seconds // 60) % 60}m, {uptime_duration.seconds % 60}s"

        # Editar mensaje con la respuesta final
        await sent_message.edit_text(uptime_text)

    except Exception as e:
        print(f"Error en el comando /uptime: {e}")
        await message.reply("<b>Ocurrió un error inesperado. Contacta al administrador.</b>")
