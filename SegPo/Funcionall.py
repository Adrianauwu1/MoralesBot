from DB.user import User 
from tortoise.exceptions import DoesNotExist 
import pandas as pd
import uuid, re, asyncio, random
from datetime import datetime
from dotenv import load_dotenv
import os, aiohttp
from urllib.parse import urlparse, parse_qs
from re import search
from capmonstercloudclient import CapMonsterClient, ClientOptions
from capmonstercloudclient.requests import RecaptchaV3ProxylessRequest
from capmonster_python import RecaptchaV2Task

load_dotenv(override=True)

class Funcionall:

    _client_options = ClientOptions(api_key=os.getenv('CAPMONSTER_KEY'))
    _cap_monster_client = CapMonsterClient(options=_client_options)

    @staticmethod
    async def rand_browser():
        user_agent = (
            f"Mozilla/5.0 (Windows NT {random.randint(11, 99)}.0; Win64; x64) AppleWebKit/"
            f"{random.randint(111, 999)}.{random.randint(11, 99)} (KHTML, like Gecko) Chrome/"
            f"{random.randint(11, 99)}.0.{random.randint(1111, 9999)}.{random.randint(111, 999)} "
            f"Safari/{random.randint(111, 999)}.{random.randint(11, 99)}"
        )
        return user_agent
    
    @staticmethod
    async def Solverv2(sitekey: str, url: str, max_retries=3, timeout=180) -> str:
        retries = 0

        while retries < max_retries:
            try:

                recaptcha_request = RecaptchaV3ProxylessRequest(
                    websiteUrl=url,
                    websiteKey=sitekey
                )

                result = await asyncio.wait_for(
                    Funcionall._cap_monster_client.solve_captcha(recaptcha_request),
                    timeout=timeout
                )

                captcha = result.get("gRecaptchaResponse")
                if not captcha:
                    raise ValueError("❌ CAPTCHA no resuelto o respuesta vacía.")

                return captcha

            except asyncio.TimeoutError:
                print("⏳ Tiempo de espera agotado para resolver el CAPTCHA.")
            except asyncio.CancelledError:
                print("❌ Tarea de resolver CAPTCHA cancelada inesperadamente.")
            except Exception as e:
                print(f"❌ Error en Solverv2: {e}")

            retries += 1
            await asyncio.sleep(1)

        print("🚨 Falló la resolución del CAPTCHA después de varios intentos.")
        return None
        
    
    @staticmethod
    async def verificar_lenguaje(userid):
        try:
            user = await User.get(userid=userid).values('language')
            return user.language
        except DoesNotExist:
            return "es"
        
    @staticmethod
    async def verificar_vip(userid):
        user = await User.get_or_none(userid=userid)
        if not user:
            return None

        if user.role != "Free User" or int(user.credits) > 0:
            return True

        return False
    
    
    @staticmethod
    async def binchek(bin: str) -> str:

        df = pd.read_csv("bins.csv", encoding='utf-8')
        df['number'] = df['number'].astype(str)
        df = df.drop_duplicates(subset=['number'])

        fila = df[df['number'] == bin]

        if not fila.empty:
            
            pais = fila.iloc[0]['country']
            
            vendor = fila.iloc[0]['vendor']
            typea = fila.iloc[0]['type']
            nivel = fila.iloc[0]['level']
            banco = fila.iloc[0]['bank']
            flag = fila.iloc[0]['flag']


            
            return bin, vendor, typea, nivel, banco, pais, flag
        else:
            return None, None, None, None, None, None, None
        
    @staticmethod
    async def get_cc(text: str):
        try:
            input_msg = text.strip()
            input_numbers = re.findall(r'\d+', input_msg)

            current_year = datetime.now().year

            if not input_numbers: 
                return False
                
            cc = input_numbers[0]


            if len(input_numbers) >= 4:
                mes = input_numbers[1]
                ano = input_numbers[2]
                cvv = input_numbers[3]

                if (cc.isdigit() and 14 <= len(cc) <= 16 and
                    mes.isdigit() and 1 <= int(mes) <= 12 and
                    ano.isdigit() and (current_year <= int(ano) <= 2099 or (21 <= int(ano) <= 99 and len(ano) == 2)) and
                    cvv.isdigit() and len(cvv) <= 4):
                    if len(ano) == 2:
                        ano = "20"+ano
                    return cc, mes, ano, cvv
                else:
                    return False
            else:
                return False
            
        except:
            return False

    def luhn(card: str) -> bool:
        
        return not sum(int(x) * (1 + i % 2) % 10 + (int(x) * (1 + i % 2) // 10) for i, x in enumerate(card[::-1])) % 10

    @staticmethod
    def braintree_generate_uuid():
        return str(uuid.uuid4())

    @staticmethod
    def braintree_generate_correlation_id():
        return str(uuid.uuid4())


    @staticmethod
    async def cc_genv(input_str):
        
        cc, mes, ano, cvv = await Funcionall.regexcc(input_str)
        ccs = []

        while len(ccs) < 10:
            card = str(cc)
            digits = '0123456789'
            list_digits = list(digits)
            random.shuffle(list_digits)
            string_digits = ''.join(list_digits)
            card = card + string_digits
            new_list = list(card)
            list_emty = []
            for i in new_list:
                if i =='x':
                    list_emty.append(str(random.randint(0,9)))
                else:
                    list_emty.append(i)
            list_empty_string = ''.join(list_emty)
            card = list_empty_string
            if card[0] == '3':
                card = card[0:15]
            else:
                card = card[0:16]
            if mes == 'x' or mes is None:
                mes_gen = random.randint(1,12)
                if len(str(mes_gen)) == 1:
                    mes_gen = '0' + str(mes_gen)
            else:
                if len(mes) == 1:
                    mes_gen = "0"+mes
                else:
                    mes_gen = mes
            if ano == 'xxxx' or ano is None:
                ano_gen = random.randint(2025,2031)
            else:
                ano_gen = ano
                if len(str(ano_gen)) == 2:
                    ano_gen = '20' + str(ano_gen)
            if cvv == 'xxx' or cvv is None:
                if card[0:1] == '3': cvv_gen = str(random.randint(1000, 9999)) 
                else: cvv_gen=  str(random.randint(100, 999))
            else:
                if card[0:1] == '3': 
                    cvv_gen = str(random.randint(1000, 9999)) 
                else:
                    cvv_gen = ""
                    for ch in cvv:
                        if ch.isalpha():  # If it's a letter, replace it with a random digit
                            cvv_gen += str(random.randint(0, 9))
                        else:
                            cvv_gen += ch

            
            x = str(card) + '|' + str(mes_gen) + '|' + str(ano_gen) + '|' + str(cvv_gen)    
            a = Funcionall.luhn_verification(card)
            if a:
                ccs.append(x)
            else:
                continue
        return ccs
    
    @staticmethod
    def luhn_verification(num):
        num = [int(d) for d in str(num)]
        check_digit = num.pop()
        num.reverse()
        total = 0
        for i,digit in enumerate(num):
            if i % 2 == 0:
                digit = digit * 2
            if digit > 9:
                digit = digit - 9
            total += digit
        total = total * 9
        return (total % 10) == check_digit
    

    @staticmethod
    async def regexcc(input_str):
        cc_pattern = re.compile(r'^[a-zA-Z0-9]{6,16}$')
        mes_pattern = re.compile(r'^\d{1,2}$')
        ano_pattern = re.compile(r'^\d{2,4}$')
        cvv_pattern = re.compile(r'^\w{3,4}$')

        parts = re.split(r'[|/,.*<>;: ]', input_str)
        
        cc = mes = ano = cvv = None
        
        
        for part in parts:

            if cc is None and cc_pattern.match(part):
                cc = part
            elif mes is None and mes_pattern.match(part) and Funcionall.is_valid_month(part):
                mes = part
            elif ano is None and ano_pattern.match(part) and Funcionall.is_valid_year(part):
                ano = part
            elif cvv is None and cvv_pattern.match(part):
                cvv = part
                

        if cc is None:
            cc = 'xxxx'
        if mes is None :
            mes = 'x'
        if ano is None:
            ano = 'xxxx'
        if cvv is None :
            cvv = 'xxx'

        if cvv == 'xxxx':
            cvv = parts[3]
        
        
        if len(cvv) >= 4:
            cvv = 'xxx'


        BIN = cc[:6]
        
        if not BIN.isdigit() or len(BIN) < 6:
            return None, None, None, None 

        return cc, mes, ano, cvv

    @staticmethod
    def is_valid_month(month):
        return month.isdigit() and 1 <= int(month) <= 12
    
    @staticmethod
    def is_valid_year(year):
        if len(year) == 2:
            year = '20' + year
        return year.isdigit() and 2023 <= int(year) <= 2040
    
    @staticmethod
    async def RandomUserUS():
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get("https://randomuser.me/api/1.2/?nat=US") as response:
                    user = await response.text()
                    street = user.split('"street":"')[1].split('"')[0]
                    city = user.split('"city":"')[1].split('"')[0]
                    state1 = user.split('"state":"')[1].split('"')[0]
                    zipcode = user.split('"postcode":')[1].split(',')[0]
                    phone = user.split('"phone":"')[1].split('"')[0]
                    name = user.split('"first":"')[1].split('"')[0]
                    last = user.split('"last":"')[1].split('"')[0]

                    state_mappings = {
                        "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR",
                        "California": "CA", "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE",
                        "Florida": "FL", "Georgia": "GA", "Hawaii": "HI", "Idaho": "ID",
                        "Illinois": "IL", "Indiana": "IN", "Iowa": "IA", "Kansas": "KS",
                        "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD",
                        "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS",
                        "Missouri": "MO", "Montana": "MT", "Nebraska": "NE", "Nevada": "NV",
                        "New Hampshire": "NH", "New Jersey": "NJ", "New Mexico": "NM", "NY": "NY",
                        "North Carolina": "NC", "North Dakota": "ND", "Ohio": "OH", "Oklahoma": "OK",
                        "Oregon": "OR", "Pennsylvania": "PA", "Rhode Island": "RI", "South Carolina": "SC",
                        "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX", "Utah": "UT",
                        "Vermont": "VT", "Virginia": "VA", "Washington": "WA", "West Virginia": "WV",
                        "Wisconsin": "WI", "Wyoming": "WY"
                    }

                    state = state_mappings.get(state1.capitalize(), "NY")

                    await session.close()
                    return street, city, state, zipcode, phone, name, last, state1
                
        except Exception as e:
            await session.close()
            street = "Street 342"
            city = "New York"
            state = "NY"
            zipcode = "10080"
            phone = "5515263214"
            name = "Jose"
            last = "Perez"
            state1 = "New York"
            return street, city, state, zipcode, phone, name, last, state1
        

    from tortoise.exceptions import DoesNotExist

    @staticmethod
    async def quitcreds(userid: int, res: str, name: str):
        try:
            # Obtener información del usuario
            user = await User.get_or_none(userid=userid)
            if not user:
                return "$Error_ ⚠️", "Usuario no encontrado"

            # Verificar tipo de usuario
            resu = await User.filter(username=name).first()
            tipo = resu.role if resu else "free"

            if tipo == "free":
                if user.credits <= 0:
                    return None, None  # Sin créditos, no se hace nada

                # Verificar y descontar créditos
                if user.credits < 1:
                    return "$Error_ ⚠️", "No le quedan Creditos | No Credits left"

                # Determinar cuántos créditos restar según la respuesta
                cred = 3 if res == "Approved ✅" else 2 if res == "Declined ❌" else 0

                if user.credits < cred:
                    return "$Error_ ⚠️", "No le quedan Creditos | No Credits left"

                # Restar créditos y guardar
                user.credits -= cred
                await user.save()
                return None, None

            else:
                if user.credits < 1:
                    return "$Error_ ⚠️", "No le quedan Creditos | No Credits left"

                cred = 3 if res == "Approved ✅" else 2 if res == "Declined ❌" else 0

                if user.credits < cred:
                    return "$Error_ ⚠️", "No le quedan Creditos | No Credits left"

                user.credits -= cred
                await user.save()
                return None, None

        except Exception as e:
            return "$Error_ ⚠️", f"Error en quitcreds: {e}"

    @staticmethod
    async def verfcredvip(userid: int):
        try:
            # Obtener el usuario
            user = await User.get_or_none(userid=userid)
            if not user:
                return "No active subscription"
            
            if user.credits == 0:
                return None

            # Verificar si el usuario tiene suficientes créditos
            if user.credits < 2:
                return "No le quedan Creditos | No Credits lef"

            # Quitar créditos y guardar cambios
            user.credits -= 2
            await user.save()
            return None  # Se quitaron créditos correctamente

        except Exception as e:
            return f"Error en verfcredvip: {e}"
        
    @staticmethod
    async def Solverv3(ar, k, co, hl, v, size, cb) -> str:
        try:
            session = aiohttp.ClientSession()
            anchor_url = f"https://www.google.com/recaptcha/api2/anchor?ar={ar}&k={k}&co={co}&hl={hl}&v={v}&size={size}&cb={cb}" 
            reload_url = f"https://www.google.com/recaptcha/api2/reload?k={k}"
            user_agent = (
                f"Mozilla/5.0 (Windows NT {random.randint(11, 99)}.0; Win64; x64) AppleWebKit/"
                f"{random.randint(111, 999)}.{random.randint(11, 99)} (KHTML, like Gecko) Chrome/"
                f"{random.randint(11, 99)}.0.{random.randint(1111, 9999)}.{random.randint(111, 999)} "
                f"Safari/{random.randint(111, 999)}.{random.randint(11, 99)}"
            )
            headers = {"User-Agent": user_agent}
            url_var = parse_qs(urlparse(anchor_url).query)

            r = await session.get(anchor_url, headers=headers)
            rs = await r.text()
            anchor_token = search(r'type="hidden" id="recaptcha-token" value="([^"]+)"', rs).group(1)

            value1 = url_var['v'][0]
            value2 = url_var['k'][0]
            value3 = url_var['co'][0]

            data = f"v={value1}&reason=q&c={anchor_token}&k={value2}&co={value3}&hl=en&size=invisible"

            headers = {"Referer": str(r.url),"Content-Type": "application/x-www-form-urlencoded"}

            r = await session.post(reload_url, headers=headers, data=data)
            ge = await r.text()
            text = ge.split('["rresp","')[1].split('"')[0]

            await session.close()
            return text
        except Exception as e:
            linea = str(e.__traceback__.tb_lineno)
            print("Error en la linea en comando ontool: " + linea + " " + str(e))
            await session.close()
            return "Error"