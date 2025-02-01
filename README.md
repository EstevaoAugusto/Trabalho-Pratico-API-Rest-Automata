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