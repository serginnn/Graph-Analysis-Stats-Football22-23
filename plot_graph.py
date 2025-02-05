import matplotlib.pyplot as plt
import networkx as nx


def plotar_grafo_completo(grafo, nome_arquivo):
    plt.figure(figsize=(24, 20))
    
    # Layout mais espaçado
    posicoes = nx.spring_layout(grafo, k=0.5)  

    nx.draw(
        grafo, pos=posicoes, with_labels=True, font_size=8, node_size=500,
        node_color='skyblue', edge_color="gray", width=0.5
    )

    plt.rcParams['font.family'] = 'DejaVu Sans'
    plt.savefig(nome_arquivo, format='png', dpi=300)
    plt.show()


def plotar_subgrafos(grafos, nome_arquivo_prefix):
    for posicao, grafo in grafos.items():
        nome_arquivo = f"{nome_arquivo_prefix}{posicao}.png"
        
        plt.figure(figsize=(24, 20))

        # Layout mais espaçado para subgrafos densos
        posicoes = nx.spring_layout(grafo, k=0.8)

        nx.draw(
            grafo, pos=posicoes, with_labels=True, font_size=8, node_size=500,
            edge_color='gray', width=0.5, node_color='skyblue'
        )

        plt.savefig(nome_arquivo, format='png', dpi=300)
        plt.close()  # Fecha a figura para evitar uso excessivo de memória
