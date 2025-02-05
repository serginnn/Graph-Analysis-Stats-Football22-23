import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from sklearn.metrics.pairwise import cosine_similarity
import heapq
from joblib import Parallel, delayed
from sklearn.preprocessing import MinMaxScaler
from plot_graph import plotar_grafo_completo, plotar_subgrafos

# Carregar o dataset
filepath = "./dataset/2022-2023FootballPlayerStats.csv"
dataset = pd.read_csv(filepath, sep=';', encoding='iso-8859-1')

# Excluir jogadores da posição DFFW (lateral que joga de ponta)
dataset = dataset[dataset['Pos'] != 'DFFW']

# Remover jogadores com menos de 400 minutos(para melhor análise dos jogadores)
dataset = dataset[dataset["Min"] >= 400]  

# Seleção de atributos relevantes
dataset = dataset[[
    "Player", "Pos", "Comp", "Min", "Goals", "G/Sh", "ShoPK", "PKatt", "PasTotCmp%",
    "Assists", "PasAss", "SCA", "GcaDrib", "TklDri%", "Int", "Err",
    "ToTkl%", "CarPrgDist", "Fls", "CrdR", "CrdY", "AerWon%", "Crs", "GcaFld", "Off", "Recov", 
]]

# Ponderação das ligas
ponderacao_liga = {
    "Premier League": 1.27,
    "La Liga": 1.13,
    "Bundesliga": 1.08,
    "Serie A": 1.01,
    "Ligue 1": 1.0,
}

# Preencher valores nulos com 0 (ou outro valor apropriado)
dataset.fillna(0, inplace=True)

# Função para calcular desempenho do jogador
def calcular_desempenho(row):
    liga = row['Comp']
    ponderacao = ponderacao_liga.get(liga, 1.0)  # Usar 1.0 se a liga não estiver no dicionário
    posicao = row['Pos']   

    # Cálculo do desempenho baseado na posição do jogador
    if posicao == 'GK':  # goleiro 
        desempenho = (row['AerWon%'] * 2 + row['PasTotCmp%'] * 1.2 + row['Recov'] * 3 - row['Err'] * 3 - 
                      row['CrdR'] * 2 - row['CrdY'] * 1.5 - 2.5 * row['GcaFld'])
    elif posicao == 'DF':  # zagueiro
        desempenho = (row['TklDri%'] * 5.5 +  row['Int'] * 3.5 +  row['ToTkl%'] * 3.2 +  row['AerWon%'] * 3 +  row['Recov'] * 1.8 +  
                      row['CarPrgDist'] * 2.2 -  row['Err'] * 2 -  row['CrdR'] * 3 -  row['CrdY'] * 1.5 -  row['Fls'] * 0.5 -  row['GcaFld'] * 1.8 +  row['PasTotCmp%'] * 1.2 )
    elif posicao == 'DFMF':  # lateral que joga de volante também 
        desempenho = (row['TklDri%'] * 3 + row['Int'] * 2 + row['AerWon%'] + row['Recov'] * 1.2 - 
                      row['Err'] * 1.5 - row['CrdR'] * 2 - row['CrdY'] * 1.1 + row['Crs'] * 1.8 - row['Fls'] * 0.3 - row['GcaFld'] * 1.1 + row['PasAss'] * 1.4 + row['PasTotCmp%'] * 1.2 + row['Assists'] * 1.5 + row['CarPrgDist'] * 1.2 + row['SCA'] * 1.3)
    elif posicao == 'MFDF':  # ponta que joga de meia atacante também 
        desempenho = (row['Goals'] * 3 + row['G/Sh'] + row['ShoPK'] * 1.5 + row['SCA'] * 1.5 + 
                      row['PasTotCmp%'] + row['Assists'] * 1.8 - row['CrdR'] * 2 - row['CrdY'] * 0.8 + 
                      row['GcaDrib'] * 1.5 + row['ShoPK'] * 1.5 + row['CarPrgDist'] * 1.2)
    elif posicao == 'MF':  # meio campo central
        desempenho = (row['PasTotCmp%'] * 2 + row['Assists'] * 3.7 + row['SCA'] * 1.8 + row['Recov'] * 1.1 + 
                      row['GcaDrib'] * 1.6 - row['Err'] * 1.2 - row['CrdY'] * 0.9 + row['Goals'] * 2.5 + 
                      row['CarPrgDist'] * 1.1  + row['PasAss'] * 1.4 - row['ToTkl%'] * 0.8 - row['Fls'] * 0.2 - row['CrdR'] * 2)
    elif posicao == 'FW':   # atacante centroavante 
        desempenho = (row['Goals'] * 5 + row['G/Sh'] * 1.5 + row['ShoPK'] * 1.5 + row['SCA'] * 1.5 + 
                      row['Assists'] * 1.3 - row['CrdR'] * 2 - row['CrdY'] * 0.9 + row['GcaDrib'] * 1.5 + 
                      row['ShoPK'] * 1.5)
    elif posicao == 'MFFW':  # meio campo que joga de atacante também
        desempenho = (row['Goals'] * 4.7 +  row['PasTotCmp%'] * 1.5 +  row['Assists'] * 3 +  row['SCA'] * 2 +  row['GcaDrib'] * 1.3 +  
                      row['CarPrgDist'] * 1.7 -  row['CrdY'] * 0.3 -  row['ToTkl%'] * 0.6 -  row['Fls'] * 0.2 -  row['CrdR'] * 2  + row['PasAss'] * 1.2)
    elif posicao == 'FWDF':  # meia atacante que joga de centravante também 
        desempenho = (row['Goals'] * 2 + row['G/Sh'] + row['ShoPK'] * 1.5 + row['SCA'] * 1.5 + 
                      row['PasTotCmp%'] + row['Assists'] * 1.3 - row['CrdR'] * 2 - row['CrdY'] * 1.2)
    elif posicao == 'FWMF':  # atacante veloz que joga de meia também
        desempenho = (row['Goals'] * 3.5  + row['SCA'] * 1.7 + 
                      row['PasTotCmp%'] * 1.1 + row['Assists'] * 2 - row['CrdR'] * 2 - row['CrdY'] * 0.7 + row['GcaDrib'] * 1.4 + row['CarPrgDist'] * 1.2 - row['ToTkl%'] * 0.8)
    else:
        desempenho = 0

    return (ponderacao) * (desempenho)

# Paralelizar o cálculo de desempenho utilizando joblib
dataset['Desempenho'] = Parallel(n_jobs=-1)(delayed(calcular_desempenho)(row) for _, row in dataset.iterrows())

# Normalização do desempenho
scaler = MinMaxScaler()
dataset["Desempenho"] = scaler.fit_transform(dataset[["Desempenho"]])

# Limpeza das colunas já utilizadas
dataset.drop(["Min", "Goals", "G/Sh", "ShoPK", "PKatt", "PasTotCmp%", "Assists", "PasAss", 
              "SCA", "GcaDrib", "TklDri%", "Int", "Err", "ToTkl%", "CarPrgDist", 
              "Fls", "CrdR", "CrdY", "AerWon%", "Crs", "GcaFld", "Off", "Recov"], axis=1, inplace=True)


# Criar o grafo separado por posição
grafo_posicoes = {}

# Dividir jogadores por posição e criar subgrafos para cada posição
for _, jogador in dataset.iterrows():
    posicao = jogador['Pos']
    if posicao not in grafo_posicoes:
        grafo_posicoes[posicao] = nx.Graph()
    
    # Adicionar o jogador ao grafo da sua posição
    grafo_posicoes[posicao].add_node(jogador['Player'], posicao=posicao, desempenho=jogador['Desempenho'])

# Limpeza de arestas
for grafo in grafo_posicoes.values():
    grafo.clear_edges()

# Selecionar as métricas de similaridade
metricas_similaridade = ["Desempenho"]

# Obter os vetores de desempenho
vetores = dataset[metricas_similaridade].values

# Calcular a matriz de similaridade de cosseno
similaridades = cosine_similarity(vetores)

# Definir limiar de similaridade
limiar_similaridade = 0.1
similaridades[similaridades < limiar_similaridade] = 0

# Arestas dentro de cada subgrafo (mesma posição)
for posicao, grafo in grafo_posicoes.items():
    jogadores = list(grafo.nodes)
    
    for i, pl1 in enumerate(jogadores):
        for j, pl2 in enumerate(jogadores):
            if i < j and similaridades[i, j] > 0.1:  # Usa similaridade como critério principal
                peso_aresta = similaridades[i, j]  # Usa diretamente a similaridade
                grafo.add_edge(pl1, pl2, peso=peso_aresta)

    grafo.remove_nodes_from(list(nx.isolates(grafo)))  # Remover nós isolados em cada subgrafo
    # Plotando os subgrafos por posição
    plotar_subgrafos({posicao: grafo}, nome_arquivo_prefix=f'graphs/subgrafo_{posicao}_antes_selecao_')


# Selecionar os nós mais relevantes de cada subgrafo com base no desempenho
n_nos_relevantes = 11  
nos_relevantes_posicoes = {}

# Calcular a seleção dos melhores jogadores com base no desempenho
for posicao, grafo in grafo_posicoes.items():
    # Ordenar os jogadores dentro do subgrafo com base no desempenho (maior desempenho primeiro)
    jogadores = list(grafo.nodes)
    jogadores_ordenados = sorted(
       jogadores, 
        key=lambda jogador: (
            grafo.nodes[jogador]['desempenho'],  # Desempenho
            -nx.degree(grafo, jogador)  # Menos conexões (grau) é preferido
        ), 
        reverse=True
    )
    # Selecionar os 'n_nos_relevantes' com maior desempenho
    nos_relevantes = jogadores_ordenados[:n_nos_relevantes]
    nos_relevantes_posicoes[posicao] = nos_relevantes


# Cria grafo final com os nós mais relevantes
grafo_final = nx.Graph()

# Adicionar nós relevantes ao grafo final
for posicao, jogadores in nos_relevantes_posicoes.items():
    for jogador in jogadores:
        if jogador in grafo_posicoes[posicao].nodes:
            atributos = grafo_posicoes[posicao].nodes[jogador]
            grafo_final.add_node(jogador, posicao=posicao, desempenho=atributos['desempenho'])

# Criar um mapeamento de índices para garantir que os índices do dataset filtrado correspondam aos da similaridade
index_mapping = {player: idx for idx, player in enumerate(dataset["Player"])}

# Arestas entre os jogadores mais relevantes (ajustando a parte do código)
for pos1, jogadores1 in nos_relevantes_posicoes.items():
    for pos2, jogadores2 in nos_relevantes_posicoes.items():
        if pos1 != pos2:
            for pl1 in jogadores1:
                for pl2 in jogadores2:
                    # Use o mapeamento de índices para acessar a matriz de similaridade
                    if pl1 in index_mapping and pl2 in index_mapping:
                        idx_pl1 = index_mapping[pl1]
                        idx_pl2 = index_mapping[pl2]
                        
                        if idx_pl1 < len(similaridades) and idx_pl2 < len(similaridades):
                            similaridade = similaridades[idx_pl1, idx_pl2]
                            if similaridade > 0.2:
                                peso_aresta = (grafo_final.nodes[pl1]['desempenho'] +
                                               grafo_final.nodes[pl2]['desempenho'])
                                grafo_final.add_edge(pl1, pl2, peso=peso_aresta)

#Função para selecionar o time ideal
def selecionar_time_ideal(grafo_final, formacao_desejada):
    time_selecionado = []
    posicoes_preenchidas = {pos: 0 for pos in formacao_desejada}
    visitados = set()
    candidatos = []
    
    centralidade = {j: grafo_final.degree(j) for j in grafo_final.nodes}
    
    max_centralidade = max(centralidade.values()) if centralidade else 1
    centralidade_norm = {k: v / max_centralidade for k, v in centralidade.items()}
    
    max_conexao = max(sum(grafo_final[u][v].get('peso', 0) for u, v in grafo_final.edges(j)) for j in grafo_final.nodes)
    conexao_total_norm = {j: sum(grafo_final[u][v].get('peso', 0) for u, v in grafo_final.edges(j)) / max_conexao for j in grafo_final.nodes}
    
    for jogador in grafo_final.nodes:
        desempenho = grafo_final.nodes[jogador]['desempenho']
        posicao = grafo_final.nodes[jogador]['posicao']
        importancia = desempenho * (1 + centralidade_norm.get(jogador, 0.1) + conexao_total_norm.get(jogador, 0.1))
        heapq.heappush(candidatos, (-importancia, jogador, posicao))
    
    posicoes_candidatos = {pos: [] for pos in formacao_desejada}
    
    while candidatos:
        importancia, jogador, posicao = heapq.heappop(candidatos)
        if posicao in posicoes_preenchidas and posicoes_preenchidas[posicao] < formacao_desejada[posicao]:
            posicoes_candidatos[posicao].append((importancia, jogador))
    
    for posicao, max_jogadores in formacao_desejada.items():
        melhores_jogadores = sorted(posicoes_candidatos[posicao], key=lambda x: x[0])[:max_jogadores]
        for importancia, jogador in melhores_jogadores:
            if jogador not in visitados:
                time_selecionado.append(jogador)
                visitados.add(jogador)
                posicoes_preenchidas[posicao] += 1
    
    desempenho_total = sum(grafo_final.nodes[j]['desempenho'] for j in time_selecionado)
    
    return time_selecionado, desempenho_total

formacao_desejada = {'GK': 1, 'DF': 2, 'DFMF': 2, 'MF': 1, 'MFDF': 1, 'MFFW': 1, 'FW': 1, 'FWMF': 1, 'FWDF': 1}
time_ideal, desempenho_total = selecionar_time_ideal(grafo_final, formacao_desejada)

print("Time Ideal:", time_ideal)
print("Desempenho Total:", desempenho_total)

# Plotando o grafo completo com os jogadores selecionados
plotar_grafo_completo(grafo_final, nome_arquivo='graphs/grafo_completo.png')
plt.show()
