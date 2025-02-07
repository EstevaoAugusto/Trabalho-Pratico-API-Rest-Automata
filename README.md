# Trabalho-Pratico-API-Rest-Automata
Trabalho Prático de Teoria da Computação: Construção de uma API REST Utilizando a Biblioteca Automata
Projeto construido em Python.

O projeto deve ser entregue até 11/02/2025. 

## Bibliotecas Usadas

- [Automate](https://github.com/caleb531/automata)
- [FastAPI](https://fastapi.tiangolo.com/)

## Instalação

```
git clone git@github.com:EstevaoAugusto/Trabalho-Pratico-API-Rest-Automata.git
cd Trabalho-Pratico-API-Rest-Automata
python -m venv .venv
pip install "fastapi[standard]"
pip install 'automata-lib[visual]'
```

Caso esteja usando o Windows, e tenha problemas em instalar a biblioteca do automata graçás a sua dependencia Pygraphviz, é preciso baixar:

- [Graphviz](https://graphviz.org/download/)
- [Ferramentas de compilação do Microsoft C++](https://visualstudio.microsoft.com/pt-br/visual-cpp-build-tools/)

Em seguida, basta digitar o comando abaixo:

```
python -m pip install --config-settings="--global-option=build_ext" --config-settings="--global-option=-IC:\Program Files\Graphviz\include" --config-settings="--global-option=-LC:\Program Files\Graphviz\lib" pygraphviz
```

Detalhes foram obtidas na [documentaçao do Pygraphviz](https://pygraphviz.github.io/documentation/stable/install.html#windows).

## Exemplos em JSON


### Automato Finito Deterministico (AFD)

```json
{
  "states": ["q0", "q1", "q2"],
  "input_symbols": ["0", "1"],
  "transitions": {
    "q0": {
      "0": "q0",
      "1": "q1"
    },
    "q1": {
      "0": "q0",
      "1": "q2"
    },
    "q2": {
      "0": "q2",
      "1": "q1"
    }
  },
  "initial_state": "q0",
  "final_states": ["q1"]
}
```

### Automato com Pilha Deterministica (APD)

```json
{
  "states": ["q0", "q1", "q2", "q3"],
  "input_symbols": ["a", "b"],
  "stack_symbols": ["0", "1"],
  "transitions": {
    "q0": {
      "a": {
        "0": ["q1", ["1", "0"]]
      }
    },
    "q1": {
      "a": {
        "1": ["q1", ["1", "1"]]
      },
      "b": {
        "1": ["q2", ""]
      }
    },
    "q2": {
      "b": {
        "1": ["q2", ""]
      },
      "": {
        "0": ["q3", ["0"]]
      }
    }
  },
  "initial_state": "q0",
  "initial_stack_symbol": "0",
  "final_states": ["q3"],
  "acceptance_mode": "final_state"
}
```

### Maquina de Turing Deterministica (MTD)

```json
{
  "states": ["q0", "q1", "q2", "q3", "q4"],
  "input_symbols": ["0", "1"],
  "tape_symbols": ["0", "1", "x", "y", "."],
  "transitions": {
    "q0": {
      "0": ["q1", "x", "R"],
      "y": ["q3", "y", "R"]
    },
    "q1": {
      "0": ["q1", "0", "R"],
      "1": ["q2", "y", "L"],
      "y": ["q1", "y", "R"]
    },
    "q2": {
      "0": ["q2", "0", "L"],
      "x": ["q0", "x", "R"],
      "y": ["q2", "y", "L"]
    },
    "q3": {
      "y": ["q3", "y", "R"],
      ".": ["q4", ".", "R"]
    }
  },
  "initial_state": "q0",
  "blank_symbol": ".",
  "final_states": ["q4"]
}
```