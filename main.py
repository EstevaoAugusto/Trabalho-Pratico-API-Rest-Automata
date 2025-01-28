from typing import Union

from fastapi import FastAPI
from user import User
from mt import TuringMachine

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.get("/soma/{x}/{y}")
def soma(x: int, y: int):
    return {"soma": str(x + y)}

@app.post("/users/")
def create_user(user: User):
    return { "user_name": user.email, "user_email": user.email}

@app.post("/turing/")
def validate_turing_machine(turing: TuringMachine): # O codigo funciona, mas é preciso instalar a biblioteca do automato para poder manipula-lo diretamente no codigo
    return {"turing": turing.states}