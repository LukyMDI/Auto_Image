####################################
#                                  #
#   Programa criado por: LukyMDI   #
#   Discord: Luky#8907             #
#                                  #
####################################


from urllib.request import urlretrieve
from bs4 import BeautifulSoup
import requests
import os
import progressbar

# Faz o tratamento do seletor CSS escolhido.
def seletor():
    obter_seletor = input('Seletor (id, class): ').lower()

    if obter_seletor == 'id':
        print('Selecionando elemento pelo id...\n')
    elif obter_seletor == 'class':
        print('Selecionando elemento pela classe...\n')
    else:
        print('Valor inválido. Por favor, digite "id" ou "class".\n')
        return seletor()
    
    return obter_seletor

# Cria a pasta Imagens [numeração]. Caso a pasta Imagens (1) exista, é criada a pasta Imagens (2) e assim sucessivamente.
def criar_pasta():
    i = 1
    while True:
        nome_pasta = f'Imagens {i}'
        if not os.path.exists(nome_pasta):
            os.makedirs(nome_pasta)
            return nome_pasta
        i += 1

# Função principal responsável pelo funcionamento do programa.
def baixar_imagens():

    # Input para obtenção da URL do site
    obter_url = input('URL: ')

    # Input para obtenção do seletor CSS
    obter_seletor = seletor()

    # Input para obtenção do nome do seletor
    obter_nome_seletor = input('Nome do seletor: ')
    print('\n')

    # Chamada da função responável por criar a pasta
    pasta_destino = criar_pasta()

    # URL do site que contém as imagens
    url = f'{obter_url}'

    # Obter o conteúdo HTML do site
    html = requests.get(url).content

    # Criar objeto beautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # Localizar a div que contém as imagens. (seletor: 'id', 'class')
    div = soup.find('div', {f'{obter_seletor}': f'{obter_nome_seletor}'})

    # Obter todas as tags 'img' dentro da div
    imgs = div.find_all('img')

    # ProgressBar
    widgets = ['Progresso: ', progressbar.Percentage(), progressbar.Bar()]
    bar = progressbar.ProgressBar(maxval=len(imgs), widgets=widgets)
    bar.start()

    for i, img in enumerate(imgs):
        try:
            src = img.get('src')
            urlretrieve(src, f"{pasta_destino}/imagem-{i}.png")
        except Exception as e:
            print(f'\nNão foi possível baixar a imagem {i}: {e}')
        bar.update(i+1)

    bar.finish()

    print('\nDownloads concluídos com sucesso!\n')

if __name__ == '__main__':
    baixar_imagens()
    input('Pressione qualquer tecla para sair...')