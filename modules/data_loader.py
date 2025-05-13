import json
import os

def load_shapes(json_path):
    """Carga y valida el archivo JSON"""
    if not os.path.exists(json_path):
        raise FileNotFoundError(f"Archivo no encontrado: {json_path}")
    
    with open(json_path, 'r') as f:
        data = json.load(f)
    
    if not data:
        raise ValueError("El archivo JSON no contiene figuras")
    
    return data