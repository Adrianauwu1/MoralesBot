from DB import *
from dotenv import load_dotenv
import os

load_dotenv(override=True)

class Privilegios:
    
    async def _obtener_nivel(userid):
        result = await User.get(userid=userid)
        return result.nivel if result else None
    
    @staticmethod
    async def verificar_nivel(userid, nivel_permiso):
        nivel_usuario = await Privilegios._obtener_nivel(userid)
        
        ownerid = os.getenv('OWNER')
        if int(userid) == int(ownerid): 
            return True

        else:
            nivel_permiso = int(nivel_permiso)

            if nivel_usuario is None:
                return False 
            
            nivel_usuario = int(nivel_usuario)

            if nivel_permiso == 0:
                return True
            
            elif nivel_permiso == 1:
                return nivel_usuario >= 1
            elif nivel_permiso == 2:
                return nivel_usuario >= 2
            elif nivel_permiso == 3:
                return nivel_usuario >= 3
            else:
                return False