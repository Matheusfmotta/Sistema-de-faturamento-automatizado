import random 
from datetime import datetime 
from fastapi import FastAPI

def gerar_id_faturamento():
    return random.randint(1000, 3000)

def data_hora_atual():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")
