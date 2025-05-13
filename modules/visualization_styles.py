# modules/visualization_styles.py
import matplotlib.pyplot as plt
from matplotlib import rcParams

THEME = {
    'background': '#f8f9fa',
    'foreground': '#212529',
    'accent': '#4a69bd',
    'highlight': '#f1f3f5',
    'error': '#e55039',
    'grid': '#adb5bd',
    'card_background': '#ffffff',
    'card_border': '#dee2e6',
    'button_background': '#4a69bd',
    'button_hover': '#3742fa',
    'button_text': '#ffffff'
}


def configure_styles():
    """Aplica configuraciones generales de estilo"""
    plt.style.use('default')
    rcParams.update({
        'font.size': 11,
        'axes.titlesize': 13,
        'axes.labelsize': 11,
        'axes.facecolor': THEME['card_background'],
        'figure.facecolor': THEME['background'],
        'grid.color': THEME['grid'],
        'grid.alpha': 0.3,
        'axes.spines.top': False,
        'axes.spines.right': False,
        'axes.prop_cycle': plt.cycler(color=plt.cm.Set3.colors)
    })
