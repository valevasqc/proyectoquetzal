# Modelo de Holt-Winters (suavizado exponencial aditivo)
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

# Cambiar directorio al del script
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Cargar los datos desde el archivo Excel
file_name = "PuertoQuetzal.xlsx"
data = pd.read_excel(file_name, sheet_name="movimientoportuario")

# Limpiar nombres de columnas por si hay espacios adicionales
data.columns = data.columns.str.strip()

# Limpiar espacios adicionales en los valores de la columna 'Puerto'
data['Puerto'] = data['Puerto'].str.strip()

# Filtrar los datos para "Puerto Quetzal"
puerto_data = data[data["Puerto"] == "Puerto Quetzal"]

# Convertir la columna "Año" a formato datetime para su ordenamiento
puerto_data["Año"] = pd.to_datetime(puerto_data["Año"], format="%Y")
puerto_data.sort_values("Año", inplace=True)

# Extraer serie temporal
fechas = puerto_data["Año"]
valores = puerto_data["Toneladas"].values

# Inicialización de parámetros
alpha = 0.3  # Nivel de suavizado
beta = 0.1   # Suavizado de tendencia
gamma = 0.2  # Suavizado de estacionalidad
season_length = 12  # Longitud de la estacionalidad (mensual, o según corresponda)

# Inicializar componentes
L = [np.mean(valores[:season_length])]  # Nivel inicial
T = [(valores[season_length] - valores[0]) / season_length]  # Tendencia inicial
S = [valores[i] / L[0] for i in range(season_length)]  # Estacionalidad inicial

# Suavizado Holt-Winters
forecast = []
for t in range(len(valores)):
    if t < season_length:
        # No hay suficiente información para predecir, usar valores reales
        forecast.append(valores[t])
    else:
        # Predicción
        forecast.append((L[-1] + T[-1]) * S[t % season_length])
        # Actualización de componentes
        L.append(alpha * (valores[t] / S[t % season_length]) + (1 - alpha) * (L[-1] + T[-1]))
        T.append(beta * (L[-1] - L[-2]) + (1 - beta) * T[-1])
        S.append(gamma * (valores[t] / L[-1]) + (1 - gamma) * S[t % season_length])

# Convertir forecast a arreglo numpy para las operaciones
forecast = np.array(forecast)

# Imprimir los componentes finales
final_L = L[-1]
final_T = T[-1]
final_S = S[-season_length:]  # Última temporada completa

print("\n=== Componentes finales del modelo Holt-Winters ===")
print(f"Nivel (L_t): {final_L}")
print(f"Tendencia (T_t): {final_T}")
print(f"Estacionalidad (S_t para los últimos {season_length} periodos): {final_S}")

# Construir la ecuación del modelo
print("\nEcuación del modelo Holt-Winters (aditivo):")
print(f"Y_t = ({final_L:.2f} + T_t * h) * S_t")

# Gráfica de resultados
plt.figure(figsize=(12, 6))
plt.plot(fechas, valores, label="Datos reales", marker="o")
plt.plot(fechas, forecast, label="Pronóstico Holt-Winters", linestyle="--", color="orange")
plt.title("Modelo Holt-Winters (Puerto Quetzal)")
plt.xlabel("Fecha")
plt.ylabel("Toneladas")
plt.legend()
plt.grid()
plt.show()
