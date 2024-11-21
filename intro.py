import pandas as pd
import matplotlib.pyplot as plt

# Cargar las hojas del archivo Excel
data_file = "PuertoQuetzal.xlsx"
movimiento = pd.read_excel(data_file, sheet_name="movimientoportuario")
tipodecambio = pd.read_excel(data_file, sheet_name="tipodecambio")
pibanual = pd.read_excel(data_file, sheet_name="pibanual")

# Limpiar y preparar los datos
# Convertir las columnas de Año a tipo entero
tipodecambio["Año"] = tipodecambio["Año"].astype(int)
pibanual["Año"] = pibanual["Año"].astype(int)

# Unificar los datos usando la columna Año
data = movimiento.merge(tipodecambio, on="Año", how="left")
data = data.merge(pibanual, on="Año", how="left")

# Convertir Toneladas a numérico
data["Toneladas"] = pd.to_numeric(data["Toneladas"], errors="coerce")

# Visualización 1: Distribución de toneladas por tipo de operación
operacion_toneladas = data.groupby(["Operación", "Puerto"])["Toneladas"].sum().unstack()
operacion_toneladas.plot(kind="bar", figsize=(10, 6))
plt.title("Distribución de Toneladas por Operación y Puerto")
plt.xlabel("Operación")
plt.ylabel("Toneladas")
plt.xticks(rotation=45)
plt.legend(title="Puerto")
plt.tight_layout()
plt.show()

# Visualización 2: Diagramas de caja (simplificados por promedio mensual)
tipo_movimiento_toneladas = data.groupby("TipoDeMovimiento")["Toneladas"].mean()
tipo_movimiento_toneladas.plot(kind="bar", figsize=(10, 6))
plt.title("Promedio de Toneladas por Tipo de Movimiento")
plt.xlabel("Tipo de Movimiento")
plt.ylabel("Toneladas Promedio")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Visualización 3: Tendencias anuales de toneladas
anual_toneladas = data.groupby(["Año", "Operación"])["Toneladas"].sum().unstack()
anual_toneladas.plot(figsize=(10, 6))
plt.title("Tendencias Anuales de Toneladas por Operación")
plt.xlabel("Año")
plt.ylabel("Toneladas")
plt.legend(title="Operación")
plt.tight_layout()
plt.show()

# Análisis de correlación
correlation_data = data[["Toneladas", "Compra", "Venta", "PIB"]].dropna()
correlation_matrix = correlation_data.corr()

# Visualización 4: Correlaciones (texto)
plt.figure(figsize=(6, 4))
plt.matshow(correlation_matrix, cmap="coolwarm", fignum=1)
plt.colorbar()
plt.xticks(range(len(correlation_matrix.columns)), correlation_matrix.columns, rotation=45)
plt.yticks(range(len(correlation_matrix.columns)), correlation_matrix.columns)
plt.title("Mapa de Calor de Correlaciones", pad=20)
plt.tight_layout()
plt.show()

# Resumen de correlaciones
print("Correlaciones entre variables económicas y toneladas movilizadas:")
print(correlation_matrix)
