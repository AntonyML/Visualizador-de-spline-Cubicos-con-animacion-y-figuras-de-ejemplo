# modules/visualization_basic.py
import matplotlib.pyplot as plt
from .visualization_styles import THEME

def show_startup_screen():
    fig = plt.figure(figsize=(8, 4), facecolor=THEME['background'])
    fig.canvas.manager.set_window_title('Spline Viewer')
    content = {
        'title': ('Spline Viewer', 24),
        'subtitle': ('Carga archivos JSON con formas paramétricas', 12),
        'instruction': ('Usa: python main.py [ruta_al_archivo.json]', 10)
    }
    y_pos = 0.7
    for text, size in content.values():
        plt.text(0.5, y_pos, text,
                 ha='center', va='center',
                 fontsize=size, color=THEME['foreground'])
        y_pos -= 0.2
    plt.axis('off')
    plt.tight_layout()
    plt.show(block=True)

def handle_error(message):
    fig = plt.figure(figsize=(6, 3), facecolor=THEME['background'])
    fig.canvas.manager.set_window_title('Error')
    plt.text(0.5, 0.7, '⚠️ Error', ha='center', va='center',
             fontsize=18, color=THEME['error'])
    plt.text(0.5, 0.4, message, ha='center', va='center',
             fontsize=11, color=THEME['foreground'], wrap=True)
    plt.axis('off')
    plt.tight_layout()
    plt.show(block=True)
