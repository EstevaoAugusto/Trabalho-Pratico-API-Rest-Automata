from typing import Dict
from fastapi import Depends, FastAPI
import os
import pygraphviz as pgv
from automata.tm.dtm import DTM # Importando maquina de turing deterministica
from automata.pda.dpda import DPDA # Importando automata de pilha deterministica
from automata.fa.dfa import DFA # Importando automata finito deterministico


from automatasClasses import TuringMachine, PushdownAutomata, FiniteAutomataDeterministic


app = FastAPI()

imagePath = "./images/"

# as variaveis abaixo sao dicionarios para cada um dos automatos do trabalho
automataDFA: Dict[str, DFA] = {} # automato finito deterministico
automataDTM: Dict[str, DTM] = {} # maquina de turing deterministica
automataDPDA: Dict[str, DPDA] = {} # maquina de pilha deterministica

def get_automataDPDA():
    return automataDPDA

def get_automataDTM():
    return automataDTM

def get_automataDFA():
    return automataDFA

# Rota inicial
# Serve para indicar que o projeto esta rodando
@app.get("/")
def root():
    return { "Hello" : "World" }

#Rota de criação de maquinas de turing deterministicas
@app.post("/create_dtm/")
def create_deterministic_turing_machine(turing : TuringMachine, automata : Dict[str, DTM] = Depends(get_automataDTM), chave : str = "dtm1"): 
    # turing é uma variavel que recebe um json do usuário
    dtm = DTM( # uma maquina de turing é instanciada a partir dos dados do json
        states = turing.states,
        input_symbols = turing.input_symbols,
        tape_symbols = turing.tape_symbols,
        transitions = turing.transitions,
        initial_state = turing.initial_state,
        blank_symbol = turing.blank_symbol,
        final_states = turing.final_states,
        
    )
    
    automata[chave] = dtm # dtm é inserido no dicionario
        
    return {  "mensagem" : "DTM criada com sucesso." }

# Rota para obter uma maquina de turing deterministica (DTM) especifica a partir de uma chave
@app.get("/get_dtm/{chave}")
def get_deterministic_turing_machine(chave : str):
    dtm = automataDTM.get(chave) # obtem DTM a partir da chave
    
    if dtm is None: #
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

# Rota para obter todos os automotos finitos deterministicos(DTM) do dicionario
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

# Rota de testar um string a partir da DTM escolhida por chave
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

# Rota que cria diagrama de maquina de turing deterministica
@app.post("/create_diagram_dtm/")
def create_diagram_of_deterministic_turing_machine(nomeDiagram : str = "maquinaTuring.png", automata: Dict[str, DTM] = Depends(get_automataDTM), chave : str = "dtm1"):
    if not os.path.exists(imagePath): # caso a pasta images nao existir
        os.makedirs(imagePath) # a pasta images é criada
    
    if not nomeDiagram.endswith(".png"): # caso o nome do diagrama nao termine com .png, a rota cessa funcionamento
        return { "error" : "O nome do diagrama nao termina com .png "}
    
    dtm = automata.get(chave)
        
    if dtm is None:
        return { "error" : f"Não existe DTM com a chave '{chave}'"}
    
    # Criar o grafo com PyGraphviz
    graph = pgv.AGraph(strict=False, directed=True)
    
    # Adicionar os estados ao grafo
    for state in dtm.states:
        if state in dtm.final_states:
            graph.add_node(state, shape='doublecircle')  # Estado de aceitação
        elif state == dtm.initial_state:
            graph.add_node(state, shape='circle', style="filled", fillcolor="lightblue")  # Estado de rejeição
        else:
            graph.add_node(state, shape='circle')
    
    # Adicionar transições ao grafo
    for (start_state, transition) in dtm.transitions.items():
        for (read_symbol, symbols_list) in transition.items():
                graph.add_edge(start_state, symbols_list[0], label=f'{read_symbol} -> {symbols_list[1]}, {symbols_list[2]}')
    
    # Gerar o diagrama e salvar em um arquivo PNG
    graph.layout(prog='dot')  # Usa o layout 'dot' do Graphviz para gerar o gráfico
    
    caminho_completo = os.path.join(imagePath, nomeDiagram)
    graph.draw(caminho_completo)
    
    return { 
                "mensagem" : f"O DTM foi gerado com sucesso. Veja em '{caminho_completo}'",
            }

# Rota que cria o automato finito deterministico
@app.post("/create_dfa/")
def create_deterministic_finite_automata(finite: FiniteAutomataDeterministic, automata: Dict[str, DFA] = Depends(get_automataDFA), chave : str = "dfa1"): 
    dfa = DFA(
        states = finite.states,
        input_symbols = finite.input_symbols,
        transitions = finite.transitions,
        initial_state = finite.initial_state,
        final_states = finite.final_states,
    )
    
    automata[chave] = dfa
        
    return { "mensagem": "DFA criado com sucesso"}

# Rota que testa o automato finito deterministico a partir de uma string
@app.get("/test_dfa/{chave}/{input_string}")
def test_deterministic_finite_automata(input_string: str, chave: str, automata: Dict[str, DFA] = Depends(get_automataDFA)):
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

# Rota que visualiza um automato finito deterministico especifico
@app.get("/get_dfa/{chave}")
def get_deterministic_finite_automata(chave: str):    
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

# Rota que visualiza todos os automatos finitos deterministicos
@app.get("/get_all_dfa/")
def get_all_deterministic_finite_automata():
    return {key: {
        "states": value.states,
        "input_symbols": value.input_symbols,
        "transitions": value.transitions,
        "initial_state": value.initial_state,
        "final_states": value.final_states
    } for key, value in automataDFA.items()}

# Rota que cria o diagrama do automato finito deterministico
@app.post("/create_diagram_dfa/")
def create_diagram_of_deterministic_finite_automata(nomeDiagram : str = "automatoFinitoDeterministico.png", automata: Dict[str, DFA] = Depends(get_automataDFA), chave : str = "dfa1"):
    if not os.path.exists(imagePath): # caso a pasta images nao existir
        os.makedirs(imagePath)
    
    if not nomeDiagram.endswith(".png"):
        return { "error" : "O nome do diagrama nao termina com .png "}
    
    dfa = automata.get(chave)
    
    if dfa is None: # caso o dfa nao exista no automataDFA
        return { "error" : f"Não existe DTM com a chave '{chave}'"}
    
    caminho_completo = os.path.join(imagePath, nomeDiagram)
    dfa.show_diagram(path=caminho_completo)
    
    return { 
                "mensagem" : f"O DFA foi gerado com sucesso. Veja em '{caminho_completo}'",
            }

# Rota que cria uma maquina com pilha deterministica
@app.post("/create_pushdown/")
def create_pushdown_automata(pushdown: PushdownAutomata, automata: Dict[str, DPDA] = Depends(get_automataDPDA), chave: str = "dpda1"): 
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

# Rota que visualiza maquina com pilha deterministica especifica
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

# Rota que visualiza todas as maquinas com pilha deterministicas disponiveis
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

# Rota que testa maquina com pilha deterministica com uma string
@app.get("/test_pushdown/{chave}/{input_string}")
def test_pushdown_automata(input_string: str, chave: str, automata: Dict[str, DPDA] = Depends(get_automataDPDA)):
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

# Rota que cria diagrama para a maquina com pilha deterministica
@app.post("/create_diagram_pushdown/")
def create_diagram_of_pushdown_automata(nomeDiagram : str = "automatoComPilha.png", automata: Dict[str, DPDA] = Depends(get_automataDPDA), chave : str = "dpda1"):
    if not os.path.exists(imagePath): # caso a pasta images nao existir
        os.makedirs(imagePath)
    
    if not nomeDiagram.endswith(".png"):
        return { "error" : "O nome do diagrama nao termina com .png "}
    
    dpda = automata.get(chave)
    
    if dpda is None: # caso o dfa nao exista no automataDFA
        return { "error" : f"Não existe DPDA com a chave '{chave}'"}
    
    caminho_completo = os.path.join(imagePath, nomeDiagram)
    dpda.show_diagram(path=caminho_completo)
    
    return { 
                "mensagem" : f"O diagrama DPDA foi gerado com sucesso. Veja em '{caminho_completo}'",
            }