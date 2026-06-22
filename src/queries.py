import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("postgresql://dvt@localhost:5432/watch_tracker")

def run_query(sql, title):
    print(f"\n{'='*50}")
    print(f" {title}")
    print('='*50)
    df = pd.read_sql(sql, engine)
    print(df.to_string(index=False))
    return df

# 1. Average price by brand (top 10)
run_query("""
    SELECT brand,
           COUNT(*) as listings,
           ROUND(AVG(price)::numeric, 2) as avg_price,
           ROUND(MIN(price)::numeric, 2) as min_price,
           ROUND(MAX(price)::numeric, 2) as max_price
    FROM watches
    WHERE price IS NOT NULL AND brand IS NOT NULL
    GROUP BY brand
    ORDER BY avg_price DESC
    LIMIT 10;
""", "Top 10 Brands by Average Price")

# 2. Churn by condition
run_query("""
    SELECT cond,
           COUNT(*) as listings,
           ROUND(AVG(price)::numeric, 2) as avg_price
    FROM watches
    WHERE price IS NOT NULL AND cond IS NOT NULL
    GROUP BY cond
    ORDER BY avg_price DESC;
""", "Average Price by Condition")

# 3. Most listed models
run_query("""
    SELECT brand, model,
           COUNT(*) as listings,
           ROUND(AVG(price)::numeric, 2) as avg_price
    FROM watches
    WHERE model IS NOT NULL AND brand IS NOT NULL
    GROUP BY brand, model
    ORDER BY listings DESC
    LIMIT 10;
""", "Top 10 Most Listed Models")

# 4. Price distribution by case material
run_query("""
    SELECT casem,
           COUNT(*) as listings,
           ROUND(AVG(price)::numeric, 2) as avg_price
    FROM watches
    WHERE casem IS NOT NULL AND price IS NOT NULL
    GROUP BY casem
    ORDER BY avg_price DESC
    LIMIT 10;
""", "Price by Case Material")

# 5. Listings by year of production
run_query("""
    SELECT yop::integer as year,
           COUNT(*) as listings,
           ROUND(AVG(price)::numeric, 2) as avg_price
    FROM watches
    WHERE yop IS NOT NULL AND yop BETWEEN 1990 AND 2024
    GROUP BY yop
    ORDER BY yop DESC
    LIMIT 15;
""", "Listings by Year of Production")