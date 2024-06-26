import pandas as pd

def ler_dados(excel_path):
    df = pd.read_excel(excel_path)
    return df

def main():
    df = ler_dados('data/Precos_Insumos.xlsx')
    from planilha_cotacao.relatorio import gerar_relatorio
    gerar_relatorio(df, 'data/Orcamentos_Salvos.csv')

if __name__ == "__main__":
    main()
