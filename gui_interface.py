
import tkinter as tk
from tkinter import ttk, messagebox
from restaurant_manager import RestaurantManager
import json

class ModernTheme:
    """Gerenciador de temas moderno"""
    
    def __init__(self):
        self.themes = {
            'dark': {
                'bg_primary': '#0D1117',       # GitHub dark background
                'bg_secondary': '#161B22',     # Card background
                'bg_tertiary': '#21262D',      # Input background
                'bg_accent': '#30363D',        # Hover background
                'text_primary': '#F0F6FC',     # Primary text
                'text_secondary': '#8B949E',   # Secondary text
                'text_muted': '#6E7681',       # Muted text
                'accent_blue': '#58A6FF',      # Primary accent
                'accent_green': '#3FB950',     # Success
                'accent_orange': '#FF8C42',    # Warning
                'accent_red': '#F85149',       # Danger
                'accent_purple': '#BC8CFF',    # Info
                'border_color': '#30363D',     # Border
                'shadow_color': '#000000'      # Shadow
            },
            'light': {
                'bg_primary': '#FFFFFF',       # Clean white
                'bg_secondary': '#F6F8FA',     # Light gray
                'bg_tertiary': '#FFFFFF',      # Input background
                'bg_accent': '#F3F4F6',        # Hover background
                'text_primary': '#24292F',     # Primary text
                'text_secondary': '#656D76',   # Secondary text
                'text_muted': '#9CA3AF',       # Muted text
                'accent_blue': '#0969DA',      # Primary accent
                'accent_green': '#1A7F37',     # Success
                'accent_orange': '#D97706',    # Warning
                'accent_red': '#D1242F',       # Danger
                'accent_purple': '#8250DF',    # Info
                'border_color': '#D0D7DE',     # Border
                'shadow_color': '#CCCCCC'      # Shadow
            }
        }

class RestaurantDialog:
    """Diálogo moderno para adicionar/editar restaurante"""
    
    def __init__(self, parent, title, name="", category="", theme_manager=None):
        self.result = None
        self.theme = theme_manager
        
        # Criar janela modal
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("450x300")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Centralizar janela
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (450 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (300 // 2)
        self.dialog.geometry(f"450x300+{x}+{y}")
        
        self.apply_theme()
        self.create_widgets(name, category)
        
        # Focar no campo nome
        self.name_entry.focus()

    def apply_theme(self):
        if self.theme:
            colors = self.theme.get_current_colors()
            self.dialog.configure(bg=colors['bg_primary'])

    def create_widgets(self, name, category):
        """Cria os widgets do diálogo"""
        colors = self.theme.get_current_colors() if self.theme else {}
        
        # Frame principal com padding
        main_frame = tk.Frame(self.dialog, bg=colors.get('bg_primary', '#0D1117'), padx=30, pady=25)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_label = tk.Label(main_frame, 
                              text="🍽️ Informações do Restaurante",
                              font=('Segoe UI', 16, 'bold'),
                              bg=colors.get('bg_primary', '#0D1117'),
                              fg=colors.get('text_primary', '#F0F6FC'))
        title_label.pack(pady=(0, 25))
        
        # Campo Nome
        name_frame = tk.Frame(main_frame, bg=colors.get('bg_primary', '#0D1117'))
        name_frame.pack(fill=tk.X, pady=(0, 15))
        
        name_label = tk.Label(name_frame, 
                             text="Nome do Restaurante *",
                             font=('Segoe UI', 10, 'bold'),
                             bg=colors.get('bg_primary', '#0D1117'),
                             fg=colors.get('text_primary', '#F0F6FC'))
        name_label.pack(anchor='w', pady=(0, 5))
        
        self.name_entry = tk.Entry(name_frame,
                                  font=('Segoe UI', 11),
                                  bg=colors.get('bg_tertiary', '#21262D'),
                                  fg=colors.get('text_primary', '#F0F6FC'),
                                  insertbackground=colors.get('text_primary', '#F0F6FC'),
                                  relief='flat',
                                  bd=0,
                                  highlightthickness=2,
                                  highlightcolor=colors.get('accent_blue', '#58A6FF'),
                                  highlightbackground=colors.get('border_color', '#30363D'))
        self.name_entry.pack(fill=tk.X, ipady=8)
        self.name_entry.insert(0, name)
        
        # Campo Categoria
        category_frame = tk.Frame(main_frame, bg=colors.get('bg_primary', '#0D1117'))
        category_frame.pack(fill=tk.X, pady=(0, 25))
        
        category_label = tk.Label(category_frame, 
                                 text="Categoria *",
                                 font=('Segoe UI', 10, 'bold'),
                                 bg=colors.get('bg_primary', '#0D1117'),
                                 fg=colors.get('text_primary', '#F0F6FC'))
        category_label.pack(anchor='w', pady=(0, 5))
        
        # ComboBox para categoria
        style = ttk.Style()
        style.configure('Modern.TCombobox',
                       fieldbackground=colors.get('bg_tertiary', '#21262D'),
                       background=colors.get('bg_tertiary', '#21262D'),
                       foreground=colors.get('text_primary', '#F0F6FC'),
                       arrowcolor=colors.get('text_primary', '#F0F6FC'),
                       borderwidth=0,
                       lightcolor=colors.get('border_color', '#30363D'),
                       darkcolor=colors.get('border_color', '#30363D'))
        
        categories = ["Pizzaria", "Hamburgeria", "Japonesa", "Italiana", "Brasileira", 
                     "Mexicana", "Chinesa", "Fast Food", "Vegetariana", "Churrascaria", "Outros"]
        
        self.category_combo = ttk.Combobox(category_frame,
                                          values=categories,
                                          font=('Segoe UI', 11),
                                          style='Modern.TCombobox',
                                          state="normal")
        self.category_combo.pack(fill=tk.X, ipady=4)
        self.category_combo.set(category)
        
        # Frame dos botões
        buttons_frame = tk.Frame(main_frame, bg=colors.get('bg_primary', '#0D1117'))
        buttons_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Botão Cancelar
        cancel_btn = tk.Button(buttons_frame,
                              text="Cancelar",
                              font=('Segoe UI', 10, 'bold'),
                              bg=colors.get('bg_accent', '#30363D'),
                              fg=colors.get('text_primary', '#F0F6FC'),
                              activebackground=colors.get('border_color', '#30363D'),
                              activeforeground=colors.get('text_primary', '#F0F6FC'),
                              relief='flat',
                              bd=0,
                              padx=25,
                              pady=10,
                              cursor='hand2',
                              command=self.cancel)
        cancel_btn.pack(side=tk.RIGHT, padx=(10, 0))
        
        # Botão Salvar
        save_btn = tk.Button(buttons_frame,
                            text="Salvar",
                            font=('Segoe UI', 10, 'bold'),
                            bg=colors.get('accent_blue', '#58A6FF'),
                            fg='white',
                            activebackground='#4A90E2',
                            activeforeground='white',
                            relief='flat',
                            bd=0,
                            padx=25,
                            pady=10,
                            cursor='hand2',
                            command=self.save)
        save_btn.pack(side=tk.RIGHT)
        
        # Bindings
        self.dialog.bind('<Return>', lambda e: self.save())
        self.dialog.bind('<Escape>', lambda e: self.cancel())

    def save(self):
        """Salva as informações"""
        name = self.name_entry.get().strip()
        category = self.category_combo.get().strip()
        
        if not name or not category:
            messagebox.showwarning("Aviso", "Nome e categoria são obrigatórios!")
            return
        
        self.result = (name, category)
        self.dialog.destroy()

    def cancel(self):
        """Cancela o diálogo"""
        self.dialog.destroy()

class RatingDialog:
    """Diálogo para avaliação de restaurante"""
    
    def __init__(self, parent, restaurant_name, theme_manager=None):
        self.result = None
        self.theme = theme_manager
        
        # Criar janela modal
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Avaliar Restaurante")
        self.dialog.geometry("400x250")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Centralizar janela
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (250 // 2)
        self.dialog.geometry(f"400x250+{x}+{y}")
        
        self.apply_theme()
        self.create_widgets(restaurant_name)

    def apply_theme(self):
        """Aplica o tema atual ao diálogo"""
        if self.theme:
            colors = self.theme.get_current_colors()
            self.dialog.configure(bg=colors['bg_primary'])

    def create_widgets(self, restaurant_name):
        """Cria os widgets do diálogo de avaliação"""
        colors = self.theme.get_current_colors() if self.theme else {}
        
        # Frame principal
        main_frame = tk.Frame(self.dialog, bg=colors.get('bg_primary', '#0D1117'), padx=30, pady=25)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_label = tk.Label(main_frame, 
                              text=f"⭐ Avaliar {restaurant_name}",
                              font=('Segoe UI', 14, 'bold'),
                              bg=colors.get('bg_primary', '#0D1117'),
                              fg=colors.get('text_primary', '#F0F6FC'))
        title_label.pack(pady=(0, 20))
        
        # Campo de avaliação
        rating_frame = tk.Frame(main_frame, bg=colors.get('bg_primary', '#0D1117'))
        rating_frame.pack(fill=tk.X, pady=(0, 20))
        
        rating_label = tk.Label(rating_frame, 
                               text="Avaliação (0.0 a 5.0):",
                               font=('Segoe UI', 10, 'bold'),
                               bg=colors.get('bg_primary', '#0D1117'),
                               fg=colors.get('text_primary', '#F0F6FC'))
        rating_label.pack(anchor='w', pady=(0, 5))
        
        # Scale para avaliação
        self.rating_var = tk.DoubleVar(value=5.0)
        self.rating_scale = tk.Scale(rating_frame,
                                    from_=0.0, to=5.0,
                                    resolution=0.1,
                                    orient=tk.HORIZONTAL,
                                    variable=self.rating_var,
                                    bg=colors.get('bg_primary', '#0D1117'),
                                    fg=colors.get('text_primary', '#F0F6FC'),
                                    activebackground=colors.get('accent_blue', '#58A6FF'),
                                    highlightthickness=0,
                                    troughcolor=colors.get('bg_tertiary', '#21262D'),
                                    font=('Segoe UI', 10))
        self.rating_scale.pack(fill=tk.X, pady=(0, 10))
        
        # Label de valor atual
        self.value_label = tk.Label(rating_frame,
                                   text="5.0 ⭐",
                                   font=('Segoe UI', 12, 'bold'),
                                   bg=colors.get('bg_primary', '#0D1117'),
                                   fg=colors.get('accent_orange', '#FF8C42'))
        self.value_label.pack()
        
        # Atualizar label quando scale muda
        self.rating_scale.configure(command=self.update_rating_label)
        
        # Frame dos botões
        buttons_frame = tk.Frame(main_frame, bg=colors.get('bg_primary', '#0D1117'))
        buttons_frame.pack(fill=tk.X, pady=(15, 0))
        
        # Botão Cancelar
        cancel_btn = tk.Button(buttons_frame,
                              text="Cancelar",
                              font=('Segoe UI', 10, 'bold'),
                              bg=colors.get('bg_accent', '#30363D'),
                              fg=colors.get('text_primary', '#F0F6FC'),
                              activebackground=colors.get('border_color', '#30363D'),
                              activeforeground=colors.get('text_primary', '#F0F6FC'),
                              relief='flat',
                              bd=0,
                              padx=25,
                              pady=8,
                              cursor='hand2',
                              command=self.cancel)
        cancel_btn.pack(side=tk.RIGHT, padx=(10, 0))
        
        # Botão Avaliar
        rate_btn = tk.Button(buttons_frame,
                            text="Avaliar",
                            font=('Segoe UI', 10, 'bold'),
                            bg=colors.get('accent_orange', '#FF8C42'),
                            fg='white',
                            activebackground='#E5782A',
                            activeforeground='white',
                            relief='flat',
                            bd=0,
                            padx=25,
                            pady=8,
                            cursor='hand2',
                            command=self.rate)
        rate_btn.pack(side=tk.RIGHT)

    def update_rating_label(self, value):
        """Atualiza o label com o valor da avaliação"""
        rating = float(value)
        stars = "⭐" * int(rating + 0.5)
        self.value_label.configure(text=f"{rating:.1f} {stars}")

    def rate(self):
        """Confirma a avaliação"""
        self.result = self.rating_var.get()
        self.dialog.destroy()

    def cancel(self):
        """Cancela a avaliação"""
        self.dialog.destroy()

class RestaurantGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🍽️ Sabor Express - Gerenciamento de Restaurantes")
        self.root.geometry("1200x800")
        self.root.minsize(800, 600)
        
        # Configurar ícone da janela (se disponível)
        try:
            self.root.iconbitmap('icon.ico')
        except:
            pass
        
        # Tema
        self.theme_manager = ModernTheme()
        self.is_dark_mode = True
        
        # Manager
        self.manager = RestaurantManager()
        
        # Variáveis de controle
        self.filter_category = tk.StringVar(value="Todas")
        self.filter_status = tk.StringVar(value="Todos")
        self.filter_favorite = tk.StringVar(value="Todos")
        self.search_var = tk.StringVar()
        
        # Aplicar tema e criar interface
        self.apply_theme()
        self.create_widgets()
        self.refresh_restaurant_list()
        
        # Bindings
        self.search_var.trace('w', self.on_search_change)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def get_current_colors(self):
        """Retorna as cores do tema atual"""
        return self.theme_manager.themes['dark' if self.is_dark_mode else 'light']

    def apply_theme(self):
        """Aplica o tema atual"""
        colors = self.get_current_colors()
        self.root.configure(bg=colors['bg_primary'])

    def toggle_theme(self):
        """Alterna entre modo escuro e claro"""
        self.is_dark_mode = not self.is_dark_mode
        
        # Recriar interface com novo tema
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.apply_theme()
        self.create_widgets()
        self.refresh_restaurant_list()

    def create_widgets(self):
        """Cria a interface principal"""
        colors = self.get_current_colors()
        
        # Frame principal
        main_frame = tk.Frame(self.root, bg=colors['bg_primary'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Header
        self.create_header(main_frame, colors)
        
        # Controles
        self.create_controls(main_frame, colors)
        
        # Lista de restaurantes
        self.create_restaurant_list(main_frame, colors)
        
        # Status bar
        self.create_status_bar(main_frame, colors)

    def create_header(self, parent, colors):
        """Cria o cabeçalho da aplicação"""
        header_frame = tk.Frame(parent, bg=colors['bg_primary'])
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Título principal
        title_label = tk.Label(header_frame, 
                              text="🍽️ Sabor Express",
                              font=('Segoe UI', 24, 'bold'),
                              bg=colors['bg_primary'],
                              fg=colors['text_primary'])
        title_label.pack(side=tk.LEFT)
        
        # Subtitle
        subtitle_label = tk.Label(header_frame, 
                                 text="Sistema de Gerenciamento de Restaurantes",
                                 font=('Segoe UI', 12),
                                 bg=colors['bg_primary'],
                                 fg=colors['text_secondary'])
        subtitle_label.pack(side=tk.LEFT, padx=(10, 0), pady=(5, 0))
        
        # Botão de tema
        theme_icon = "🌙" if self.is_dark_mode else "☀️"
        theme_text = "Modo Claro" if self.is_dark_mode else "Modo Escuro"
        
        theme_btn = tk.Button(header_frame,
                             text=f"{theme_icon} {theme_text}",
                             font=('Segoe UI', 10, 'bold'),
                             bg=colors['bg_accent'],
                             fg=colors['text_primary'],
                             activebackground=colors['border_color'],
                             activeforeground=colors['text_primary'],
                             relief='flat',
                             bd=0,
                             padx=15,
                             pady=8,
                             cursor='hand2',
                             command=self.toggle_theme)
        theme_btn.pack(side=tk.RIGHT)

    def create_controls(self, parent, colors):
        """Cria os controles da aplicação"""
        controls_frame = tk.LabelFrame(parent,
                                      text=" 🔧 Controles ",
                                      font=('Segoe UI', 12, 'bold'),
                                      bg=colors['bg_secondary'],
                                      fg=colors['text_primary'],
                                      relief='flat',
                                      bd=1,
                                      highlightbackground=colors['border_color'])
        controls_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Frame interno com padding
        inner_frame = tk.Frame(controls_frame, bg=colors['bg_secondary'])
        inner_frame.pack(fill=tk.BOTH, padx=15, pady=15)
        
        # Botões de ação
        self.create_action_buttons(inner_frame, colors)
        
        # Filtros
        self.create_filters(inner_frame, colors)

    def create_action_buttons(self, parent, colors):
        """Cria os botões de ação"""
        buttons_frame = tk.Frame(parent, bg=colors['bg_secondary'])
        buttons_frame.pack(fill=tk.X, pady=(0, 15))
        
        buttons_config = [
            ("➕ Adicionar", self.add_restaurant, colors['accent_blue'], 'white'),
            ("✏️ Editar", self.edit_restaurant, colors['accent_orange'], 'white'),
            ("🔄 Status", self.toggle_restaurant, colors['accent_purple'], 'white'),
            ("⭐ Favorito", self.toggle_favorite, '#FFD700', colors['text_primary']),
            ("📊 Avaliar", self.rate_restaurant, colors['accent_green'], 'white'),
            ("📈 Estatísticas", self.show_statistics, colors['accent_green'], 'white'),
            ("🗑️ Excluir", self.delete_restaurant, colors['accent_red'], 'white'),
            ("🔄 Atualizar", self.refresh_restaurant_list, colors['bg_accent'], colors['text_primary'])
        ]
        
        for i, (text, command, bg_color, fg_color) in enumerate(buttons_config):
            btn = tk.Button(buttons_frame,
                           text=text,
                           font=('Segoe UI', 9, 'bold'),
                           bg=bg_color,
                           fg=fg_color,
                           activebackground=self.adjust_color(bg_color, -20),
                           activeforeground=fg_color,
                           relief='flat',
                           bd=0,
                           padx=12,
                           pady=6,
                           cursor='hand2',
                           command=command)
            btn.pack(side=tk.LEFT, padx=(0, 8))

    def create_filters(self, parent, colors):
        """Cria os filtros"""
        filters_frame = tk.Frame(parent, bg=colors['bg_secondary'])
        filters_frame.pack(fill=tk.X)
        
        # Filtro por categoria
        category_frame = tk.Frame(filters_frame, bg=colors['bg_secondary'])
        category_frame.pack(side=tk.LEFT, padx=(0, 20))
        
        tk.Label(category_frame, 
                text="Categoria:",
                font=('Segoe UI', 9, 'bold'),
                bg=colors['bg_secondary'],
                fg=colors['text_primary']).pack(anchor='w')
        
        self.category_combo = ttk.Combobox(category_frame,
                                          textvariable=self.filter_category,
                                          values=["Todas"],
                                          state="readonly",
                                          width=12,
                                          font=('Segoe UI', 9))
        self.category_combo.pack(pady=(2, 0))
        self.category_combo.bind('<<ComboboxSelected>>', self.on_filter_change)
        
        # Filtro por status
        status_frame = tk.Frame(filters_frame, bg=colors['bg_secondary'])
        status_frame.pack(side=tk.LEFT, padx=(0, 20))
        
        tk.Label(status_frame,
                text="Status:",
                font=('Segoe UI', 9, 'bold'),
                bg=colors['bg_secondary'],
                fg=colors['text_primary']).pack(anchor='w')
        
        status_combo = ttk.Combobox(status_frame,
                                   textvariable=self.filter_status,
                                   values=["Todos", "Ativos", "Inativos"],
                                   state="readonly",
                                   width=12,
                                   font=('Segoe UI', 9))
        status_combo.pack(pady=(2, 0))
        status_combo.bind('<<ComboboxSelected>>', self.on_filter_change)
        
        # Filtro por favoritos
        favorite_frame = tk.Frame(filters_frame, bg=colors['bg_secondary'])
        favorite_frame.pack(side=tk.LEFT, padx=(0, 20))
        
        tk.Label(favorite_frame,
                text="Favoritos:",
                font=('Segoe UI', 9, 'bold'),
                bg=colors['bg_secondary'],
                fg=colors['text_primary']).pack(anchor='w')
        
        favorite_combo = ttk.Combobox(favorite_frame,
                                     textvariable=self.filter_favorite,
                                     values=["Todos", "Favoritos", "Não Favoritos"],
                                     state="readonly",
                                     width=12,
                                     font=('Segoe UI', 9))
        favorite_combo.pack(pady=(2, 0))
        favorite_combo.bind('<<ComboboxSelected>>', self.on_filter_change)
        
        # Campo de busca
        search_frame = tk.Frame(filters_frame, bg=colors['bg_secondary'])
        search_frame.pack(side=tk.LEFT)
        
        tk.Label(search_frame,
                text="Buscar:",
                font=('Segoe UI', 9, 'bold'),
                bg=colors['bg_secondary'],
                fg=colors['text_primary']).pack(anchor='w')
        
        search_entry = tk.Entry(search_frame,
                               textvariable=self.search_var,
                               font=('Segoe UI', 9),
                               bg=colors['bg_tertiary'],
                               fg=colors['text_primary'],
                               insertbackground=colors['text_primary'],
                               relief='flat',
                               bd=1,
                               highlightthickness=1,
                               highlightcolor=colors['accent_blue'],
                               highlightbackground=colors['border_color'],
                               width=20)
        search_entry.pack(pady=(2, 0), ipady=2)

    def create_restaurant_list(self, parent, colors):
        """Cria a lista de restaurantes"""
        list_frame = tk.LabelFrame(parent,
                                  text=" 📋 Lista de Restaurantes ",
                                  font=('Segoe UI', 12, 'bold'),
                                  bg=colors['bg_secondary'],
                                  fg=colors['text_primary'],
                                  relief='flat',
                                  bd=1,
                                  highlightbackground=colors['border_color'])
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # Frame interno
        inner_frame = tk.Frame(list_frame, bg=colors['bg_secondary'])
        inner_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Configurar estilo do Treeview
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configurar cores
        style.configure('Modern.Treeview',
                       background=colors['bg_tertiary'],
                       foreground=colors['text_primary'],
                       fieldbackground=colors['bg_tertiary'],
                       borderwidth=0,
                       relief='flat',
                       rowheight=30)
        
        style.configure('Modern.Treeview.Heading',
                       background=colors['bg_primary'],
                       foreground=colors['text_primary'],
                       borderwidth=1,
                       relief='flat',
                       font=('Segoe UI', 10, 'bold'))
        
        style.map('Modern.Treeview',
                 background=[('selected', colors['accent_blue'])],
                 foreground=[('selected', 'white')])
        
        # Treeview
        columns = ('ID', 'Nome', 'Categoria', 'Status', 'Favorito', 'Avaliacao', 'Acoes')
        self.tree = ttk.Treeview(inner_frame,
                                columns=columns,
                                show='headings',
                                style='Modern.Treeview')
        
        # Configurar colunas
        column_config = {
            'ID': {'width': 50, 'anchor': 'center'},
            'Nome': {'width': 200, 'anchor': 'w'},
            'Categoria': {'width': 120, 'anchor': 'center'},
            'Status': {'width': 80, 'anchor': 'center'},
            'Favorito': {'width': 80, 'anchor': 'center'},
            'Avaliacao': {'width': 120, 'anchor': 'center'},
            'Acoes': {'width': 100, 'anchor': 'center'}
        }
        
        for col, config in column_config.items():
            self.tree.heading(col, text=col.replace('_', ' ').title())
            self.tree.column(col, width=config['width'], anchor=config['anchor'])
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(inner_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Eventos
        self.tree.bind('<Double-1>', self.on_double_click)
        self.tree.bind('<Button-3>', self.show_context_menu)

    def create_status_bar(self, parent, colors):
        """Cria a barra de status"""
        self.status_var = tk.StringVar(value="Sistema iniciado - Pronto para uso!")
        
        status_frame = tk.Frame(parent, bg=colors['bg_secondary'], relief='flat', bd=1)
        status_frame.pack(fill=tk.X)
        
        status_label = tk.Label(status_frame,
                               textvariable=self.status_var,
                               font=('Segoe UI', 9),
                               bg=colors['bg_secondary'],
                               fg=colors['text_secondary'],
                               anchor='w',
                               padx=10,
                               pady=5)
        status_label.pack(fill=tk.X)

    def refresh_restaurant_list(self):
        """Atualiza a lista de restaurantes"""
        try:
            # Limpar lista atual
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Obter restaurantes filtrados
            restaurants = self.get_filtered_restaurants()
            
            # Adicionar à lista
            for restaurant in restaurants:
                # Status
                status = "✅ Ativo" if restaurant['ativo'] else "❌ Inativo"
                
                # Favorito
                favorito = "⭐" if restaurant.get('favorito', False) else "☆"
                
                # Avaliação
                avaliacao = restaurant.get('avaliacao', 0.0)
                num_avaliacoes = restaurant.get('num_avaliacoes', 0)
                if num_avaliacoes > 0:
                    avaliacao_str = f"⭐ {avaliacao:.1f} ({num_avaliacoes})"
                else:
                    avaliacao_str = "Sem avaliação"
                
                self.tree.insert('', tk.END, values=(
                    restaurant['id'],
                    restaurant['nome'],
                    restaurant['categoria'],
                    status,
                    favorito,
                    avaliacao_str,
                    "Ações"
                ))
            
            # Atualizar combobox de categorias
            categories = ["Todas"] + self.manager.get_categories()
            self.category_combo['values'] = categories
            
            # Atualizar status
            total = len(restaurants)
            self.status_var.set(f"Exibindo {total} restaurante{'s' if total != 1 else ''}")
            
        except Exception as e:
            self.status_var.set(f"Erro ao atualizar lista: {str(e)}")

    def get_filtered_restaurants(self):
        """Retorna lista filtrada de restaurantes"""
        restaurants = self.manager.get_all_restaurants()
        
        # Filtro por categoria
        if self.filter_category.get() != "Todas":
            restaurants = [r for r in restaurants if r['categoria'] == self.filter_category.get()]
        
        # Filtro por status
        if self.filter_status.get() == "Ativos":
            restaurants = [r for r in restaurants if r['ativo']]
        elif self.filter_status.get() == "Inativos":
            restaurants = [r for r in restaurants if not r['ativo']]
        
        # Filtro por favoritos
        if self.filter_favorite.get() == "Favoritos":
            restaurants = [r for r in restaurants if r.get('favorito', False)]
        elif self.filter_favorite.get() == "Não Favoritos":
            restaurants = [r for r in restaurants if not r.get('favorito', False)]
        
        # Filtro por busca
        search_term = self.search_var.get().strip()
        if search_term:
            restaurants = [r for r in restaurants if 
                          search_term.lower() in r['nome'].lower() or 
                          search_term.lower() in r['categoria'].lower()]
        
        return restaurants

    def get_selected_restaurant_id(self):
        """Retorna o ID do restaurante selecionado"""
        selection = self.tree.selection()
        if not selection:
            return None
        item = self.tree.item(selection[0])
        return int(item['values'][0])

    def add_restaurant(self):
        """Adiciona um novo restaurante"""
        dialog = RestaurantDialog(self.root, "Adicionar Restaurante", theme_manager=self)
        if dialog.result:
            name, category = dialog.result
            if self.manager.add_restaurant(name, category):
                messagebox.showinfo("Sucesso", f"Restaurante '{name}' adicionado com sucesso!")
                self.refresh_restaurant_list()
                self.status_var.set(f"Restaurante '{name}' adicionado")
            else:
                messagebox.showerror("Erro", "Já existe um restaurante com este nome!")

    def edit_restaurant(self):
        """Edita o restaurante selecionado"""
        restaurant_id = self.get_selected_restaurant_id()
        if not restaurant_id:
            messagebox.showwarning("Aviso", "Selecione um restaurante para editar!")
            return
        
        restaurant = self.manager.get_restaurant_by_id(restaurant_id)
        if not restaurant:
            messagebox.showerror("Erro", "Restaurante não encontrado!")
            return
        
        dialog = RestaurantDialog(self.root, "Editar Restaurante", 
                                 restaurant['nome'], restaurant['categoria'],
                                 theme_manager=self)
        if dialog.result:
            name, category = dialog.result
            if self.manager.update_restaurant(restaurant_id, name, category):
                messagebox.showinfo("Sucesso", f"Restaurante '{name}' atualizado com sucesso!")
                self.refresh_restaurant_list()
                self.status_var.set(f"Restaurante '{name}' atualizado")
            else:
                messagebox.showerror("Erro", "Erro ao atualizar restaurante ou nome já existe!")

    def toggle_restaurant(self):
        """Alterna o status do restaurante"""
        restaurant_id = self.get_selected_restaurant_id()
        if not restaurant_id:
            messagebox.showwarning("Aviso", "Selecione um restaurante para alterar o status!")
            return
        
        restaurant = self.manager.toggle_restaurant_status(restaurant_id)
        if restaurant:
            status = "ativado" if restaurant['ativo'] else "desativado"
            messagebox.showinfo("Sucesso", f"Restaurante '{restaurant['nome']}' {status}!")
            self.refresh_restaurant_list()
            self.status_var.set(f"Status do restaurante '{restaurant['nome']}' alterado")

    def toggle_favorite(self):
        """Alterna o status de favorito"""
        restaurant_id = self.get_selected_restaurant_id()
        if not restaurant_id:
            messagebox.showwarning("Aviso", "Selecione um restaurante para marcar como favorito!")
            return
        
        restaurant = self.manager.toggle_favorite(restaurant_id)
        if restaurant:
            status = "adicionado aos favoritos" if restaurant.get('favorito', False) else "removido dos favoritos"
            messagebox.showinfo("Sucesso", f"Restaurante '{restaurant['nome']}' {status}!")
            self.refresh_restaurant_list()
            self.status_var.set(f"Favorito alterado para '{restaurant['nome']}'")

    def rate_restaurant(self):
        """Avalia o restaurante selecionado"""
        restaurant_id = self.get_selected_restaurant_id()
        if not restaurant_id:
            messagebox.showwarning("Aviso", "Selecione um restaurante para avaliar!")
            return
        
        restaurant = self.manager.get_restaurant_by_id(restaurant_id)
        if not restaurant:
            messagebox.showerror("Erro", "Restaurante não encontrado!")
            return
        
        dialog = RatingDialog(self.root, restaurant['nome'], theme_manager=self)
        if dialog.result:
            rating = dialog.result
            if self.manager.add_rating(restaurant_id, rating):
                messagebox.showinfo("Sucesso", f"Avaliação {rating:.1f}⭐ adicionada para '{restaurant['nome']}'!")
                self.refresh_restaurant_list()
                self.status_var.set(f"Avaliação adicionada para '{restaurant['nome']}'")
            else:
                messagebox.showerror("Erro", "Erro ao adicionar avaliação!")

    def delete_restaurant(self):
        """Exclui o restaurante selecionado"""
        restaurant_id = self.get_selected_restaurant_id()
        if not restaurant_id:
            messagebox.showwarning("Aviso", "Selecione um restaurante para excluir!")
            return
        
        restaurant = self.manager.get_restaurant_by_id(restaurant_id)
        if not restaurant:
            messagebox.showerror("Erro", "Restaurante não encontrado!")
            return
        
        if messagebox.askyesno("Confirmar Exclusão", 
                              f"Tem certeza que deseja excluir o restaurante '{restaurant['nome']}'?\n\n"
                              f"Esta ação não pode ser desfeita!"):
            if self.manager.delete_restaurant(restaurant_id):
                messagebox.showinfo("Sucesso", f"Restaurante '{restaurant['nome']}' excluído com sucesso!")
                self.refresh_restaurant_list()
                self.status_var.set(f"Restaurante '{restaurant['nome']}' excluído")
            else:
                messagebox.showerror("Erro", "Erro ao excluir restaurante!")

    def show_statistics(self):
        """Exibe estatísticas do sistema"""
        stats = self.manager.get_statistics()
        colors = self.get_current_colors()
        
        # Janela de estatísticas
        stats_window = tk.Toplevel(self.root)
        stats_window.title("📊 Estatísticas do Sistema")
        stats_window.geometry("600x500")
        stats_window.configure(bg=colors['bg_primary'])
        stats_window.transient(self.root)
        stats_window.grab_set()
        
        # Centralizar
        stats_window.update_idletasks()
        x = (stats_window.winfo_screenwidth() // 2) - (600 // 2)
        y = (stats_window.winfo_screenheight() // 2) - (500 // 2)
        stats_window.geometry(f"600x500+{x}+{y}")
        
        # Frame principal
        main_frame = tk.Frame(stats_window, bg=colors['bg_primary'], padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_label = tk.Label(main_frame, 
                              text="📊 Estatísticas do Sistema",
                              font=('Segoe UI', 18, 'bold'),
                              bg=colors['bg_primary'],
                              fg=colors['text_primary'])
        title_label.pack(pady=(0, 20))
        
        # Estatísticas gerais
        general_frame = tk.LabelFrame(main_frame,
                                     text="Resumo Geral",
                                     font=('Segoe UI', 12, 'bold'),
                                     bg=colors['bg_secondary'],
                                     fg=colors['text_primary'],
                                     relief='flat',
                                     bd=1)
        general_frame.pack(fill=tk.X, pady=(0, 15))
        
        general_inner = tk.Frame(general_frame, bg=colors['bg_secondary'])
        general_inner.pack(fill=tk.X, padx=15, pady=15)
        
        stats_text = [
            f"📈 Total de restaurantes: {stats['total']}",
            f"✅ Restaurantes ativos: {stats['ativos']}",
            f"❌ Restaurantes inativos: {stats['inativos']}",
            f"⭐ Restaurantes favoritos: {stats.get('favoritos', 0)}"
        ]
        
        for text in stats_text:
            label = tk.Label(general_inner,
                            text=text,
                            font=('Segoe UI', 11),
                            bg=colors['bg_secondary'],
                            fg=colors['text_primary'])
            label.pack(anchor='w', pady=2)
        
        # Categorias
        if stats['categorias']:
            categories_frame = tk.LabelFrame(main_frame,
                                           text="Distribuição por Categoria",
                                           font=('Segoe UI', 12, 'bold'),
                                           bg=colors['bg_secondary'],
                                           fg=colors['text_primary'],
                                           relief='flat',
                                           bd=1)
            categories_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
            
            categories_inner = tk.Frame(categories_frame, bg=colors['bg_secondary'])
            categories_inner.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
            
            for categoria, count in stats['categorias'].items():
                percentage = (count / stats['total'] * 100) if stats['total'] > 0 else 0
                text = f"• {categoria}: {count} ({percentage:.1f}%)"
                label = tk.Label(categories_inner,
                               text=text,
                               font=('Segoe UI', 10),
                               bg=colors['bg_secondary'],
                               fg=colors['text_secondary'])
                label.pack(anchor='w', pady=1)
        
        # Botão fechar
        close_btn = tk.Button(main_frame,
                             text="Fechar",
                             font=('Segoe UI', 11, 'bold'),
                             bg=colors['accent_blue'],
                             fg='white',
                             activebackground='#4A90E2',
                             activeforeground='white',
                             relief='flat',
                             bd=0,
                             padx=30,
                             pady=10,
                             cursor='hand2',
                             command=stats_window.destroy)
        close_btn.pack(pady=(15, 0))

    def show_context_menu(self, event):
        """Exibe menu de contexto"""
        # Para implementação futura
        pass

    def on_filter_change(self, event=None):
        """Callback para mudança nos filtros"""
        self.refresh_restaurant_list()

    def on_search_change(self, *args):
        """Callback para mudança na busca"""
        self.refresh_restaurant_list()

    def on_double_click(self, event):
        """Callback para duplo clique"""
        self.edit_restaurant()

    def on_closing(self):
        """Callback para fechamento da aplicação"""
        if messagebox.askokcancel("Sair", "Deseja realmente sair do sistema?"):
            self.root.destroy()

    def adjust_color(self, color, adjustment):
        """Ajusta a cor para criar efeito hover"""
        # Simplificado - retorna a mesma cor
        return color

def main():
    """Função principal"""
    root = tk.Tk()
    app = RestaurantGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
