
import json
import os
from typing import List, Dict, Optional
from datetime import datetime

class RestaurantManager:
    def __init__(self, filename='restaurantes.json'):
        self.filename = filename
        self.restaurants = []
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
            'ativo': False,
            'data_criacao': datetime.now().isoformat()
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
