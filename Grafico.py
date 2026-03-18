import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.image as mpimg

# ----------------------------------------------------------------------
# DATOS: Precio del dólar en Colombia
# ----------------------------------------------------------------------
años = [2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026]
precios = [2951, 2958, 3283, 3693, 3749, 4260, 4322, 4074, 4049, 3698]

# ----------------------------------------------------------------------
# CREAR EL GRÁFICO
# ----------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 6))
linea, = ax.plot([], [], 'bo-', linewidth=2, markersize=8)

# Configurar ejes
ax.set_xlim(2016.5, 2026.5)
ax.set_ylim(2500, 4500)
ax.set_xticks(años)
ax.set_xticklabels(años, rotation=45)
ax.set_xlabel('Año', fontsize=12)
ax.set_ylabel('Precio del dólar (COP)', fontsize=12)
ax.set_title('Evolución del precio del dólar en Colombia', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3)

# Añadir instrucción para el usuario
ax.text(0.02, 0.98, 'Haz CLICK en cualquier parte para pausar/reanudar', 
        transform=ax.transAxes, fontsize=10, color='red',
        verticalalignment='top', bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.3))


# ----------------------------------------------------------------------
# CARGAR Y MOSTRAR LA IMAGEN DE FONDO (CORREGIDO)
# ----------------------------------------------------------------------
try:
    # Cargar la imagen
    img = mpimg.imread('img/fondo.jpg')
    
    # CORRECCIÓN: extent debe coincidir con los límites de los ejes
    # extent = [x_inicio, x_fin, y_inicio, y_fin]
    ax.imshow(img, 
              extent=[2016.5, 2026.5, 2500, 4500],  # ¡AHORA COINCIDE CON TUS DATOS!
              aspect='auto',    # 'auto' para que se estire al tamaño del gráfico
              alpha=0.3,        # Transparencia (0.3 = 30% opaco)
              zorder=-1)        # Detrás de todo
    
    print("✅ Imagen de fondo cargada correctamente")
    
except FileNotFoundError:
    print("⚠️  No se encontró 'fondo.jpg' - el gráfico continuará sin imagen")
except Exception as e:
    print(f"⚠️  Error al cargar la imagen: {e}")

# Crear la línea de datos (con zorder mayor que la imagen)
linea, = ax.plot([], [], 'bo-', linewidth=2, markersize=8, zorder=1)

# ----------------------------------------------------------------------
# CONFIGURAR LA ANIMACIÓN CON PAUSA
# ----------------------------------------------------------------------

# Variable para controlar si está pausado
pausado = False

def animar(frame):
    """Función que actualiza la animación en cada frame"""
    if not pausado:  # Solo actualiza si NO está pausado
        años_a_mostrar = frame + 1
        años_seleccionados = años[:años_a_mostrar]
        precios_seleccionados = precios[:años_a_mostrar]
        
        linea.set_data(años_seleccionados, precios_seleccionados)
        
        año_actual = años[frame]
        precio_actual = precios[frame]
        ax.set_title(f'Dólar en Colombia: {año_actual} = ${precio_actual:,.0f} COP', 
                    fontsize=14, fontweight='bold')
    
    return linea,

def toggle_pausa(event):
    """Función que se llama cuando el usuario hace click"""
    global pausado
    pausado = not pausado  # Cambia el estado (pausado → reanudar, o viceversa)
    if pausado:
        print("⏸️  Animación PAUSADA - Haz click para reanudar")
    else:
        print("▶️  Animación REANUDADA")

# Conectar el evento de click del mouse con nuestra función
fig.canvas.mpl_connect('button_press_event', toggle_pausa)

# Crear la animación
animacion = animation.FuncAnimation(
    fig,              # La figura
    animar,           # La función que se llama en cada frame
    frames=10,        # Número total de frames
    interval=1000,    # 1 segundo entre frames
    repeat=True,      # Repetir al terminar
    blit=False        # False para que funcione el título
)

# Mostrar la animación
plt.tight_layout()
plt.show()