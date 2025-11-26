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

#OP FLUXO DE CAIXA COM LIMITES
#(...)
#OP FLUXO DE CAIXA COM LIMITES

def entrada_dados_estrutura_de_capital_da_empresa():
    investimento_op_giro = input("Digite o valor do investimento operacional em giro:\n")
    investimento_ativos_fixos = input("Digite o valor dos investimentos em ativos fixos\n")
    divida_liquida_curto_prazo = input("Digite o valor da dívida líquida a curto prazo\n")
    divida_longo_prazo = input("Digite o valor das dívidas a longo prazo\n")
    capital_proprio = input("Digite o valor do capital próprio\n")

    return int(investimento_op_giro), int(investimento_ativos_fixos), int(divida_liquida_curto_prazo), int(divida_longo_prazo), int(capital_proprio)

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

    imagem = Image.new("RGB", (largura, altura), "black")
    desenho = ImageDraw.Draw(imagem)

    desenho.rectangle([0, 0, largura-1, altura-1], outline="black")

    # Calcula as coordenadas de cada caixa
    iaf_rec = [0, altura-iaf_rec_t, largura/2, altura]
    iopg_rec = [0, altura-iopg_rec_t-iaf_rec_t, largura/2, altura-iaf_rec_t]
    cp_rec = [largura/2, altura-cp_rec_t, largura, altura]
    dlp_rec = [largura/2, altura-cp_rec_t-dlp_rec_t, largura, altura-cp_rec_t]
    dlcp_rec = [largura/2, altura-cp_rec_t-dlp_rec_t-dlcp_rec_t, largura, altura-cp_rec_t-dlp_rec_t]

    # Calcula o tamanho das fontes
    fonte_iaf = ImageFont.truetype("arial.ttf", int(math.ceil(iaf_rec_t/10)))
    fonte_iopg = ImageFont.truetype("arial.ttf", int(math.ceil(iopg_rec_t/10)))
    fonte_dlcp = ImageFont.truetype("arial.ttf", int(math.ceil(dlcp_rec_t/10)))
    fonte_dlp = ImageFont.truetype("arial.ttf", int(math.ceil(dlp_rec_t/10)))
    fonte_cp = ImageFont.truetype("arial.ttf", int(math.ceil(cp_rec_t/10)))

    # Desenha cada uma das caixas e escreve o texto de acordo
    desenho.rectangle(iaf_rec, outline="black", fill="#cccc98") # Retângulo investimento em ativos fixos
    desenho.multiline_text((10, (altura - iaf_rec_t)), "Investimento\nem\nAtivos Fixos", fill="black", font=fonte_iaf, align="center")

    desenho.rectangle(iopg_rec, outline="black", fill="#cccc98") # Retângulo investimento operacional em giro
    desenho.multiline_text((10, (altura - iopg_rec_t - iaf_rec_t)), "Investimento\nOperacional\nem Giro", fill="black", font=fonte_iopg, align="center")
    
    desenho.rectangle(dlcp_rec, outline="black", fill="#cccc98") # Retângulo dívida líquida a curto prazo
    desenho.multiline_text(((largura/2) + 10, altura - cp_rec_t - dlp_rec_t - dlcp_rec_t), "Divida Líquida\na Curto Prazo", fill="black", font=fonte_dlcp, align="center")

    desenho.rectangle(dlp_rec, outline="black", fill="#cccc98") # Retângulo dívida a longo prazo
    desenho.multiline_text(((largura/2) + 10, altura - cp_rec_t - dlp_rec_t), "Dívida\na\nLongo Prazo", fill="black", font=fonte_dlp, align="center")

    desenho.rectangle(cp_rec, outline="black", fill="#cccc98") # Retângulo capital próprio
    desenho.multiline_text(((largura/2) + 10, (altura - cp_rec_t)), "Capital\nPróprio", fill="black", font=fonte_cp, align="center")

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
        pass
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