import pandas as pd
import glob

all_files = glob.glob("fogo/*.csv")

print(f"Found {len(all_files)} files:")
for file in all_files:
    print(f"  - {file}")

df_list = []
for file in all_files:
    print(f"Lendo {file}...")
    df_temp = pd.read_csv(file)
    print(f"  → {len(df_temp):,} records")
    df_list.append(df_temp)

print("\nCombining all files...")
df_combined = pd.concat(df_list, ignore_index=True)

print(f"\nQuantidade total: {len(df_combined):,}")
print(f"Data total: {df_combined['acq_date'].min()} to {df_combined['acq_date'].max()}")


df_combined['year'] = pd.to_datetime(df_combined['acq_date']).dt.year
print("\nPor ano:")
print(df_combined['year'].value_counts().sort_index())


df_combined.to_csv('australia_fogo_all.csv', index=False)
print(f"\nSalvo em 'australia_fogo_all.csv'")
