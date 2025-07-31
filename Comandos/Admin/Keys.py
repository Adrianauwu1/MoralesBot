from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from tortoise.exceptions import DoesNotExist
from DB import KeyUser
from SegPo.FuncionBan import *
from SegPo.FuncionNiveles import *
from SegPo.FuncionRegister import *
from SegPo.Plantillas import MoralesPlantillas
from Prefijos import PrefijosComandos
from datetime import datetime
import random, string, os
from dotenv import load_dotenv

router = Router()

load_dotenv(override=True)



def generar_clave(longitud=5):
    caracteres = string.ascii_letters + string.digits
    return ''.join(random.choice(caracteres) for _ in range(longitud))

@router.message(Command("keygen", prefix=PrefijosComandos))
async def key_gen(message: Message):
    try:
        user_id = message.from_user.id

        # Verificar registro
        if not await Register.verificar_registro(user_id):
            return await message.reply(MoralesPlantillas.unregister())

        # Verificar si está baneado
        valor, razon = await BanUser.verificar_ban(user_id)
        if valor:
            return await message.reply(MoralesPlantillas.ban_user(razon))

        # Verificar privilegios
        if not await Privilegios.verificar_nivel(user_id, 0):
            return await message.reply(MoralesPlantillas.nivel_restringido())

        # Validar parámetros
        args = message.text.split()
        if len(args) < 3:
            return await message.reply("""<b> Usar <code>/keygen dias rango</code></b>""")

        dias = args[1]
        rango = args[2]

        if not dias.isdigit() or int(dias) < 1:
            return await message.reply("""<b> Los días deben ser un número válido mayor a 0.</b>""")


        ALLOWED_RANGES = list(map(str.strip, os.getenv('RANGOS_VENDIDOS', "").split(",")))

        if rango not in ALLOWED_RANGES:
            return await message.reply(f"""<b> Rango no válido. Usa uno de estos: {', '.join(ALLOWED_RANGES)}</b>""")

        # Generar clave única
        key = f"Morales~{generar_clave()}~{generar_clave()}~Bot"

        # Guardar en la base de datos
        await KeyUser.create(
            user_id=user_id,
            key_gen=key,
            key_status="A",
            status=rango,
            expiry=int(dias),
            antispam=0,
            userid=user_id
        )

        # Formatear fecha
        fecha_hora_actual = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

        # Responder al usuario
        plan = MoralesPlantillas.gen_key(key, dias, message.from_user.username, fecha_hora_actual, rango)
        await message.reply(plan)

    except Exception as e:
        print(f"Error en el comando /keygen: {e}")
        await message.reply("<b>Ocurrió un error inesperado. Contacta al administrador.</b>")
