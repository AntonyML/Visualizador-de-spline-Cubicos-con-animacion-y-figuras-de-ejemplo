import sys
import os
import matplotlib.pyplot as plt
from modules.data_loader import load_shapes
from modules.spline_math import calculate_spline
from modules.visualization import (
    configure_styles,
    handle_error,
    show_startup_screen,
    show_gallery,
    create_detail_figure
)


def main():
    configure_styles()

    # RUTA POR DEFECTO relativa al proyecto
    default_json = os.path.join(os.path.dirname(__file__), 'data', 'shapes.json')

    try:
        # Si me pasan un arg[1], lo uso; si no, tiro de la ruta por defecto
        if len(sys.argv) > 1:
            json_path = sys.argv[1]
        else:
            json_path = default_json

        shapes = load_shapes(json_path)
        if not shapes:
            raise FileNotFoundError(f"No se cargaron formas desde {json_path!r}")

        if len(shapes) == 1:
            name, pts = next(iter(shapes.items()))
            x_fine, y_fine, x_ctrl, y_ctrl = calculate_spline(pts)
            fig = create_detail_figure(x_fine, y_fine, x_ctrl, y_ctrl, name, '#4a69bd')
            plt.show(block=True)
        else:
            show_gallery(shapes)
            plt.show(block=True)

    except Exception as e:
        handle_error(str(e))
        plt.close('all')


if __name__ == '__main__':
    main()
