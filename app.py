import streamlit as st
import pandas as pd

st.set_page_config(page_title="Simulador de Préstamos SV", page_icon="💰")

st.title("💰 Simulador de Préstamos – El Salvador")

EXCEL_FILE = "Simulador_Prestamos_Estetico_El_Salvador.xlsx"

def cuota_mensual(monto, tasa_anual, meses):
    tasa_mensual = tasa_anual / 100 / 12
    return monto * (tasa_mensual * (1 + tasa_mensual)**meses) / ((1 + tasa_mensual)**meses - 1)

user_df = pd.read_excel(EXCEL_FILE, sheet_name="Datos_Usuario", header=None)
bancos_df = pd.read_excel(EXCEL_FILE, sheet_name="Bancos")

monto = st.number_input("Monto del préstamo ($)", value=float(user_df.iloc[1,1]))
plazo = st.number_input("Plazo (meses)", value=int(user_df.iloc[2,1]))
ingreso = st.number_input("Ingreso mensual ($)", value=float(user_df.iloc[3,1]))
ratio = st.slider("Porcentaje máximo de cuota (%)", 10, 50, 30) / 100

cuota_max = ingreso * ratio

resultados = []

for _, b in bancos_df.iterrows():
    cuota = cuota_mensual(monto, b["Tasa Anual (%)"], plazo)
    seguro = monto * b["Seguro Mensual (%)"] / 100
    cuota_total = cuota + seguro
    comision = monto * b["Comisión Apertura (%)"] / 100
    costo_total = cuota_total * plazo + comision

    resultados.append({
        "Banco": b["Banco"],
        "Cuota Mensual": round(cuota_total, 2),
        "Costo Total": round(costo_total, 2),
        "Evaluación": "✅ CONVIENE" if cuota_total <= cuota_max else "❌ NO CONVIENE"
    })

df = pd.DataFrame(resultados).sort_values("Costo Total")

st.subheader("📊 Resultados")
st.dataframe(df, use_container_width=True)

st.success(f"🏆 Mejor opción hoy: {df.iloc[0]['Banco']}")
