from typing import Union
from fastapi import FastAPI
from user import User

from automata.tm.dtm import DTM # Importando maquina de turing deterministica
from automata.tm.ntm import NTM # Importando maquina de turing nao deterministica
from automata.pda.dpda import DPDA # Importando automata de pilha deterministica
from automata.pda.npda import NPDA # Importando automata de pilha nao deterministica
from automata.fa.dfa import DFA # Importando automata finito deterministico


from automatasClasses import TuringMachine, PushdownAutomata, FiniteAutomataDeterministic


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
def validate_turing_machine(turing: TuringMachine): 
    dtm = DTM(
        states = turing.states,
        input_symbols = turing.input_symbols,
        tape_symbols = turing.tape_symbols,
        transitions = turing.transitions,
        initial_state = turing.initial_state,
        blank_symbol = turing.blank_symbol,
        final_states = turing.final_states,
        
    )
    
    return {
        "states": turing.states,
        "input_symbols": turing.input_symbols,
        "tape_symbols": turing.tape_symbols,
        "transitions": turing.transitions,
        "initial_state": turing.initial_state,
        "blank_symbol": turing.blank_symbol,
        "final_states": turing.final_states
    }

@app.post("/finite/")
def validate_finite_automata_deterministic(finite: FiniteAutomataDeterministic): 
    dfa = DFA(
        states = finite.states,
        input_symbols = finite.input_symbols,
        tape_symbols = finite.tape_symbols,
        transitions = finite.transitions,
        initial_state = finite.initial_state,
        blank_symbol = finite.blank_symbol,
        final_states = finite.final_states,
        
    )
    
    return {
        "states": finite.states,
        "input_symbols": finite.input_symbols,
        "tape_symbols": finite.tape_symbols,
        "transitions": finite.transitions,
        "initial_state": finite.initial_state,
        "blank_symbol": finite.blank_symbol,
        "final_states": finite.final_states
    }
    
@app.post("/pushdown/")
def validate_pushdown_automata(pushdown: PushdownAutomata): 
    dpda = DPDA(
        states = pushdown.states,
        input_symbols = pushdown.input_symbols,
        stack_symbols = pushdown.stack_symbols,
        transitions = pushdown.transitions,
        initial_state = pushdown.initial_state,
        initial_state_symbol = pushdown.initial_stack_symbol,
        final_states = pushdown.final_states,
        acceptance_mode = pushdown.acceptance_mode,
        
    )
    
    return {
        "states": pushdown.states,
        "input_symbols": pushdown.input_symbols,
        "stack_symbols": pushdown.stack_symbols,
        "transitions": pushdown.transitions,
        "initial_state": pushdown.initial_state,
        "final_states": pushdown.final_states,
        "allow_partial": pushdown.allow_partial,
    }
