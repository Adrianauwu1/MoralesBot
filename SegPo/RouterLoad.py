import os
import importlib
import logging
import sys
from aiogram import Router

def RouterCargados():
    routers = []
    base_folders = ["Comandos", "Callbacks"]

    for base_folder in base_folders:
        for root, _, files in os.walk(base_folder):
            for file in files:
                if file.endswith(".py") and file != "__init__.py":
                    module_path = os.path.join(root, file)
                    module_name = module_path.replace(os.sep, ".").replace(".py", "")

                    try:
                        if module_name in sys.modules:
                            del sys.modules[module_name]
                            
                        module = importlib.import_module(module_name)

                        if hasattr(module, "router") and isinstance(module.router, Router):
                            routers.append(module.router)
                            print(f"✅ Router cargado: {module_name}")
                            
                    except Exception as e:
                        print(f"❌ Error al importar {module_name}: {e}")

    return routers