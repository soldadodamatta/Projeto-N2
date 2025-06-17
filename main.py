from interface import (
    exibir_nome_do_programa,
    exibir_opcao,
    finalizar_app,
    opcao_invalida,
    cadastrar_novo_restaurante,
    listar_restaurantes,
    alternar_estado_restaurante,
    limpar_tela
)
from banco_dados import carregar_restaurantes

def escolher_opcao():
    try:
        opcao = int(input('Escolha uma opção: '))
        if opcao == 1:
            cadastrar_novo_restaurante()
        elif opcao == 2:
            listar_restaurantes()
        elif opcao == 3:
            alternar_estado_restaurante()
        elif opcao == 4:
            finalizar_app()
            return False  # encerra o laço
        else:
            opcao_invalida()
    except:
        opcao_invalida()
    return True  # continua executando

def main():
    carregar_restaurantes()
    executando = True
    while executando:
        limpar_tela()
        exibir_nome_do_programa()
        exibir_opcao()
        executando = escolher_opcao()  # só para se retornar False

if __name__ == '__main__':
    main()
