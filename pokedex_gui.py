import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import requests
from threading import Thread


class PokedexGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Pokédex - Interfaz Gráfica")
        self.root.geometry("750x720")
        self.root.resizable(False, False)
        
        self.root.overrideredirect(True)
        
        self.offset_x = 0
        self.offset_y = 0
        
        self.pokedex = []
        
        self.colores = {
            'rojo': '#DC0A2D',
            'rojo_oscuro': '#A80A24',
            'blanco': '#FFFFFF',
            'negro': '#000000',
            'azul_pantalla': '#88CCF1',
            'gris_oscuro': '#3A3A3A',
            'verde': '#48D0B0',
            'amarillo': '#FFCB05'
        }
        
        self.pokemon_cache = {}
        self.luz_grande_canvas = None
        self.luces_pequeñas_canvas = []
        self.animacion_activa = False
        self.panel_buscar_expandido = False
        self.panel_agregar_expandido = False
        self.panel_buscar_animando = False
        self.panel_agregar_animando = False
        
        self.configurar_estilo()
        self.crear_interfaz()
    
    def configurar_estilo(self):
        self.root.configure(bg=self.colores['rojo'])
        
        try:
            if self.root.tk.call('tk', 'windowingsystem') == 'x11':
                self.root.attributes('-type', 'dialog')
        except:
            pass
    
    def hacer_ventana_arrastrable(self, widget):
        widget.bind('<Button-1>', self.iniciar_arrastre)
        widget.bind('<B1-Motion>', self.arrastrar_ventana)
    
    def iniciar_arrastre(self, event):
        self.offset_x = event.x
        self.offset_y = event.y
    
    def arrastrar_ventana(self, event):
        x = self.root.winfo_x() + event.x - self.offset_x
        y = self.root.winfo_y() + event.y - self.offset_y
        self.root.geometry(f'+{x}+{y}')
    
    def crear_interfaz(self):
        contenedor_principal = tk.Frame(self.root, bg=self.colores['rojo'], 
                                       relief="raised", bd=3,
                                       highlightbackground=self.colores['negro'],
                                       highlightthickness=2)
        contenedor_principal.pack(fill="both", expand=True, padx=2, pady=2)
        
        header_frame = tk.Frame(contenedor_principal, bg=self.colores['rojo'], height=80)
        header_frame.pack(fill="x", padx=15, pady=(15, 0))
        header_frame.pack_propagate(False)
        
        self.hacer_ventana_arrastrable(header_frame)
        
        top_section = tk.Frame(header_frame, bg=self.colores['rojo'])
        top_section.pack(fill="both", expand=True)
        self.hacer_ventana_arrastrable(top_section)
        
        luces_frame = tk.Frame(top_section, bg=self.colores['rojo'])
        luces_frame.pack(side="left", padx=10, pady=10)
        
        self.luz_grande_canvas = tk.Canvas(luces_frame, width=50, height=50, 
                              bg=self.colores['rojo'], highlightthickness=0)
        self.luz_grande_canvas.pack(side="left")
        self.luz_grande_canvas.create_oval(5, 5, 45, 45, fill=self.colores['azul_pantalla'], 
                              outline=self.colores['blanco'], width=3, tags="luz_grande")
        self.luz_grande_canvas.create_oval(12, 10, 22, 20, fill=self.colores['blanco'], 
                              outline="", tags="brillo")
        
        luces_pequeñas = tk.Frame(luces_frame, bg=self.colores['rojo'])
        luces_pequeñas.pack(side="left", padx=10)
        
        colores_luces = [self.colores['rojo_oscuro'], self.colores['amarillo'], self.colores['verde']]
        for i, color in enumerate(colores_luces):
            luz = tk.Canvas(luces_pequeñas, width=16, height=16, 
                           bg=self.colores['rojo'], highlightthickness=0)
            luz.pack(side="left", padx=2)
            luz.create_oval(2, 2, 14, 14, fill=color, outline=self.colores['negro'], 
                           width=2, tags=f"luz_{i}")
            self.luces_pequeñas_canvas.append((luz, color))
        
        titulo = tk.Label(top_section, text="󰐝 POKÉDEX", 
                         font=("Arial", 18, "bold"),
                         bg=self.colores['rojo'],
                         fg=self.colores['blanco'])
        titulo.pack(side="right", padx=20)
        self.hacer_ventana_arrastrable(titulo)
        
        btn_cerrar = tk.Button(top_section, text="✕", 
                              command=self.detener_animaciones,
                              font=("Arial", 12, "bold"),
                              bg=self.colores['rojo_oscuro'],
                              fg=self.colores['blanco'],
                              relief="flat",
                              cursor="hand2",
                              padx=8,
                              pady=2,
                              bd=0)
        btn_cerrar.pack(side="right", padx=5)
        
        bisagra = tk.Frame(contenedor_principal, bg=self.colores['rojo_oscuro'], height=6)
        bisagra.pack(fill="x", padx=15)
        
        cuerpo_frame = tk.Frame(contenedor_principal, bg=self.colores['rojo'])
        cuerpo_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        pantalla_container = tk.Frame(cuerpo_frame, bg=self.colores['rojo'])
        pantalla_container.pack(fill="both", expand=True, padx=15, pady=15)
        
        self.crear_pantalla_principal(pantalla_container)
        
        # Panel de pestañas DEBAJO de la pantalla principal
        pestanas_frame = tk.Frame(cuerpo_frame, bg=self.colores['rojo'])
        pestanas_frame.pack(fill="x", padx=15, pady=(0, 10))
        
        self.crear_pestanas(pestanas_frame)
        
        controles_frame = tk.Frame(cuerpo_frame, bg=self.colores['rojo'])
        controles_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        self.crear_controles(controles_frame)
        
        self.iniciar_animacion_luces()
    
    def iniciar_animacion_luces(self):
        self.animacion_activa = True
        self.animar_luz_grande()
        self.animar_luces_pequeñas(0)
    
    def animar_luz_grande(self):
        if not self.animacion_activa or not self.luz_grande_canvas.winfo_exists():
            return
        
        current_color = self.luz_grande_canvas.itemcget("luz_grande", "fill")
        
        if current_color == self.colores['azul_pantalla']:
            new_color = '#A0D8F0'
        else:
            new_color = self.colores['azul_pantalla']
        
        self.luz_grande_canvas.itemconfig("luz_grande", fill=new_color)
        
        self.root.after(1000, self.animar_luz_grande)
    
    def animar_luces_pequeñas(self, indice):
        if not self.animacion_activa:
            return
        
        for i, (canvas, color_original) in enumerate(self.luces_pequeñas_canvas):
            if not canvas.winfo_exists():
                return
            
            if i == indice:
                canvas.itemconfig(f"luz_{i}", fill='#FFFFFF')
            else:
                canvas.itemconfig(f"luz_{i}", fill=color_original)
        
        siguiente = (indice + 1) % len(self.luces_pequeñas_canvas)
        self.root.after(500, lambda: self.animar_luces_pequeñas(siguiente))
    
    def crear_pantalla_principal(self, parent):
        pantalla_frame = tk.Frame(parent, bg=self.colores['blanco'], 
                                 relief="solid", bd=3,
                                 highlightbackground=self.colores['gris_oscuro'],
                                 highlightthickness=1)
        pantalla_frame.pack(fill="both", expand=True)
        
        pantalla_interior = tk.Frame(pantalla_frame, bg=self.colores['azul_pantalla'])
        pantalla_interior.pack(fill="both", expand=True, padx=3, pady=3)
        
        scroll_frame = tk.Frame(pantalla_interior, bg=self.colores['azul_pantalla'])
        scroll_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        scrollbar = tk.Scrollbar(scroll_frame, bg=self.colores['gris_oscuro'])
        scrollbar.pack(side="right", fill="y")
        
        self.lista_text = scrolledtext.ScrolledText(scroll_frame,
                                                    font=("Courier New", 10, "bold"),
                                                    bg=self.colores['azul_pantalla'],
                                                    fg=self.colores['negro'],
                                                    relief="flat",
                                                    bd=0,
                                                    yscrollcommand=scrollbar.set,
                                                    state="disabled",
                                                    wrap="word",
                                                    padx=10,
                                                    pady=10)
        self.lista_text.pack(fill="both", expand=True)
        scrollbar.config(command=self.lista_text.yview)
        
        self.actualizar_lista()
    
    def crear_pestanas(self, parent):
        # Contenedor para las dos pestañas lado a lado
        contenedor_pestanas = tk.Frame(parent, bg=self.colores['rojo'])
        contenedor_pestanas.pack(fill="x")
        
        # Pestaña BUSCAR (izquierda)
        self.crear_pestana_buscar(contenedor_pestanas)
        
        # Espacio entre pestañas
        tk.Frame(contenedor_pestanas, bg=self.colores['rojo'], width=10).pack(side="left")
        
        # Pestaña AGREGAR (derecha)
        self.crear_pestana_agregar(contenedor_pestanas)
    
    def crear_controles(self, parent):
        # Solo botones principales en una fila horizontal
        botones_frame = tk.Frame(parent, bg=self.colores['rojo'])
        botones_frame.pack(fill="x")
        
        btn_agregar = tk.Button(botones_frame,
                               text="󰐝 AGREGAR",
                               command=self.agregar_pokemon,
                               font=("Arial", 10, "bold"),
                               bg=self.colores['verde'],
                               fg=self.colores['negro'],
                               relief="raised",
                               cursor="hand2",
                               pady=10,
                               bd=3)
        btn_agregar.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        btn_eliminar = tk.Button(botones_frame,
                                text="✖ ELIMINAR",
                                command=self.eliminar_pokemon,
                                font=("Arial", 10, "bold"),
                                bg=self.colores['rojo_oscuro'],
                                fg=self.colores['blanco'],
                                relief="raised",
                                cursor="hand2",
                                pady=10,
                                bd=3)
        btn_eliminar.pack(side="left", fill="x", expand=True, padx=5)
        
        btn_actualizar = tk.Button(botones_frame,
                                  text="⟲ ACTUALIZAR",
                                  command=self.actualizar_lista,
                                  font=("Arial", 10, "bold"),
                                  bg=self.colores['azul_pantalla'],
                                  fg=self.colores['negro'],
                                  relief="raised",
                                  cursor="hand2",
                                  pady=10,
                                  bd=3)
        btn_actualizar.pack(side="left", fill="x", expand=True, padx=5)
        
        btn_limpiar = tk.Button(botones_frame,
                               text="⌫ LIMPIAR",
                               command=self.limpiar_campos,
                               font=("Arial", 10, "bold"),
                               bg=self.colores['gris_oscuro'],
                               fg=self.colores['blanco'],
                               relief="raised",
                               cursor="hand2",
                               pady=10,
                               bd=3)
        btn_limpiar.pack(side="left", fill="x", expand=True, padx=(5, 0))
        
        # Contador debajo de los botones
        contador_frame = tk.Frame(parent, bg=self.colores['negro'], 
                                 relief="sunken", bd=2,
                                 highlightbackground=self.colores['verde'],
                                 highlightthickness=1)
        contador_frame.pack(fill="x", pady=(10, 0))
        
        self.label_contador = tk.Label(contador_frame,
                                       text="TOTAL: 0 POKÉMON",
                                       font=("Arial", 10, "bold"),
                                       bg=self.colores['negro'],
                                       fg=self.colores['verde'],
                                       pady=8)
        self.label_contador.pack(expand=True)
    
    def crear_pestana_buscar(self, parent):
        # Contenedor de la pestaña (mitad del ancho)
        self.pestana_container_buscar = tk.Frame(parent, bg=self.colores['rojo'])
        self.pestana_container_buscar.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        # Botón clickeable directamente
        self.btn_tab_buscar = tk.Button(self.pestana_container_buscar,
                                   text="🔍 BUSCAR EN POKEAPI\n(Click para abrir)",
                                   command=lambda: self.toggle_panel_buscar(),
                                   font=("Arial", 12, "bold"),
                                   bg=self.colores['amarillo'],
                                   fg=self.colores['negro'],
                                   activebackground=self.colores['negro'],
                                   activeforeground=self.colores['amarillo'],
                                   relief="raised",
                                   cursor="hand2",
                                   bd=4,
                                   pady=15)
        self.btn_tab_buscar.pack(fill="x")
        
        # Panel expandible (oculto inicialmente)
        self.panel_buscar = tk.Frame(self.pestana_container_buscar, 
                                     bg=self.colores['gris_oscuro'],
                                     relief="raised", bd=3,
                                     highlightbackground=self.colores['amarillo'],
                                     highlightthickness=2)
        
        # Contenido del panel
        contenido_buscar = tk.Frame(self.panel_buscar, bg=self.colores['gris_oscuro'])
        contenido_buscar.pack(fill="both", expand=True, padx=10, pady=10)
        
        tk.Label(contenido_buscar,
                text="BUSCAR POKÉMON",
                font=("Arial", 9, "bold"),
                bg=self.colores['gris_oscuro'],
                fg=self.colores['amarillo']).pack(pady=(0, 8))
        
        tk.Label(contenido_buscar,
                text="Nombre o #:",
                font=("Arial", 8),
                bg=self.colores['gris_oscuro'],
                fg=self.colores['blanco']).pack(anchor="w")
        
        self.entrada_buscar = tk.Entry(contenido_buscar,
                                       font=("Arial", 9),
                                       bg=self.colores['blanco'],
                                       fg=self.colores['negro'],
                                       relief="sunken",
                                       bd=2,
                                       width=20)
        self.entrada_buscar.pack(fill="x", pady=(0, 8))
        self.entrada_buscar.bind('<Return>', lambda e: self.buscar_pokemon_api())
        
        btn_buscar_api = tk.Button(contenido_buscar,
                                   text="🔍 BUSCAR API",
                                   command=self.buscar_pokemon_api,
                                   font=("Arial", 9, "bold"),
                                   bg=self.colores['amarillo'],
                                   fg=self.colores['negro'],
                                   relief="raised",
                                   cursor="hand2",
                                   pady=6,
                                   bd=3)
        btn_buscar_api.pack(fill="x")
    
    def crear_pestana_agregar(self, parent):
        # Contenedor de la pestaña (mitad del ancho)
        self.pestana_container_agregar = tk.Frame(parent, bg=self.colores['rojo'])
        self.pestana_container_agregar.pack(side="left", fill="both", expand=True, padx=(5, 0))
        
        # Botón clickeable directamente
        self.btn_tab_agregar = tk.Button(self.pestana_container_agregar,
                                    text="📝 VER/EDITAR DATOS\n(Click para abrir)",
                                    command=lambda: self.toggle_panel_agregar(),
                                    font=("Arial", 12, "bold"),
                                    bg=self.colores['verde'],
                                    fg=self.colores['negro'],
                                    activebackground=self.colores['negro'],
                                    activeforeground=self.colores['verde'],
                                    relief="raised",
                                    cursor="hand2",
                                    bd=4,
                                    pady=15)
        self.btn_tab_agregar.pack(fill="x")
        
        # Panel expandible (oculto inicialmente)
        self.panel_agregar = tk.Frame(self.pestana_container_agregar,
                                      bg=self.colores['gris_oscuro'],
                                      relief="raised", bd=3,
                                      highlightbackground=self.colores['verde'],
                                      highlightthickness=2)
        
        # Contenido del panel
        contenido_agregar = tk.Frame(self.panel_agregar, bg=self.colores['gris_oscuro'])
        contenido_agregar.pack(fill="both", expand=True, padx=8, pady=8)
        
        tk.Label(contenido_agregar,
                text="DATOS POKÉMON",
                font=("Arial", 9, "bold"),
                bg=self.colores['gris_oscuro'],
                fg=self.colores['amarillo']).pack(pady=(0, 8))
        
        tk.Label(contenido_agregar,
                text="NOMBRE:",
                font=("Arial", 8, "bold"),
                bg=self.colores['gris_oscuro'],
                fg=self.colores['blanco']).pack(anchor="w")
        
        self.entrada_nombre = tk.Entry(contenido_agregar,
                                       font=("Arial", 9),
                                       bg=self.colores['blanco'],
                                       fg=self.colores['negro'],
                                       relief="sunken",
                                       bd=2,
                                       width=20)
        self.entrada_nombre.pack(fill="x", pady=(0, 6))
        
        tk.Label(contenido_agregar,
                text="TIPO:",
                font=("Arial", 8, "bold"),
                bg=self.colores['gris_oscuro'],
                fg=self.colores['blanco']).pack(anchor="w")
        
        self.entrada_tipo = tk.Entry(contenido_agregar,
                                     font=("Arial", 9),
                                     bg=self.colores['blanco'],
                                     fg=self.colores['negro'],
                                     relief="sunken",
                                     bd=2,
                                     width=20)
        self.entrada_tipo.pack(fill="x", pady=(0, 6))
        
        tk.Label(contenido_agregar,
                text="PS:",
                font=("Arial", 8, "bold"),
                bg=self.colores['gris_oscuro'],
                fg=self.colores['blanco']).pack(anchor="w")
        
        self.entrada_ps = tk.Entry(contenido_agregar,
                                   font=("Arial", 9),
                                   bg=self.colores['blanco'],
                                   fg=self.colores['negro'],
                                   relief="sunken",
                                   bd=2,
                                   width=20)
        self.entrada_ps.pack(fill="x")
    
    def toggle_panel_buscar(self):
        if self.panel_buscar_expandido:
            # Cerrar panel
            self.panel_buscar.pack_forget()
            self.panel_buscar_expandido = False
            self.btn_tab_buscar.config(text="🔍 BUSCAR EN POKEAPI\n(Click para abrir)")
        else:
            # Abrir panel con altura fija para que sea visible
            self.panel_buscar.pack(fill="both", pady=(10, 0))
            self.panel_buscar.config(height=120)  # Altura fija
            self.panel_buscar_expandido = True
            self.btn_tab_buscar.config(text="🔍 BUSCAR EN POKEAPI\n(Click para cerrar)")
            # Dar foco al campo de búsqueda
            self.entrada_buscar.focus()
    
    def toggle_panel_agregar(self):
        if self.panel_agregar_expandido:
            # Cerrar panel
            self.panel_agregar.pack_forget()
            self.panel_agregar_expandido = False
            self.btn_tab_agregar.config(text="📝 VER/EDITAR DATOS\n(Click para abrir)")
        else:
            # Abrir panel con altura fija para que sea visible
            self.panel_agregar.pack(fill="both", pady=(10, 0))
            self.panel_agregar.config(height=180)  # Altura fija (más alto porque tiene 3 campos)
            self.panel_agregar_expandido = True
            self.btn_tab_agregar.config(text="📝 VER/EDITAR DATOS\n(Click para cerrar)")
            # Dar foco al primer campo
            self.entrada_nombre.focus()
    
    def animar_panel(self, panel, size_inicial, size_final, callback, direccion='width'):
        pasos = 10
        diferencia = size_final - size_inicial
        incremento = diferencia / pasos
        
        def paso_animacion(paso_actual=0):
            if paso_actual <= pasos:
                nuevo_size = int(size_inicial + (incremento * paso_actual))
                if direccion == 'width':
                    panel.config(width=nuevo_size)
                else:
                    panel.config(height=nuevo_size)
                self.root.after(20, lambda: paso_animacion(paso_actual + 1))
            else:
                if size_final == 0:
                    panel.pack_forget()
                callback()
        
        paso_animacion()
    
    def finalizar_animacion_buscar(self, expandido):
        self.panel_buscar_expandido = expandido
        self.panel_buscar_animando = False
    
    def finalizar_animacion_agregar(self, expandido):
        self.panel_agregar_expandido = expandido
        self.panel_agregar_animando = False
    
    def buscar_pokemon_api(self):
        nombre_o_id = self.entrada_buscar.get().strip().lower()
        
        if not nombre_o_id:
            messagebox.showwarning("Campo Vacío", "Por favor ingresa el nombre o número del Pokémon")
            return
        
        if nombre_o_id in self.pokemon_cache:
            self.rellenar_datos(self.pokemon_cache[nombre_o_id])
            return
        
        loading_label = tk.Label(self.root, 
                                text="Buscando en PokeAPI...",
                                font=("Arial", 12, "bold"),
                                bg=self.colores['rojo'],
                                fg=self.colores['amarillo'])
        loading_label.place(relx=0.5, rely=0.5, anchor="center")
        self.root.update()
        
        def buscar():
            try:
                response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{nombre_o_id}", timeout=10)
                
                if response.status_code == 200:
                    pokemon_data = response.json()
                    
                    species_response = requests.get(pokemon_data['species']['url'], timeout=10)
                    species_data = species_response.json()
                    
                    nombre_es = next((n['name'] for n in species_data['names'] if n['language']['name'] == 'es'), 
                                    pokemon_data['name'].capitalize())
                    
                    tipos = []
                    for tipo_info in pokemon_data['types']:
                        tipo_response = requests.get(tipo_info['type']['url'], timeout=10)
                        tipo_data = tipo_response.json()
                        tipo_es = next((n['name'] for n in tipo_data['names'] if n['language']['name'] == 'es'), 
                                      tipo_info['type']['name'])
                        tipos.append(tipo_es)
                    
                    tipo_str = '/'.join(tipos)
                    
                    ps = pokemon_data['stats'][0]['base_stat']
                    
                    pokemon_info = {
                        'nombre': nombre_es,
                        'tipo': tipo_str,
                        'ps': ps,
                        'numero': pokemon_data['id'],
                        'sprite': pokemon_data['sprites']['front_default']
                    }
                    
                    self.pokemon_cache[nombre_o_id] = pokemon_info
                    
                    self.root.after(0, lambda: self.rellenar_datos(pokemon_info))
                    self.root.after(0, lambda: loading_label.destroy())
                else:
                    self.root.after(0, lambda: messagebox.showerror("Error", f"No se encontró el Pokémon '{nombre_o_id}'"))
                    self.root.after(0, lambda: loading_label.destroy())
            except requests.exceptions.Timeout:
                self.root.after(0, lambda: messagebox.showerror("Error", "La búsqueda tardó demasiado. Intenta de nuevo."))
                self.root.after(0, lambda: loading_label.destroy())
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", f"Error al buscar en PokeAPI: {str(e)}"))
                self.root.after(0, lambda: loading_label.destroy())
        
        Thread(target=buscar, daemon=True).start()
    
    def rellenar_datos(self, pokemon_info):
        self.entrada_nombre.delete(0, tk.END)
        self.entrada_nombre.insert(0, pokemon_info['nombre'])
        
        self.entrada_tipo.delete(0, tk.END)
        self.entrada_tipo.insert(0, pokemon_info['tipo'])
        
        self.entrada_ps.delete(0, tk.END)
        self.entrada_ps.insert(0, str(pokemon_info['ps']))
        
        self.entrada_buscar.delete(0, tk.END)
        
        messagebox.showinfo("Pokémon Encontrado", 
                           f"#{pokemon_info['numero']:03d} - {pokemon_info['nombre']}\n"
                           f"Tipo: {pokemon_info['tipo']}\n"
                           f"PS: {pokemon_info['ps']}\n\n"
                           f"Los datos han sido cargados en el formulario.")
    
    def agregar_pokemon(self):
        nombre = self.entrada_nombre.get().strip()
        tipo = self.entrada_tipo.get().strip()
        ps = self.entrada_ps.get().strip()
        
        if not nombre:
            messagebox.showwarning("Campo Vacío", "Por favor ingresa el nombre del Pokémon")
            self.entrada_nombre.focus()
            return
        
        if not tipo:
            messagebox.showwarning("Campo Vacío", "Por favor ingresa el tipo del Pokémon")
            self.entrada_tipo.focus()
            return
        
        if not ps:
            messagebox.showwarning("Campo Vacío", "Por favor ingresa los PS del Pokémon")
            self.entrada_ps.focus()
            return
        
        try:
            ps = int(ps)
            if ps < 0:
                messagebox.showerror("Error", "Los PS deben ser un número positivo")
                self.entrada_ps.focus()
                return
        except ValueError:
            messagebox.showerror("Error", "Los PS deben ser un número entero")
            self.entrada_ps.focus()
            return
        
        pokemon = {
            "nombre": nombre,
            "tipo": tipo,
            "ps": ps
        }
        
        self.pokedex.append(pokemon)
        
        messagebox.showinfo("Éxito", f"✓ ¡{nombre} ha sido agregado a la Pokédex!")
        
        self.limpiar_campos()
        self.actualizar_lista()
        self.actualizar_contador()
    
    def actualizar_lista(self):
        self.lista_text.config(state="normal")
        self.lista_text.delete(1.0, tk.END)
        
        if not self.pokedex:
            self.lista_text.insert(tk.END, "╔════════════════════════════════╗\n")
            self.lista_text.insert(tk.END, "║   POKÉDEX VACÍA                ║\n")
            self.lista_text.insert(tk.END, "║                                ║\n")
            self.lista_text.insert(tk.END, "║   Agrega algunos Pokémon       ║\n")
            self.lista_text.insert(tk.END, "║   para comenzar!               ║\n")
            self.lista_text.insert(tk.END, "║                                ║\n")
            self.lista_text.insert(tk.END, "║   Tip: Usa BUSCAR POKÉMON      ║\n")
            self.lista_text.insert(tk.END, "║   para autocompletar datos     ║\n")
            self.lista_text.insert(tk.END, "╚════════════════════════════════╝\n")
        else:
            for i, pokemon in enumerate(self.pokedex, 1):
                self.lista_text.insert(tk.END, f"╔════════════════════════════════╗\n")
                self.lista_text.insert(tk.END, f"║ Nº {i:03d}                     ║\n")
                self.lista_text.insert(tk.END, f"╠════════════════════════════════╣\n")
                
                nombre_formatted = pokemon['nombre'][:21]
                tipo_formatted = pokemon['tipo'][:21]
                ps_formatted = str(pokemon['ps'])[:21]
                
                self.lista_text.insert(tk.END, f"║ NOMBRE: {nombre_formatted:<21} ║\n")
                self.lista_text.insert(tk.END, f"║ TIPO:   {tipo_formatted:<21}   ║\n")
                self.lista_text.insert(tk.END, f"║ PS:     {ps_formatted:<21}     ║\n")
                self.lista_text.insert(tk.END, f"╚════════════════════════════════╝\n\n")
        
        self.lista_text.config(state="disabled")
    
    def eliminar_pokemon(self):
        if not self.pokedex:
            messagebox.showinfo("Pokédex Vacía", "No hay Pokémon para eliminar")
            return
        
        ventana_eliminar = tk.Toplevel(self.root)
        ventana_eliminar.title("Eliminar Pokémon")
        ventana_eliminar.geometry("400x200")
        ventana_eliminar.configure(bg=self.colores['rojo'])
        ventana_eliminar.resizable(False, False)
        
        tk.Label(ventana_eliminar,
                text="ELIMINAR POKÉMON",
                font=("Arial", 14, "bold"),
                bg=self.colores['rojo'],
                fg=self.colores['blanco']).pack(pady=20)
        
        tk.Label(ventana_eliminar,
                text="NOMBRE DEL POKÉMON:",
                font=("Arial", 10, "bold"),
                bg=self.colores['rojo'],
                fg=self.colores['amarillo']).pack(pady=(0, 5))
        
        entrada_nombre_eliminar = tk.Entry(ventana_eliminar,
                                          font=("Arial", 11),
                                          bg=self.colores['blanco'],
                                          fg=self.colores['negro'],
                                          relief="sunken",
                                          bd=2)
        entrada_nombre_eliminar.pack(ipady=8, padx=40, fill="x", pady=(0, 20))
        entrada_nombre_eliminar.focus()
        
        def confirmar_eliminar():
            nombre = entrada_nombre_eliminar.get().strip()
            
            if not nombre:
                messagebox.showwarning("Campo Vacío", "Por favor ingresa el nombre del Pokémon")
                return
            
            pokemon_encontrado = False
            for pokemon in self.pokedex:
                if pokemon["nombre"].lower() == nombre.lower():
                    self.pokedex.remove(pokemon)
                    messagebox.showinfo("Éxito", f"✓ {pokemon['nombre']} ha sido eliminado de la Pokédex")
                    pokemon_encontrado = True
                    ventana_eliminar.destroy()
                    self.actualizar_lista()
                    self.actualizar_contador()
                    break
            
            if not pokemon_encontrado:
                messagebox.showerror("No Encontrado", f"No se encontró ningún Pokémon con el nombre '{nombre}'")
        
        btn_frame = tk.Frame(ventana_eliminar, bg=self.colores['rojo'])
        btn_frame.pack(fill="x", padx=40)
        
        btn_confirmar = tk.Button(btn_frame,
                                 text="✖ ELIMINAR",
                                 command=confirmar_eliminar,
                                 font=("Arial", 11, "bold"),
                                 bg=self.colores['rojo_oscuro'],
                                 fg=self.colores['blanco'],
                                 relief="raised",
                                 cursor="hand2",
                                 padx=20,
                                 pady=8,
                                 bd=3)
        btn_confirmar.pack(side="left", expand=True, fill="x", padx=(0, 5))
        
        btn_cancelar = tk.Button(btn_frame,
                                text="↶ CANCELAR",
                                command=ventana_eliminar.destroy,
                                font=("Arial", 11, "bold"),
                                bg=self.colores['gris_oscuro'],
                                fg=self.colores['blanco'],
                                relief="raised",
                                cursor="hand2",
                                padx=20,
                                pady=8,
                                bd=3)
        btn_cancelar.pack(side="right", expand=True, fill="x", padx=(5, 0))
        
        ventana_eliminar.bind('<Return>', lambda e: confirmar_eliminar())
        ventana_eliminar.bind('<Escape>', lambda e: ventana_eliminar.destroy())
    
    def limpiar_campos(self):
        self.entrada_nombre.delete(0, tk.END)
        self.entrada_tipo.delete(0, tk.END)
        self.entrada_ps.delete(0, tk.END)
        self.entrada_nombre.focus()
    
    def actualizar_contador(self):
        total = len(self.pokedex)
        self.label_contador.config(text=f"TOTAL: {total} POKÉMON")
    
    def detener_animaciones(self):
        self.animacion_activa = False
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = PokedexGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.detener_animaciones)
    root.mainloop()
