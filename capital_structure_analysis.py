# ----------------------------------------------------------------- #
#          INFORMAÇÕES SOBRE O TRABALHO PRÁTICO                     #
# ----------------------------------------------------------------- #
# - ALUNOS: Carla Beatriz Ferreira                                  #
#           Vítor Terra Mattos do Pratrocínio Veloso                #
# - DISCIPLINA: Administração Financeira (CAD167)                   #
# - PROFESSOR: Prof. Dr. Bruno Pérez Ferreira                       #
# - TRABALHO PRÁTICO 2 - ANÁLISE DA ESTRUTURA DE CAPITAL            #
# ----------------------------------------------------------------- #
# - DESCRIÇÃO: Este script realiza a análise da estrutura           #
#   de capital de uma empresa com base em dados financeiros         #
#   obtidos via API e informações fornecidas pelo usuário.          #
# ----------------------------------------------------------------- #
# - OPÇÕES DE ANÁLISE:                                              #
# todo adicionar descrições das opções!
#   0: Modelo Dinâmico e Termômetro de Liquidez                     #
#       - 
#   1: Limites e Saldos de Caixa Ótimo                              #
#      -
#   2: Fluxo de Caixa com Limites                                   #
#     -
#   3: Estrutura de Capital                                         #
#      -
# ----------------------------------------------------------------- #
# - REPOSITÓRIO GITHUB:                                             #
#   https://github.com/carlabferreira/Capital_Structure_Analysis    #
# ----------------------------------------------------------------- #
# - INSTRUÇÕES DE USO:                                              #
# 1) INSTALE AS BIBLIOTECAS NECESSÁRIAS:                            #
# > pip install -r requirements.txt                                 #
#                                                                   #
# 2) ABRA O TERMINAL E NAVEGUE ATÉ O DIRETÓRIO DO PROJETO.          #
# - EX: > cd C:\Users\SeuUsuario\Capital_Structure_Analysis         #
#                                                                   #
# 3) EXECUTE O SCRIPT COM OS ARGUMENTOS NECESSÁRIOS:                #
# - EX: > python capital_structure_analysis.py -t SEU_TOKEN -o 3    #
#                                                                   #
# 4) (OPCIONAL) ADICIONE O ARGUMENTO DE RELATÓRIO:                  #
# - EX: > python capital_structure_analysis.py -t SEU_TOKEN -o 3    #
#          -w relatorio_estrutura_capital.html                      #
#                                                                   #
# 5) SIGA AS INSTRUÇÕES NO TERMINAL PARA FORNECER DADOS ADICIONAIS. #
# ----------------------------------------------------------------- #



import matplotlib.pyplot as plt
import numpy as np
import argparse
import math
import requests
from enum import Enum
from PIL import Image, ImageDraw, ImageFont

def setup():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--token", help="API Token", required=False)
    parser.add_argument("-o", "--option", help="Analysis option", choices=[0, 1, 2, 3], type=int, required=True)
    parser.add_argument("-w", "--report", help="Generates a report file with given name", required=False)
    args = parser.parse_args()
    return args

class Option(Enum):
    MODELO_DINAMICO_E_TERMOMETRO_DE_LIQUIDEZ = 0
    LIMITES_E_SALDOS_DE_CAIXA_OTIMO = 1
    FLUXO_DE_CAIXA_COM_LIMITES = 2
    ESTRUTURA_DE_CAPITAL = 3 

def entrada_dados_usuario_op_modelo_dinamico():
    p_passivo = input("Digite o valor do passivo permanente:\n")
    p_ativo = input("Digite o valor do ativo permanente:\n")
    c_passivo = input("Digite o valor do passivo cíclico:\n")
    c_ativo = input("Digite o valor do ativo cíclico:\n")
    e_passivo = input("Digite o valor do passivo errático:\n")
    e_ativo = input("Digite o valor do ativo errático:\n")
    return float(p_passivo), float(p_ativo), float(c_passivo), float(c_ativo), float(e_passivo), float(e_ativo)

def analise_modelo_dinamico_e_termometro_de_liquidez(p_passivo, p_ativo, c_passivo, c_ativo, e_passivo, e_ativo):
    d = {}
    d["cdg"] = p_passivo - p_ativo
    d["ncg"] = c_ativo - c_passivo
    d["t"] = e_ativo - e_passivo
    d["tl"] = d["t"]/abs(d["ncg"])

    return d

def entrada_dados_usuario_op_caixa_otimo():
    c_fixo_transacao = input("Digite o custo fixo de transação (F):\n")
    variancia_fluxo_caixa = input("Digite a variância dos fluxos de caixa (σ²):\n")
    custo_oportunidade = input("Digite o custo de oportunidade (K):\n")
    limite_inferior = input("Digite o limite inferior definido (I):\n")
    return float(c_fixo_transacao), float(variancia_fluxo_caixa), float(custo_oportunidade), float(limite_inferior)

def analise_caixa_otimo(c_fixo_transacao, variancia_fluxo_caixa, custo_oportunidade, limite_inferior):
    d = {}
    d["co"] = (((3 * c_fixo_transacao * variancia_fluxo_caixa) / (custo_oportunidade * 4)) ** (1/3)) + limite_inferior
    d["lim_sup_co"] = (3 * d["co"]) - (2 * limite_inferior)
    d["cmo"] = ((4 * d["co"]) - limite_inferior) / 3
    
    return d

def entrada_dados_usuario_op_fluxo_caixa():
    print(f"Forneça dados para análise de fluxo de caixa com limites.\nSugestão: Caso deseje, utilize a opção {Option.LIMITES_E_SALDOS_DE_CAIXA_OTIMO} para calcular valores base de caixa ótimo." )
    saldo_caixa_apropriado = float(input("Digite o saldo de caixa apropriado (D):\n"))
    limite_inferior = float(input("Digite o limite inferior definido pela gestão (I):\n"))
    limite_superior = float(input("Digite o limite superior (S):\n"))
    
    if limite_inferior >= saldo_caixa_apropriado or saldo_caixa_apropriado >= limite_superior:
        print("Erro: Os valores fornecidos não satisfazem a condição I < D < S. Por favor, insira os valores novamente.\n")
        return entrada_dados_usuario_op_fluxo_caixa()
    
    return float(saldo_caixa_apropriado), float(limite_inferior), float(limite_superior)

def entrada_dados_historicos_usuario_op_fluxo_caixa():
    num_periodos = int(input("Digite o número de períodos históricos disponíveis:\n"))
    fluxos_caixa = {}
    for i in range(num_periodos):
        fluxo = float(input(f"Digite o fluxo de caixa do período {i+1}:\n"))
        fluxos_caixa[i] = fluxo
    return fluxos_caixa

def obter_dados_historicos_api_op_fluxo_caixa(TOKEN):
    print("Utilizando informações da API dadosdemercado.com.br para obter dados históricos de fluxo de caixa...")
    print("Informação utilizada: \"operating\" (Caixa líquido atividades operacionais)")
    
    URL = "https://api.dadosdemercado.com.br/v1/companies"

    CONSULTA = "cash_flows"
    EMPRESA = input("Digite o código da empresa (CVM Code) para a qual deseja obter os dados (ex: padrão é 5410 para WEG):\n")
    if not EMPRESA.isdigit():
        print("Código da empresa inválido. Por favor, insira apenas números.")
        return obter_dados_historicos_api_op_fluxo_caixa(TOKEN)
    
    URL_COMPLETA = f"{URL}/{EMPRESA}/{CONSULTA}"

    HEADERS = {
        'Authorization': f'Bearer {TOKEN}',
        'Accept': 'application/json'
    }

    # Obtenção de informações via API
    try:
        response = requests.get(URL_COMPLETA, headers=HEADERS)

        # Verifica se a requisição foi bem-sucedida (código 200)
        if response.status_code == 200:
            # Converte a resposta JSON para um dicionário Python
            dados_json = response.json()
            print(f"Dados Recebidos...")
            # print(dados_json)
            
            # Define o período analisado (últimos 20 valores)
            periodo_analisado = 20
            
            # Forma um dicionário de data e valor de operating
            lista_de_balancos = dados_json

            if not isinstance(lista_de_balancos, list) or not lista_de_balancos:
                print("A resposta da API está vazia ou não é uma lista válida de balanços.")
                return None
            
            ultimos_balancos = lista_de_balancos[-periodo_analisado:]

            dados_finais = {
                item['period_end']: item['operating'] 
                for item in ultimos_balancos 
                if 'period_end' in item and 'operating' in item
            }

            if ultimos_balancos and ultimos_balancos[0].get('period_type') == 'year':
                 print("\nALERTA: Dados obtidos são ANUAIS. O Modelo Miller-Orr requer volatilidade DIÁRIA. Use estes dados com cautela ou procure dados trimestrais/diários, se disponíveis.")
        
            print(f"Dados processados (últimos {len(dados_finais)} períodos):")
            
            # Converte a chave (data) e o valor (operating) para listas separadas
            datas = list(dados_finais.keys())
            valores = list(dados_finais.values())
            
            print(f"Datas de Fim do Período: {datas}")
            print(f"Valores de Operating: {valores}")
            
            return dados_finais

        elif response.status_code == 401:
            print(f"Erro {response.status_code}: Não Autorizado. Verifique se o seu token está correto ou expirado.")
            return None

        else:
            print(f"Erro na requisição. Código HTTP: {response.status_code}")
            print("Mensagem de erro:", response.text)
            return None

    except requests.exceptions.RequestException as e:
        print(f"Ocorreu um erro de conexão: {e}")
        return None

def mostrar_grafico_fluxo_caixa_com_limites(dados_fluxo_caixa, saldo_caixa_apropriado, limite_inferior, limite_superior):
    plt.figure(figsize=(10, 5))

    # Utiliza os dados fornecidos para plotar o gráfico
    datas = list(dados_fluxo_caixa.keys())
    valores = list(dados_fluxo_caixa.values())
    plt.plot(datas, valores, marker='o', label='Fluxo de Caixa Histórico', color='black')

    # Imprime as linhas dos limites
    x_pos = len(datas) - 1 + 0.1  # Posição x para as legendas ao lado da linha
    plt.axhline(y=saldo_caixa_apropriado, color='g', linestyle='--', xmax = len(datas) - 1)
    plt.axhline(y=limite_inferior, color='r', linestyle='--', xmax = len(datas) - 1)
    plt.axhline(y=limite_superior, color='b', linestyle='--', xmax = len(datas) - 1)

    # Adiciona legendas ao lado da linha para os limites
    # Obtém os limites atuais do eixo y para posicionar o texto corretamente
    y_min, y_max = plt.ylim()
    amplitude_y = y_max - y_min
    offset_percentual = 0.02  # Deslocamento de 1% da amplitude do eixo y
    deslocamento_y = amplitude_y * offset_percentual
    
    
    plt.text(x_pos, saldo_caixa_apropriado - deslocamento_y, '(D)', 
         color='g', va='center', ha='left', fontsize=9)
    
    plt.text(x_pos, limite_inferior + deslocamento_y, '(I)', 
         color='r', va='center', ha='left', fontsize=9)
    
    plt.text(x_pos, limite_superior - deslocamento_y, '(S)', 
         color='b', va='center', ha='left', fontsize=9)

    # Adiciona informações relevantes ao gráfico
    plt.title('Fluxo de Caixa com Limites')
    plt.xlabel('Períodos')
    plt.ylabel('Caixa (R$)')
    plt.legend()
    plt.grid()
    
    # Ajuste dos rótulos do eixo x para melhor visualização
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    # Salva a imagem
    plt.savefig("Fluxo de Caixa com Limites.png")

    return
#(...)
#OP FLUXO DE CAIXA COM LIMITES

def entrada_dados_estrutura_de_capital_da_empresa():
    investimento_op_giro = input("Digite o valor do investimento operacional em giro:\n")
    investimento_ativos_fixos = input("Digite o valor dos investimentos em ativos fixos\n")
    divida_liquida_curto_prazo = input("Digite o valor da dívida líquida a curto prazo\n")
    divida_longo_prazo = input("Digite o valor das dívidas a longo prazo\n")
    capital_proprio = input("Digite o valor do capital próprio\n")

    return int(investimento_op_giro), int(investimento_ativos_fixos), int(divida_liquida_curto_prazo), int(divida_longo_prazo), int(capital_proprio)

# Obtem o tamanho e estilo da fonte com base no tamanho da caixa, 
# utilizado na função mostrar_estrutura_de_capital_da_empresa
def obter_fonte(tamanho_caixa):
    # Definições de tamanho mínimo e fator de escala para as fontes
    TAMANHO_MINIMO_FONTE = 12
    FATOR_ESCALA_FONTE = 10

    tamanho_fonte = max(TAMANHO_MINIMO_FONTE, int(math.ceil(tamanho_caixa / FATOR_ESCALA_FONTE)))
    return ImageFont.truetype("arial.ttf", tamanho_fonte)

def mostrar_estrutura_de_capital_da_empresa(investimento_op_giro, investimento_ativos_fixos, divida_liquida_curto_prazo, divida_longo_prazo, capital_proprio):
    
    # Toma como padrão o maior valor; 
    # isto é feito para que nenhuma fonte fique grande demais (a maior fonte será o padrão)
    standard = max(investimento_op_giro, investimento_ativos_fixos, divida_liquida_curto_prazo, divida_longo_prazo, capital_proprio)

    # A altura da maior caixa é definida em 500 (se mudar este valor for desejável, 
    # mudar também a largura padrão da imagem)
    standard_t = 500
    # A largura da imagem é definida em 700 (se mudar este valor for desejável, 
    # mudar também a altura padrão da maior caixa)
    largura = 700

    # O tamanho de cada caixa é calculado fazendo uma regra de 3 com o tamanho padrão
    iaf_rec_t = int((investimento_ativos_fixos * standard_t) / standard)
    iopg_rec_t = int((investimento_op_giro * standard_t) / standard)
    dlcp_rec_t = int((divida_liquida_curto_prazo * standard_t) / standard)
    dlp_rec_t = int((divida_longo_prazo * standard_t) / standard)
    cp_rec_t = int((capital_proprio * standard_t) / standard)

    # A altura da imagem é definida pela altura da coluna mais alta
    altura = max(iaf_rec_t + iopg_rec_t, dlcp_rec_t + dlp_rec_t + cp_rec_t)

    imagem = Image.new("RGB", (largura, altura), "white")
    desenho = ImageDraw.Draw(imagem)

    desenho.rectangle([0, 0, largura-1, altura-1], outline="white")

    # Calcula as coordenadas de cada caixa
    iaf_rec = [0, altura-iaf_rec_t, largura/2, altura]
    iopg_rec = [0, altura-iopg_rec_t-iaf_rec_t, largura/2, altura-iaf_rec_t]
    cp_rec = [largura/2, altura-cp_rec_t, largura, altura]
    dlp_rec = [largura/2, altura-cp_rec_t-dlp_rec_t, largura, altura-cp_rec_t]
    dlcp_rec = [largura/2, altura-cp_rec_t-dlp_rec_t-dlcp_rec_t, largura, altura-cp_rec_t-dlp_rec_t]

    # Calcula o tamanho das fontes
    # O valor é o máximo entre uma proporção do valor calculado a partir do tamanho da caixa 
    # e o tamanho mínimo definido, para evitar fontes muito pequenas
    fonte_iaf = obter_fonte(iaf_rec_t)
    fonte_iopg = obter_fonte(iopg_rec_t)
    fonte_dlcp = obter_fonte(dlcp_rec_t)
    fonte_dlp = obter_fonte(dlp_rec_t)
    fonte_cp = obter_fonte(cp_rec_t)

    # Desenha cada uma das caixas e escreve o texto de acordo
    # Retângulo investimento em ativos fixos
    desenho.rectangle(iaf_rec, outline="black", fill="#cccc98")
    pos_x_iaf = largura / 4
    pos_y_iaf = iaf_rec[1] + (iaf_rec_t / 2) # Y_inicio + (altura_caixa / 2)
    desenho.multiline_text((pos_x_iaf, pos_y_iaf), "Investimento\nem\nAtivos Fixos", 
                            fill="black", font=fonte_iaf, align="center", anchor="mm")
    
    # Retângulo investimento operacional em giro
    desenho.rectangle(iopg_rec, outline="black", fill="#cccc98") 
    pos_x_iopg = largura / 4
    pos_y_iopg = iopg_rec[1] + (iopg_rec_t / 2)
    desenho.multiline_text((pos_x_iopg, pos_y_iopg), "Investimento\nOperacional\nem Giro", 
                            fill="black", font=fonte_iopg, align="center", anchor="mm")
    
    # Retângulo dívida líquida a curto prazo
    desenho.rectangle(dlcp_rec, outline="black", fill="#cccc98") 
    pos_x_dlcp = (3 * largura) / 4
    pos_y_dlcp = dlcp_rec[1] + (dlcp_rec_t / 2)
    desenho.multiline_text((pos_x_dlcp, pos_y_dlcp), "Dívida Líquida\na Curto Prazo", 
                        fill="black", font=fonte_dlcp, align="center", anchor="mm")

    # Retângulo dívida a longo prazo
    desenho.rectangle(dlp_rec, outline="black", fill="#cccc98")
    pos_x_dlp = (3 * largura) / 4
    pos_y_dlp = dlp_rec[1] + (dlp_rec_t / 2)
    desenho.multiline_text((pos_x_dlp, pos_y_dlp), "Dívida\na\nLongo Prazo", 
                        fill="black", font=fonte_dlp, align="center", anchor="mm")

    # Retângulo capital próprio
    desenho.rectangle(cp_rec, outline="black", fill="#cccc98") 
    pos_x_cp = (3 * largura) / 4
    pos_y_cp = cp_rec[1] + (cp_rec_t / 2)
    desenho.multiline_text((pos_x_cp, pos_y_cp), "Capital\nPróprio", 
                        fill="black", font=fonte_cp, align="center", anchor="mm")
    
    # Exibe a imagem na tela
    imagem.show()
    # Salva a imagem com o nome dado
    imagem.save("Estrutura de Capital da Empresa.png")

def main():
    # Organiza os argumentos de entrada e informa a forma correta de uso para o usuário
    args = setup()

    # Extrai os argumentos necessários
    token = args.token
    opt = Option(args.option)

    if (opt == Option.MODELO_DINAMICO_E_TERMOMETRO_DE_LIQUIDEZ):
        print("Análise: Modelo Dinâmico e Termômetro de Liquidez selecionada.")
        
        p_passivo, p_ativo, c_passivo, c_ativo, e_passivo, e_ativo = entrada_dados_usuario_op_modelo_dinamico()
        dados  = analise_modelo_dinamico_e_termometro_de_liquidez(float(p_passivo), float(p_ativo), float(c_passivo), float(c_ativo), float(e_passivo), float(e_ativo))

        print(f"Capital de Giro: {dados["cdg"]}")
        print(f"Necessidades de Capital de Giro: {dados["ncg"]}")
        print(f"Saldo de Tesouraria: {dados["t"]}")
        print(f"Termômetro de Liquidez: {dados["tl"]}")

    elif (opt == Option.LIMITES_E_SALDOS_DE_CAIXA_OTIMO):
        print("Análise: Limites e Saldos de Caixa Ótimo selecionada.")

        c_fixo_transacao, variancia_fluxo_caixa, custo_oportunidade, limite_inferior = entrada_dados_usuario_op_caixa_otimo()
        dados = analise_caixa_otimo(float(c_fixo_transacao), float(variancia_fluxo_caixa), float(custo_oportunidade), float(limite_inferior))
        
        print(f"Saldo de Caixa Ótimo: {dados["co"]}")
        print(f"Limite Superior de Caixa Ótimo: {dados["lim_sup_co"]}")
        print(f"Saldo de Caixa Médio Ótimo: {dados["cmo"]}")

    elif (opt == Option.FLUXO_DE_CAIXA_COM_LIMITES):
        print("Análise: Fluxo de Caixa com Limites selecionada.")
        saldo_caixa_apropriado, limite_inferior, limite_superior = entrada_dados_usuario_op_fluxo_caixa()
        if not token:
            print("Nenhum token de API fornecido. Insira os valores históricos manualmente.")
            dados_fluxo_caixa = entrada_dados_historicos_usuario_op_fluxo_caixa()
        else:
            print("Token de API fornecido. Obtendo dados via API...")
            dados_fluxo_caixa = obter_dados_historicos_api_op_fluxo_caixa(token)
        
        if dados_fluxo_caixa is None:
            print("Não foi possível obter os dados históricos de fluxo de caixa. Encerrando a análise.")
            return

        mostrar_grafico_fluxo_caixa_com_limites(dados_fluxo_caixa, saldo_caixa_apropriado, limite_inferior, limite_superior)

    elif (opt == Option.ESTRUTURA_DE_CAPITAL):
        print("Análise: Estrutura de Capital selecionada.")
        iopg, iaf, dlcp, dlp, cp = entrada_dados_estrutura_de_capital_da_empresa()
        mostrar_estrutura_de_capital_da_empresa(iopg, iaf, dlcp, dlp, cp)
        pass

    # Verifica se usuário solicitou geração de relatório e se sim, gera o arquivo com o nome dado
    if args.report:
        report_fname = args.report
        if not report_fname.endswith(".html"):
            report_fname += ".html"
        # todo generate report



if __name__ == "__main__":
    main()