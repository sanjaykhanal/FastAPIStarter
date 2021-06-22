import os
import sys
import json
import importlib
import threading

from logger.logger import set_size_based_rotating_log
set_size_based_rotating_log()
import logging

from fastapi import FastAPI

from database.db import Base, engine
from config.config import DEFAULT_USER_SCOPES
from flags import get_flags


flags = get_flags()


sys.path.append('.')
Base.metadata.create_all(bind=engine)


app = FastAPI()

if flags.allow_cors:
    from middlewares.cors.cors import attach_cors_middleware
    attach_cors_middleware(app)


@app.on_event("startup")
def start_threaded_test_consoles():
    if flags.enable_test_console:
        from modules.console_example import start_example_console
        # add other imports of consoles here
        all_consoles = [start_example_console]
        threads = [threading.Thread(target=console, args=()) for console in all_consoles]
        for t in threads:
            t.start()


def __load_modules():
    """load all available api modules"""
    required_modules = os.listdir('modules')
    try:
        required_modules = [d for d in required_modules if not d.startswith(('.', '_'))]
    except Exception as e:
        logging.error(e)

    required_modules = [mod for mod in required_modules if os.path.isdir(os.path.join('modules', mod))]

    print(required_modules)

    imported_modules = {}

    for mod in required_modules:
        imported_modules[mod] = importlib.import_module('modules.'+mod)

    return imported_modules


def __load_routes(modules):
    """load routes details from each module"""

    all_routes = {}
    for module_name, module in modules.items():
        logging.info("loading routes from module: {}".format(module_name))
        for routes in module.routes:
            for route in routes.value:
                for route_ in route:
                    all_routes.update({route_.name: route_.value})
        logging.info("loaded routes from module: {}".format(module_name))
        with open(os.path.join("middlewares", "authentication", "routes.json"), "w+") as f:
            json.dump(all_routes, f)


def __load_scopes():
    """load scope details from each api module"""

    all_scopes = DEFAULT_USER_SCOPES
    for module_name, module in modules.items():

        logging.info("loading scopes from module: {}".format(module_name))
        for scopes in module.scopes:
            if scopes.name in all_scopes:
                all_scopes[scopes.name].extend(scopes.value)
            else:
                all_scopes[scopes.name] = scopes.value
        logging.info("loaded scopes from module: {}".format(module_name))
        with open(os.path.join("middlewares", "authentication", "scopes.json"), "w+") as f:
            json.dump(all_scopes, f)


def __register_routes():
    """register all the routes inside every modules"""
    for module_name, module in modules.items():

        logging.info("loading routers from module: {}".format(module_name))
        for routers in module.routers:
            for router in routers.value:
                logging.info("Loading router: {}.{}".format(module_name, routers.name))
                app.include_router(
                    router,
                    tags = [module_name+'.'+routers.name]
                )
        logging.info("loaded routes from module: {}".format(module_name))



if __name__=='__main__':
    import uvicorn

    modules = __load_modules()
    __load_routes(modules)
    __load_scopes()
    __register_routes()


    uvicorn.run(app, host="0.0.0.0", port=8000, loop='asyncio')
