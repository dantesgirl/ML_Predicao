import pandas as pd
from datetime import datetime

df = pd.read_csv('australia_fogo_all.csv')
print(f"\n Arquivos do fogo {len(df):,} carregados")
print(f"Alcance de data: {df['acq_date'].min()} to {df['acq_date'].max()}")

def timsort_implementation(df, column):
    print(f"\nOrdena {len(df):,} os dados by '{column} usando o Timsort...")
    start_time = datetime.now()
    #python organiza internamente com o tim
    df_sorted = df.sort_values(by=column, ascending=True)
    end_time = datetime.now()
    elapsed = (end_time - start_time).total_seconds()

    print(f"Organização completa em {elapsed:.3f} segundos")
    print(f"Algoritmo usado: Timsort")
    print(f"Primeira data: {df_sorted[column].iloc[0]}")
    print(f"Ultima data: {df_sorted[column].iloc[-1]}")

    return df_sorted

#aplicando 
df_sorted = timsort_implementation(df, 'acq_date')

df_sorted.to_csv('timsort_fogo_australia.csv', index=False)
print(f"Organização salva em 'timsort_fogo_australia.csv'")
