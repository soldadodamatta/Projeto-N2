
"""
Interface de console para o sistema de gerenciamento de restaurantes
Alternativa à interface gráfica
"""

import os
import sys
from restaurant_manager import RestaurantManager

def limpar_tela():
    """Limpa a tela do terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')

def exibir_cabecalho():
    """Exibe o cabeçalho do programa"""
    print("=" * 50)
    print("🍽️  SABOR EXPRESS - GERENCIAMENTO DE RESTAURANTES")
    print("=" * 50)
    print()

def exibir_menu():
    """Exibe o menu principal"""
    print("📋 MENU PRINCIPAL:")
    print("1. 📝 Cadastrar restaurante")
    print("2. 📋 Listar restaurantes") 
    print("3. 🔍 Buscar restaurante")
    print("4. ✏️  Editar restaurante")
    print("5. 🔄 Ativar/Desativar restaurante")
    print("6. 🗑️  Excluir restaurante")
    print("7. 📊 Estatísticas")
    print("8. 🚪 Sair")
    print()

def obter_opcao():
    """Obtém a opção escolhida pelo usuário"""
    try:
        opcao = int(input("👉 Escolha uma opção (1-8): "))
        return opcao
    except ValueError:
        return None

def pausar():
    """Pausa a execução e aguarda input do usuário"""
    input("\n⏸️  Pressione ENTER para continuar...")

def cadastrar_restaurante(manager):
    """Cadastra um novo restaurante"""
    limpar_tela()
    print("📝 CADASTRAR NOVO RESTAURANTE")
    print("-" * 30)
    
    nome = input("Nome do restaurante: ").strip()
    if not nome:
        print("❌ Nome não pode estar vazio!")
        pausar()
        return
    
    categoria = input("Categoria: ").strip()
    if not categoria:
        print("❌ Categoria não pode estar vazia!")
        pausar()
        return
    
    if manager.add_restaurant(nome, categoria):
        print(f"✅ Restaurante '{nome}' cadastrado com sucesso!")
    else:
        print(f"❌ Erro: Já existe um restaurante com o nome '{nome}'!")
    
    pausar()

def listar_restaurantes(manager):
    """Lista todos os restaurantes"""
    limpar_tela()
    print("📋 LISTA DE RESTAURANTES")
    print("-" * 40)
    
    restaurantes = manager.get_all_restaurants()
    
    if not restaurantes:
        print("📭 Nenhum restaurante cadastrado.")
        pausar()
        return
    
    print(f"{'ID':<4} {'NOME':<25} {'CATEGORIA':<15} {'STATUS':<10}")
    print("-" * 60)
    
    for rest in restaurantes:
        status = "✅ Ativo" if rest['ativo'] else "❌ Inativo"
        print(f"{rest['id']:<4} {rest['nome']:<25} {rest['categoria']:<15} {status:<10}")
    
    print(f"\n📊 Total: {len(restaurantes)} restaurantes")
    pausar()

def buscar_restaurantes(manager):
    """Busca restaurantes por nome ou categoria"""
    limpar_tela()
    print("🔍 BUSCAR RESTAURANTES")
    print("-" * 25)
    
    termo = input("Digite o termo de busca (nome ou categoria): ").strip()
    if not termo:
        print("❌ Termo de busca não pode estar vazio!")
        pausar()
        return
    
    resultados = manager.search_restaurants(termo)
    
    if not resultados:
        print(f"📭 Nenhum restaurante encontrado para '{termo}'")
        pausar()
        return
    
    print(f"\n🔍 Resultados para '{termo}':")
    print(f"{'ID':<4} {'NOME':<25} {'CATEGORIA':<15} {'STATUS':<10}")
    print("-" * 60)
    
    for rest in resultados:
        status = "✅ Ativo" if rest['ativo'] else "❌ Inativo"
        print(f"{rest['id']:<4} {rest['nome']:<25} {rest['categoria']:<15} {status:<10}")
    
    print(f"\n📊 {len(resultados)} resultado(s) encontrado(s)")
    pausar()

def editar_restaurante(manager):
    """Edita um restaurante existente"""
    limpar_tela()
    print("✏️  EDITAR RESTAURANTE")
    print("-" * 20)
    
    try:
        id_rest = int(input("ID do restaurante para editar: "))
    except ValueError:
        print("❌ ID inválido!")
        pausar()
        return
    
    restaurante = manager.get_restaurant_by_id(id_rest)
    if not restaurante:
        print(f"❌ Restaurante com ID {id_rest} não encontrado!")
        pausar()
        return
    
    print(f"\n📝 Editando: {restaurante['nome']}")
    print(f"Categoria atual: {restaurante['categoria']}")
    print()
    
    novo_nome = input(f"Novo nome ({restaurante['nome']}): ").strip()
    if not novo_nome:
        novo_nome = restaurante['nome']
    
    nova_categoria = input(f"Nova categoria ({restaurante['categoria']}): ").strip()
    if not nova_categoria:
        nova_categoria = restaurante['categoria']
    
    if manager.update_restaurant(id_rest, novo_nome, nova_categoria):
        print(f"✅ Restaurante atualizado com sucesso!")
    else:
        print(f"❌ Erro ao atualizar restaurante!")
    
    pausar()

def alternar_status(manager):
    """Alterna o status ativo/inativo de um restaurante"""
    limpar_tela()
    print("🔄 ATIVAR/DESATIVAR RESTAURANTE")
    print("-" * 35)
    
    try:
        id_rest = int(input("ID do restaurante: "))
    except ValueError:
        print("❌ ID inválido!")
        pausar()
        return
    
    restaurante = manager.toggle_restaurant_status(id_rest)
    if restaurante:
        status = "ativado" if restaurante['ativo'] else "desativado"
        print(f"✅ Restaurante '{restaurante['nome']}' {status} com sucesso!")
    else:
        print(f"❌ Restaurante com ID {id_rest} não encontrado!")
    
    pausar()

def excluir_restaurante(manager):
    """Exclui um restaurante"""
    limpar_tela()
    print("🗑️  EXCLUIR RESTAURANTE")
    print("-" * 20)
    
    try:
        id_rest = int(input("ID do restaurante para excluir: "))
    except ValueError:
        print("❌ ID inválido!")
        pausar()
        return
    
    restaurante = manager.get_restaurant_by_id(id_rest)
    if not restaurante:
        print(f"❌ Restaurante com ID {id_rest} não encontrado!")
        pausar()
        return
    
    print(f"\n⚠️  Você está prestes a excluir:")
    print(f"Nome: {restaurante['nome']}")
    print(f"Categoria: {restaurante['categoria']}")
    
    confirmacao = input("\n❓ Tem certeza? (s/N): ").strip().lower()
    
    if confirmacao == 's':
        if manager.delete_restaurant(id_rest):
            print(f"✅ Restaurante '{restaurante['nome']}' excluído com sucesso!")
        else:
            print(f"❌ Erro ao excluir restaurante!")
    else:
        print("❌ Operação cancelada.")
    
    pausar()

def exibir_estatisticas(manager):
    """Exibe estatísticas do sistema"""
    limpar_tela()
    print("📊 ESTATÍSTICAS DO SISTEMA")
    print("-" * 30)
    
    stats = manager.get_statistics()
    
    print(f"📈 Total de restaurantes: {stats['total']}")
    print(f"✅ Restaurantes ativos: {stats['ativos']}")
    print(f"❌ Restaurantes inativos: {stats['inativos']}")
    
    if stats['categorias']:
        print("\n🏷️  DISTRIBUIÇÃO POR CATEGORIA:")
        print("-" * 35)
        
        for categoria, count in stats['categorias'].items():
            percentage = (count / stats['total'] * 100) if stats['total'] > 0 else 0
            print(f"   • {categoria}: {count} ({percentage:.1f}%)")
    
    pausar()

def main():
    """Função principal da aplicação console"""
    manager = RestaurantManager()
    
    while True:
        limpar_tela()
        exibir_cabecalho()
        exibir_menu()
        
        opcao = obter_opcao()
        
        if opcao == 1:
            cadastrar_restaurante(manager)
        elif opcao == 2:
            listar_restaurantes(manager)
        elif opcao == 3:
            buscar_restaurantes(manager)
        elif opcao == 4:
            editar_restaurante(manager)
        elif opcao == 5:
            alternar_status(manager)
        elif opcao == 6:
            excluir_restaurante(manager)
        elif opcao == 7:
            exibir_estatisticas(manager)
        elif opcao == 8:
            limpar_tela()
            print("👋 Obrigado por usar o Sabor Express!")
            print("🍽️  Até logo!")
            break
        else:
            limpar_tela()
            print("❌ Opção inválida! Escolha um número entre 1 e 8.")
            pausar()

if __name__ == "__main__":
    main()
