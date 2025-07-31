from aiogram import Router, types
from aiogram.filters import Command
from SegPo.Funcionall import *
from SegPo.FuncionBan import *
from SegPo.FuncionNiveles import *
from SegPo.FuncionRegister import *
from SegPo.FuncionGrupos import Grupos
from SegPo.Plantillas import MoralesPlantillas
from DB import User, Tool
from Prefijos import PrefijosComandos
import re

router = Router()

@router.message(Command("bin", prefix=PrefijosComandos))
async def bin_tool(message: types.Message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    grupo = Grupos()


    if not await Register.verificar_registro(user_id):
        return await message.reply(MoralesPlantillas.unregister())

    valor, razon = await BanUser.verificar_ban(user_id)
    if valor:
        return await message.reply(MoralesPlantillas.ban_user(razon))

    user_info = await User.get_or_none(userid=user_id)
    if not user_info:
        return await message.reply("<b>Error: No se encontró la información del usuario.</b>")
    role = user_info.role

    chat_type = message.chat.type
    chat_name = message.chat.title
    chat_username = message.chat.username or ""

    await grupo.registrar(chat_id, chat_name, chat_username, chat_type)

    bin_tool_info = await Tool.get_or_none(name="Bin")
    if not bin_tool_info:
        return await message.reply("<b>⚠️ There is a problem with the bin command, which we cannot show you the information you have just requested.</b>")

    status, review, reason, tipo = bin_tool_info.status, bin_tool_info.review, bin_tool_info.razon, bin_tool_info.type

    # Validar acceso según el tipo de herramienta
    user_is_vip = await Funcionall.verificar_vip(user_id)
    group_is_premium = await grupo.verificar_premium(chat_id)

    if tipo == "Free" and not user_is_vip:
        if chat_type == "private":
            return await message.reply(MoralesPlantillas.reply_freeuser(), reply_markup=MoralesPlantillas.reply_freeuser2())
        if chat_type in ["supergroup", "group"] and not group_is_premium:
            return await message.reply(MoralesPlantillas.reply_freeuser(), reply_markup=MoralesPlantillas.reply_freeuser2())

    if tipo == "paid" and not (user_is_vip or group_is_premium):
        return await message.reply(MoralesPlantillas.reply_freeuser(), reply_markup=MoralesPlantillas.reply_freeuser2())

    # Validar si la herramienta está desactivada
    if status == 0:
        return await message.reply(MoralesPlantillas.off_tool("Bin", review, reason))

    # Obtener el BIN del mensaje
    input_text = message.reply_to_message.text if message.reply_to_message else message.text

    bin_numbers = re.findall(r'\d{6}', input_text)

    if not bin_numbers:
        return await message.reply(f""" Usar <code>$bin 416497</code></b>""")

    bin_code = bin_numbers[0]

    try:
        bin_data = await Funcionall.binchek(bin_code)
        bin_code, brand, types, level, bank, country_name, country_flag = bin_data
    except Exception as e:
        print(f"Error: {e} ")
        return await message.reply(f' Bin Not found: <code>{bin_code} ❌</code></b>')

    return await message.reply(MoralesPlantillas.bin_chk(bin_code, brand, level, bank, country_name, country_flag, types, message.from_user.username, role))