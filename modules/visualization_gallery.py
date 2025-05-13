# modules/visualization_gallery.py
import numpy as np
import matplotlib.pyplot as plt
from .visualization_plotters import plot_shape, plot_cartesian_plane
from .visualization_styles import THEME
from .button_handlers import add_buttons, animate_shape, cycle_area_color

class CartesianGallery:
    """Organiza figuras dentro de tarjetas con título y plano cartesiano."""
    def __init__(self, shapes):
        self.shapes = shapes
        self.fig = plt.figure(figsize=(14, 8), facecolor=THEME['background'])
        self.fig.canvas.manager.set_window_title('Visualización de Splines')
        
        # Referencias para evitar recolección de garbage collector
        self.fig._button_refs = []
        
        self.axes = []
        self.points = []
        self.original_titles = []
        self.area_colors = [THEME['accent'], THEME['highlight'], THEME['error']]
        self.area_index = {}
        
        # Conectar evento para manejar clics
        self.fig.canvas.mpl_connect('button_press_event', self._on_click)
        
        self._create_layout()
    
    def _on_click(self, event):
        """Manejador de eventos para clics en la figura"""
        # Este método es útil para debugging y detección de problemas con los botones
        if event.inaxes is None:
            print(f"Clic detectado fuera de los ejes en: ({event.x}, {event.y})")
        else:
            print(f"Clic detectado en ejes: {event.inaxes}")
    
    def _create_layout(self):
        n = len(self.shapes)
        cols = min(3, n)
        rows = int(np.ceil(n / cols))
        self.gs = self.fig.add_gridspec(
            rows, cols,
            top=0.85, bottom=0.2,  
            left=0.05, right=0.95,
            hspace=0.9, wspace=0.7  
        )
        self._add_main_title()
        self._create_cards()
    
    def _add_main_title(self):
        self.fig.suptitle(
            'Visualización de Figuras con Plano Cartesiano',
            fontsize=18, y=0.98, color=THEME['foreground'], weight='semibold'
        )
    
    def _create_cards(self):
        for idx, (name, pts) in enumerate(self.shapes.items()):
            # Agregamos un print para debug
            print(f"Creando tarjeta {idx+1}: {name}")
            
            ax = self.fig.add_subplot(self.gs[idx])
            self._decorate_card(ax, name)
            plot_shape(ax, pts)
            self.axes.append(ax)
            self.points.append(np.array(pts))
            self.original_titles.append(name)
            
            # Ajustamos el límite y del eje para dejar más espacio para los botones
            current_ylim = ax.get_ylim()
            data_height = current_ylim[1] - current_ylim[0]
            ax.set_ylim(current_ylim[0] - 0.05 * data_height, current_ylim[1])
            
            add_buttons(
                self.fig, ax, idx,
                animate_callback=self._animate_shape,
                color_callback=self._cycle_area_color,
                area_index=self.area_index,
                area_colors=self.area_colors
            )
    
    def _decorate_card(self, ax, title):
        ax.set_facecolor(THEME['card_background'])
        for spine in ax.spines.values():
            spine.set_edgecolor(THEME['card_border'])
            spine.set_linewidth(1.2)
        ax.set_title(title, fontsize=12, color=THEME['foreground'], pad=15)
        ax.title.set_position([.5, 1.05])
    
    def _animate_shape(self, idx):
        print(f"Llamando animate_shape para figura {idx+1}")
        animate_shape(
            self.fig,
            self.axes,
            self.points,
            self.original_titles,
            idx,
            self.area_index,
            self.area_colors
        )
    
    def _cycle_area_color(self, idx):
        print(f"Llamando cycle_area_color para figura {idx+1}")
        cycle_area_color(
            self.axes,
            self.points,
            idx,
            self.area_index,
            self.area_colors
        )


def create_detail_figure(x_fine, y_fine, x_ctrl, y_ctrl, title, color_accent):  # reexported
    fig = plt.figure(figsize=(7, 7), facecolor=THEME['background'])
    ax = fig.add_subplot(111)
    plot_cartesian_plane(ax)
    ax.plot(x_fine, y_fine, '-', lw=2.5, color=color_accent, zorder=3)
    ax.scatter(x_ctrl, y_ctrl, s=50, color=color_accent, zorder=4)
    fig.canvas.manager.set_window_title(f'Detalle - {title}')
    plt.tight_layout()
    return fig


def show_gallery(shapes):
    print("Inicializando galería de visualización...")
    gallery = CartesianGallery(shapes)
    print("Mostrando galería. Haz clic en los botones para interactuar.")
    plt.show(block=True)