import pandas as pd 

df_combined = pd.read_csv('australia_fogo_all.csv')

print("formato dos conjuto de dados:", df_combined.shape)
print("\nNome das colunas:")
print(df_combined.columns.tolist())
print("\nApenas as primeiras colunas:")
print(df_combined.head())
print("\nTipos de dados:")
print(df_combined.dtypes)
print("\nEstatiticas basicas:")
print(df_combined.describe())
