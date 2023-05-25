# Hugo, Franciane e Rafael
# Processamento Digital de Imagens
# 24/05/2023
# Contador de Moedas

# Importando depêndencias
import cv2
import sys
import numpy as np

# Depois de alguns testes, a cor media das moedas é essa (Variando um pouco)
dados_cores = {5:(111, 149, 194), 10:(90, 146, 178), 25:(116, 152, 169), 50:(71, 73, 72), 100:(68, 82, 89)}

# Passando a imagem para binario
def to_binario(gray_image):
    unique_values, counts = np.unique(gray_image, return_counts=True)
    mode_index = np.argmax(counts)
    cor_fundo = unique_values[mode_index]
    imbw = gray_image.copy()
    for i in range(altura):
        for j in range(largura):
                imbw[i][j] = 0 if imbw[i][j] == cor_fundo else 255
    return imbw

# Calcular a diferença entre duas cores, util para ver o valor de uma moeda
def diferenca_cor(cor1, cor2):
    return abs(cor2[0] - cor1[0]) + abs(cor2[1] - cor1[1]) + abs(cor2[2] - cor1[2])

# Função que conta as moedas da foto e armazena os pixels em um vetor
def contador(image):
    moedas = list()
    visitados = set()
    # Percorrer a imagem
    for y in range(altura):
        for x in range(largura):
            # Verificar se o pixel é branco (255) e se ainda não foi visitado
            if image[y, x] == 255 and (y, x) not in visitados:
                # Marcar os pixels do contorno da moeda usando busca em profundidade (DFS)
                moeda = set()
                pilha = [(y, x)]
                
                while pilha:
                    cy, cx = pilha.pop()
                    
                    if (cy, cx) in visitados:
                        continue
                    
                    visitados.add((cy, cx))
                    moeda.add((cy, cx))
                    
                    vizinhos = [(cy - 1, cx), (cy + 1, cx), (cy, cx - 1), (cy, cx + 1)]

                    # Colocando na pilha os pixels que são moedas
                    for ny, nx in vizinhos:
                        if ny >= 0 and ny < altura and nx >= 0 and nx < largura and image[ny, nx] == 255:
                            pilha.append((ny, nx))
                
                # Incrementar o contador de moedas e calcular o valor total
                moedas.append(moeda)             
    # Retorna as moedas
    return  moedas

def encontrar_valor(moedas):
    valor_total = 0.0
    contador_moedas = 0
    for moeda in moedas:
        cor_moeda = calcular_cor_media(img, moeda)
        for valor, cor_padrao in dados_cores.items():
            if diferenca_cor(cor_padrao, cor_moeda) < 25:
                valor_total = valor_total + int(valor)
                contador_moedas += 1 
                #print(f"Moeda de {int(valor)} encontrada!")   
                break
    #print(f"Numero de moedas: {contador_moedas}\nValor total: R${valor_total/100} reais.")
    print(f"{valor_total/100}")

# Calcula a cor media de uma moeda
def calcular_cor_media(imagem, moeda):
    soma_r = 0
    soma_g = 0
    soma_b = 0

    for y, x in moeda:
        pixel = imagem[y, x]
        soma_r += pixel[2]  # Canal Vermelho
        soma_g += pixel[1]  # Canal Verde
        soma_b += pixel[0]  # Canal Azul

    tamanho_moeda = len(moeda)
    cor_media = (soma_b // tamanho_moeda, soma_g // tamanho_moeda, soma_r // tamanho_moeda)
    return cor_media

if __name__ == '__main__':
    # Lendo a imagem
    #num_teste = 8
    #filename = f"teste{num_teste}.png"
    filename = sys.argv[1]
    img = cv2.imread(filename) # Imagem colorida
    gray_image = cv2.imread(filename,0) # Imagem cinza
    altura, largura, canais = img.shape

    # Passando imagem pra binario
    imbw = to_binario(gray_image)  # Imagem binária

    kernel = np.ones((3,3), np.uint8)
    imbw_opened = cv2.morphologyEx(imbw, cv2.MORPH_OPEN, kernel) # Imagem binaria com abertura (remover a linha da imagem 5 por exemplo)

    # Identifica as moedas e contabiliza
    moedas = contador(imbw_opened) # Pixels contendo as moedas em forma de set
    encontrar_valor(moedas)

    #cv2.imshow("Imagem original", img)
    #cv2.imshow("Imagem em tons de cinza", gray_image)
    #cv2.imshow("Imagem binaria", imbw)
    #cv2.imshow("Imagem binaria apos a abertura", imbw_opened)

    cv2.waitKey(0)
