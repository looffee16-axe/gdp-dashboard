import streamlit as st
import pandas as pd
import math
from pathlib import Path

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='My Sales Dashboard',
    page_icon=':bicyclist:', # This is an emoji shortcode. Could be a URL too.
)

st.title('Bike Sales Dashboard')
st.divider()

# -----------------------------------------------------------------------------
# Declare some useful functions.

@st.cache_data

def get_data():
    DATA_FILENAME = Path(__file__).parent/'../data/Sales_2015.csv'
    fct_df1 = pd.read_csv(DATA_FILENAME)
    DATA_FILENAME = Path(__file__).parent/'../data/Sales_2016.csv'
    fct_df2 = pd.read_csv(DATA_FILENAME)
    DATA_FILENAME = Path(__file__).parent/'../data/Sales_2017.csv'
    fct_df3 = pd.read_csv(DATA_FILENAME)
    DATA_FILENAME = Path(__file__).parent/'../data/Products.csv'
    dim_products_df = pd.read_csv(DATA_FILENAME)
    DATA_FILENAME = Path(__file__).parent/'../data/Categories.csv'
    dim_categories_df = pd.read_csv(DATA_FILENAME)
    DATA_FILENAME = Path(__file__).parent/'../data/Subcategories.csv'
    dim_subcategories_df = pd.read_csv(DATA_FILENAME)

    df_list = [fct_df1,fct_df2,fct_df3]

    fct_df = pd.concat(df_list, ignore_index=True)

    df = pd.merge(fct_df,dim_products_df,left_on='ProductKey',right_on='ProductKey',how='left')
    df = pd.merge(df,dim_subcategories_df,left_on='ProductSubcategoryKey',right_on='ProductSubcategoryKey',how='left')
    df = pd.merge(df,dim_categories_df,left_on='ProductCategoryKey',right_on='ProductCategoryKey',how='left')

    df['Year'] = df['OrderDate'].str.split('/').str[2]

    # Convert years from string to integers
    df['Year'] = pd.to_numeric(df['Year'])

    MIN_YEAR = df['Year'].min()
    MAX_YEAR = df['Year'].max()

    df = df.groupby(['Year','CategoryName']).agg({'OrderQuantity':'sum'}).reset_index()

    return df

df = get_data()
''
''
min_value = df['Year'].min()
max_value = df['Year'].max()

from_year, to_year = st.slider(
    'Which years are you interested in?',
    min_value=min_value,
    max_value=max_value,
    value=[min_value, max_value])

filter = df['CategoryName'].unique()

if not len(filter):
    st.warning("Select at least one")

selected_filter = st.multiselect(
    'Which category would you like to view?',
    filter,
    ['Bikes','Accessories','Clothing'])

''
''
''

# Filter the data
filtered_df = df[
    (df['CategoryName'].isin(selected_filter))
    & (df['Year'] <= to_year)
    & (from_year <= df['Year'])
]

st.header('Category', divider='gray')

''

st.bar_chart(
    filtered_df,
    x='Year',
    y='OrderQuantity',
    color='CategoryName',
)

''
''


first_year = df[df['Year'] == from_year]
last_year = df[df['Year'] == to_year]

