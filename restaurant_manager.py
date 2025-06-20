
import json
import os
import re
from typing import List, Dict, Optional
from datetime import datetime

class RestaurantManager:
    def __init__(self, filename='restaurantes.json'):
        self.filename = filename
        self.restaurants = []
        self.notifications = []
        self.load_restaurants()

    def load_restaurants(self):
        """Carrega restaurantes do arquivo JSON"""
        try:
            if os.path.exists(self.filename):
                with open(self.filename, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    self.restaurants = data.get('restaurants', [])
            else:
                self.restaurants = []
        except Exception as e:
            print(f"Erro ao carregar restaurantes: {e}")
            self.restaurants = []

    def save_restaurants(self):
        """Salva restaurantes no arquivo JSON"""
        try:
            data = {
                'restaurants': self.restaurants,
                'version': '1.0',
                'last_updated': datetime.now().isoformat()
            }
            with open(self.filename, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Erro ao salvar restaurantes: {e}")
            return False

    def add_restaurant(self, name: str, category: str) -> bool:
        """Adiciona um novo restaurante"""
        if self.restaurant_exists(name):
            return False
        
        # Gera novo ID
        max_id = max([r.get('id', 0) for r in self.restaurants], default=0)
        new_id = max_id + 1

        restaurant = {
            'id': new_id,
            'nome': name.strip(),
            'categoria': category.strip(),
            'ativo': True,
            'favorito': False,
            'avaliacao': 0.0,
            'num_avaliacoes': 0,
            'telefone': '',
            'email': '',
            'endereco': '',
            'cnpj': '',
            'data_criacao': datetime.now().isoformat(),
            'data_atualizacao': datetime.now().isoformat()
        }
        
        self.restaurants.append(restaurant)
        return self.save_restaurants()

    def restaurant_exists(self, name: str) -> bool:
        """Verifica se um restaurante já existe"""
        return any(r['nome'].lower() == name.lower().strip() for r in self.restaurants)

    def get_all_restaurants(self) -> List[Dict]:
        """Retorna todos os restaurantes"""
        return self.restaurants.copy()

    def get_restaurants_by_category(self, category: str) -> List[Dict]:
        """Retorna restaurantes filtrados por categoria"""
        if not category or category.lower() == 'todas':
            return self.restaurants.copy()
        return [r for r in self.restaurants if r['categoria'].lower() == category.lower()]

    def get_restaurants_by_status(self, active_only: bool = None) -> List[Dict]:
        """Retorna restaurantes filtrados por status"""
        if active_only is None:
            return self.restaurants.copy()
        return [r for r in self.restaurants if r['ativo'] == active_only]

    def search_restaurants(self, search_term: str) -> List[Dict]:
        """Busca restaurantes por nome ou categoria"""
        if not search_term:
            return self.restaurants.copy()
        
        search_lower = search_term.lower()
        return [r for r in self.restaurants if 
                search_lower in r['nome'].lower() or 
                search_lower in r['categoria'].lower()]

    def update_restaurant(self, restaurant_id: int, name: str, category: str) -> bool:
        """Atualiza um restaurante existente"""
        for restaurant in self.restaurants:
            if restaurant.get('id') == restaurant_id:
                # Verifica se o novo nome já existe (exceto para o próprio restaurante)
                if name.lower() != restaurant['nome'].lower() and self.restaurant_exists(name):
                    return False
                
                restaurant['nome'] = name.strip()
                restaurant['categoria'] = category.strip()
                restaurant['data_atualizacao'] = datetime.now().isoformat()
                return self.save_restaurants()
        return False

    def toggle_restaurant_status(self, restaurant_id: int) -> Optional[Dict]:
        """Alterna o status ativo/inativo de um restaurante"""
        for restaurant in self.restaurants:
            if restaurant.get('id') == restaurant_id:
                restaurant['ativo'] = not restaurant['ativo']
                restaurant['data_atualizacao'] = datetime.now().isoformat()
                if self.save_restaurants():
                    return restaurant
        return None

    def delete_restaurant(self, restaurant_id: int) -> bool:
        """Remove um restaurante"""
        for i, restaurant in enumerate(self.restaurants):
            if restaurant.get('id') == restaurant_id:
                self.restaurants.pop(i)
                return self.save_restaurants()
        return False

    def get_categories(self) -> List[str]:
        """Retorna todas as categorias únicas"""
        categories = list(set(r['categoria'] for r in self.restaurants))
        return sorted(categories)

    def get_statistics(self) -> Dict:
        """Retorna estatísticas do sistema"""
        total = len(self.restaurants)
        active = sum(1 for r in self.restaurants if r['ativo'])
        inactive = total - active
        
        # Distribuição por categoria
        category_counts = {}
        for restaurant in self.restaurants:
            category = restaurant['categoria']
            category_counts[category] = category_counts.get(category, 0) + 1

        return {
            'total': total,
            'ativos': active,
            'inativos': inactive,
            'categorias': category_counts
        }

    def get_restaurant_by_id(self, restaurant_id: int) -> Optional[Dict]:
        """Retorna um restaurante específico pelo ID"""
        for restaurant in self.restaurants:
            if restaurant.get('id') == restaurant_id:
                return restaurant.copy()
        return None

    def add_rating(self, restaurant_id: int, rating: float) -> bool:
        """Adiciona uma avaliação ao restaurante"""
        if not (0 <= rating <= 5):
            return False
            
        for restaurant in self.restaurants:
            if restaurant.get('id') == restaurant_id:
                # Inicializar campos de avaliação se não existirem
                if 'avaliacao' not in restaurant:
                    restaurant['avaliacao'] = 0.0
                if 'num_avaliacoes' not in restaurant:
                    restaurant['num_avaliacoes'] = 0
                
                # Calcular nova média
                total_atual = restaurant['avaliacao'] * restaurant['num_avaliacoes']
                restaurant['num_avaliacoes'] += 1
                restaurant['avaliacao'] = (total_atual + rating) / restaurant['num_avaliacoes']
                restaurant['data_atualizacao'] = datetime.now().isoformat()
                
                return self.save_restaurants()
        return False

    def toggle_favorite(self, restaurant_id: int) -> Optional[Dict]:
        """Alterna o status de favorito de um restaurante"""
        for restaurant in self.restaurants:
            if restaurant.get('id') == restaurant_id:
                restaurant['favorito'] = not restaurant.get('favorito', False)
                restaurant['data_atualizacao'] = datetime.now().isoformat()
                
                if self.save_restaurants():
                    return restaurant
        return None

    def get_favorite_restaurants(self) -> List[Dict]:
        """Retorna apenas os restaurantes favoritos"""
        return [r for r in self.restaurants if r.get('favorito', False)]

    @staticmethod
    def validate_email(email: str) -> bool:
        """Valida formato de email"""
        if not email:
            return True  # Email é opcional
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    @staticmethod
    def validate_phone(phone: str) -> bool:
        """Valida formato de telefone brasileiro"""
        if not phone:
            return True  # Telefone é opcional
        # Remove caracteres não numéricos
        digits = re.sub(r'\D', '', phone)
        # Aceita formatos: (11) 99999-9999, 11999999999, etc.
        return len(digits) >= 10 and len(digits) <= 11

    @staticmethod
    def validate_cnpj(cnpj: str) -> bool:
        """Valida CNPJ brasileiro"""
        if not cnpj:
            return True  # CNPJ é opcional
        
        # Remove caracteres não numéricos
        cnpj = re.sub(r'\D', '', cnpj)
        
        # Verifica se tem 14 dígitos
        if len(cnpj) != 14:
            return False
        
        # Verifica se todos os dígitos são iguais
        if len(set(cnpj)) == 1:
            return False
        
        # Calcula os dígitos verificadores
        def calculate_digit(cnpj_digits, weights):
            total = sum(int(digit) * weight for digit, weight in zip(cnpj_digits, weights))
            remainder = total % 11
            return 0 if remainder < 2 else 11 - remainder
        
        # Pesos para cálculo
        weights1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        weights2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        
        # Verifica primeiro dígito
        first_digit = calculate_digit(cnpj[:12], weights1)
        if first_digit != int(cnpj[12]):
            return False
        
        # Verifica segundo dígito
        second_digit = calculate_digit(cnpj[:13], weights2)
        if second_digit != int(cnpj[13]):
            return False
        
        return True

    def validate_restaurant_data(self, name: str, category: str, 
                               phone: str = "", email: str = "", cnpj: str = "") -> tuple:
        """Valida todos os dados do restaurante"""
        errors = []
        
        if not name or not name.strip():
            errors.append("Nome é obrigatório")
        
        if not category or not category.strip():
            errors.append("Categoria é obrigatória")
        
        if phone and not self.validate_phone(phone):
            errors.append("Telefone inválido. Use formato: (11) 99999-9999")
        
        if email and not self.validate_email(email):
            errors.append("Email inválido")
        
        if cnpj and not self.validate_cnpj(cnpj):
            errors.append("CNPJ inválido")
        
        return len(errors) == 0, errors

    def update_restaurant_full(self, restaurant_id: int, name: str, category: str,
                              phone: str = "", email: str = "", endereco: str = "", cnpj: str = "") -> tuple:
        """Atualiza um restaurante com validação completa"""
        # Validar dados
        is_valid, errors = self.validate_restaurant_data(name, category, phone, email, cnpj)
        if not is_valid:
            return False, errors
        
        for restaurant in self.restaurants:
            if restaurant.get('id') == restaurant_id:
                # Verifica se o novo nome já existe (exceto para o próprio restaurante)
                if name.lower() != restaurant['nome'].lower() and self.restaurant_exists(name):
                    return False, ["Já existe um restaurante com este nome"]
                
                restaurant['nome'] = name.strip()
                restaurant['categoria'] = category.strip()
                restaurant['telefone'] = phone.strip()
                restaurant['email'] = email.strip()
                restaurant['endereco'] = endereco.strip()
                restaurant['cnpj'] = cnpj.strip()
                restaurant['data_atualizacao'] = datetime.now().isoformat()
                
                if self.save_restaurants():
                    return True, []
                else:
                    return False, ["Erro ao salvar dados"]
        
        return False, ["Restaurante não encontrado"]

    def add_notification(self, message: str, type: str = "info") -> None:
        """Adiciona uma notificação"""
        notification = {
            'id': len(self.notifications) + 1,
            'message': message,
            'type': type,  # info, success, warning, error
            'timestamp': datetime.now().isoformat(),
            'read': False
        }
        self.notifications.append(notification)
        
        # Manter apenas as últimas 50 notificações
        if len(self.notifications) > 50:
            self.notifications = self.notifications[-50:]
