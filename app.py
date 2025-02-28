import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

# ---------------------------
# Backend: Acesso à Planilha
# ---------------------------
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
CREDS = Credentials.from_service_account_file("credentials.json", scopes=SCOPES)
client = gspread.authorize(CREDS)
SPREADSHEET_ID = "1wQtlPKVhkXNzsVTYfbEaXDkW9mSBHtkO2H5RV6KFxsY"

def carregar_tabela_rastreabilidade():
    try:
        sheet = client.open_by_key(SPREADSHEET_ID).worksheet("Rastreabilidade")
        dados = sheet.get_all_values()
        df = pd.DataFrame(dados[1:], columns=dados[0])
        # Filtra registros onde a coluna H (oitava coluna) está vazia (após remover espaços)
        df_filtrado = df[df.iloc[:, 7].str.strip() == ""]
        # Seleciona as colunas "Modelo" e "OP"
        df_resultado = df_filtrado[["Modelo", "OP"]]
        # Remove duplicatas com base na coluna "OP"
        df_resultado = df_resultado.drop_duplicates(subset="OP", keep="first")
        # Reseta o índice para não exibir a coluna extra de índice
        df_resultado.reset_index(drop=True, inplace=True)
        return df_resultado
    except Exception as e:
        st.error(f"Erro ao carregar os dados: {e}")
        return pd.DataFrame(columns=["Modelo", "OP"])

# ---------------------------
# Interface com Streamlit (sem HTML customizado)
# ---------------------------
def main():
    st.title("Liberação de Máquina")
    
    # Campo para inserir a OP (a lógica dos botões pode ser adicionada posteriormente)
    op = st.text_input("Digite a OP:", "")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Buscar"):
            st.info(f"Buscando dados para a OP: {op}")
    with col2:
        if st.button("Aprovado"):
            st.info(f"Aprovação para a OP: {op}")
    with col3:
        if st.button("Comparar"):
            st.info(f"Comparando dados para a OP: {op}")
    
    st.subheader("OP's Aguardando Liberação")
    tabela = carregar_tabela_rastreabilidade()
    
    if tabela is not None and not tabela.empty:
        # Ajuste o parâmetro 'width' para aumentar a largura da tabela
        st.dataframe(tabela, width=1000)
    else:
        st.info("Nenhuma OP encontrada para liberação.")

if __name__ == "__main__":
    main()