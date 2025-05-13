import numpy as np
from scipy.interpolate import CubicSpline

def calculate_spline(pts, num_points=500):
    """
    Calcula un spline cúbico natural a partir de una lista de puntos 2D.

    Parámetros:
    - pts: lista o arreglo de puntos [(x0, y0), (x1, y1), ..., (xn, yn)]
    - num_points: cantidad de puntos interpolados que se quieren en el resultado

    Retorna:
    - (x_interpolado, y_interpolado, x_original, y_original)
    """
    
    # Convertimos la lista de puntos en un arreglo de numpy para mejor manejo
    pts = np.array(pts)
    
    # Creamos un vector t que representa un parámetro "tiempo", de 0 a 1
    # Cada punto (x,y) se asigna a un valor de t igualmente espaciado
    t = np.linspace(0, 1, len(pts))
    
    # Creamos un trazador cúbico natural para las coordenadas x
    # bc_type='natural' establece que la segunda derivada en los extremos sea 0
    cs_x = CubicSpline(t, pts[:,0], bc_type='natural')
    
    # Creamos un trazador cúbico natural para las coordenadas y
    cs_y = CubicSpline(t, pts[:,1], bc_type='natural')
    
    # Generamos muchos valores de t (muchos más que puntos originales)
    # para obtener una curva suave cuando evaluemos los splines
    t_fine = np.linspace(0, 1, num_points)
    
    # Evaluamos ambos splines en los nuevos valores t_fine
    # Esto nos da los puntos (x, y) del trazador interpolado
    return cs_x(t_fine), cs_y(t_fine), pts[:,0], pts[:,1]

def calculate_spline_natural(pts, num_points=500):
    """
    Calcula un spline cúbico natural a partir de una lista de puntos 2D,
    implementado desde cero sin usar librerías de interpolación.

    Parámetros:
    - pts: lista o arreglo de puntos [(x0, y0), (x1, y1), ..., (xn, yn)]
    - num_points: cantidad de puntos interpolados que se quieren en el resultado

    Retorna:
    - (x_interpolado, y_interpolado, x_original, y_original)
    """
    # PASO 1: Convertimos la lista de puntos en un arreglo de numpy y extraemos las coordenadas
    pts = np.array(pts)
    x = pts[:, 0]
    y = pts[:, 1]
    n = len(pts) - 1  # Número de intervalos (n+1 puntos)
    
    # PASO 2: Calculamos las diferencias entre puntos consecutivos
    h = np.zeros(n)
    for i in range(n):
        h[i] = x[i+1] - x[i]
    
    # PASO 3: Establecemos el sistema tridiagonal para resolver
    # Para un spline cúbico natural, las segundas derivadas en los extremos son cero
    # Necesitamos resolver el sistema: A * M = B donde M son las segundas derivadas
    
    # Configuramos la matriz tridiagonal A
    A = np.zeros((n+1, n+1))
    A[0, 0] = 1.0  # Condición de borde izquierdo: M[0] = 0 (natural)
    A[n, n] = 1.0  # Condición de borde derecho: M[n] = 0 (natural)
    
    # Configuramos las diagonales de la matriz tridiagonal
    for i in range(1, n):
        A[i, i-1] = h[i-1]
        A[i, i] = 2 * (h[i-1] + h[i])
        A[i, i+1] = h[i]
    
    # PASO 4: Configuramos el vector B (lado derecho de la ecuación)
    B = np.zeros(n+1)
    # B[0] y B[n] ya son 0 por la condición natural del spline
    
    # Calculamos las diferencias divididas de segundo orden
    for i in range(1, n):
        B[i] = 6 * ((y[i+1] - y[i]) / h[i] - (y[i] - y[i-1]) / h[i-1])
    
    # PASO 5: Resolvemos el sistema A * M = B para encontrar M (segundas derivadas)
    M = np.linalg.solve(A, B)
    
    # PASO 6: Generamos puntos para la curva suave
    x_interp = np.linspace(x[0], x[n], num_points)
    y_interp = np.zeros(num_points)
    
    # PASO 7: Para cada punto interpolado, identificamos el intervalo y calculamos el valor
    for k in range(num_points):
        # Encontramos el intervalo [x_i, x_i+1] que contiene a x_interp[k]
        i = 0
        while i < n and x[i+1] < x_interp[k]:
            i += 1
        
        # Si estamos fuera del rango, ajustamos
        if i >= n:
            i = n - 1
        
        # Calculamos los coeficientes del spline en este intervalo
        dx = x[i+1] - x[i]
        a = (M[i+1] - M[i]) / (6 * dx)
        b = M[i] / 2
        c = (y[i+1] - y[i]) / dx - (M[i+1] + 2 * M[i]) * dx / 6
        d = y[i]
        
        # Calculamos la coordenada x relativa al punto i
        t = x_interp[k] - x[i]
        
        # Evaluamos el polinomio cúbico S(x) = a*(x-xi)³ + b*(x-xi)² + c*(x-xi) + d
        y_interp[k] = a * t**3 + b * t**2 + c * t + d
        
    return x_interp, y_interp, x, y

# Comparaciones

#SciPy: ofrece una solución concisa, optimizada y con comprobaciones internas.
# Conviene usarla en producción o prototipos rápidos.

#Implementación manual: refuerza la comprensión de la teoría
# y permite personalizar detalles (p. ej. condiciones de contorno diferentes).