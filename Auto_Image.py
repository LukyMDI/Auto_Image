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
from PIL import Image

# Faz o tratamento do seletor CSS escolhido.
def seletor():
    tipo_seletor = input('Seletor (id, class): ').lower()

    if tipo_seletor == 'id':
        print('Selecionando elemento pelo id...\n')
    elif tipo_seletor == 'class':
        print('Selecionando elemento pela classe...\n')
    else:
        print('Valor inválido. Por favor, digite "id" ou "class".\n')
        # Caso o usuário digite um valor inválido, a função é chamada recursivamente
        return seletor()
    
    return tipo_seletor

# Cria a pasta Imagens [numeração]. Caso a pasta Imagens (1) exista, é criada a pasta Imagens (2) e assim sucessivamente.
def criar_pasta_destino():
    i = 1
    while True:
        nome_pasta = f'Imagens {i}'
        if not os.path.exists(nome_pasta):
            os.makedirs(nome_pasta)
            return nome_pasta
        i += 1

# Função para exibir o menu de ajuda
def exibir_ajuda():
    print('####################################')
    print('#                                  #')
    print('#          MENU DE AJUDA           #')
    print('#                                  #')
    print('####################################\n')

    print('Este programa tem como objetivo baixar imagens de um site e salvá-las em uma pasta. Para utilizá-lo, siga os passos abaixo:\n')
    print('1 - Informe a URL do site onde estão localizadas as imagens.')
    print('2 - Informe se deseja selecionar as imagens pelo "id" ou "class".')
    print('3 - Informe o nome do "id" ou "class" que será utilizado como seletor.')
    print('4 - Aguarde o fim do download das imagens.\n')
    print('#######################################################################################################################\n')


# Função principal responsável pelo funcionamento do programa.
def baixar_imagens():

    print('####################################')
    print('#                                  #')
    print('#   Programa criado por: LukyMDI   #')
    print('#   Discord: Luky#8907             #')
    print('#                                  #')
    print('####################################\n')
    print('#######################################################################################################################\n')

    # Exibe o menu de ajuda
    exibir_ajuda()

    # Input para obtenção da URL do site
    url = input('URL: ')

    # Input para obtenção do seletor CSS
    tipo_seletor = seletor()

    # Input para obtenção do nome do seletor
    nome_seletor = input('Nome do seletor: ')
    print('\n')
    os.system('cls')

    # Chamada da função responável por criar a pasta
    pasta_saida = criar_pasta_destino()

    # URL do site que contém as imagens
    url = f'{url}'

    # Obter o conteúdo HTML do site
    html = requests.get(url).content

    # Criar objeto beautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # Localizar a div que contém as imagens. (seletor: 'id', 'class')
    div = soup.find('div', {f'{tipo_seletor}': f'{nome_seletor}'})

    if div is None:
        print('Erro: Não foi encontrado nenhum elemento com esse seletor no site.\n')
        input('Pressione qualquer tecla para tentar novamente...')
        os.system('cls')
        return baixar_imagens()

    # Obter todas as tags 'img' dentro da div
    imgs = div.find_all('img')

    # ProgressBar
    widgets = ['Progresso: ', progressbar.Percentage(), progressbar.Bar(marker='#', left='[', right=']')]
    bar = progressbar.ProgressBar(maxval=len(imgs), widgets=widgets)
    bar.start()

    for i, imagem in enumerate(imgs):
        try:
            src = imagem.get('src')

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
            response = requests.get(src, headers=headers, stream=True)

            content_type = response.headers.get('content-type')

            if 'image' not in content_type:
                print(f'Erro ao baixar imagem {i}. O conteúdo não é uma imagem.')
                continue

            nome_arquivo, tipo_arquivo = os.path.splitext(os.path.basename(src))

            # Abre a imagem com PIL e salva no formato JPG
            imagem_pil = Image.open(response.raw)
            imagem_pil = imagem_pil.convert('RGB')
            nome_arquivo = f'Imagem {i}.png'
            imagem_pil.save(os.path.join(pasta_saida, nome_arquivo), 'PNG')

        except Exception as e:
            print(f'\nNão foi possível baixar a imagem {i}: {e}')
        bar.update(i+1)

    bar.finish()

    print('\nDownloads concluídos com sucesso!\n')

    # Verificar se o usuário deseja continuar utilizando o programa
    resposta = input('Deseja baixar mais imagens? (s/n): ').lower()
    if resposta == 's':
        os.system('cls')
        return baixar_imagens()
    else:
        print('\nPrograma encerrado.\n')

if __name__ == '__main__':
    baixar_imagens()
    input('Pressione qualquer tecla para sair...')