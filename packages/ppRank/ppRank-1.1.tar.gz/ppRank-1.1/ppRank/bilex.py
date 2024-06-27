import csv

def bilex(R_file, T_file, has_header=False):
    """
    Calcula a matriz A usando a abordagem biobjetiva lexicográfica.
    
    Args:
        R_file (str): Nome do arquivo R contendo os valores para R. Valores da execução do algoritmo.
        T_file (str): Nome do arquivo T contendo os valores para T. Valores com o tempo de execução dos algoritmos.
        has_header (bool): Indica se o arquivo têm cabeçalho
    
    Returns:
        list: Matriz A resultante

    Abordagem biobjetiva lexicográfica:
        Mais detalhes sobre a abordagem biobjetiva lexicográfica podem ser encontrados em (https://...)
    """


    # Inicializa a lsita R como uma lista vazia
    R = []

    # Inicializa a lista T como uma lista vazia
    T = []

    # Inicializa a lista names como uma lista vazia
    names = []
    
    

    # Lê os valores do arquivo R_file e atribui a matriz vazia R, e adiciona os nomes à lista names
    with open(R_file, 'r') as arquivo:
        arquivo_csv = csv.reader(arquivo, delimiter=',')
        if has_header:
            next(arquivo_csv)  # Pula a linha do cabeçalho
        for line in arquivo_csv:
            names.append(line[0])  # Adiciona o primeiro elemento de cada linha à lista names
            valores = [float(valor) if (valor != '' and valor != '0.0') else 0.0 for valor in line[1:]]
            R.append(valores)

    # Lê os valores do arquivo T_file e atribui a matriz vazia T, e adiciona os nomes à lista names
    with open(T_file, 'r') as arquivo:
        arquivo_csv = csv.reader(arquivo, delimiter=',')
        if has_header:
            next(arquivo_csv)  # Pula a linha do cabeçalho
        for line in arquivo_csv:
            valores = [float(valor) if (valor != '' and valor != '0.0') else 0.0 for valor in line[1:]]
            T.append(valores)

    
    # Inicializa as variáveis m e n com o número total de listas em R e com o comprimento da última lista, respectivamente.
    m, n = len(R), (len(R[0-1]))
    
    # Inicializa a matriz A com o mesmo comprimento de R preenchida com 1's
    A = [[1] * n for _ in range(m)]



    # Bloco para calcular os valores da matriz A
    for i in range(0,m):
        maior = 1   # Variável para calcular a classificação do maior valor na matriz. (0.0 é considerado o maior valor) Os demais valores seguem a ordenação decimal.

        # Bloco que percorre cada linha da matriz A e atualiza os valores
        for j in range(n):

            # Caso haja apenas um valor na linha ele recebe 1.0
            if n == 0:
                A[i][j] = 1.0
            else:

                if R[i][j-1] == 0.0:

                    if R[i][j] != 0.0:  # Se o valor anterior de R (R[i][j-1]) for igual a zero e o atual R[i][j] for diferente de zero
                        maior += 1      # Soma 1 a variável maior

                        
                        A[i][j] = A[i][j-1]     # O valor atual de A na linha recebe a classificação do anterior 
                        A[i][j-1] = maior       # e o atual recebe a maior classificação

                        # Fazer com que todos os zeros também recebam maior:
                        for k in range (j):
                            if R[i][k] == 0.0:  # Atribui a classificação maior em A para todos os valores 0.0 correspondentes em R 
                                A[i][k] = maior
  
                    # Caso o valor em R seja 0.0, A[i][j] recebe a maior classificação
                    else:
                        A[i][j] = maior
                        #Colocar todos os 0's de R faltantes como classificação maior em A
                        for k in range (j):
                            if R[i][k] == 0.0:
                                A[i][k] = maior
                        

                # Caso o anterior de R seja menor que o atual
                elif R[i][j-1] < R[i][j]:

                    maior += 1      # Incrementa maior já que um novo valor foi adicionado
                    # Bloco para atualizar os valores anteriores a R[i][j]
                    for k in range (j):
                            if R[i][k] == 0:    # Se o valor em R for 0.0, a posição em A correspondente recebe a maior classificação
                                A[i][k] = maior
                            elif R[i][k] == R[i][j]:    # Se o valor for igual a R[i][j], o equivalente de R[i][j] em A recebe a mesma classificação
                                A[i][j] = A[i][k]   
                                maior += 1
                            elif R[i][k] > R[i][j]:     # Se o valor for maior que R[i][j], sua classificação é aumentada
                                A[i][k] += 1
                            elif R[i][k] < R[i][j] and R[i][k] != 0.0:  # Se o valor for menor que R[i][j] então a classificação de A[i][j] é aumentada 
                                A[i][j] += 1

                    if(A[i][j] == maior):
                        maior += 1
                        for(k) in range(j):
                            if R[i][k] == 0.0:
                                A[i][k] = maior


                # Caso a posição anterior de R tenha o mesmo valor que a atual
                elif R[i][j-1] == R[i][j]:
                    if T[i][j-1] < T[i][j]:  # Se o tempo do anterior for menor do que o atual então a posição atual em A recebe a classificação do anterior incrementada em 1
                        A[i][j] = A[i][j-1] + 1
                    elif T[i][j-1] > T[i][j]:  # Se o tempo do anterior for maior que o atual então a posição atual em A recebe a classificação da anterior, e a anterior recebe a atual + 1
                        A[i][j] = A[i][j-1]
                        A[i][j-1] = A[i][j] + 1 
                    else:
                        A[i][j] = A[i][j-1] # Caso os valores de tempo sejam iguais a atual recebe a classificação da anterior
                    maior += 1

                elif R[i][j] == 0.0:
                    A[i][j] = maior    # Se a posição atual em A tiver o correspondente em R igual a 0.0, A recebe a maior classificação

                # Caso a posição anterior de R tenha valor maior que a atual
                elif R[i][j-1] > R[i][j]:
                    # Bloco para atualizar os valores anteriores a R[i][j]
                    for k in range (j):
                        if R[i][k] > R[i][j]:   # Se o valor for maior que R[i][j], sua classificação em A é aumentada
                            A[i][k] += 1
                        elif R[i][k] < R[i][j]: # Se o valor for menor que R[i][j] então a classificação de A[i][j] é aumentada 
                            A[i][j] = A[i][j] + 1
                        elif R[i][k] == R[i][j]: # Se o valor for igual a R[i][j], então A[i][j] recebe a mesma classificação de A[i][k]
                            A[i][j] = A[i][k]

    
                #Ajustar os valores de classificação caso seja a última repetição do bloco
                if j == n-1:
                    # criar matriz do tamanho de R com valores -1
                    ranks = [-1] * n

                    # Bloco para atualizar os valores
                    for k in range (n):
                        for l in range (n):
                            if A[i][k] == l+1:
                                ranks[l] += 1
                        
                    print(ranks)
                    for k in range (n):
                        for l in range (n-1):
                            if A[i][k] == l+1 and ranks[l] >= 1:
                                A[i][k] += ranks[l]*0.5
            
    return A