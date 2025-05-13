# modules/visualization_plotters.py
import numpy as np
from scipy.interpolate import CubicSpline
import matplotlib.pyplot as plt
from .visualization_styles import THEME

def plot_cartesian_plane(ax):
    """Dibuja plano cartesiano básico."""
    ax.axhline(0, color=THEME['foreground'], alpha=0.4, lw=1)
    ax.axvline(0, color=THEME['foreground'], alpha=0.4, lw=1)
    ax.grid(True, linestyle='--', color=THEME['grid'], alpha=0.5)
    ax.set_xlabel('Eje X', color=THEME['foreground'])
    ax.set_ylabel('Eje Y', color=THEME['foreground'])
    ax.tick_params(colors=THEME['foreground'])

def plot_shape(ax, pts, color=THEME['accent']):
    """Dibuja un spline junto al plano cartesiano y puntos."""
    pts = np.array(pts)
    t = np.linspace(0, 1, len(pts))
    cs_x = CubicSpline(t, pts[:, 0], bc_type='natural')
    cs_y = CubicSpline(t, pts[:, 1], bc_type='natural')
    
    t_fine = np.linspace(0, 1, 300)
    x_fine, y_fine = cs_x(t_fine), cs_y(t_fine)
    
    plot_cartesian_plane(ax)
    
    # Trazo del spline
    ax.plot(x_fine, y_fine, '-', lw=2.5, color=color, zorder=3)
    
    # Relleno de área debajo del spline con un color más suave
    ax.fill(x_fine, y_fine, color=color, alpha=0.1, zorder=2)  # Menos opacidad para una mejor visibilidad
    
    # Puntos de control
    ax.scatter(pts[:, 0], pts[:, 1], s=100, color=color, edgecolor='white', lw=2, zorder=4, label=f'Puntos de control ({len(pts)})')

    # Configuración del gráfico
    ax.axis('equal')
    ax.legend(loc='upper right', frameon=True, facecolor=THEME['card_background'])


