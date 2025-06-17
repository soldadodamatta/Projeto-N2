import csv

restaurantes = []

def salvar_restaurantes():
    with open('restaurantes.csv', 'w', newline='', encoding='utf-8') as arquivo:
        escritor = csv.writer(arquivo)
        escritor.writerow(['nome', 'categoria', 'ativo'])
        for restaurante in restaurantes:
            escritor.writerow([restaurante['nome'], restaurante['categoria'], restaurante['ativo']])

def carregar_restaurantes():
    restaurantes.clear()
    try:
        with open('restaurantes.csv', 'r', encoding='utf-8') as arquivo:
            leitor = csv.DictReader(arquivo)
            for linha in leitor:
                restaurantes.append({
                    'nome': linha['nome'],
                    'categoria': linha['categoria'],
                    'ativo': linha['ativo'].lower() == 'true'
                })
    except FileNotFoundError:
        pass
