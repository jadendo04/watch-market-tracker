import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

engine = create_engine("postgresql://dvt@localhost:5432/watch_tracker")

st.set_page_config(page_title="Watch Market Tracker", layout="wide")
st.title("⌚ Luxury Watch Market Tracker")
st.markdown("Live analysis of 269,826 listings from Chrono24")

# ── Sidebar filters ──────────────────────────────────────
st.sidebar.header("Filters")

brands = pd.read_sql("SELECT DISTINCT brand FROM watches WHERE brand IS NOT NULL ORDER BY brand", engine)
selected_brands = st.sidebar.multiselect("Brand", brands['brand'].tolist(),
                                          default=["Rolex", "Patek Philippe", "Audemars Piguet"])

price_range = st.sidebar.slider("Price Range ($)", 0, 500000, (0, 200000), step=5000)

# ── KPI Cards ────────────────────────────────────────────
st.markdown("### Market Overview")
col1, col2, col3, col4 = st.columns(4)

kpis = pd.read_sql("""
    SELECT COUNT(*) as total,
           ROUND(AVG(price)::numeric, 0) as avg_price,
           ROUND(MIN(price)::numeric, 0) as min_price,
           ROUND(MAX(price)::numeric, 0) as max_price
    FROM watches WHERE price IS NOT NULL
""", engine)

col1.metric("Total Listings", f"{int(kpis['total'][0]):,}")
col2.metric("Avg Price", f"${int(kpis['avg_price'][0]):,}")
col3.metric("Min Price", f"${int(kpis['min_price'][0]):,}")
col4.metric("Max Price", f"${int(kpis['max_price'][0]):,}")

# ── Chart 1: Avg price by brand ──────────────────────────
st.markdown("### Average Price by Brand")
brand_filter = "', '".join(selected_brands)
df_brand = pd.read_sql(f"""
    SELECT brand,
           COUNT(*) as listings,
           ROUND(AVG(price)::numeric, 0) as avg_price
    FROM watches
    WHERE brand IN ('{brand_filter}')
      AND price BETWEEN {price_range[0]} AND {price_range[1]}
    GROUP BY brand
    ORDER BY avg_price DESC
""", engine)

fig1 = px.bar(df_brand, x='brand', y='avg_price', color='brand',
              text='listings', labels={'avg_price': 'Avg Price ($)', 'brand': 'Brand'},
              title="Average Listing Price by Brand")
st.plotly_chart(fig1, use_container_width=True)

# ── Chart 2: Price by condition ──────────────────────────
st.markdown("### Price by Condition")
df_cond = pd.read_sql(f"""
    SELECT cond, COUNT(*) as listings,
           ROUND(AVG(price)::numeric, 0) as avg_price
    FROM watches
    WHERE brand IN ('{brand_filter}')
      AND price BETWEEN {price_range[0]} AND {price_range[1]}
      AND cond IS NOT NULL
    GROUP BY cond
    ORDER BY avg_price DESC
""", engine)

fig2 = px.bar(df_cond, x='cond', y='avg_price', color='cond',
              labels={'avg_price': 'Avg Price ($)', 'cond': 'Condition'},
              title="Average Price by Watch Condition")
st.plotly_chart(fig2, use_container_width=True)

# ── Chart 3: Listings by year ────────────────────────────
st.markdown("### Market Activity by Year")
df_year = pd.read_sql(f"""
    SELECT yop::integer as year,
           COUNT(*) as listings,
           ROUND(AVG(price)::numeric, 0) as avg_price
    FROM watches
    WHERE brand IN ('{brand_filter}')
      AND yop BETWEEN 1990 AND 2024
      AND price BETWEEN {price_range[0]} AND {price_range[1]}
    GROUP BY yop
    ORDER BY yop
""", engine)

fig3 = px.line(df_year, x='year', y='avg_price', markers=True,
               labels={'avg_price': 'Avg Price ($)', 'year': 'Year'},
               title="Average Price Trend by Production Year")
st.plotly_chart(fig3, use_container_width=True)

# ── Chart 4: Case material breakdown ────────────────────
st.markdown("### Price by Case Material")
df_case = pd.read_sql(f"""
    SELECT casem,
           COUNT(*) as listings,
           ROUND(AVG(price)::numeric, 0) as avg_price
    FROM watches
    WHERE brand IN ('{brand_filter}')
      AND casem IS NOT NULL
      AND price BETWEEN {price_range[0]} AND {price_range[1]}
    GROUP BY casem
    ORDER BY avg_price DESC
    LIMIT 10
""", engine)

fig4 = px.pie(df_case, values='listings', names='casem',
              title="Listing Share by Case Material")
st.plotly_chart(fig4, use_container_width=True)

# ── Raw data table ───────────────────────────────────────
st.markdown("### Raw Listings")
df_table = pd.read_sql(f"""
    SELECT 
        COALESCE(name, '-') as name,
        COALESCE(brand, '-') as brand,
        COALESCE(model, '-') as model,
        price,
        COALESCE(cond, '-') as condition,
        COALESCE(casem, '-') as case_material,
        COALESCE(yop::text, '-') as year,
        COALESCE(size::text, '-') as size_mm
    FROM watches
    WHERE brand IN ('{brand_filter}')
      AND price BETWEEN {price_range[0]} AND {price_range[1]}
    ORDER BY price DESC
    LIMIT 100
""", engine)
st.dataframe(df_table, width='stretch')