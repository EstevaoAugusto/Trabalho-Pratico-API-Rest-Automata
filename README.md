# Trabalho-Pratico-API-Rest-Automata
Trabalho prático da disciplina de Teoria da Computação, focado na construção de uma API REST para manipulação de autômatos utilizando a biblioteca Automata e o framework FastAPI

O projeto deve ser entregue até 11/02/2025. 

## Bibliotecas Usadas

- [Automata](https://github.com/caleb531/automata) - Biblioteca para manipulação de autômatos
- [FastAPI](https://fastapi.tiangolo.com/) - Framework para criação de APIs rápidas e eficientes

## Instalação

#### Clonagem do Repositório
```
git clone git@github.com:EstevaoAugusto/Trabalho-Pratico-API-Rest-Automata.git
cd Trabalho-Pratico-API-Rest-Automata
```

#### Criando e ativando o ambiente virtual

```
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# No Windows:
# .venv\Scripts\activate
```

#### Instalando dependencias

```
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

#### Executando a API

Para iniciar o servidor FastAPI, execute:
```
fastapi dev main.py
```

A API estará disponível em: http://127.0.0.1:8000/docs

Para criar e utilizar os automatos, é preciso inseri-los no formato JSON. Abaixo estão alguns exemplos.

## Exemplos em JSON


### Automato Finito Deterministico (AFD)
AFD que aceita (ou rejeita) strings binárias terminadas em um número ímpar de '1's

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
APD que aceita (ou rejeita) strings com zero ou mais 'a's, seguido pelo mesmo número de 'b's (aceitando pelo estado final).

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
MTD que aceita (ou rejeita) strings que começam com '0' e seguidas pelo mesmo número de '1'

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
