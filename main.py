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

automataDFA: Dict[str, DFA] = {}
automataDTM: Dict[str, DTM] = {}
automataDPDA: Dict[str, DPDA] = {}

def get_automataDPDA():
    return automataDPDA

def get_automataDTM():
    return automataDTM

def get_automataDFA():
    return automataDFA

@app.post("/create_dtm/")
def create_deterministic_turing_machine(turing : TuringMachine, automata : Dict[str, DTM] = Depends(get_automataDTM), chave : str = "dtm1"): 
    dtm = DTM(
        states = turing.states,
        input_symbols = turing.input_symbols,
        tape_symbols = turing.tape_symbols,
        transitions = turing.transitions,
        initial_state = turing.initial_state,
        blank_symbol = turing.blank_symbol,
        final_states = turing.final_states,
        
    )
    
    automata[chave] = dtm
    
    return {  "mensagem" : "DTM criada com sucesso." }

@app.get("/get_dtm/{chave}")
def get_deterministic_turing_machine(chave : str):
    dtm = automataDTM.get(chave)
    
    if dtm is None:
        return { "error" : f"Nenhum DTM foi encontrado com a chave '{chave}'" }
    
    
    return {
        "chave" : chave,
        "states" : dtm.states,
        "input_symbols" : dtm.input_symbols,
        "tape_symbols" : dtm.tape_symbols,
        "transitions" : dtm.transitions,
        "initial_state" : dtm.initial_state,
        "blank_symbol" : dtm.blank_symbol,
        "final_states" : dtm.final_states,
    }

@app.get("/get_all_dtm/")
def get_all_deterministic_turing_machine():
    return {key: {
        "states": value.states,
        "input_symbols": value.input_symbols,
        "tape_symbols" : value.tape_symbols,
        "transitions": value.transitions,
        "initial_state": value.initial_state,
        "blank_symbol" : value.blank_symbol,
        "final_states": value.final_states,
    } for key, value in automataDTM.items()}


@app.get("/test_dtm/{chave}/{input_string}")
def test_deterministic_turing_machine(input_string: str, chave: str, automata: Dict[str, DTM] = Depends(get_automataDTM)):
    dtm = automata.get(chave)
    
    if dtm is None:
        return {"error": "Nenhum DTM encontrado"}
    
    try:
        result = dtm.accepts_input(input_string)
    except Exception as e:
        return {"error": f"Erro ao processar DFA: {str(e)}"}
    
    return {
                "chave": chave,
                "input_string" : input_string,
                "accepted" : result,
                "states" : dtm.states,
                "input_symbols" : dtm.input_symbols,
                "tape_symbols" : dtm.tape_symbols,
                "transitions" : dtm.transitions,
                "initial_state" : dtm.initial_state,
                "blank_symbol" : dtm.blank_symbol,
                "final_states" : dtm.final_states,
            }

@app.post("/create_dfa/")
def create_deterministic_finite_automata(finite: FiniteAutomataDeterministic, automata: Dict[str, DFA] = Depends(get_automataDFA), chave : str = "dfa" + str(len(automataDFA)+1)): 
    dfa = DFA(
        states = finite.states,
        input_symbols = finite.input_symbols,
        transitions = finite.transitions,
        initial_state = finite.initial_state,
        final_states = finite.final_states,
    )
    
    automata[chave] = dfa
        
    return { "mensagem": "DFA criado com sucesso"}

@app.get("/test_dfa/{chave}/{input_string}")
def test_dfa(input_string: str, chave: str, automata: Dict[str, DFA] = Depends(get_automataDFA)):
    dfa = automata.get(chave)
    
    if dfa is None:
        return {"error": "Nenhum DFA encontrado"}
    
    try:
        result = dfa.accepts_input(input_string)
    except Exception as e:
        return {"error": f"Erro ao processar DFA: {str(e)}"}
    
    return {
                "chave": chave,
                "input_string" : input_string,
                "accepted" : result,
                "states" : dfa.states,
                "input_symbols" : dfa.input_symbols,
                "transitions" : dfa.transitions,
                "initial_state" : dfa.initial_state,
                "final_states" : dfa.final_states,
            }

@app.get("/get_dfa/{chave}")
def get_dfa(chave: str):    
    dfa = automataDFA.get(chave)

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

@app.get("/get_all_dfa/")
def get_all_dfa():
    return {key: {
        "states": value.states,
        "input_symbols": value.input_symbols,
        "transitions": value.transitions,
        "initial_state": value.initial_state,
        "final_states": value.final_states
    } for key, value in automataDFA.items()}

@app.post("/create_pushdown/")
def create_pushdown_automata(pushdown: PushdownAutomata, automata: Dict[str, DPDA] = Depends(get_automataDPDA), chave: str = "DPDA1"): 
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
    
    automata[chave] = dpda
    
    return { "mensagem" : "DPDA criado com sucesso"}

@app.get("/get_pushdown/{chave}")
def get_pushdown_automata(chave : str):
    dpda = automataDPDA.get(chave)
    
    if dpda is None:
        return { "error" : "Automato com Pilha Deterministica não encontrado" }
    
    return {
        "chave" : chave,
        "states" : dpda.states,
        "input_symbols" : dpda.input_symbols,
        "stack_symbols" : dpda.stack_symbols,
        "transitions" : dpda.transitions,
        "initial_state" : dpda.initial_state,
        "initial_state_symbol" : dpda.initial_stack_symbol,
        "final_states" : dpda.final_states,
        "acceptance_mode" : dpda.acceptance_mode,
    }
    
@app.get("/get_all_pushdown")
def get_all_pushdown_automata():
    return{key : {
        "states" : value.states,
        "input_symbols" : value.input_symbols,
        "stack_symbols" : value.stack_symbols,
        "transitions" : value.transitions,
        "initial_state" : value.initial_state,
        "initial_state_symbol" : value.initial_stack_symbol,
        "final_states" : value.final_states,
        "acceptance_mode" : value.acceptance_mode,
    } for key, value in automataDPDA.items()}
    
@app.post("/test_pushdown/{chave}/{input_string}")
def test_dfa(input_string: str, chave: str, automata: Dict[str, DPDA] = Depends(get_automataDPDA)):
    dpda = automata.get(chave)
    
    if dpda is None:
        return {"error": "Nenhum DPDA encontrado"}
    
    try:
        result = dpda.accepts_input(input_string)
    except Exception as e:
        return {"error": f"Erro ao processar DPDA: {str(e)}"}
    
    return {
                "chave": chave,
                "input_string" : input_string,
                "accepted" : result,
                "states" : dpda.states,
                "input_symbols" : dpda.input_symbols,
                "stack_symbols" : dpda.stack_symbols,
                "transitions" : dpda.transitions,
                "initial_state" : dpda.initial_state,
                "initial_stack_symbol" : dpda.initial_stack_symbol,
                "final_states" : dpda.final_states,
                "acceptance_mode" : dpda.acceptance_mode,
            }