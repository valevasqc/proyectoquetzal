import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA


data = pd.ExcelFile("Flujo _de_Carga_Tidy Data .xlsx")


movimiento_portuario = data.parse('Movimiento Portuario ')
tipo_cambio = data.parse('Tipo de Cambio ')
pib_anual = data.parse('PIB Anual ')

# Limpieza y estandarización de los nombres de columnas
movimiento_portuario.columns = movimiento_portuario.columns.str.strip()
tipo_cambio.columns = tipo_cambio.columns.str.strip()
pib_anual.columns = pib_anual.columns.str.strip()


movimiento_merged = movimiento_portuario.merge(tipo_cambio, on="Año")
final_data = movimiento_merged.merge(pib_anual, on="Año")

# Datos climáticos 
climatic_data = {
    2016: {"Temperatura": 25.3, "Precipitacion": 1800},
    2017: {"Temperatura": 25.5, "Precipitacion": 1850},
    2018: {"Temperatura": 25.7, "Precipitacion": 1900},
    2019: {"Temperatura": 25.6, "Precipitacion": 1855},
    2020: {"Temperatura": 25.8, "Precipitacion": 1820},
    2021: {"Temperatura": 25.9, "Precipitacion": 1805},
    2022: {"Temperatura": 26.0, "Precipitacion": 1780},
    2023: {"Temperatura": 26.1, "Precipitacion": 1755},
}

final_data["Temperatura"] = final_data["Año"].map(lambda x: climatic_data[x]["Temperatura"])
final_data["Precipitacion"] = final_data["Año"].map(lambda x: climatic_data[x]["Precipitacion"])

# datos anuales a nivel mensual
final_data["Toneladas_Mensual"] = final_data["Toneladas"] / 12

monthly_data = []
for _, row in final_data.iterrows():
    for mes in range(1, 13):
        monthly_data.append({
            "Año": row["Año"],
            "Mes": mes,
            "Puerto": row["Puerto"],
            "Toneladas_Mensual": row["Toneladas"] / 12,
            "Compra": row["Compra"],
            "PIB (Millones Q)": row["PIB (Millones Q)"],
            "Temperatura": row["Temperatura"],
            "Precipitacion": row["Precipitacion"]
        })

df_monthly = pd.DataFrame(monthly_data)


X = df_monthly[["Compra", "PIB (Millones Q)", "Temperatura", "Precipitacion"]]
y = df_monthly["Toneladas_Mensual"]

# Normalización (Min-Max Scaling)
scaler = MinMaxScaler()
X_normalized = scaler.fit_transform(X)

# Representación matricial y cálculo manual de los coeficientes beta
X_matrix = np.hstack((np.ones((X_normalized.shape[0], 1)), X_normalized))  
Y_matrix = y.values.reshape(-1, 1)
beta = np.linalg.inv(X_matrix.T @ X_matrix) @ X_matrix.T @ Y_matrix

# Determinante de X^T X
determinante = np.linalg.det(X_matrix.T @ X_matrix)

# Eigenvalores y eigenvectores de X^T X
eigvals, eigvecs = np.linalg.eig(X_matrix.T @ X_matrix)

# Descomposición en Componentes Principales 
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_normalized)


X_train_pca, X_test_pca, y_train, y_test = train_test_split(X_pca, y, test_size=0.2, random_state=42)
model_pca = LinearRegression()
model_pca.fit(X_train_pca, y_train)


y_pred_pca = model_pca.predict(X_test_pca)
r2_pca = r2_score(y_test, y_pred_pca)
mse_pca = mean_squared_error(y_test, y_pred_pca)




plt.figure(figsize=(10, 6))
plt.scatter(y_test, y_pred_pca, alpha=0.7, label="Predicciones vs. Reales")
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], '--r', linewidth=2, label="Línea Ideal")
plt.xlabel("Valores Reales (Toneladas Mensuales)")
plt.ylabel("Predicciones (Toneladas Mensuales)")
plt.title("Valores Reales vs. Predicciones (Modelo PCA)")
plt.legend()
plt.grid()
plt.show()

# Comparar gráficas de normalización vs PCA
fig, axs = plt.subplots(1, 2, figsize=(16, 6))

# Gráfica antes de PCA (normalización solamente)
axs[0].scatter(X_normalized[:, 0], y, alpha=0.7, label="Normalización")
axs[0].set_xlabel("Tipo de Cambio (Compra, Normalizado)")
axs[0].set_ylabel("Toneladas Mensuales")
axs[0].set_title("Relación: Tipo de Cambio y Toneladas (Normalizado)")
axs[0].grid()

# Gráfica después de PCA
axs[1].scatter(X_pca[:, 0], y, alpha=0.7, color='orange', label="PCA")
axs[1].set_xlabel("Componente Principal 1")
axs[1].set_ylabel("Toneladas Mensuales")
axs[1].set_title("Relación: PCA y Toneladas")
axs[1].grid()

plt.show()

coef_df = pd.DataFrame({
"Variable": ["Intercepto", "Tipo de Cambio (Compra)", "PIB", "Temperatura", "Precipitación"],
"Coeficiente": beta.flatten(),
"Interpretación": [
"Base de la predicción",
"Impacto positivo significativo",
"Relación marginal negativa",
"Impacto positivo significativo",
"Impacto negativo en la demanda"
]
})


print("\nResultados adicionales:")
print(f"Determinante de X^T X: {determinante}")
print(f"Autovalores: {eigvals}")
print(f"R² del modelo PCA: {r2_pca}")
print(f"Error Cuadrático Medio (MSE): {mse_pca}")
print(coef_df)
#Ecuación del modelo 
print(f"Ecuación del modelo: y = {beta[0, 0]:.2f} + ({beta[1, 0]:.2f} * x1) + ({beta[2, 0]:.2f} * x2) + ({beta[3, 0]:.2f} * x3) + ({beta[4, 0]:.2f} * x4)")

