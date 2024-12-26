import numpy as np

# Função para calcular o Coeficiente de Gini
def gini_coefficient(categories):
    """
    Calcula o índice de Gini para uma lista de categorias.
    Quanto mais impuro for o conjunto de categorias, maior será o valor de Gini.
    """
    _, counts = np.unique(categories, return_counts=True)  # Conta a frequência de cada categoria
    probabilities = counts / len(categories)  # Calcula a probabilidade de cada classe
    return 1 - np.sum(probabilities ** 2)  # Fórmula do índice de Gini

# Função para criar a árvore de decisão
def decision_tree(data, categories, max_depth=5, depth=0):
    """
    Constrói uma árvore de decisão baseada nos dados e nas categorias fornecidas.
    A função faz divisões recursivas com base no valor de Gini.
    """
    num_samples, num_features = data.shape  # Obtém o número de amostras e características
    gini = gini_coefficient(categories)  # Calcula o Gini para a amostra atual

    # Condições de parada: se não houver dados ou atingirmos a profundidade máxima
    if num_samples == 0 or depth == max_depth:
        return {'leaf': True, 'label': np.unique(categories)[0], 'gini': gini}

    best_split = None  # Melhor divisão
    best_gini = float('inf')  # O melhor valor de Gini (inicialmente infinito)
    best_left_data, best_left_categories = None, None  # Dados e categorias da parte esquerda
    best_right_data, best_right_categories = None, None  # Dados e categorias da parte direita

    # Loop sobre cada feature (característica) para encontrar a melhor divisão
    for i in range(num_features):
        # Garantir que os dados estão no formato correto, substituindo vírgulas por pontos
        data_column = data[:, i].astype(str)  # Converte para string
        data_column = np.array([val.replace(',', '.') for val in data_column])  # Substitui vírgula por ponto
        data_column = data_column.astype(float)  # Converte novamente para float

        thresholds = np.unique(data_column)  # Identifica todos os valores únicos na coluna
        for threshold in thresholds:
            # Divisão em dados à esquerda e à direita, com base no threshold
            left_indices = data_column <= threshold
            right_indices = data_column > threshold

            # Se algum dos conjuntos de divisão estiver vazio, ignoramos essa divisão
            if np.sum(left_indices) == 0 or np.sum(right_indices) == 0:
                continue

            left_categories = categories[left_indices]  # Categorias para os dados à esquerda
            right_categories = categories[right_indices]  # Categorias para os dados à direita

            # Calcula o Gini ponderado (média ponderada dos Ginis dos dois lados)
            weighted_gini = (len(left_categories) * gini_coefficient(left_categories) +
                             len(right_categories) * gini_coefficient(right_categories)) / num_samples

            # Atualiza a melhor divisão se o Gini ponderado for menor
            if weighted_gini < best_gini:
                best_gini = weighted_gini
                best_split = (i, threshold)  # Armazena a feature e o valor de threshold da melhor divisão
                best_left_data = data[left_indices]  # Dados para o lado esquerdo
                best_left_categories = left_categories  # Categorias para o lado esquerdo
                best_right_data = data[right_indices]  # Dados para o lado direito
                best_right_categories = right_categories  # Categorias para o lado direito

    # Se não encontrarmos uma boa divisão, retornamos uma folha
    if best_split is None:
        return {'leaf': True, 'label': np.unique(categories)[0], 'gini': gini}

    # Recursivamente divide os dados à esquerda e à direita
    left_tree = decision_tree(best_left_data, best_left_categories, depth=depth + 1, max_depth=max_depth)
    right_tree = decision_tree(best_right_data, best_right_categories, depth=depth + 1, max_depth=max_depth)

    return {
        'feature_index': best_split[0],  # Índice da feature usada para dividir
        'threshold': best_split[1],  # Valor de threshold utilizado para a divisão
        'left': left_tree,  # Subárvore à esquerda
        'right': right_tree,  # Subárvore à direita
        'gini': best_gini,  # Gini da divisão atual
        'leaf': False  # Não é uma folha (ainda há divisão a ser feita)
    }

# Função para imprimir a árvore de decisão de forma legível
def print_tree(tree, feature_names=None, indent=""):
    """
    Imprime a árvore de decisão de forma recursiva, detalhando as divisões feitas em cada nó.
    """
    if tree['leaf']:  # Se for uma folha, imprime a classe final e o Gini
        print(f"{indent}Folha: {tree['label']} (Gini: {tree['gini']:.4f})")
    else:
        # Se não for uma folha, imprime a divisão feita no nó
        feature_name = feature_names[tree['feature_index']] if feature_names else f"Feature {tree['feature_index']}"
        print(f"{indent}Feature: {feature_name} <= {tree['threshold']} (Gini: {tree['gini']:.4f})")
        print(f"{indent}  Esquerda:")  # Parte esquerda da árvore
        print_tree(tree['left'], feature_names, indent + "    ")
        print(f"{indent}  Direita:")  # Parte direita da árvore
        print_tree(tree['right'], feature_names, indent + "    ")

# Função para visualização gráfica da árvore de decisão em formato DOT
def visualize_tree(tree):
    """
    Gera a representação visual da árvore de decisão em formato DOT para uso com Graphviz.
    """
    dot_data = "digraph G {\n"

    # Função recursiva que cria a representação do grafo em DOT
    def recurse(tree, node_id=0):
        if tree['leaf']:  # Se for uma folha, representa o nó como folha
            dot_data = f'    node{node_id} [label="Folha: {tree["label"]}\\nGini: {tree["gini"]:.4f}", shape=box, style=filled, fillcolor=lightgreen];\n'
        else:
            # Caso contrário, cria um nó de decisão com base na feature e threshold
            feature_name = f"Feature {tree['feature_index']}"
            dot_data = f'    node{node_id} [label="{feature_name} <= {tree["threshold"]}\\nGini: {tree["gini"]:.4f}", shape=box, style=filled, fillcolor=lightblue];\n'
            left_node_id = node_id + 1
            right_node_id = node_id + 2
            dot_data += recurse(tree['left'], left_node_id)  # Subárvore esquerda
            dot_data += recurse(tree['right'], right_node_id)  # Subárvore direita
            dot_data += f'    node{node_id} -> node{left_node_id} [label="Verdadeiro"];\n'  # Caminho para a esquerda
            dot_data += f'    node{node_id} -> node{right_node_id} [label="Falso"];\n'  # Caminho para a direita
        return dot_data

    dot_data += recurse(tree)  # Inicia a recursão para criar o DOT
    dot_data += "}"  # Fecha o gráfico DOT
    return dot_data

# Exemplo de dados (substitua por seus dados reais)
data = np.array([[44.51], [50.00], [15.34], [19.88], [29.99], [20.34], [30.47], [14.97]])
categories = np.array(['Alimentos', 'Higiene', 'Limpeza', 'Alimentos', 'Limpeza', 'Higiene', 'Limpeza', 'Alimentos'])

# Criar a árvore de decisão com base nos dados
tree = decision_tree(data, categories, max_depth=5)

# Imprimir a árvore de decisão
print_tree(tree)

# Visualização da árvore em formato DOT
dot_data = visualize_tree(tree)
print("\nVisualização em formato DOT:\n")
print(dot_data)

# Para gerar a árvore visualmente com Graphviz, se você tiver o Graphviz instalado:
# from graphviz import Source
# graph = Source(dot_data)
# graph.render('decision_tree')  # Isso cria um arquivo 'decision_tree.png'
