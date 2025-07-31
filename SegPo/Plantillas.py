import random

class MoralesPlantillas:
    @staticmethod
    def yaregistrado():
        return "Ya estás registrado."

    @staticmethod
    def register(user_id):
        return f"Usuario {user_id} registrado con éxito."

    @staticmethod
    def infouser(username, userid, first, baned, role, creditos, antispam, dias):
        return (
            f"Información del usuario:\n"
            f"Username: {username}\n"
            f"ID: {userid}\n"
            f"Nombre: {first}\n"
            f"Baneado: {baned}\n"
            f"Rol: {role}\n"
            f"Créditos: {creditos}\n"
            f"Antispam: {antispam}\n"
            f"Tiempo restante: {dias}"
        )

    @staticmethod
    def reply_freeuser2():
        freeusers = {
            "inline_keyboard": [
                [
                    {"text": "𝒎𝒐𝒓𝒂𝒍𝒆𝒔 ", "url": "https://t.me/CR3MA"}
                                                    ]
            ]
        }
        return freeusers
    
    @staticmethod
    def unregister():
        return "Usuario no registrado. Por favor, usa /register para registrarte."
    
    @staticmethod
    def ban_user(razon):
        return f"Estás baneado. Razón: {razon}"
    
    @staticmethod
    def nivel_restringido():
        return "Tu nivel de acceso es restringido. No tienes permiso para usar este comando."
    
    @staticmethod
    def reply_freeuser():
        return "Este comando es solo para usuarios premium. Por favor, actualiza tu cuenta para acceder a esta herramienta."

    @staticmethod
    def off_tool(name, review, razon):
        return (
            f"La herramienta {name} está desactivada.\n"
            f"Fecha de revisión: {review}\n"
            f"Razón: {razon}"
        )

    @staticmethod
    def bin_chk(BIN, brand, level, bank, country_name, country_flag, types, username, role):
        return (
            f"Información del BIN:\n"
            f"BIN: <code>{BIN}</code>\n"
            f"Marca: {brand}\n"
            f"Nivel: {level}\n"
            f"Banco: {bank}\n"
            f"País: {country_name} {country_flag}\n"
            f"Tipo: {types}\n"
            f"Solicitado por: @{username} ({role})"
        )
    @staticmethod
    def addtool(name, tipo, comand, date1):
        return (
            f"Herramienta añadida con éxito:\n"
            f"Nombre: <code>{name}</code>\n"
            f"Comando: <code>{comand}</code>\n"
            f"Tipo: <code>{tipo}</code>\n"
            f"Fecha de revisión: <code>{date1}</code>"
        )
    
    @staticmethod
    def all_users(results, vip, dev, admin, seller, free, usadas, libres, keys, grupos, bins, userban):
        return (
            f"Total de usuarios registrados: {results}\n"
            f"Premium: {vip}, DEV: {dev}, Owner: {admin}, Seller: {seller}, Free User: {free}\n"
            f"Keys usadas: {usadas}, Keys libres: {libres}, Total de keys: {keys}\n"
            f"Grupos autorizados: {grupos}, Bins baneados: {bins}, Usuarios baneados: {userban}"
        )
    
    @staticmethod
    def gen_key(key, dias, username, fecha_hora_actual, rango):
        return (
            f"Clave generada con éxito:\n"
            f"Clave: <code>{key}</code>\n"
            f"Días de validez: {dias}\n"
            f"Generada por: @{username}\n"
            f"Fecha y hora: {fecha_hora_actual}\n"
            f"Rango: {rango}"
        )
    @staticmethod
    def key_success(key, first, userid, dias, antispam, now, rango):
        return (
            f"La clave <code>{key}</code> ha sido reclamada con éxito.\n"
            f"Usuario: {first}\n"
            f"ID: {userid}\n"
            f"Días de validez: {dias}\n"
            f"Antispam: {antispam}\n"
            f"Fecha y hora: {now}\n"
            f"Rango: {rango}"
        )
    @staticmethod
    def msg_succes(userid, dias, now, rango):
        return (
            f"Tu clave ha sido reclamada con éxito.\n"
            f"ID: {userid}\n"
            f"Días de validez: {dias}\n"
            f"Fecha y hora: {now}\n"
            f"Rango: {rango}"
        )
    @staticmethod
    def add_cred(username, userid, creditos, user_act, ide_act):
        return (
            f"Créditos añadidos con éxito:\n"
            f"Usuario: @{username} ({userid})\n"
            f"Créditos añadidos: {creditos}\n"
            f"Usuario afectado: @{user_act} ({ide_act})"
        )

    @staticmethod
    def unban_user(username, userid, replyuser, replyid):
        return (
            f"Usuario desbaneado con éxito:\n"
            f"Desbaneado por: @{username} ({userid})\n"
            f"Usuario afectado: @{replyuser} ({replyid})"
        )

    @staticmethod
    def ban_user2(razon, username, userid, replyuser, replyid):
        return (
            f"Usuario baneado con éxito:\n"
            f"Razón: {razon}\n"
            f"Ban por: @{username} ({userid})\n"
            f"Usuario afectado: @{replyuser} ({replyid})"
        )

    @staticmethod
    def unban_user(username, userid, replyuser, replyid):
        return (
            f"Usuario desbaneado con éxito:\n"
            f"Desbaneado por: @{username} ({userid})\n"
            f"Usuario afectado: @{replyuser} ({replyid})"
        )