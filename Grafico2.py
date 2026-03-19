import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
from matplotlib.widgets import Button

# Datos de países con mayor índice de hambruna (2017-2026)
paises = ("Yemen", "Sudán del Sur", "Somalia", "Etiopía", "Afganistán", "Haití")

# Índice de hambruna para cada año (2017-2026)
años = list(range(2017, 2027))
datos_hambre = {
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

x = np.arange(len(paises))
ancho = 0.6

# Usar solo el primer año (índice 0) para crear las barras iniciales
valores_iniciales = [datos_hambre[pais][0] for pais in paises]
barras = ax.bar(x, valores_iniciales, ancho, color='#ff9999', alpha=0.8)

# Configuración inicial
ax.set_ylabel('Índice de Hambruna (GHI)', fontsize=12, fontweight='bold')
ax.set_xlabel('Países', fontsize=12, fontweight='bold')
ax.set_title('Evolución del Hambre por Países (2017-2026)', 
             fontsize=14, fontweight='bold', pad=20)
ax.set_xticks(x)
ax.set_xticklabels(paises, fontsize=10)
ax.set_ylim(0, 70)
ax.grid(axis='y', alpha=0.3, linestyle='--')

# Líneas de umbral
ax.axhline(y=35, color='orange', linestyle='--', linewidth=1, alpha=0.7, label='Umbral alarmante (35)')
ax.axhline(y=50, color='red', linestyle='--', linewidth=1, alpha=0.7, label='Umbral extremo (50)')
ax.legend(loc='upper left', fontsize=9)

# Texto para mostrar el año actual
texto_año = ax.text(0.02, 0.95, f'Año: {años[0]}', transform=ax.transAxes, fontsize=14, 
                   fontweight='bold', verticalalignment='top',
                   bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))

# Variables para la animación
indice_año_actual = 0
animacion_en_ejecucion = True

# Función de actualización para la animación
def actualizar(frame):
    global indice_año_actual
    indice_año_actual = frame
    
    # Actualizar alturas de las barras
    for i, pais in enumerate(paises):
        barras[i].set_height(datos_hambre[pais][frame])
        
        # Cambiar color según la intensidad
        valor = datos_hambre[pais][frame]
        if valor >= 50:
            barras[i].set_color('#8B0000')  # Rojo oscuro
        elif valor >= 35:
            barras[i].set_color('#FF6B6B')  # Rojo claro
        else:
            barras[i].set_color('#4ECDC4')  # Verde azulado
    
    # Actualizar texto del año
    texto_año.set_text(f'Año: {años[frame]}')
    
    # Actualizar título con el año también
    ax.set_title(f'Evolución del Hambre por Países ({años[0]}-{años[-1]}) - Mostrando: {años[frame]}', 
                 fontsize=14, fontweight='bold', pad=20)
    
    return barras

# Función para pausar/reanudar
def alternar_animacion(event=None):
    global animacion_en_ejecucion
    if animacion_en_ejecucion:
        anim.event_source.stop()
        animacion_en_ejecucion = False
        boton_pausa.label.set_text('▶ Reanudar')
    else:
        anim.event_source.start()
        animacion_en_ejecucion = True
        boton_pausa.label.set_text('⏸ Pausar')

# Función para manejar clics en el gráfico
def al_hacer_click(event):
    # Verificar que el clic fue dentro del área del gráfico (no en los botones)
    if event.inaxes == ax:
        alternar_animacion()

# Función para reiniciar
def reiniciar_animacion(event):
    global indice_año_actual, animacion_en_ejecucion
    indice_año_actual = 0
    if not animacion_en_ejecucion:
        anim.event_source.start()
        animacion_en_ejecucion = True
        boton_pausa.label.set_text('⏸ Pausar')
    # Reiniciar la animación
    anim.frame_seq = anim.new_frame_seq()
    anim.event_source.stop()
    anim.event_source.start()

# Función para avanzar manualmente
def avanzar_paso(event):
    global indice_año_actual, animacion_en_ejecucion
    if animacion_en_ejecucion:
        alternar_animacion(event)
    indice_año_actual = (indice_año_actual + 1) % len(años)
    actualizar(indice_año_actual)
    plt.draw()

# Función para retroceder manualmente
def retroceder_paso(event):
    global indice_año_actual, animacion_en_ejecucion
    if animacion_en_ejecucion:
        alternar_animacion(event)
    indice_año_actual = (indice_año_actual - 1) % len(años)
    actualizar(indice_año_actual)
    plt.draw()

# Crear botones
ax_pausa = plt.axes([0.7, 0.05, 0.1, 0.05])
ax_reiniciar = plt.axes([0.81, 0.05, 0.1, 0.05])
ax_avanzar = plt.axes([0.59, 0.05, 0.1, 0.05])
ax_retroceder = plt.axes([0.48, 0.05, 0.1, 0.05])

boton_pausa = Button(ax_pausa, '⏸ Pausar', color='lightgray', hovercolor='gold')
boton_reiniciar = Button(ax_reiniciar, '↺ Reiniciar', color='lightgray', hovercolor='gold')
boton_avanzar = Button(ax_avanzar, '→ Avanzar', color='lightgray', hovercolor='gold')
boton_retroceder = Button(ax_retroceder, '← Retroceder', color='lightgray', hovercolor='gold')

# Conectar botones con funciones
boton_pausa.on_clicked(alternar_animacion)
boton_reiniciar.on_clicked(reiniciar_animacion)
boton_avanzar.on_clicked(avanzar_paso)
boton_retroceder.on_clicked(retroceder_paso)

# Conectar el evento de clic en el gráfico
fig.canvas.mpl_connect('button_press_event', al_hacer_click)

# Información adicional
texto_info = fig.text(0.5, 0.01, 'Datos: Global Hunger Index (2017-2023 reales, 2024-2026 proyecciones) - Haz clic en el gráfico para pausar/reanudar',
                    ha='center', fontsize=9, style='italic',
                    bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

# Crear animación
anim = animation.FuncAnimation(fig, actualizar, frames=len(años), 
                             interval=1000, repeat=True, blit=False)

# Mostrar año inicial (2017)
plt.show()