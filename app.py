import streamlit as st
import streamlit.components.v1 as components

# Código HTML completo que você forneceu
html_code = """
<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8">
    <title>Liberação de Máquina</title>
    <style>
      /* Seu CSS aqui */
      body {
        font-family: Arial, sans-serif;
        background-color: #f7f7f7;
        margin: 20px;
      }
      h2 {
        color: #333;
      }
      input, textarea, button {
        padding: 10px;
        font-size: 16px;
        margin: 5px 0;
        width: 100%;
        box-sizing: border-box;
      }
      button {
        cursor: pointer;
        background-color: #4285f4;
        border: none;
        color: #fff;
        border-radius: 4px;
        margin-top: 10px;
      }
      button:hover {
        background-color: #357ae8;
      }
      /* Botões específicos */
      #btn-aprovado {
        background-color: #28a745; /* Verde */
      }
      #btn-aprovado:hover {
        background-color: #218838;
      }
      
      #resultado {
        margin-top: 20px;
      }
      table {
        width: 100%;
        border-collapse: collapse;
        margin-bottom: 20px;
        background-color: #fff;
      }
      caption {
        caption-side: top;
        font-weight: bold;
        font-size: 18px;
        margin-bottom: 10px;
      }
      th, td {
        border: 1px solid #ddd;
        padding: 8px;
        text-align: left;
      }
      th {
        background-color: #4285f4;
        color: white;
      }
      tr:nth-child(even) {
        background-color: #f2f2f2;
      }
      .registro {
        margin-bottom: 30px;
        padding-bottom: 10px;
        border-bottom: 2px solid #ccc;
      }
      /* Estilo para o valor do Modelo */
      #valorE {
        margin-left: 20px;
        font-weight: bold;
        font-size: 16px;
        color: #333;
        display: block;
      }
      /* Container para os botões */
      #botoes-container {
        display: flex;
        gap: 10px;
        margin-top: 20px;
      }
      #botoes-container button {
        flex: 1;
        padding: 10px;
        font-size: 16px;
      }
      /* Modal de Senha */
      .modal {
        display: none; /* Oculto por padrão */
        position: fixed; /* Fica fixo na tela */
        z-index: 1; /* Fica na frente */
        left: 0;
        top: 0;
        width: 100%;
        height: 100%;
        overflow: auto;
        background-color: rgba(0,0,0,0.4);
      }
      .modal-content {
        background-color: #fefefe;
        margin: 15% auto;
        padding: 20px;
        border: 1px solid #888;
        width: 300px;
        border-radius: 5px;
      }
      .close {
        color: #aaa;
        float: right;
        font-size: 24px;
        font-weight: bold;
        cursor: pointer;
      }
      .close:hover,
      .close:focus {
        color: black;
        text-decoration: none;
      }
      /* Tabela de Rastreabilidade */
      #tabela-rastreabilidade-container {
        margin-top: 20px;
      }
      #tabela-rastreabilidade {
        width: 100%;
        border-collapse: collapse;
        margin-bottom: 20px;
        background-color: #fff;
      }
      #tabela-rastreabilidade th, #tabela-rastreabilidade td {
        border: 1px solid #ddd;
        padding: 8px;
        text-align: left;
      }
      #tabela-rastreabilidade th {
        background-color: #6c757d;
        color: white;
      }
      #tabela-rastreabilidade tr:nth-child(even) {
        background-color: #f2f2f2;
      }
      #tabela-rastreabilidade tr {
        cursor: pointer;
      }
      #tabela-rastreabilidade tr:hover {
        background-color: #d1ecf1;
      }
      /* Spinner global (overlay) */
      #global-spinner-overlay {
        display: none; /* Oculto por padrão */
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
        border: 10px solid #f3f3f3;
        border-radius: 50%;
        border-top: 10px solid #3498db;
        width: 60px;
        height: 60px;
        animation: spin 1s linear infinite;
      }
      @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
      }
      /* Spinner do modal de senha (pequeno) */
      .spinner {
        position: absolute;
        right: 10px;
        top: 50%;
        transform: translateY(-50%);
        width: 20px;
        height: 20px;
        border: 3px solid #f3f3f3;
        border-top: 3px solid #3498db;
        border-radius: 50%;
        animation: spin 1s linear infinite;
      }
      .input-container {
        position: relative;
        margin-bottom: 15px;
      }
      table {
        width: auto; /* Permite que a tabela expanda conforme necessário */
      }
      th, td {
        min-width: 100px; /* Define uma largura mínima para as células */
        text-align: center; /* Centraliza o conteúdo */
      }
      /* Estilos para Categorias */
      .categoria {
        margin-bottom: 20px;
      }
      .categoria h4 {
        background-color: #6c757d;
        color: white;
        padding: 8px;
        border-radius: 4px;
      }
      .categoria table {
        margin-top: 10px;
        width: 100%;
        border-collapse: collapse;
        background-color: #fff;
        border-radius: 5px;
        overflow: hidden;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
      }
      .categoria table th, .categoria table td {
        border: 1px solid #ddd;
        padding: 10px;
        text-align: center;
      }
      .categoria table th {
        background-color: #17a2b8;
        color: white;
      }
      .categoria table tr:nth-child(even) {
        background-color: #f9f9f9;
      }
      .categoria table tr:hover {
        background-color: #e2f0f9;
      }
      /* Estilos para Tabelas Comparáveis */
      table.comparavel {
        border: 2px solid #ff9800; /* Borda laranja */
      }
      table.comparavel caption {
        color: #ff9800; /* Título laranja */
      }
      table.comparavel th, table.comparavel td {
        border: 1px solid #ddd;
        padding: 10px;
        text-align: center;
      }
      table.comparavel th {
        background-color: #ff9800;
        color: white;
      }
      table.comparavel tr:nth-child(even) {
        background-color: #fff3e0;
      }
      table.comparavel tr:hover {
        background-color: #ffe0b2;
      }
    </style>
    <script>
      // Seu código JavaScript (mantido conforme fornecido)
      let modeloGlobal = "";
      let rastreabilidadeGlobal = {};
      function formatNumber(value) {
        if (typeof value === 'number') {
          return value.toFixed(2);
        } else if (typeof value === 'string' && !isNaN(parseFloat(value))) {
          return parseFloat(value).toFixed(2);
        }
        return value;
      }
      function showGlobalSpinner() {
        document.getElementById('global-spinner-overlay').style.display = 'block';
      }
      function hideGlobalSpinner() {
        document.getElementById('global-spinner-overlay').style.display = 'none';
      }
      function processarCampo(campo) {
        if (!campo) return campo;
        let partes = campo.split('/');
        let novoCampo = partes.length > 1 ? partes[partes.length - 1].trim() : partes[0].trim();
        if (novoCampo.toUpperCase() === "2 COMPRESSORES") {
          novoCampo = "2° COMPRESSOR";
        }
        return novoCampo;
      }
      function extrairUltimoTexto(modeloCompleto) {
        if (!modeloCompleto) return modeloCompleto;
        if (modeloCompleto.indexOf('- ') === -1) {
          return modeloCompleto.trim();
        }
        let partes = modeloCompleto.split('- ');
        return partes[partes.length - 1].trim();
      }
      function buscarDados() {
        let opDigitada = document.getElementById('ordem').value.trim();
        if (!opDigitada) {
          alert('Digite a OP.');
          return;
        }
        if (opDigitada.toUpperCase().startsWith('F')) {
          showGlobalSpinner();
          google.script.run
            .withSuccessHandler((res) => {
              hideGlobalSpinner();
              if (res && res.OPEncontrada) {
                document.getElementById('ordem').value = res.OPEncontrada;
                buscarDados();
              } else {
                alert("Nenhuma OP encontrada para esse modelo.");
              }
            })
            .withFailureHandler((err) => {
              hideGlobalSpinner();
              alert("Erro ao buscar OP por modelo: " + err.message);
              console.error(err);
            })
            .buscarOPPorModelo(opDigitada);
          return;
        }
        showGlobalSpinner();
        document.getElementById('resultado').innerHTML = "";
        document.getElementById('valorE').innerText = "Modelo:";
        google.script.run
          .withSuccessHandler((res) => {
            hideGlobalSpinner();
            tratarResultado(res);
          })
          .withFailureHandler((err) => {
            hideGlobalSpinner();
            alert("Erro ao buscar dados de produção: " + err.message);
            console.error(err);
          })
          .buscarDadosPlanilha(opDigitada);
      }
      function tratarResultado(resultadoCompleto) {
        console.log("Resultado Completo:", resultadoCompleto);
        let container = document.getElementById('resultado');
        container.innerHTML = "";
        if (resultadoCompleto.Erro) {
          container.innerHTML = '<p style="color: red;">' + resultadoCompleto.Erro + '</p>';
          return;
        }
        if (resultadoCompleto.registros && resultadoCompleto.registros.length > 0) {
          resultadoCompleto.registros.forEach((reg) => {
            let divReg = document.createElement('div');
            divReg.className = "registro";
            let htmlTabelas = "";
            if (reg["1° teste"] && reg["1° teste"].length > 0) {
              htmlTabelas += montarTabela(reg["1° teste"], "1° teste");
            }
            if (reg["Teste final"] && reg["Teste final"].length > 0) {
              htmlTabelas += montarTabela(reg["Teste final"], "Teste final");
            }
            divReg.innerHTML = htmlTabelas;
            container.appendChild(divReg);
          });
        } else {
          container.innerHTML = '<p>Nenhum dado encontrado na Produção.</p>';
        }
        google.script.run
          .withSuccessHandler(function(modelo) {
            modeloGlobal = modelo;
            document.getElementById('valorE').innerText = "Modelo: " + (modeloGlobal || "N/A");
            if (modeloGlobal) {
              showGlobalSpinner();
              google.script.run
                .withSuccessHandler((res) => {
                  hideGlobalSpinner();
                  tratarRastreabilidade(res);
                })
                .withFailureHandler((err) => {
                  hideGlobalSpinner();
                  alert("Erro ao buscar rastreabilidade: " + err.message);
                  console.error(err);
                })
                .buscarRastreabilidadePorModelo(modeloGlobal);
            }
          })
          .withFailureHandler((err) => {
            alert("Erro ao buscar Modelo: " + err.message);
            console.error(err);
          })
          .buscarModeloPorOP(document.getElementById('ordem').value.trim());
        document.getElementById('btn-comparar').disabled = false;
      }
      function montarTabela(dadosArray, titulo) {
        let html = '<table';
        if (titulo === "1° teste" || titulo === "Teste final") {
          html += ' class="comparavel">';
        } else {
          html += '>';
        }
        html += '<caption>' + titulo + '</caption>';
        html += '<tr><th>Nome do teste</th><th>Teste atual</th></tr>';
        dadosArray.forEach(item => {
          let campoProc = processarCampo(item.campo);
          if (item.valor === undefined || item.valor === null || item.valor === "") return;
          let valorFormatado = formatNumber(item.valor);
          html += '<tr><td>' + campoProc + '</td><td>' + valorFormatado + '</td></tr>';
        });
        html += '</table>';
        return html;
      }
      function tratarRastreabilidade(dados) {
        let container = document.getElementById('resultado');
        if (dados.Erro) {
          container.innerHTML += '<p style="color:red;">' + dados.Erro + '</p>';
          return;
        }
        if (!dados || Object.keys(dados).length === 0) {
          container.innerHTML += '<p>Nenhum dado de Rastreabilidade encontrado.</p>';
          return;
        }
        let categorias = {};
        for (let chave in dados) {
          if (dados.hasOwnProperty(chave)) {
            let item = dados[chave];
            let categoria = item.categoria || "Desconhecida";
            if (!categorias[categoria]) {
              categorias[categoria] = [];
            }
            categorias[categoria].push(item);
          }
        }
        let listaPeçasDiv = document.createElement('div');
        listaPeçasDiv.id = "lista-pecas";
        let headerListaPeças = document.createElement('h3');
        headerListaPeças.innerText = "Lista de Peças";
        listaPeçasDiv.appendChild(headerListaPeças);
        container.appendChild(listaPeçasDiv);
        for (let categoria in categorias) {
          if (categorias.hasOwnProperty(categoria)) {
            let items = categorias[categoria];
            let divCategoria = document.createElement('div');
            divCategoria.className = "categoria";
            let tituloCategoria = document.createElement('h4');
            tituloCategoria.innerText = categoria;
            divCategoria.appendChild(tituloCategoria);
            let tabela = document.createElement('table');
            tabela.innerHTML = `
              <tr>
                <th>Código do produto</th>
                <th>Descrição do produto</th>
              </tr>
            `;
            items.forEach(item => {
              let tr = document.createElement('tr');
              let tdCodigo = document.createElement('td');
              tdCodigo.textContent = item.valorF;
              let tdDescricao = document.createElement('td');
              tdDescricao.textContent = item.valorG;
              tr.appendChild(tdCodigo);
              tr.appendChild(tdDescricao);
              tabela.appendChild(tr);
            });
            divCategoria.appendChild(tabela);
            listaPeçasDiv.appendChild(divCategoria);
          }
        }
      }
      function carregarTabelaRastreabilidade() {
        showGlobalSpinner();
        google.script.run
          .withSuccessHandler((res) => {
            hideGlobalSpinner();
            popularTabelaRastreabilidade(res);
          })
          .withFailureHandler((err) => {
            hideGlobalSpinner();
            alert("Erro ao carregar a tabela de Rastreabilidade: " + err.message);
            console.error(err);
          })
          .obterTabelaRastreabilidade();
      }
      function popularTabelaRastreabilidade(dados) {
        const tbody = document.querySelector('#tabela-rastreabilidade tbody');
        tbody.innerHTML = "";
        if (dados.Erro) {
          tbody.innerHTML = '<tr><td colspan="2" style="color:red;">' + dados.Erro + '</td></tr>';
          return;
        }
        if (!dados || dados.length === 0) {
          tbody.innerHTML = '<tr><td colspan="2">Nenhum dado encontrado.</td></tr>';
          return;
        }
        dados.forEach(item => {
          let tr = document.createElement('tr');
          let tdC = document.createElement('td');
          let tdD = document.createElement('td');
          tdC.textContent = item.colunaC;
          tdD.textContent = item.colunaD;
          tr.appendChild(tdC);
          tr.appendChild(tdD);
          tbody.appendChild(tr);
        });
        adicionarEventoCliqueTabelaRastreabilidade();
      }
      function adicionarEventoCliqueTabelaRastreabilidade() {
        let linhas = document.querySelectorAll('#tabela-rastreabilidade tbody tr');
        linhas.forEach(linha => {
          linha.addEventListener('click', function() {
            let opClicada = this.cells[1].innerText;
            if (opClicada) {
              document.getElementById('ordem').value = opClicada;
              buscarDados();
            }
          });
        });
      }
      function aprovado() {
        let op = document.getElementById('ordem').value.trim();
        if (!op) {
          alert('Digite a OP antes de aprovar.');
          return;
        }
        document.getElementById('modalSenha').style.display = 'block';
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
        let op = document.getElementById('ordem').value.trim();
        document.getElementById('spinner').style.display = 'block';
        let btnConfirmar = event.target;
        if (btnConfirmar) btnConfirmar.disabled = true;
        google.script.run
          .withSuccessHandler((res) => {
            document.getElementById('spinner').style.display = 'none';
            if (btnConfirmar) btnConfirmar.disabled = false;
            if (res.sucesso) {
              alert(`OP "${op}" aprovada! Linhas atualizadas: ${res.linhasAtualizadas}.`);
              removerOPDaTabela(op);
            } else {
              alert("Falha ao aprovar OP: " + res.mensagem);
            }
            fecharModal();
          })
          .withFailureHandler((err) => {
            document.getElementById('spinner').style.display = 'none';
            if (btnConfirmar) btnConfirmar.disabled = false;
            alert("Erro ao aprovar a OP: " + err.message);
            fecharModal();
          })
          .aprovarOP(op, senha);
      }
      function removerOPDaTabela(ordemProducao) {
        let tabela = document.getElementById('tabela-rastreabilidade');
        let linhas = tabela.getElementsByTagName('tr');
        for (let i = 1; i < linhas.length; i++) {
          let celulaOP = linhas[i].getElementsByTagName('td')[1];
          if (celulaOP && celulaOP.textContent.trim().toLowerCase() === ordemProducao.trim().toLowerCase()) {
            tabela.deleteRow(i);
            break;
          }
        }
      }
      window.onclick = function(event) {
        let modal = document.getElementById('modalSenha');
        if (event.target == modal) {
          fecharModal();
        }
      };
      window.onload = function() {
        carregarTabelaRastreabilidade();
      };
      function comparar() {
        const opDigitada = document.getElementById('ordem').value.trim();
        const modelo = modeloGlobal;
        if (!opDigitada || !modelo) {
          alert('Digite a OP e realize a busca antes de comparar.');
          return;
        }
        showGlobalSpinner();
        google.script.run
          .withSuccessHandler((res) => {
            hideGlobalSpinner();
            tratarResultadoComparacao(res);
          })
          .withFailureHandler((err) => {
            hideGlobalSpinner();
            alert("Erro ao comparar dados: " + err.message);
            console.error(err);
          })
          .comparar(opDigitada, modelo);
      }
      function tratarResultadoComparacao(resultados) {
        console.log("Resultados recebidos:", resultados);
        function removerPrefixoTeste(campo) {
          if (!campo) {
            console.log("removerPrefixoTeste: Campo está vazio ou indefinido.");
            return campo;
          }
          let campoProcessado = campo.replace(/^\dº TESTE \/ /, '').trim();
          console.log(`removerPrefixoTeste: "${campo}" transformado em "${campoProcessado}"`);
          return campoProcessado;
        }
        let container = document.getElementById('resultado');
        if (resultados.Erro) {
          console.error("Erro recebido:", resultados.Erro);
          container.innerHTML = '<p style="color: red;">' + resultados.Erro + '</p>';
          return;
        }
        let tabelasComparaveis = container.querySelectorAll('table.comparavel');
        resultados.forEach(aba => {
          console.log("Processando aba:", aba.aba);
          if (aba.registros && aba.registros.length > 0) {
            aba.registros.forEach((registro, index) => {
              console.log("Processando registro:", registro);
              tabelasComparaveis.forEach(tabela => {
                let cabecalho = tabela.getElementsByTagName('th');
                let linhas = tabela.getElementsByTagName('tr');
                let opValor = registro.OP;
                let novoCabecalho = document.createElement('th');
                novoCabecalho.textContent = `OP ${opValor}`;
                cabecalho[cabecalho.length - 1].insertAdjacentElement('afterend', novoCabecalho);
                console.log("Cabeçalho adicionado:", novoCabecalho.textContent);
                Array.from(linhas).forEach((linha, linhaIndex) => {
                  if (linhaIndex === 0) return;
                  let celulas = linha.getElementsByTagName('td');
                  let campo = celulas[0].textContent.trim();
                  let campoSemPrefixo = removerPrefixoTeste(campo);
                  console.log("Campo na tabela:", campo);
                  console.log("Campo sem prefixo:", campoSemPrefixo);
                  console.log("Valor no registro:", registro[campoSemPrefixo]);
                  if (registro[campoSemPrefixo] !== undefined && registro[campoSemPrefixo] !== "") {
                    let valorFormatado = formatNumber(registro[campoSemPrefixo]);
                    let novaCelula = document.createElement('td');
                    novaCelula.textContent = valorFormatado;
                    celulas[celulas.length - 1].insertAdjacentElement('afterend', novaCelula);
                    console.log("Valor adicionado:", valorFormatado);
                  } else {
                    console.log("Campo não encontrado ou valor vazio no registro.");
                    let novaCelula = document.createElement('td');
                    novaCelula.textContent = "N/A";
                    celulas[celulas.length - 1].insertAdjacentElement('afterend', novaCelula);
                  }
                });
              });
            });
          }
        });
      }
      function removerPrefixoTeste(campo) {
        if (!campo) return campo;
        return campo.replace(/^\dº TESTE \/ /, '').trim();
      }
      function montarTabelaComparacao(dadosArray, titulo) {
        let html = '<table>';
        html += '<caption>' + titulo + '</caption>';
        html += '<tr><th>Nome do teste</th><th>Resultado do teste</th></tr>';
        dadosArray.forEach(item => {
          Object.keys(item).forEach(campo => {
            if (item[campo]) {
              html += '<tr><td>' + campo + '</td><td>' + item[campo] + '</td></tr>';
            }
          });
        });
        html += '</table>';
        return html;
      }
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
      <button id="btn-comparar" onclick="comparar()" disabled>Comparar</button>
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

# Exibe o HTML completo no app
components.html(html_code, height=1200, scrolling=True)
