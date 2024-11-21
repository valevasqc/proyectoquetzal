import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

mov = pd.read_excel('PuertoQuetzal.xlsx', sheet_name='MovimientoPortuario')
cambio = pd.read_excel('PuertoQuetzal.xlsx', sheet_name='TipoDeCambio')
pib = pd.read_excel('PuertoQuetzal.xlsx', sheet_name='PIBAnual')

# Preparar datos: Agregar columnas útiles
mov['Mes'] = mov.groupby('Año').cumcount() + 1
mov['Año'] = pd.to_datetime(mov['Año'], format='%Y').dt.year   # Asegurar formato correcto

# Gráfico de tendencia mensual por tipo de carga
plt.figure(figsize=(12, 6))
for tipo in mov['Tipo de carga'].unique():
    datos_tipo = mov[mov['Tipo de carga'] == tipo]
    tendencia_mensual = datos_tipo.groupby('Mes')['Tonelada'].mean()
    plt.plot(tendencia_mensual.index, tendencia_mensual.values, label=tipo)

plt.title('Tendencia Mensual por Tipo de Carga')
plt.xlabel('Mes')
plt.ylabel('Toneladas promedio')
plt.legend()
plt.grid()
plt.show()

# Diagrama de caja para las toneladas por tipo de carga
plt.figure(figsize=(12, 6))
mov.boxplot(column='Tonelada', by='Tipo de carga', grid=False)
plt.title('Distribución de Toneladas por Tipo de Carga')
plt.suptitle('')  # Quita el título automático de pandas
plt.xlabel('Tipo de Carga')
plt.ylabel('Toneladas')
plt.xticks(rotation=45)
plt.show()

# Fusionar datos para análisis de correlación
# Unir las tablas por el año
merged_data = mov.merge(cambio, on='Año').merge(pib, on='Año')

# Crear matriz de correlación
correlation_matrix = merged_data[['Tonelada', 'Compra', 'Venta', 'PIB']].corr()

# Visualizar matriz de correlación
plt.figure(figsize=(8, 6))
plt.imshow(correlation_matrix, cmap='coolwarm', interpolation='nearest')
plt.colorbar(label='Coeficiente de correlación')
plt.xticks(range(len(correlation_matrix.columns)), correlation_matrix.columns, rotation=45)
plt.yticks(range(len(correlation_matrix.columns)), correlation_matrix.columns)
plt.title('Matriz de Correlación')
plt.show()

