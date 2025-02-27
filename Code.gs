/**
 * ID global da planilha que contém todas as abas:
 * - PRODUÇÃO 2 - F/ ESCOPO
 * - PRODUÇÃO 1 - ESCOPO
 * - Ficha tecnica
 * - Rastreabilidade
 * - Outros dados
 */
var SPREADSHEET_ID = "1wQtlPKVhkXNzsVTYfbEaXDkW9mSBHtkO2H5RV6KFxsY";
var SPREADSHEET_ID2 = "1Kzg7LngaUig6t2CLabS1fhZ-iD5idrmv1ZesIUVOy1M";

/**
 * Converte uma referência de coluna (A, B, C, ... AA, AB, etc.) para seu índice numérico (base zero).
 */
function colunaParaIndice(col) {
  var letras = col.toUpperCase().split('');
  var indice = 0;
  for (var i = 0; i < letras.length; i++) {
    indice = indice * 26 + (letras[i].charCodeAt(0) - 64);
  }
  return indice - 1;
}

/**
 * Extrai os primeiros 5 dígitos de um texto.
 */
function extrairPrimeiros5Digitos(texto) {
  if (!texto) return "";
  var match = texto.toString().match(/\d{5}/); // Busca exatamente 5 dígitos consecutivos
  return match ? match[0] : texto.toString().substring(0, 5);
}

/**
 * Busca os dados de Produção conforme especificado, procurando a OP na coluna F.
 */
function buscarDadosProducao(ordemProducao) {
  try {
    Logger.log("Buscar Dados de Produção para OP: " + ordemProducao);

    var ss = SpreadsheetApp.openById(SPREADSHEET_ID2);

    // Configurações para as abas de produção, na ordem de busca
    var configAbas = [
      {
        nomeAba: 'PRODUÇÃO 2 - F/ ESCOPO',
        colunaBusca: 'F',
        colunasRetorno: ['D','X','Y','Z','AA','AB','AC','AD','AE','AJ','AY','BA','BB','BC'],
        extrairTesteFinal: true
      },
      {
        nomeAba: 'PRODUÇÃO 1 - ESCOPO',
        colunaBusca: 'F',
        colunasRetorno: ['D','T','U','V','W','X','Y','AA','AC','AD','AH','AL','AN','AO','AP','AR','AS','AT'],
        extrairTesteFinal: false
      }
    ];
    
    // Colunas usadas no "Teste final" apenas na 'PRODUÇÃO 2 - F/ ESCOPO'
    var testeFinalColunas = ['BD','BE','BF','BG','BH','BI','BJ','BK','BL','BM','BO','BP','BQ'];
    var testeFinalIndices = testeFinalColunas.map(colunaParaIndice);
    
    // Converter as colunas de busca e de retorno para índices
    configAbas.forEach(function(config) {
      config.indiceBusca = colunaParaIndice(config.colunaBusca);
      config.indicesRetorno = config.colunasRetorno.map(colunaParaIndice);
    });
    
    var resultados = [];
    var encontrou = false;
    
    for (var j = 0; j < configAbas.length; j++) {
      var config = configAbas[j];
      var sheet = ss.getSheetByName(config.nomeAba);
      if (!sheet) {
        Logger.log("Aba " + config.nomeAba + " não encontrada.");
        throw "Aba " + config.nomeAba + " não encontrada.";
      }
      
      var data = sheet.getDataRange().getValues();
      if (data.length < 1) {
        Logger.log("Aba " + config.nomeAba + " está vazia.");
        continue;
      }
      
      var cabecalho = data[0];
      Logger.log("Processando Aba: " + config.nomeAba);
      
      // Verifica cada linha, comparando a coluna F (ordemProducao)
      for (var i = 1; i < data.length; i++) {
        var valorBusca = data[i][config.indiceBusca];
        if (!valorBusca) continue;
        
        var opNaLinha = valorBusca.toString().trim().toLowerCase();
        var opProcurada = ordemProducao.trim().toLowerCase();
        
        if (opNaLinha === opProcurada) {
          // Monta a tabela "1° teste"
          var tabelaTeste = [];
          config.indicesRetorno.forEach(function(indice) {
            if (indice >= cabecalho.length) return;
            tabelaTeste.push({
              campo: cabecalho[indice],
              valor: data[i][indice]
            });
          });
          
          // Extrai os primeiros 5 dígitos da coluna D (que é uma das colunas retornadas)
          var valorColD = data[i][colunaParaIndice('D')];
          var firstFiveDigits = extrairPrimeiros5Digitos(valorColD);
          
          var registro = {
            "1° teste": tabelaTeste,
            "firstFiveDigits": firstFiveDigits
          };
          
          // Se for a aba "PRODUÇÃO 2 - F/ ESCOPO", extrai "Teste final"
          if (config.extrairTesteFinal) {
            var tabelaFinal = [];
            testeFinalIndices.forEach(function(indice) {
              if (indice >= cabecalho.length) return;
              tabelaFinal.push({
                campo: cabecalho[indice],
                valor: data[i][indice]
              });
            });
            registro["Teste final"] = tabelaFinal;
          }
          
          resultados.push(registro);
          encontrou = true;
        }
      }
      if (encontrou) {
        // Se já encontrou, interrompe a busca nas abas seguintes
        break;
      }
    }

    Logger.log("Total de Registros Encontrados: " + resultados.length);
    return resultados;
    
  } catch (e) {
    Logger.log("Erro em buscarDadosProducao: " + e);
    return { "Erro": e.toString() };
  }
}

/**
 * Obtém a definição de família a partir da aba 'Definição familia'.
 */
function obterDefinicaoFamilia() {
  try {
    var ss = SpreadsheetApp.openById(SPREADSHEET_ID);
    var sheet = ss.getSheetByName('Definição familia');
    if (!sheet) throw "Aba 'Definição familia' não encontrada.";
    
    var data = sheet.getDataRange().getValues();
    if (data.length < 2) return {};
    
    var definicao = {};
    for (var i = 1; i < data.length; i++) {
      var grupo = data[i][0]; // Coluna 'Grupo'
      var descricao = data[i][1]; // Coluna 'Descrição'
      if (grupo && descricao) {
        definicao[grupo.toString().trim()] = descricao.toString().trim();
      }
    }
    return definicao;
  } catch (e) {
    Logger.log("Erro em obterDefinicaoFamilia: " + e);
    return { "Erro": e.toString() };
  }
}

/**
 * Busca na planilha "Ficha tecnica" os registros do Modelo especificado, incluindo categoria.
 */
function buscarRastreabilidadePorModelo(modelo) {
  try {
    Logger.log("Buscar Rastreabilidade para o Modelo: " + modelo);

    var ss = SpreadsheetApp.openById(SPREADSHEET_ID);
    var sheetFicha = ss.getSheetByName('Ficha tecnica');
    if (!sheetFicha) throw "Aba 'Ficha tecnica' não encontrada.";

    var definicaoFamilia = obterDefinicaoFamilia();
    if (definicaoFamilia.Erro) throw definicaoFamilia.Erro;

    var dataFicha = sheetFicha.getDataRange().getValues();
    if (dataFicha.length < 1) return {};

    var resultadosAux = {};

    for (var i = 1; i < dataFicha.length; i++) {
      var modeloEncontrado = dataFicha[i][0]; // Coluna A
      if (modeloEncontrado) {
        var modeloProcessado = modeloEncontrado.toString().trim().toLowerCase();
        var modeloProcurado = modelo.trim().toLowerCase();

        if (modeloProcessado === modeloProcurado) {
          var valorB = dataFicha[i][1]; // Coluna B (valorF)
          var valorC = dataFicha[i][2]; // Coluna C (valorG)

          // Extrair grupo da valorF (Código do produto)
          var valorF = valorB;
          var categoria = "Desconhecida";
          if (valorF) {
            var codigoProduto = valorF.toString().trim();
            var grupoStr = codigoProduto.split('.')[0].replace(/^0+/, ''); // Remove zeros à esquerda
            var grupo = parseInt(grupoStr, 10);
            if (!isNaN(grupo) && definicaoFamilia[grupo]) {
              categoria = definicaoFamilia[grupo];
            }
          }

          // Monta uma chave única para evitar repetição
          var chave = (valorB || "") + "|" + (valorC || "");
          resultadosAux[chave] = { valorF: valorB, valorG: valorC, categoria: categoria };
        }
      }
    }

    // Constrói o objeto de retorno no formato { "Item 1": {...}, "Item 2": {...} }
    var resultadosUnicos = {};
    var contador = 1;
    for (var chave in resultadosAux) {
      resultadosUnicos["Item " + contador] = resultadosAux[chave];
      contador++;
    }

    Logger.log("Total de Itens Encontrados (Rastreabilidade): " + (contador - 1));
    return resultadosUnicos;

  } catch (e) {
    Logger.log("Erro em buscarRastreabilidadePorModelo: " + e);
    return { "Erro": e.toString() };
  }
}

/**
 * Aprova uma OP: atualiza a coluna H na aba "Rastreabilidade" se a senha for correta.
 */
function aprovarOP(ordemProducao, senha) {
  try {
    Logger.log("Aprovando OP: " + ordemProducao);

    var ss = SpreadsheetApp.openById(SPREADSHEET_ID);
    var sheetOutros = ss.getSheetByName('Outros dados');
    if (!sheetOutros) throw "Aba 'Outros dados' não encontrada.";
    
    var senhaCorreta = sheetOutros.getRange('A1').getValue().toString().trim();
    if (senha !== senhaCorreta) {
      throw "Senha incorreta.";
    }
    
    var sheetRastreabilidade = ss.getSheetByName('Rastreabilidade');
    if (!sheetRastreabilidade) throw "Aba 'Rastreabilidade' não encontrada.";
    
    var data = sheetRastreabilidade.getDataRange().getValues();
    if (data.length < 1) throw "Aba 'Rastreabilidade' está vazia.";
    
    var indiceOP = colunaParaIndice('D'); // Coluna D
    var indiceHora = colunaParaIndice('H'); // Coluna H
    var linhasAtualizadas = 0;
    
    var dataHoraAtual = Utilities.formatDate(new Date(), ss.getSpreadsheetTimeZone(), "dd/MM/yyyy HH:mm:ss");
    
    for (var i = 1; i < data.length; i++) {
      var valorOP = data[i][indiceOP];
      if (valorOP && valorOP.toString().trim().toLowerCase() === ordemProducao.trim().toLowerCase()) {
        sheetRastreabilidade.getRange(i + 1, indiceHora + 1).setValue(dataHoraAtual);
        linhasAtualizadas++;
      }
    }
    
    if (linhasAtualizadas > 0) {
      Logger.log(`OP "${ordemProducao}" aprovada. Linhas atualizadas: ${linhasAtualizadas}.`);
      return { sucesso: true, linhasAtualizadas: linhasAtualizadas };
    } else {
      return { sucesso: false, mensagem: `OP "${ordemProducao}" não encontrada na aba 'Rastreabilidade'.` };
    }
    
  } catch (e) {
    Logger.log("Erro em aprovarOP: " + e);
    return { sucesso: false, mensagem: e.toString() };
  }
}

/**
 * Obtém linhas da aba 'Rastreabilidade' onde a coluna H está vazia,
 * retornando colunas C e D, sem duplicatas.
 */
function obterTabelaRastreabilidade() {
  try {
    Logger.log("Obtendo tabela da aba 'Rastreabilidade' (OP's aguardando liberação).");

    var ss = SpreadsheetApp.openById(SPREADSHEET_ID);
    var sheet = ss.getSheetByName('Rastreabilidade');
    if (!sheet) throw "Aba 'Rastreabilidade' não encontrada.";
    
    var data = sheet.getDataRange().getValues();
    if (data.length < 1) return [];
    
    var colunaC = 2; // índice 2 = Coluna C
    var colunaD = 3; // índice 3 = Coluna D
    var colunaH = 7; // índice 7 = Coluna H
    
    var resultadosAux = {};
    
    for (var i = 1; i < data.length; i++) {
      var valorH = data[i][colunaH];
      if (!valorH) { // se coluna H está vazia
        var valorC = data[i][colunaC];
        var valorD = data[i][colunaD];
        if (valorC && valorD) {
          var chave = valorC.toString().trim() + '|' + valorD.toString().trim();
          resultadosAux[chave] = { colunaC: valorC, colunaD: valorD };
        }
      }
    }
    
    var resultadosUnicos = [];
    for (var chave in resultadosAux) {
      resultadosUnicos.push(resultadosAux[chave]);
    }
    
    Logger.log("Total de itens na tabela: " + resultadosUnicos.length);
    return resultadosUnicos;
    
  } catch (e) {
    Logger.log("Erro em obterTabelaRastreabilidade: " + e);
    return { "Erro": e.toString() };
  }
}

/**
 * Função que integra as buscas de Produção.
 */
function buscarDadosPlanilha(ordemProducao) {
  try {
    Logger.log("Iniciando busca completa para OP: " + ordemProducao);

    var resultadoProducao = buscarDadosProducao(ordemProducao);
    
    if (resultadoProducao.Erro) {
      return { "Erro": resultadoProducao.Erro };
    }
    
    return {
      registros: resultadoProducao
    };
    
  } catch (e) {
    Logger.log("Erro em buscarDadosPlanilha: " + e);
    return { "Erro": e.toString() };
  }
}

/**
 * Extrai o último trecho de texto após "- "
 */
function extrairUltimoTexto(modeloCompleto) {
  if (!modeloCompleto) return "";
  var partes = modeloCompleto.split('- ');
  return partes[partes.length - 1].trim();
}

/**
 * Função que serve a página HTML
 */
function doGet() {
  return HtmlService.createHtmlOutputFromFile('etiquetas_zpl')
                    .setTitle('Busca de Ordem de Produção')
                    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
}

/**
 * Função para comparar dados de OP e Modelo
 */
function comparar(ordemProducao, modelo) {
  try {
    Logger.log("Comparando dados para OP: " + ordemProducao + " e Modelo: " + modelo);

    var ss = SpreadsheetApp.openById(SPREADSHEET_ID2);
    var resultados = [];

    // Configurações para as abas de produção
    var configAbas = [
      {
        nomeAba: 'PRODUÇÃO 2 - F/ ESCOPO',
        colunaBusca: 'F',
        colunaModelo: 'D',
        colunaCritério: 'CL',
        colunasRetorno: ['F', 'D', 'X', 'Y', 'Z', 'AA', 'AB', 'AC', 'AD', 'AE', 'AJ', 'AY', 'BA', 'BB', 'BC', 'BD', 'BE', 'BF', 'BG', 'BH', 'BI', 'BJ', 'BK', 'BL', 'BM', 'BO', 'BP', 'BQ'] // Inclui Teste Final
      },
      {
        nomeAba: 'PRODUÇÃO 1 - ESCOPO',
        colunaBusca: 'F',
        colunaModelo: 'D',
        colunaCritério: 'BP',
        colunasRetorno: ['F', 'D', 'T', 'U', 'V', 'W', 'X', 'Y', 'AA', 'AC', 'AD', 'AH', 'AL', 'AN', 'AO', 'AP', 'AR', 'AS', 'AT']
      }
    ];

    configAbas.forEach(function(config) {
      Logger.log("Processando aba: " + config.nomeAba);

      var sheet = ss.getSheetByName(config.nomeAba);
      if (!sheet) {
        Logger.log("Aba " + config.nomeAba + " não encontrada.");
        return;
      }

      var data = sheet.getDataRange().getValues();
      if (data.length < 1) return;

      var cabecalho = data[0];
      var indiceBusca = colunaParaIndice(config.colunaBusca);
      var indiceModelo = colunaParaIndice(config.colunaModelo);
      var indiceCritério = colunaParaIndice(config.colunaCritério);
      var indicesRetorno = config.colunasRetorno.map(colunaParaIndice);

      Logger.log("Índices de retorno: " + indicesRetorno.join(", "));

      // Encontrar a linha da OP
      var linhaOP = -1;
      for (var i = 1; i < data.length; i++) {
        var valorBusca = data[i][indiceBusca];
        if (valorBusca && valorBusca.toString().trim().toLowerCase() === ordemProducao.trim().toLowerCase()) {
          linhaOP = i;
          Logger.log("Linha da OP encontrada: " + linhaOP);
          break;
        }
      }

      if (linhaOP === -1) {
        Logger.log("OP não encontrada na aba " + config.nomeAba);
        return;
      }

      // Buscar os últimos 5 registros acima da linha da OP que atendem ao critério
      var registrosEncontrados = [];
      for (var i = linhaOP - 1; i >= 0 && registrosEncontrados.length < 5; i--) {
        var valorModelo = data[i][indiceModelo];
        var valorCritério = data[i][indiceCritério];

        Logger.log("Verificando linha " + i + ": Modelo = " + valorModelo + ", Critério = " + valorCritério);

        if (valorModelo && valorModelo.toString().trim().toLowerCase().includes(modelo.trim().toLowerCase()) && valorCritério) {
          var registro = {};
          indicesRetorno.forEach(function(indice) {
            if (indice >= cabecalho.length) return;
            let campoOriginal = cabecalho[indice];
            let campoProcessado = removerPrefixoTeste(campoOriginal);
            registro[campoProcessado] = data[i][indice];
          });

          // Adicionar o valor da coluna F como 'OP'
          registro['OP'] = data[i][colunaParaIndice('F')]; // Supondo que coluna F contém o valor da OP

          registrosEncontrados.push(registro);
          Logger.log("Registro encontrado: " + JSON.stringify(registro));
        }
      }

      resultados.push({
        aba: config.nomeAba,
        registros: registrosEncontrados
      });
    });

    Logger.log("Total de Registros Encontrados: " + resultados.length);
    Logger.log("Resultados: " + JSON.stringify(resultados));
    return resultados;
    
  } catch (e) {
    Logger.log("Erro em comparar: " + e);
    return { "Erro": e.toString() };
  }
}

/**
 * Função para remover prefixos como "1º TESTE / " das chaves
 */
function removerPrefixoTeste(campo) {
  if (!campo) return campo;
  return campo.replace(/^\dº TESTE \/ /, '').trim();
}

/**
 * Busca a OP correspondente ao modelo informado (caso a OP digitada comece com "F").
 */
function buscarOPPorModelo(modelo) {
  try {
    Logger.log("Buscando OP pelo modelo: " + modelo);

    var ss = SpreadsheetApp.openById(SPREADSHEET_ID2);
    var configAbas = [
      {
        nomeAba: 'PRODUÇÃO 2 - F/ ESCOPO',
        colunaModelo: 'D',
        colunaRetorno: 'F',
        colunaCriterio: 'CL' // CL não pode estar vazia
      },
      {
        nomeAba: 'PRODUÇÃO 1 - ESCOPO',
        colunaModelo: 'D',
        colunaRetorno: 'F',
        colunaCriterio: 'BP' // BP não pode estar vazia
      }
    ];

    for (var j = 0; j < configAbas.length; j++) {
      var config = configAbas[j];
      var sheet = ss.getSheetByName(config.nomeAba);
      if (!sheet) continue;

      var data = sheet.getDataRange().getValues();
      if (data.length < 1) continue;

      var indiceModelo = colunaParaIndice(config.colunaModelo);
      var indiceRetorno = colunaParaIndice(config.colunaRetorno);
      var indiceCriterio = colunaParaIndice(config.colunaCriterio);

      var opEncontrada = null;

      // Percorre as linhas de baixo para cima para encontrar o último registro válido
      for (var i = data.length - 1; i > 0; i--) {
        var valorModelo = data[i][indiceModelo];
        var valorCriterio = data[i][indiceCriterio];

        if (!valorModelo || !valorCriterio) continue;

        var partes = valorModelo.toString().split('- ');
        var modeloExtraido = partes.length > 1 ? partes[partes.length - 1].trim() : valorModelo.toString().trim();

        if (modeloExtraido.toUpperCase() === modelo.toUpperCase()) {
          opEncontrada = data[i][indiceRetorno];
          Logger.log("OP encontrada: " + opEncontrada + " na aba " + config.nomeAba);
          break;
        }
      }

      if (opEncontrada) {
        return { OPEncontrada: opEncontrada };
      }
    }

    return { OPEncontrada: null };

  } catch (e) {
    Logger.log("Erro em buscarOPPorModelo: " + e);
    return { "Erro": e.toString() };
  }
}

/**
 * Busca o valor do Modelo (coluna E) para a OP informada (na coluna F).
 * @param {string} op - A ordem de produção informada.
 * @return {string} - O valor da coluna E ou string vazia caso não encontre.
 */
function buscarModeloPorOP(op) {
  try {
    var ss = SpreadsheetApp.openById(SPREADSHEET_ID2);
    var abas = ['PRODUÇÃO 2 - F/ ESCOPO', 'PRODUÇÃO 1 - ESCOPO'];
    var idxF = colunaParaIndice('F'); // coluna onde a OP está
    var idxE = colunaParaIndice('E'); // coluna que contém o Modelo

    for (var i = 0; i < abas.length; i++) {
      var sheet = ss.getSheetByName(abas[i]);
      if (!sheet) continue;
      var data = sheet.getDataRange().getValues();
      for (var j = 1; j < data.length; j++) {
        var opPlanilha = data[j][idxF];
        if (opPlanilha && opPlanilha.toString().trim().toLowerCase() === op.trim().toLowerCase()) {
          return data[j][idxE] ? data[j][idxE].toString() : "";
        }
      }
    }
    return "";
  } catch (e) {
    Logger.log("Erro em buscarModeloPorOP: " + e);
    return "";
  }
}
