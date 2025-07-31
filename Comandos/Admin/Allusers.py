from aiogram import Router, types
from aiogram.filters import Command
from Prefijos import PrefijosComandos
from SegPo.FuncionBan import *
from SegPo.FuncionNiveles import *
from SegPo.FuncionRegister import *
from SegPo.Plantillas import MoralesPlantillas
from DB import User, KeyUser, Grupo, Bin
from dotenv import load_dotenv
import os

load_dotenv(override=True)

router = Router()

@router.message(Command("allusers", prefix=PrefijosComandos))
async def all_users(message: types.Message):
    verfreg = await Register.verificar_registro(message.from_user.id)
    if not verfreg:
        return await message.reply(MoralesPlantillas.unregister())

    valor, razon = await BanUser.verificar_ban(message.from_user.id)
    if valor:
        return await message.reply(MoralesPlantillas.ban_user(razon))

    verfniv = await Privilegios.verificar_nivel(message.from_user.id, 1)
    if not verfniv:
        return await message.reply(MoralesPlantillas.nivel_restringido())

    try:
        results = await User.all().count()
        if results == 0:
            return await message.reply('<b> No hay usuarios registrados</b>')

        vip = await User.filter(role="Premium").count()
        dev = await User.filter(role="DEV").count()
        admin = await User.filter(role="ADMIN").count()
        seller = await User.filter(role="SELLER").count()
        free = await User.filter(role="Free User").count()

        usadas = await KeyUser.filter(key_status="CL").count()
        libres = await KeyUser.filter(key_status="A").count()
        keys = await KeyUser.all().count()

        grupos = await Grupo.filter(autorizado=1).count()
        bins = await Bin.filter(baned=True).count()
        userban = await User.filter(baned=True).count()

        mensaje = MoralesPlantillas.all_users(results, vip, dev, admin, seller, free, usadas, libres, keys, grupos, bins, userban)
        return await message.reply(mensaje)



    except Exception as e:
        print(f"Error en el comando allusers: {e}")
        return await message.reply("<b>Error al obtener los usuarios</b>")
