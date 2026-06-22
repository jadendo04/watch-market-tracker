import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("postgresql://dvt@localhost:5432/watch_tracker")

# Load CSV
df = pd.read_csv("data/watches.csv", low_memory=False)

# Drop unnamed index column
df = df.drop(columns=['Unnamed: 0'])

# Clean price — remove $, commas
df['price'] = df['price'].astype(str).str.replace('$', '', regex=False)
df['price'] = df['price'].str.replace(',', '', regex=False)
df['price'] = pd.to_numeric(df['price'], errors='coerce')

# Clean size — keep only first number
df['size'] = df['size'].astype(str).str.extract(r'(\d+\.?\d*)')
df['size'] = pd.to_numeric(df['size'], errors='coerce')

# Clean year — extract 4 digit year only
df['yop'] = df['yop'].astype(str).str.extract(r'(\d{4})')
df['yop'] = pd.to_numeric(df['yop'], errors='coerce')

# Drop rows with no price
df = df.dropna(subset=['price'])

print(f"Loading {len(df)} rows into PostgreSQL...")

# Let pandas create the table schema automatically
df.to_sql('watches', engine, if_exists='replace', index=False)

print("✓ Data loaded successfully!")
print(f"Total rows loaded: {len(df)}")
print(df.head())