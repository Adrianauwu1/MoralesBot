from aiogram import Router, types
from aiogram.filters import Command
from datetime import datetime
from DB import User
from SegPo.Plantillas import MoralesPlantillas
from Prefijos import PrefijosComandos

router = Router()  # Se usa Router en vez de Dispatcher


async def get_user_info(user_id: int):
    """Obtiene información del usuario desde la base de datos"""
    
    user = await User.get_or_none(userid=user_id)
    
    if not user:
        return None, MoralesPlantillas.unregister()

    # Obtener valores
    role = user.role
    username = user.username
    creditos = user.credits
    antispam = user.antispam
    inicio = user.DInicio
    expiracion = user.DFinal
    banned = user.baned
    apodo = user.apodo
    nivel = user.nivel

    baned = "True" if banned else "False"

    if nivel:
        antispam = f"<code> {antispam}</code> | <b>Rango:</b> [<code>{nivel}</code>]"
    else:
        antispam = f"<code> {antispam}</code>"


    # Calcular tiempo restante
    if inicio and expiracion:
        expiracion_dt = datetime.strptime(expiracion, "%d-%m-%Y %H:%M:%S")
        ahora = datetime.now()
        diferencia = expiracion_dt - ahora
        
        dias = diferencia.days
        horas, resto_minutos = divmod(diferencia.seconds, 3600)
        minutos, segundos = divmod(resto_minutos, 60)

        tiempo_restante = f"<i>{dias}/{horas}/{minutos}/{segundos}</i>"
    else:
        tiempo_restante = "0"

    if apodo:
        role = f"{role} [<code>{apodo}</code>]"

    return user, MoralesPlantillas.infouser(username, user_id, user.firstname, baned, role, creditos, antispam, tiempo_restante)


@router.message(Command("me", prefix=PrefijosComandos))
async def cmd_me(message: types.Message):
    args = message.text.split()[1:]  # Obtener argumentos después del comando
    if args and args[0].isdigit():
        user_id = int(args[0])  # Si hay un argumento numérico, usarlo como ID
    elif message.reply_to_message:
        user_id = message.reply_to_message.from_user.id  # Si es una respuesta, usar el ID del usuario respondido
    else:
        user_id = message.from_user.id  # Si no hay argumentos ni respuesta, usar el ID del usuario que envió el mensaje

    user, response = await get_user_info(user_id)

    if user:
        reply_markup = MoralesPlantillas.reply_freeuser2() if user.role == "Free User" else None
        await message.reply(response, reply_markup=reply_markup, parse_mode="HTML")
    else:
        await message.reply(response, parse_mode="HTML")
