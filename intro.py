# Visualización inicial de datos
import pandas as pd
import matplotlib.pyplot as plt

data_file = "PuertoQuetzal.xlsx"
movimiento = pd.read_excel(data_file, sheet_name="movimientoportuario")
tipodecambio = pd.read_excel(data_file, sheet_name="tipodecambio")
pibanual = pd.read_excel(data_file, sheet_name="pibanual")

tipodecambio["Año"] = tipodecambio["Año"].astype(int)
pibanual["Año"] = pibanual["Año"].astype(int)
data = movimiento.merge(tipodecambio, on="Año", how="left")
data = data.merge(pibanual, on="Año", how="left")
data["Toneladas"] = pd.to_numeric(data["Toneladas"], errors="coerce")

# Gráfica 1: Distribución de toneladas por tipo de operación
operacion_toneladas = data.groupby(["Operación", "Puerto"])["Toneladas"].sum().unstack()
operacion_toneladas.plot(kind="bar", figsize=(10, 6))
plt.title("Distribución de Toneladas por Operación y Puerto")
plt.xlabel("Operación")
plt.ylabel("Toneladas")
plt.xticks(rotation=45)
plt.legend(title="Puerto")
plt.tight_layout()
plt.show()

# Gráfica 2: Promedio de toneladas por tipo de movimiento
# tipo_movimiento_toneladas = data.groupby("TipoDeMovimiento")["Toneladas"].mean()
# tipo_movimiento_toneladas.plot(kind="bar", figsize=(10, 6))
# plt.title("Promedio de Toneladas por Tipo de Movimiento")
# plt.xlabel("Tipo de Movimiento")
# plt.ylabel("Toneladas Promedio")
# plt.xticks(rotation=45)
# plt.tight_layout()
# plt.show()

# Gráfica 3: Tendencias anuales de toneladas
anual_toneladas = data.groupby(["Año", "Operación"])["Toneladas"].sum().unstack()
anual_toneladas.plot(figsize=(10, 6))
plt.title("Tendencias Anuales de Toneladas por Operación")
plt.xlabel("Año")
plt.ylabel("Toneladas")
plt.legend(title="Operación")
plt.tight_layout()
plt.show()

# Gráfica 4: Evolución del tipo de cambio (compra y venta) a lo largo de los años
# tipodecambio.plot(x="Año", y=["Compra", "Venta"], kind="line", figsize=(10, 6), marker="o")
# plt.title("Evolución del Tipo de Cambio (Compra y Venta)")
# plt.xlabel("Año")
# plt.ylabel("Tipo de Cambio")
# plt.legend(["Compra", "Venta"])
# plt.grid()
# plt.tight_layout()
# plt.show()

# Gráfica 5: Evolución del PIB anual
# pibanual.plot(x="Año", y="PIB", kind="line", figsize=(10, 6), color="green", marker="o")
# plt.title("Evolución del PIB Anual")
# plt.xlabel("Año")
# plt.ylabel("PIB")
# plt.grid()
# plt.tight_layout()
# plt.show()

# Gráfica 6: Comparación de toneladas movilizadas vs. PIB
toneladas_vs_pib = data.groupby("Año")[["Toneladas", "PIB"]].sum()
fig, ax1 = plt.subplots(figsize=(10, 6))

ax1.set_xlabel("Año")
ax1.set_ylabel("Toneladas", color="blue")
ax1.plot(toneladas_vs_pib.index, toneladas_vs_pib["Toneladas"], color="blue", marker="o", label="Toneladas")
ax1.tick_params(axis="y", labelcolor="blue")

ax2 = ax1.twinx()
ax2.set_ylabel("PIB", color="green")
ax2.plot(toneladas_vs_pib.index, toneladas_vs_pib["PIB"], color="green", marker="s", label="PIB")
ax2.tick_params(axis="y", labelcolor="green")

plt.title("Comparación de Toneladas Movilizadas vs. PIB Anual")
fig.tight_layout()
plt.show()

# Gráfica 7: Comparación de toneladas movilizadas vs. tipo de cambio
toneladas_vs_cambio = data.groupby("Año")[["Toneladas", "Compra"]].sum()
fig, ax1 = plt.subplots(figsize=(10, 6))

ax1.set_xlabel("Año")
ax1.set_ylabel("Toneladas", color="blue")
ax1.plot(toneladas_vs_cambio.index, toneladas_vs_cambio["Toneladas"], color="blue", marker="o", label="Toneladas")
ax1.tick_params(axis="y", labelcolor="blue")

ax2 = ax1.twinx()
ax2.set_ylabel("Tipo de Cambio (Compra)", color="green")
ax2.plot(toneladas_vs_cambio.index, toneladas_vs_cambio["Compra"], color="green", marker="s", label="Tipo de Cambio")
ax2.tick_params(axis="y", labelcolor="green")

plt.title("Comparación de Toneladas Movilizadas vs. Tipo de Cambio (Compra)")
fig.tight_layout()
plt.show()
