# modules/button_handlers.py
import matplotlib.pyplot as plt
import random as random
from matplotlib.widgets import Button
from matplotlib.animation import FuncAnimation
import numpy as np
from .visualization_plotters import plot_cartesian_plane
from .visualization_styles import THEME


def add_buttons(fig, ax, idx, animate_callback, color_callback, area_index, area_colors):
    """
    Añade los botones 'Animar' y 'Color' a la figura y los asocia a callbacks externos.
    
    :param fig: instancia de matplotlib.figure.Figure
    :param ax: eje de la tarjeta donde se dibujan los botones
    :param idx: índice de la tarjeta (para identificar qué forma manejar)
    :param animate_callback: función a llamar en click de Animar(idx)
    :param color_callback: función a llamar en click de Color(idx)
    :param area_index: dict compartido para llevar el índice de color de cada tarjeta
    :param area_colors: lista de colores disponibles
    """
    # Asegurar layout actualizado
    fig.canvas.draw()
    pos = ax.get_position()
    btn_height = 0.04
    # Ajustar la posición de los botones
    y_btn = pos.y0 - btn_height - 0.08  # Aumentado de 0.04 a 0.08
    width = pos.width / 2 - 0.01
    
    # Botón Animar
    anim_ax = fig.add_axes([pos.x0, y_btn, width, btn_height])
    anim_ax.set_zorder(10)  # Mayor zorder para asegurar que esté encima
    anim_ax.button_name = f"anim_btn_{idx}"
    btn_anim = Button(
        anim_ax, 'Animar', color=THEME['button_background'], hovercolor=THEME['button_hover']
    )
    btn_anim.label.set_color(THEME['button_text'])
    
   
    def animate_with_log(ev):
        print(f"Botón 'Animar' presionado para la figura {idx+1}")
        animate_callback(idx)
    
    btn_anim.on_clicked(animate_with_log)
    
    # Botón Color
    color_ax = fig.add_axes([pos.x0 + width + 0.02, y_btn, width, btn_height])
    color_ax.set_zorder(10)  # Mayor zorder
    color_ax.button_name = f"color_btn_{idx}"
    btn_color = Button(
        color_ax, 'Color', color=THEME['button_background'], hovercolor=THEME['button_hover']
    )
    btn_color.label.set_color(THEME['button_text'])
  
    def color_with_log(ev):
        print(f"Botón 'Color' presionado para la figura {idx+1}")
        color_callback(idx)
    
    btn_color.on_clicked(color_with_log)
    
    # Guardar referencias a los botones para evitar que sean recolectados por el garbage collector
    if not hasattr(fig, '_button_refs'):
        fig._button_refs = []
    fig._button_refs.extend([btn_anim, btn_color])


def animate_shape(fig, axes, points, titles, idx, area_index, area_colors):
    """
    Lógica de animación de una forma en la tarjeta `idx`.
    """
    print(f"Iniciando animación para la figura {idx+1}...")
    ax = axes[idx]
    pts = points[idx]
    
    # Guardar estado previo de visibilidad de botones
    button_states = {btn: btn.ax.get_visible() for btn in fig._button_refs}
    
    # Ocultar solo los botones, no otros ejes
    for btn in fig._button_refs:
        btn.ax.set_visible(False)
    
    # Limpiar y preparar eje para animación
    ax.clear()
    from .visualization_plotters import plot_shape  # Importar plot_shape
    from .visualization_styles import THEME
    for spine in ax.spines.values():
        spine.set_edgecolor(THEME['card_border'])
        spine.set_linewidth(1.2)
    ax.set_title(titles[idx], color=THEME['foreground'], pad=15)
    plot_cartesian_plane(ax)
    plot_shape(ax, pts)  # Redibujar figura estática
    
    # Configurar elementos de animación
    color_aleatorio = random.choice(plt.cm.Set3.colors)
    line, = ax.plot([], [], '-', lw=2.5, color=color_aleatorio, zorder=3)
    scat = ax.scatter([], [], s=70, color=color_aleatorio, zorder=4)
    
    ax.set_xlim(np.min(pts[:,0]) - 1, np.max(pts[:,0]) + 1)
    ax.set_ylim(np.min(pts[:,1]) - 1, np.max(pts[:,1]) + 1)
    
    # Contador de frames para logging
    current_frame = [0]  # Usar lista para mutabilidad en closure
    
    def update(i):
        nonlocal current_frame
        current_frame[0] = i
        progress = f"{i}/{len(pts)}"
        if i < len(pts):
            print(f"Animando figura {idx+1}: Punto {i+1} ({progress})")
        line.set_data(pts[:i,0], pts[:i,1])
        scat.set_offsets(pts[:i])
        if i == len(pts):
            ax.fill(pts[:,0], pts[:,1], color=area_colors[area_index.get(idx, 0)], alpha=0.1, zorder=2)
            print(f"✅ Animación de figura {idx+1} completada ({progress}).")
        fig.canvas.draw_idle()
        return line, scat
    
    # Configurar animación con temporizador mejorado
    ani = FuncAnimation(
        fig, 
        update, 
        frames=len(pts)+1, 
        interval=50,  # Más rápido
        blit=False, 
        repeat=False
    )
    
    # Guardar referencia para evitar garbage collection
    if not hasattr(fig, '_animations'):
        fig._animations = []
    fig._animations.append(ani)
    
    # Callback de finalización robusto
    def on_animation_end():
        print(f"🔄 Reactivando botones para figura {idx+1}...")
        for btn in fig._button_refs:
            btn.ax.set_visible(button_states[btn])
        plt.draw()
    
    # Usar evento 'finished' en lugar de hack _stop
    ani._fig = fig  # Asegurar referencia
    ani.event_source.add_callback(lambda: on_animation_end())
    
    plt.draw()


    # Reactivar botones al finalizar
    def on_done(event):
        print(f"Reactivando botones para la figura {idx+1}...")
        for ax in fig.axes:
            if hasattr(ax, 'button_name'):
                ax.set_visible(True)
        plt.draw()
    ani._stop = on_done


def cycle_area_color(axes, points, idx, area_index, area_colors):
    """
    Cicla el color de relleno de la forma en la tarjeta `idx`.
    """
    ax = axes[idx]
    pts = points[idx]
    prev_index = area_index.get(idx, 0)
    area_index[idx] = (prev_index + 1) % len(area_colors)
    color = area_colors[area_index[idx]]
    # Eliminar rellenos previos
    ax.collections = [c for c in ax.collections if not hasattr(c, 'get_paths')]
    ax.fill(pts[:,0], pts[:,1], color=color, alpha=0.1, zorder=2)
    print(f"Color cambiado para figura {idx+1}: {prev_index+1} → {area_index[idx]+1}")
    plt.draw()