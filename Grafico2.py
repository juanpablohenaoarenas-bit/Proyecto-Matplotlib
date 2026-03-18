import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
from matplotlib.widgets import Button

# Datos de países con mayor índice de hambruna (2017-2026)
countries = ("Yemen", "Sudán del Sur", "Somalia", "Etiopía", "Afganistán", "Haití")

# Índice de hambruna para cada año (2017-2026)
years = list(range(2017, 2027))
hunger_data = {
    'Yemen': [45.2, 46.1, 47.3, 48.7, 50.1, 51.2, 52.4, 53.6, 54.7, 55.8],
    'Sudán del Sur': [52.8, 53.5, 54.4, 55.3, 56.2, 57.5, 58.7, 59.6, 60.4, 61.2],
    'Somalia': [48.6, 49.3, 50.1, 51.2, 52.4, 53.6, 54.8, 55.7, 56.6, 57.5],
    'Etiopía': [42.3, 43.1, 44.0, 44.8, 45.6, 46.5, 47.6, 48.4, 49.3, 50.3],
    'Afganistán': [38.7, 39.5, 40.3, 41.5, 42.4, 43.3, 44.3, 45.2, 46.5, 47.8],
    'Haití': [35.2, 36.1, 37.5, 38.9, 40.0, 41.1, 42.1, 43.2, 44.4, 45.6]
}

# Configuración del gráfico
fig, ax = plt.subplots(figsize=(14, 8))
plt.subplots_adjust(bottom=0.2)  # Espacio para los botones

x = np.arange(len(countries))
width = 0.6

# CORRECCIÓN: Usar solo el primer año (índice 0) para crear las barras iniciales
initial_values = [hunger_data[country][0] for country in countries]
bars = ax.bar(x, initial_values, width, color='#ff9999', alpha=0.8)

# Configuración inicial
ax.set_ylabel('Índice de Hambruna (GHI)', fontsize=12, fontweight='bold')
ax.set_xlabel('Países', fontsize=12, fontweight='bold')
ax.set_title('Evolución de la Hambruna por Países (2017-2026)', 
             fontsize=14, fontweight='bold', pad=20)
ax.set_xticks(x)
ax.set_xticklabels(countries, fontsize=10)
ax.set_ylim(0, 70)
ax.grid(axis='y', alpha=0.3, linestyle='--')

# Líneas de umbral
ax.axhline(y=35, color='orange', linestyle='--', linewidth=1, alpha=0.7, label='Umbral alarmante (35)')
ax.axhline(y=50, color='red', linestyle='--', linewidth=1, alpha=0.7, label='Umbral extremo (50)')
ax.legend(loc='upper left', fontsize=9)

# Texto para mostrar el año actual
year_text = ax.text(0.02, 0.95, f'Año: {years[0]}', transform=ax.transAxes, fontsize=14, 
                   fontweight='bold', verticalalignment='top',
                   bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))

# Variables para la animación
current_year_idx = 0
anim_running = True

# Función de actualización para la animación
def update(frame):
    global current_year_idx
    current_year_idx = frame
    
    # Actualizar alturas de las barras
    for i, country in enumerate(countries):
        bars[i].set_height(hunger_data[country][frame])
        
        # Cambiar color según la intensidad
        value = hunger_data[country][frame]
        if value >= 50:
            bars[i].set_color('#8B0000')  # Rojo oscuro
        elif value >= 35:
            bars[i].set_color('#FF6B6B')  # Rojo claro
        else:
            bars[i].set_color('#4ECDC4')  # Verde azulado
    
    # Actualizar texto del año
    year_text.set_text(f'Año: {years[frame]}')
    
    # Actualizar título con el año también
    ax.set_title(f'Evolución de la Hambruna por Países ({years[0]}-{years[-1]}) - Mostrando: {years[frame]}', 
                 fontsize=14, fontweight='bold', pad=20)
    
    return bars

# Función para pausar/reanudar
def toggle_animation(event=None):  # Añadido event=None para que funcione con el clic
    global anim_running
    if anim_running:
        anim.event_source.stop()
        anim_running = False
        pause_button.label.set_text('▶ Reanudar')
    else:
        anim.event_source.start()
        anim_running = True
        pause_button.label.set_text('⏸ Pausar')

# Función para manejar clics en el gráfico
def on_click(event):
    # Verificar que el clic fue dentro del área del gráfico (no en los botones)
    if event.inaxes == ax:
        toggle_animation()

# Función para reiniciar
def restart_animation(event):
    global current_year_idx, anim_running
    current_year_idx = 0
    if not anim_running:
        anim.event_source.start()
        anim_running = True
        pause_button.label.set_text('⏸ Pausar')
    # Reiniciar la animación
    anim.frame_seq = anim.new_frame_seq()
    anim.event_source.stop()
    anim.event_source.start()

# Función para avanzar manualmente
def step_forward(event):
    global current_year_idx, anim_running
    if anim_running:
        toggle_animation(event)
    current_year_idx = (current_year_idx + 1) % len(years)
    update(current_year_idx)
    plt.draw()

# Función para retroceder manualmente
def step_backward(event):
    global current_year_idx, anim_running
    if anim_running:
        toggle_animation(event)
    current_year_idx = (current_year_idx - 1) % len(years)
    update(current_year_idx)
    plt.draw()

# Crear botones
ax_pause = plt.axes([0.7, 0.05, 0.1, 0.05])
ax_restart = plt.axes([0.81, 0.05, 0.1, 0.05])
ax_forward = plt.axes([0.59, 0.05, 0.1, 0.05])
ax_backward = plt.axes([0.48, 0.05, 0.1, 0.05])

pause_button = Button(ax_pause, '⏸ Pausar', color='lightgray', hovercolor='gold')
restart_button = Button(ax_restart, '↺ Reiniciar', color='lightgray', hovercolor='gold')
forward_button = Button(ax_forward, '→ Avanzar', color='lightgray', hovercolor='gold')
backward_button = Button(ax_backward, '← Retroceder', color='lightgray', hovercolor='gold')

# Conectar botones con funciones
pause_button.on_clicked(toggle_animation)
restart_button.on_clicked(restart_animation)
forward_button.on_clicked(step_forward)
backward_button.on_clicked(step_backward)

# Conectar el evento de clic en el gráfico
fig.canvas.mpl_connect('button_press_event', on_click)

# Información adicional
info_text = fig.text(0.5, 0.01, 'Datos: Global Hunger Index (2017-2023 reales, 2024-2026 proyecciones) - Haz clic en el gráfico para pausar/reanudar',
                    ha='center', fontsize=9, style='italic',
                    bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

# Crear animación
anim = animation.FuncAnimation(fig, update, frames=len(years), 
                             interval=1000, repeat=True, blit=False)

# Mostrar año inicial (2017)
plt.show()