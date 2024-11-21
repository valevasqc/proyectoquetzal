# MODELO DE SUAVIZADO EXPONENCIAL SIMPLE 
import pandas as pd
import matplotlib.pyplot as plt

# Cargar datos desde el archivo Excel
file_path = "PuertoQuetzal.xlsx"

# Leer las hojas
movimientoportuario = pd.read_excel(file_path, sheet_name=0)
tipodecambio = pd.read_excel(file_path, sheet_name=1)
pibanual = pd.read_excel(file_path, sheet_name=2)


# Filtrar y agrupar los datos necesarios
# Suponemos que "Año" es el índice temporal y "Toneladas" contiene el peso
movimientoportuario['Mes'] = pd.to_datetime(movimientoportuario['Año '].astype(str) + '-01')  # Si no tiene mes exacto
toneladas_mensuales = movimientoportuario.groupby('Mes')['Toneladas '].sum()

# Suavizado exponencial manual
alpha = 0.2# Parámetro de suavizado
suavizado = [toneladas_mensuales.iloc[0]]  # Inicializar con el primer valor

for i in range(1, len(toneladas_mensuales)):
    valor_suavizado = alpha * toneladas_mensuales.iloc[i] + (1 - alpha) * suavizado[-1]
    suavizado.append(valor_suavizado)

# Convertir la lista de valores suavizados en una serie de pandas
suavizado = pd.Series(suavizado, index=toneladas_mensuales.index)

# Graficar los datos originales y la tendencia suavizada
plt.figure(figsize=(12, 6))
plt.plot(toneladas_mensuales, label="Datos Originales", color="blue", marker="o")
plt.plot(suavizado, label="Tendencia Suavizada (alpha={})".format(alpha), color="red")
plt.title("Tendencia de Peso Mensual de Carga")
plt.xlabel("Mes")
plt.ylabel("Toneladas")
plt.legend()
plt.grid()
plt.show()

# Interpretación 
print("La tendencia muestra un patrón de: ")
if suavizado.iloc[-1] > suavizado.iloc[0]:
    print("Crecimiento")
elif suavizado.iloc[-1] < suavizado.iloc[0]:
    print("Disminución")
else:
    print("Estabilidad")
