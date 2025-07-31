from DB import *

class Register:
    
    @staticmethod
    async def verificar_registro(userid: int) -> bool:
        return await User.exists(userid=userid)
