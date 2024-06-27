import csv

def par10(G_file, has_header = False):

    G = []

    names = []

    # Lê os valores do arquivo G_file e atribui a matriz vazia G, e adiciona os nomes à lista names
    with open(G_file, 'r') as arquivo:
        arquivo_csv = csv.reader(arquivo, delimiter=',')
        if has_header:
            next(arquivo_csv)  # Pula a linha do cabeçalho
        for line in arquivo_csv:
            names.append(line[0])  # Adiciona o primeiro elemento de cada linha à lista names
            valores = [float(valor) if (valor != '' and valor != '0.0') else 0.0 for valor in line[1:]]
            G.append(valores)


    # Inicializa as variáveis m e n com o número total de listas em G e com o comprimento da última lista, respectivamente.
    m, n = len(G), (len(G[0-1]))
    
    # Inicializa a matriz A com o mesmo comprimento de G preenchida com 1's
    A = [[1] * n for _ in range(m)]

    for i in range(0,m):
        

        # Bloco que percorre cada linha da matriz A e atualiza os valores
        for j in range(n):
            # Caso haja apenas um valor na linha ele recebe 1.0
            if n == 0:
                A[i][j] = G[i][j]
            else:
                A[i][j] = G[i][j]


        # Variável para calcular o maior valor na linha
        max_value = max(A[i])

        for j in range(n):
            # Caso A[i][j] == 0 então A[i][j] recebe o maior valor da linha multiplicado por 10
            if A[i][j] == 0:
                A[i][j] = max_value * 10


    return A