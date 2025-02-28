import streamlit as st

st.title("Minha Página com Dois Campos")

# Criação dos campos de entrada
teste1 = st.text_input("Teste 1")
teste2 = st.text_input("Teste 2")

# Exibindo o que foi digitado
st.write("Você digitou:")
st.write("Teste 1:", teste1)
st.write("Teste 2:", teste2)
