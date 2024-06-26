import pandas as pd

def gerar_relatorio(df, output_csv_path):
    df.to_csv(output_csv_path, index=False)
