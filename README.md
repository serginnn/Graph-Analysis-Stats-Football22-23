# 💻 Implementação em Python

<div align="center">
   <img align="center" height="20px" width="80px" alt="Ubuntu" src="https://img.shields.io/badge/Ubuntu-E95420?logo=ubuntu&logoColor=white"/>
   <img align="center" height="20px" width="80px" src="https://img.shields.io/badge/VS%20Code-blue?logo=visual%20studio%20code"/>
   <img align="center" height="20px" width="60px" src="https://img.shields.io/badge/Python-3670A0?logo=python&logoColor=ffdd54"/>
</div>

## 🗂 Arquivos

- `src/plot_graphs.py`: Implementação do algoritmo Merge Sort em Python.
- `src/main.py`: Programa principal que executa o algoritmo Merge Sort.

## 📚 Como Usar
Aqui está uma breve orientação de como funciona o processo de execução e compilação:

```bash
git clone https://github.com/dudatsouza/Merge-Sort.git
```

Existe duas maneiras para executar este programa:
1. Através do terminal, onde é executado o programa, e exibido o resultado no terminal.
2. Através do script executável `../manager/main.py`, neste é executado o programa e gerado o gráfico de desempenho.

### 1. Através do terminal
Para executar o programa através do terminal, siga os passos abaixo:

1. Abra seu terminal e navegue até o diretório `src/python/src`:
    ```bash
    cd src/python/src
    ```

2. Execute o comando `python3` para executar o programa:
    ```bash
    python3 main.py
    ```

3. O programa será executado e o resultado será exibido no terminal.
<p align="right"><a href="#-implementação-em-python">⬆️ Voltar para ao Início</a></p>

### 2. Através do script executável
Para compilar e executar o programa através do script executável, siga os passos abaixo:

1. Abra seu terminal e navegue até o diretório `src/manager`:
    ```bash
    cd src/manager
    ```
2. Execute o script em python:
    ```bash
    python3 main.py
    ```

3. O programa será executado e o gráfico de desempenho será gerado.

> [!CAUTION]
> Caso não tenha o python instalado, instale-o através do comando:
> ```bash
> sudo apt install python3
> ```

<p align="right"><a href="#-implementação-em-python">⬆️ Voltar para ao Início</a></p>

## 📊 Implementação
Foi implementado o algoritmo Merge Sort de acordo com o pseudocódigo que está no [README.md](../../README.md) principal. Foram feitas algumas modificações para que o algoritmo pudesse ser executado em Python. Veja abaixo algumas informações sobre a implementação:

- **Bibliotecas**: Foram utilizadas a biblioteca `time` para calcular o tempo de execução do algoritmo.

- **Funções**: 
    - `merge`: Função que faz a junção dos vetores ordenados.
    - `mergeSort`: Função que faz a divisão do vetor em subvetores.
    - `definirArray`: Função que define o vetor a ser ordenado.
    - `salvarTempo`: Função que salva o tempo de execução do algoritmo em um arquivo `.csv`.
    - `run`: Função que executa o algoritmo.

- **Entrada**: O programa exige que entre com 3 valores: o tamanho do vetor, o nome do arquivo de entrada e o nome do arquivo de saída. O arquivo de entrada deve estar no formato `.txt` e deve conter os valores do vetor separados por espaço, o arquivo de saída será um arquivo `.csv` que conterá o tempo de execução do algoritmo e o tamanho do vetor, que será até qual posição o vetor será ordenado.

- **Saída**: O programa apenas guarda o tempo de execução do algoritmo em um arquivo `.csv` em `../../datasets/outputs/output.csv`. Além de exibir o tempo de execução no terminal. Depois é gerado alguns gráficos de desempenho.

## 📈 Resultados
Os resultados do desempenho do algoritmo da linguagem Python, foram discutidos no artigo do projeto. Para mais informações, acesse o nosso [artigo](../../artigo/Artigo.pdf) ou o [README.md](../../README.md) principal.
<p align="right"><a href="#-implementação-em-python">⬆️ Voltar para ao Início</a></p>


## ⛏ Python

O Python é uma linguagem de programação de alto nível, interpretada, de script, imperativa, orientada a objetos, funcional, de tipagem dinâmica e forte. É uma linguagem de programação multiparadigma, pois aceita o paradigma orientado a objetos, imperativo e funcional. Por ser uma linguagem interpretada, não é necessário compilar o código para executá-lo. Para executar o programa, basta ter o Python instalado em sua máquina.
<p align="right"><a href="#-implementação-em-python">⬆️ Voltar para ao Início</a></p>

## 🔧 Ambiente de Compilação
A seguir estão os detalhes do ambiente de compilação onde o programa foi executado:

| Componente      | Detalhes                          |
|-----------------|-----------------------------------|
| Sistema Operacional | Ubuntu 24.04 LTS |
| Modelo do hardware| Dell Inspiron 13 5330|
| Processador     | Intel Core i7-1360P Processor (18MB Cache, up to 5.00 GHz)|
| Memória RAM     | 16GB 4800MHz LPDDR5 Memory Onboard|
| Armazenamento   | 512GB M.2 PCIe NVMe Solid State Drive|
| Placa de vídeo  | Intel(R) Iris(R) Xe Graphics |
| IDE             | Visual Studio Code 1.63.2|

> [!IMPORTANT]
> Os detalhes acima são baseados no ambiente de compilação utilizado durante o desenvolvimento do programa e podem variar em diferentes sistemas.
<p align="right"><a href="#-implementação-em-python">⬆️ Voltar para ao Início</a></p>

## 📧 Contato dos Colaboradores
Para mais informações ou sugestões, sinta-se à vontade para entrar em contato:

| Participante           |  Contato  |                     
| -----------------------| ----------|
|  Maíra Lacerda | [![Gmail][Gmail Badge]][Gmail Colab 1] [![Linkedin][Linkedin Badge]][Linkedin Colab 1] [![Instagram][Instagram Badge]][Instagram Colab 1] [![GitHub][GitHub Badge]][GitHub Colab 1]|
|  Maria Eduarda Teixeira | [![Gmail][Gmail Badge]][Gmail Colab 2] [![Linkedin][Linkedin Badge]][Linkedin Colab 2] [![Instagram][Instagram Badge]][Instagram Colab 2] [![GitHub][GitHub Badge]][GitHub Colab 2]|
|  Sergio Ramos | [![Gmail][Gmail Badge]][Gmail Colab 3] [![Linkedin][Linkedin Badge]][Linkedin Colab 3] [![Instagram][Instagram Badge]][Instagram Colab 3] [![GitHub][GitHub Badge]][GitHub Colab 3]          |  

Ficaremos felizes em receber feedbacks, contribuições ou responder a quaisquer dúvidas que você possa ter sobre o programa.
<p align="right"><a href="#-implementação-em-python">⬆️ Voltar para ao Início</a></p>


