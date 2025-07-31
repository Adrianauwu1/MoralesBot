from aiogram import Router, types
from aiogram.filters import Command
from tortoise.transactions import in_transaction
from datetime import datetime, timedelta
from DB import User, KeyUser
from SegPo.FuncionBan import *
from SegPo.FuncionNiveles import *
from SegPo.FuncionRegister import *
from SegPo.Plantillas import MoralesPlantillas
from Prefijos import PrefijosComandos

router = Router()

@router.message(Command("delkey", prefix=PrefijosComandos))
async def delete_key(message: types.Message):
    try:
        # Obtener el user_id del remitente
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

        # Validar argumentos
        args = message.text.split()
        if len(args) < 2:
            return await message.reply("""<b> Usar <code>/delkey Morales-xxx-xxx</code></b>""")

        key = args[1]

        # Buscar la clave en la base de datos
        key_record = await KeyUser.get_or_none(key_gen=key)
        if not key_record:
            return await message.reply(f"""<b> La clave <code>{key}</code> no existe</b>""")

        # Si la clave pertenece a un usuario, ajustar su tiempo de suscripción
        if key_record.status == "CL":
            async with in_transaction():
                user_claim = await User.get_or_none(userid=key_record.userid)
                if user_claim:
                    # Si no tiene créditos, ajustar la suscripción
                    if user_claim.credits == 0:
                        if user_claim.role == "Free User":
                            await user_claim.update_from_dict({"DInicio": None, "DFinal": None, "role": "User"})
                            await user_claim.save()
                        else:
                            if user_claim.DFinal:
                                final_date = datetime.strptime(user_claim.DFinal, "%d-%m-%Y %H:%M:%S")
                                new_date = final_date - timedelta(days=key_record.expiry)
                                if new_date < datetime.now():
                                    await user_claim.update_from_dict({"DInicio": None, "DFinal": None, "role": "User"})
                                else:
                                    await user_claim.update_from_dict({"DFinal": new_date.strftime("%d-%m-%Y %H:%M:%S")})
                                await user_claim.save()

                    # Eliminar la clave
                    await key_record.delete()
                    await message.reply(f"""<b> La clave {key} ha sido eliminada ✅</b>""")
                    return

        # Eliminar la clave si no está reclamada o es de tipo "A"
        await key_record.delete()
        await message.reply(f"""<b> La clave {key} ha sido eliminada ✅</b>""")

    except Exception as e:
        print(f"Error en /delkey: {e}")
        await message.reply("<b>❌ Ocurrió un error al procesar el comando.</b>")
