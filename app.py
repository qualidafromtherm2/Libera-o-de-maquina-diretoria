import streamlit as st
import streamlit.components.v1 as components

html_code = r"""
<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8">
    <title>Liberação de Máquina</title>
    <!-- Importa a fonte Roboto do Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap" rel="stylesheet">
    <style>
      /* Reset e configurações gerais */
      * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
      }
      body {
        font-family: 'Roboto', Arial, sans-serif;
        /* Removido o background-color para deixar o fundo padrão */
        color: #444;
        line-height: 1.6;
        padding: 30px;
      }
      h2, h3, h4 {
        margin-bottom: 20px;
      }
      h2 {
        color: #333;
        text-align: center;
        margin-bottom: 30px;
      }
      input, textarea, button {
        padding: 12px;
        font-size: 16px;
        margin: 8px 0;
        width: 100%;
        border: 1px solid #ccc;
        border-radius: 4px;
      }
      input:focus, textarea:focus {
        outline: none;
        border-color: #4285f4;
        box-shadow: 0 0 5px rgba(66, 133, 244, 0.5);
      }
      button {
        cursor: pointer;
        background-color: #4285f4;
        border: none;
        color: #fff;
        font-weight: 500;
        transition: background-color 0.3s ease;
      }
      button:hover {
        background-color: #357ae8;
      }
      /* Botões específicos */
      #btn-aprovado {
        background-color: #28a745;
      }
      #btn-aprovado:hover {
        background-color: #218838;
      }
      /* Layout dos botões */
      #botoes-container {
        display: flex;
        gap: 15px;
        margin-top: 20px;
      }
      #botoes-container button {
        flex: 1;
      }
      /* Layout de inputs */
      .input-modelo-container {
        max-width: 500px;
        margin: 0 auto 20px auto;
        display: flex;
        flex-direction: column;
        gap: 10px;
      }
      #valorE {
        font-weight: 500;
        font-size: 16px;
        color: #555;
      }
      /* Estilo para as tabelas */
      table {
        width: 100%;
        border-collapse: collapse;
        margin: 20px 0;
        background-color: #fff;
        border-radius: 5px;
        overflow: hidden;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
      }
      caption {
        background-color: #4285f4;
        color: #fff;
        font-weight: 500;
        font-size: 18px;
        padding: 10px;
      }
      th, td {
        border: 1px solid #e0e0e0;
        padding: 12px;
        text-align: center;
      }
      th {
        background-color: #4285f4;
        color: #fff;
      }
      tr:nth-child(even) {
        background-color: #f7f7f7;
      }
      tr:hover {
        background-color: #f1f1f1;
      }
      /* Registro de dados */
      .registro {
        margin-bottom: 30px;
        padding: 15px;
        background-color: #fff;
        border-radius: 5px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.08);
      }
      /* Modal de Senha */
      .modal {
        display: none;
        position: fixed;
        z-index: 1000;
        left: 0;
        top: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0,0,0,0.5);
        align-items: center;
        justify-content: center;
      }
      .modal-content {
        background-color: #fff;
        padding: 25px;
        border-radius: 8px;
        width: 300px;
        position: relative;
        box-shadow: 0 2px 10px rgba(0,0,0,0.2);
      }
      .close {
        position: absolute;
        right: 15px;
        top: 10px;
        font-size: 24px;
        font-weight: 700;
        color: #aaa;
        cursor: pointer;
      }
      .close:hover {
        color: #000;
      }
      /* Spinner Global */
      #global-spinner-overlay {
        display: none;
        position: fixed;
        z-index: 9999;
        left: 0;
        top: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0,0,0,0.4);
      }
      #global-spinner {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        border: 8px solid #f3f3f3;
        border-radius: 50%;
        border-top: 8px solid #4285f4;
        width: 50px;
        height: 50px;
        animation: spin 1s linear infinite;
      }
      @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
      }
      /* Spinner do modal */
      .spinner {
        position: absolute;
        right: 10px;
        top: 50%;
        transform: translateY(-50%);
        width: 20px;
        height: 20px;
        border: 3px solid #f3f3f3;
        border-top: 3px solid #4285f4;
        border-radius: 50%;
        animation: spin 1s linear infinite;
      }
      .input-container {
        position: relative;
        margin-bottom: 15px;
      }
      /* Categorias e peças */
      .categoria {
        margin-bottom: 20px;
      }
      .categoria h4 {
        background-color: #6c757d;
        color: #fff;
        padding: 10px;
        border-radius: 4px;
      }
      .categoria table {
        margin-top: 10px;
      }
      /* Tabelas comparáveis */
      table.comparavel {
        border: 2px solid #ff9800;
      }
      table.comparavel caption {
        background-color: #ff9800;
      }
    </style>
    <script>
      // Variáveis e funções JavaScript (exemplo simplificado)
      let modeloGlobal = "";
      function showGlobalSpinner() {
        document.getElementById('global-spinner-overlay').style.display = 'block';
      }
      function hideGlobalSpinner() {
        document.getElementById('global-spinner-overlay').style.display = 'none';
      }
      function buscarDados() {
        let opDigitada = document.getElementById('ordem').value.trim();
        if (!opDigitada) {
          alert('Digite a OP.');
          return;
        }
        showGlobalSpinner();
        // Simulação de busca
        setTimeout(() => { 
          hideGlobalSpinner();
          document.getElementById('valorE').innerText = "Modelo: Exemplo";
        }, 1500);
      }
      function aprovado() {
        let op = document.getElementById('ordem').value.trim();
        if (!op) {
          alert('Digite a OP antes de aprovar.');
          return;
        }
        document.getElementById('modalSenha').style.display = 'flex';
      }
      function fecharModal() {
        document.getElementById('modalSenha').style.display = 'none';
        document.getElementById('spinner').style.display = 'none';
        document.getElementById('senha').value = '';
      }
      function confirmarSenha() {
        let senha = document.getElementById('senha').value.trim();
        if (!senha) {
          alert("Digite a senha.");
          return;
        }
        document.getElementById('spinner').style.display = 'block';
        setTimeout(() => {
          document.getElementById('spinner').style.display = 'none';
          alert("Senha confirmada!");
          fecharModal();
        }, 1500);
      }
      window.onclick = function(event) {
        let modal = document.getElementById('modalSenha');
        if (event.target == modal) {
          fecharModal();
        }
      };
    </script>
  </head>
  <body>
    <h2>Liberação de Máquina</h2>
    <div class="input-modelo-container">
      <input type="text" id="ordem" placeholder="Digite a OP">
      <span id="valorE">Modelo:</span>
    </div>
    <div id="botoes-container">
      <button onclick="buscarDados()">Buscar</button>
      <button id="btn-aprovado" onclick="aprovado()">Aprovado</button>
      <button id="btn-comparar" onclick="alert('Comparar')" disabled>Comparar</button>
    </div>
    <div id="tabela-rastreabilidade-container">
      <h3>OP's aguardando liberação</h3>
      <table id="tabela-rastreabilidade">
        <thead>
          <tr>
            <th>Modelo</th>
            <th>OP</th>
          </tr>
        </thead>
        <tbody></tbody>
      </table>
    </div>
    <div id="resultado"></div>
    <div id="modalSenha" class="modal">
      <div class="modal-content">
        <span class="close" onclick="fecharModal()">&times;</span>
        <h3>Inserir Senha</h3>
        <div class="input-container">
          <input type="password" id="senha" placeholder="Digite a senha">
          <div id="spinner" class="spinner" style="display: none;"></div>
        </div>
        <button onclick="confirmarSenha()">Confirmar</button>
      </div>
    </div>
    <div id="global-spinner-overlay">
      <div id="global-spinner"></div>
    </div>
  </body>
</html>
"""

components.html(html_code, height=1200, scrolling=True)



import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

# Configuração das credenciais e escopo
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
CREDS = Credentials.from_service_account_file("credentials.json", scopes=SCOPES)
client = gspread.authorize(CREDS)

# ID da planilha (extraído da URL)
SPREADSHEET_ID = "1wQtlPKVhkXNzsVTYfbEaXDkW9mSBHtkO2H5RV6KFxsY"

def carregar_tabela_rastreabilidade():
    try:
        # Abrir a planilha e a aba "Rastreabilidade"
        sheet = client.open_by_key(SPREADSHEET_ID).worksheet("Rastreabilidade")
        # Obter todos os dados (lista de listas)
        dados = sheet.get_all_values()
        
        # Converter para DataFrame para facilitar a manipulação
        df = pd.DataFrame(dados[1:], columns=dados[0])
        
        # Supondo que as colunas na planilha estão nomeadas conforme as letras:
        # Caso não tenham nomes, podemos criar nomes temporários.
        # Aqui, vamos assumir que a coluna C se refere a "Modelo" e a coluna D a "OP".
        # Se os cabeçalhos não estiverem assim, você pode renomeá-los:
        # Exemplo: df.columns = ["A", "B", "Modelo", "OP", "E", "F", "G", "H", ...]
        # Se a coluna H for a oitava coluna (índice 7), filtramos linhas onde ela está vazia.
        
        # Filtrar registros onde a coluna H está vazia:
        df_filtrado = df[df.iloc[:, 7] == ""]  # índice 7 corresponde à coluna H
        
        # Selecionar apenas as colunas Modelo (índice 2) e OP (índice 3)
        df_resultado = df_filtrado.iloc[:, [2, 3]]
        # Renomear as colunas, se desejar:
        df_resultado.columns = ["Modelo", "OP"]
        
        return df_resultado
    except Exception as e:
        st.error(f"Erro ao carregar os dados: {e}")
        return None

