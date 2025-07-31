from DB import *


class BanUser:
    
    @staticmethod
    async def verificar_ban(userid):

        ban = await User.get(userid=userid)
        if ban.baned == 1:
            return True, ban.razon
        else:
            return False, None