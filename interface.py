import os
from banco_dados import restaurantes, salvar_restaurantes

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def exibir_nome_do_programa():
    print('Ｓａｂｏｒ Ｅｘｐｒｅｓｓ\n')

def exibir_opcao():
    print('1. Cadastrar restaurante')
    print('2. Listar restaurantes')
    print('3. Ativar/Desativar restaurante')
    print('4. Finalizar app\n')

def finalizar_app():
    limpar_tela()
    print('Finalizando app.\n')

def opcao_invalida():
    print('Opção inválida.\n')
    input('Clique em qualquer tecla para voltar ao menu principal.\n')

def cadastrar_novo_restaurante():
    limpar_tela()
    print('Cadastro de novos restaurantes.\n')
    nome = input('Digite o nome do restaurante: ')
    categoria = input(f'Digite a categoria do restaurante {nome}: ')
    dados = {'nome': nome, 'categoria': categoria, 'ativo': False}
    restaurantes.append(dados)
    salvar_restaurantes()
    print(f'\nO restaurante {nome} foi cadastrado com sucesso!\n')
    input('Pressione qualquer tecla para voltar ao menu principal.\n')

def listar_restaurantes():
    limpar_tela()
    print('Listagem de restaurantes:\n')
    print(f'{"Nome".ljust(20)} | {"Categoria".ljust(15)} | {"Status"}')
    print('-' * 50)
    for restaurante in restaurantes:
        nome = restaurante['nome'].ljust(20)
        categoria = restaurante['categoria'].ljust(15)
        status = 'Ativado' if restaurante['ativo'] else 'Desativado'
        print(f'{nome} | {categoria} | {status}')
    print('-' * 50)
    input('\nPressione qualquer tecla para voltar ao menu principal.\n')

def alternar_estado_restaurante():
    limpar_tela()
    print('Ativar/Desativar restaurante\n')
    nome = input('Digite o nome do restaurante: ')

    encontrado = False
    for restaurante in restaurantes:
        if restaurante['nome'].lower() == nome.lower():
            encontrado = True
            restaurante['ativo'] = not restaurante['ativo']
            salvar_restaurantes()
            status = 'Ativado' if restaurante['ativo'] else 'Desativado'
            print(f'\nO restaurante {nome} foi {status} com sucesso!\n')
            break

    if not encontrado:
        print(f'\nO restaurante "{nome}" não foi encontrado.\n')

    input('Pressione qualquer tecla para voltar ao menu principal.\n')
