from typing import NoReturn
import netron

def show_model_in_netron(model_path: str, port: int) -> NoReturn:
    netron.start(model_path, port=port)
