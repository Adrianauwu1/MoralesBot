from datetime import datetime, timedelta
from DB import *

class Grupos:
    async def registrar(self, group_id, name, username, chat_type):
        if chat_type not in ("supergroup", "group"):
            return False

        grupo = await Grupo.get_or_none(group_id=group_id)
        if not grupo:
            await Grupo.create(
                group_id=group_id,
                autorizado=0, 
                name=name,
                username=username or "",
                Inicio="",
                Fin="",
                userid=0,
                level="user"
            )
            return True

        return False

    async def activar_premium(self, group_id, dias, userid):
        grupo = await Grupo.get_or_none(group_id=group_id)
        if not grupo:
            return False

        fecha_actual = datetime.now()

        if grupo.autorizado == 1 and grupo.Fin:
            fecha_final = datetime.strptime(grupo.Fin, "%d-%m-%Y %H:%M:%S")
            fecha_expiracion = fecha_final + timedelta(days=dias)
        else:
            fecha_expiracion = fecha_actual + timedelta(days=dias)

        grupo.Inicio = fecha_actual.strftime("%d-%m-%Y %H:%M:%S")
        grupo.Fin = fecha_expiracion.strftime("%d-%m-%Y %H:%M:%S")
        grupo.userid = userid
        grupo.autorizado = 1

        await grupo.save()
        return True

    async def desactivar_premium(self, group_id):
        grupo = await Grupo.get_or_none(group_id=group_id)
        if not grupo:
            return False

        grupo.autorizado = 0
        grupo.Inicio = ""
        grupo.Fin = ""

        await grupo.save()
        return True

    async def verificar_premium(self, group_id):
        grupo = await Grupo.get_or_none(group_id=group_id)
        return grupo and grupo.autorizado == 1
