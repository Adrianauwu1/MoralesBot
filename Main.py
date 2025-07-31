import asyncio
import logging
import importlib
import sys, os
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv
from tortoise import Tortoise
from SegPo.RouterLoad import RouterCargados


# Cargar variables de entorno
load_dotenv()
TOKEN = os.getenv("TOKEN")
# Configurar el logging
if not TOKEN:
    raise ValueError("El token del bot no está configurado en las variables de entorno.")

logging.basicConfig(level=logging.INFO)

dp = Dispatcher()

async def init_db():
    """Inicializa la base de datos SQLite."""
    try:
        await Tortoise.init(
            db_url="sqlite://Morales.db",
            modules={"models": ["DB"]}
        )
        await Tortoise.generate_schemas(safe=True)
        logging.info(f"✅ Base de datos Morales conectada")
    except Exception as e:
        logging.error(f"❌ Error al conectar la base de datos: {e}")

async def close_db():
    """Cierra la base de datos."""
    await Tortoise.close_connections()

async def on_startup(bot: Bot):
    """Iniciar bot y monitorear cambios en comandos."""
    logging.info("🚀 Iniciando bot con polling...")

    routers = RouterCargados()
    for router in routers:
        dp.include_router(router)

async def on_shutdown(bot: Bot):
    """Cierra correctamente el bot."""
    logging.info("🛑 Apagando bot...")
    await close_db()
    await bot.session.close()

async def main():
    """Función principal."""
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode="HTML"))

    await init_db()
    await on_startup(bot)

    try:
        await dp.start_polling(bot)
    finally:
        await on_shutdown(bot)

if __name__ == "__main__":
    asyncio.run(main())
