# 🔴 POKÉDEX - Interfaz Gráfica

Una aplicación de Pokédex interactiva desarrollada en Python con interfaz gráfica usando Tkinter, que incluye integración con la PokeAPI para obtener información real de Pokémon.

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green.svg)
![PokeAPI](https://img.shields.io/badge/API-PokeAPI-red.svg)

## 🎮 Características

### ✨ Interfaz Gráfica Completa
- **Diseño auténtico** inspirado en la Pokédex original
- **Ventana sin bordes** con funcionalidad de arrastre personalizada
- **Luces animadas** que pulsan como la Pokédex real
- **Colores oficiales** (#DC0A2D rojo, #88CCF1 pantalla azul)

### 🔍 Búsqueda con PokeAPI
- Búsqueda por **nombre** o **número** de Pokémon
- Obtención automática de datos en **español**
- Autocompletado de formularios con información de la API
- **Caché local** para búsquedas rápidas

### 📝 Gestión de Pokémon
- **Agregar** Pokémon a tu colección
- **Eliminar** Pokémon por nombre
- **Actualizar** lista en tiempo real
- **Limpiar** campos del formulario
- **Contador** de Pokémon totales

### 🎨 Paneles Expandibles
- Panel de **búsqueda PokeAPI** (botón amarillo)
- Panel de **datos** para ver/editar (botón verde)
- Animación suave al expandir/contraer

## 📋 Requisitos

- Python 3.11 o superior
- Tkinter (incluido con Python)
- requests

## 🚀 Instalación

1. **Clonar el repositorio:**
```bash
git clone https://github.com/Charly-bite/POKEDEX.git
cd POKEDEX
```

2. **Crear entorno virtual (opcional pero recomendado):**
```bash
python -m venv .venv
source .venv/bin/activate  # En Linux/Mac
# .venv\Scripts\activate   # En Windows
```

3. **Instalar dependencias:**
```bash
pip install requests
```

## 💻 Uso

### Versión GUI (Interfaz Gráfica)
```bash
python pokedex_gui.py
```

### Versión Consola
```bash
python pokedex.py
```

## 🎯 Funcionalidades Detalladas

### 🔍 Buscar Pokémon
1. Click en el botón **"🔍 BUSCAR EN POKEAPI"** (amarillo)
2. Ingresa el nombre o número del Pokémon
3. Presiona Enter o click en "🔍 BUSCAR API"
4. Los datos se cargarán automáticamente en el formulario

### ➕ Agregar Pokémon
1. Click en **"📝 VER/EDITAR DATOS"** (verde) para abrir el formulario
2. Completa: Nombre, Tipo, PS (puntos de salud)
3. Click en **"󰐝 AGREGAR"**
4. El Pokémon se agregará a la lista

### ❌ Eliminar Pokémon
1. Click en **"✖ ELIMINAR"**
2. Ingresa el nombre del Pokémon a eliminar
3. Confirma la eliminación

### 🔄 Otras Funciones
- **⟲ ACTUALIZAR**: Refresca la lista de Pokémon
- **⌫ LIMPIAR**: Limpia todos los campos del formulario
- **✕**: Cerrar la aplicación

## 🏗️ Estructura del Proyecto

```
POKEDEX/
├── pokedex_gui.py          # Aplicación con interfaz gráfica
├── pokedex.py              # Versión de consola
├── instrucciones.json      # Especificación del proyecto
├── README.md               # Este archivo
└── .venv/                  # Entorno virtual (no incluido en Git)
```

## 🎨 Paleta de Colores

| Color | Hex | Uso |
|-------|-----|-----|
| Rojo Pokédex | `#DC0A2D` | Fondo principal |
| Rojo Oscuro | `#A80A24` | Botones de acción |
| Azul Pantalla | `#88CCF1` | Display LCD |
| Verde | `#48D0B0` | Botones positivos |
| Amarillo | `#FFCB05` | Botón de búsqueda |
| Gris Oscuro | `#3A3A3A` | Paneles expandibles |

## 🔧 Tecnologías Utilizadas

- **Python 3.11+**: Lenguaje principal
- **Tkinter**: Framework GUI nativo
- **requests**: Cliente HTTP para PokeAPI
- **threading**: Búsquedas asíncronas sin bloquear UI
- **PokeAPI**: Base de datos RESTful de Pokémon

## 📚 API Reference

Este proyecto utiliza [PokeAPI](https://pokeapi.co/) v2:
```
GET https://pokeapi.co/api/v2/pokemon/{id or name}
```

## 🤝 Contribuciones

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for pull request guidelines and how to set up development, and adhere to [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) in all community interactions.

## 📝 Licencia

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.


## 👨‍💻 Autor

**Charly-bite**
- GitHub: [@Charly-bite](https://github.com/Charly-bite)

## 🙏 Agradecimientos

- [PokeAPI](https://pokeapi.co/) por proporcionar la API gratuita
- La comunidad de Python por las excelentes herramientas
- Nintendo/Game Freak por crear Pokémon

## 📸 Screenshots

*La interfaz presenta:*
- Luces animadas en el header
- Pantalla LCD azul para mostrar la lista
- Botones expandibles para búsqueda y edición
- Diseño fiel a la Pokédex original

## 🐛 Problemas Conocidos

Si encuentras algún bug, por favor repórtalo en la sección de [Issues](https://github.com/Charly-bite/POKEDEX/issues).

## 🔮 Futuras Mejoras

- [ ] Agregar imágenes de Pokémon (sprites)
- [ ] Soporte para evoluciones
- [ ] Exportar/Importar colección a JSON
- [ ] Modo oscuro
- [ ] Filtros por tipo
- [ ] Estadísticas detalladas

---

⭐ Si te gusta este proyecto, no olvides darle una estrella!
