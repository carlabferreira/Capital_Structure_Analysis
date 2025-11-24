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
from enum import Enum

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


def main():
    # Organiza os argumentos de entrada e informa a forma correta de uso para o usuário
    args = setup()

    # Extrai os argumentos necessários
    token = args.token
    opt = Option(args.option)

    if (opt == Option.MODELO_DINAMICO_E_TERMOMETRO_DE_LIQUIDEZ):
        print("Análise: Modelo Dinâmico e Termômetro de Liquidez selecionada.")
        pass
    elif (opt == Option.LIMITES_E_SALDOS_DE_CAIXA_OTIMO):
        print("Análise: Limites e Saldos de Caixa Ótimo selecionada.")
        pass
    elif (opt == Option.FLUXO_DE_CAIXA_COM_LIMITES):
        print("Análise: Fluxo de Caixa com Limites selecionada.")
        pass
    elif (opt == Option.ESTRUTURA_DE_CAPITAL):
        print("Análise: Estrutura de Capital selecionada.")
        pass

    # Verifica se usuário solicitou geração de relatório e se sim, gera o arquivo com o nome dado
    if args.report:
        report_fname = args.report
        if not report_fname.endswith(".html"):
            report_fname += ".html"
        # todo generate report



if __name__ == "__main__":
    main()