import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(layout="wide")
st.title("Meu Aplicativo Streamlit")
st.write("Olá! Este é meu aplicativo.")

# Exemplo de gráfico simples:
x = np.linspace(0, 10, 100)
y = np.sin(x)
fig, ax = plt.subplots()
ax.plot(x, y)
st.pyplot(fig)
