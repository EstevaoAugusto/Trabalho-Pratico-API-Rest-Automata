# Turing Machine Model

from pydantic import BaseModel
from typing import Set, Tuple, Dict, List

class FiniteAutomataDeterministic(BaseModel):
    states: Set[str]
    input_symbols: Set[str]
    transitions: Dict[str, Dict[str, str]]
    initial_state: str
    final_states: Set[str]


class TuringMachine(BaseModel):
    states: Set[str]
    input_symbols: Set[str]
    tape_symbols: Set[str]
    transitions: Dict[str, Dict[str, Tuple[str, str, str]]]
    initial_state: str
    blank_symbol: str
    final_states: Set[str]
    
class PushdownAutomata(BaseModel):
    states: Set[str]
    input_symbols: Set[str]
    stack_symbols: Set[str]
    transitions: Dict[str, Dict[str, Tuple[str, str, str]]]
    initial_state: str
    initial_stack_symbol: str
    final_states: Set[str]
    acceptance_mode: str
    