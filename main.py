from typing import Dict
from fastapi import Depends, FastAPI
import json
from automata.tm.dtm import DTM # Importando maquina de turing deterministica
from automata.tm.ntm import NTM # Importando maquina de turing nao deterministica
from automata.pda.dpda import DPDA # Importando automata de pilha deterministica
from automata.pda.npda import NPDA # Importando automata de pilha nao deterministica
from automata.fa.dfa import DFA # Importando automata finito deterministico


from automatasClasses import TuringMachine, PushdownAutomata, FiniteAutomataDeterministic


app = FastAPI()

automata: Dict[str, DFA] = {}


def get_automata():
    return automata

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/turing/")
def validate_turing_machine(turing: TuringMachine, input_string: str): 
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
        "accepted": str(dtm.accepts_input(input_string)),
        "states": turing.states,
        "input_symbols": turing.input_symbols,
        "tape_symbols": turing.tape_symbols,
        "transitions": turing.transitions,
        "initial_state": turing.initial_state,
        "blank_symbol": turing.blank_symbol,
        "final_states": turing.final_states
    }

@app.post("/create_dfa/")
def create_dfa(finite: FiniteAutomataDeterministic, automata: Dict[str, DFA] = Depends(get_automata), chave : str = "dfa" + str(len(automata)+1)): 
    dfa = DFA(
        states = finite.states,
        input_symbols = finite.input_symbols,
        transitions = finite.transitions,
        initial_state = finite.initial_state,
        final_states = finite.final_states,
    )
    
    automata[chave] = dfa
        
    return { "mensagem": "DFA criado com sucesso"}

@app.get("/test_dfa/")
def test_dfa(input_string: str, chave: str, automata: Dict[str, DFA] = Depends(get_automata)):
    dfa = automata.get(chave)
    
    if not dfa:
        return {"error": "Nenhum DFA encontrado"}
    
    result = dfa.accepts_input(input_string)
    
    return {
                "chave": chave,
                "string": input_string, 
                "accepted": result,
                "states" : dfa.states,
                "input_symbols" : dfa.input_symbols,
                "transitions" : dfa.transitions,
                "initial_state" : dfa.initial_state,
                "final_states" : dfa.final_states,
            }

@app.get("/get_dfa/{chave}")
def get_dfa(chave: str):    
    dfa = automata.get(chave)

    if dfa is None:
        return { "error": f"Nenhum DFA foi encontrado com a chave '{chave}'"}
    
    return { 
                "chave": chave,
                "states" : dfa.states,
                "input_symbols" : dfa.input_symbols,
                "transitions" : dfa.transitions,
                "initial_state" : dfa.initial_state,
                "final_states" : dfa.final_states,
            }

@app.post("/pushdown/")
def validate_pushdown_automata(pushdown: PushdownAutomata): 
    dpda = DPDA(
        states = pushdown.states,
        input_symbols = pushdown.input_symbols,
        stack_symbols = pushdown.stack_symbols,
        transitions = pushdown.transitions,
        initial_state = pushdown.initial_state,
        initial_stack_symbol = pushdown.initial_stack_symbol,
        final_states = pushdown.final_states,
        acceptance_mode = pushdown.acceptance_mode,
        
    )
    
    return {
        "states": pushdown.states,
        "input_symbols": pushdown.input_symbols,
        "stack_symbols": pushdown.stack_symbols,
        "transitions": pushdown.transitions,
        "initial_stack_symbol": pushdown.initial_stack_symbol,
        "initial_state": pushdown.initial_state,
        "final_states": pushdown.final_states,
        "allow_partial": pushdown.allow_partial,
    }
