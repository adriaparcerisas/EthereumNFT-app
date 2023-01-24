#!/usr/bin/env python
# coding: utf-8

# In[1]:


import streamlit as st
import pandas as pd
import numpy as np
from shroomdk import ShroomDK
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as md
import matplotlib.ticker as ticker
import numpy as np
import plotly.express as px
sdk = ShroomDK("7bfe27b2-e726-4d8d-b519-03abc6447728")


# In[2]:


st.title('NFT royalties')


# In[3]:


st.markdown('**NFT royalties** are payments that compensate original NFT creators for the use of their non-fungible tokens (NFTs). In business, royalties generally pay the creator a percentage of sales or profits. With NFTs, royalties are usually set by the owner during the minting process.') 
st.markdown('It is intended to provide an overview of the current marketplace royalties and fees for NFTs in Ethereum on several NFT marketplaces.')


# In[4]:


st.markdown('In this section, we are gonna track several royalty metrics of the major and most commont NFT marketplaces on Ethereum Ecosystem:') 
st.write('- NFT marketplaces activity by Royalty Type')
st.write('- 0% Marketplace wash sale activity')
st.write('')


# In[15]:


st.subheader("NFT marketplaces activity by Royalty Type")
st.write("In this part it can be seen all the information about the activity of Ethereum NFT sales on marketplaces by its royalties. The analysis displays information about the current sales, purchasers and volume sold in USD in a global basis, as well as the cumulative trends.")


# In[16]:


sql = f"""
SELECT
	date_trunc('day', block_timestamp)  as date, 
	CASE WHEN PLATFORM_NAME in ('looksrare','x2y2','sudoswap') THEN '0% Marketplace'
  	else 'Royalty Marketplace' END marketplace_type,
  	sum(price_usd) as sales_volume,
    sum(sales_volume) over (partition by marketplace_type order by date) as cum_sales_volume,
	median(price_usd) as median_price,
	count(DISTINCT tx_hash) as sales,
    sum(sales) over (partition by marketplace_type order by date) as cum_sales,
    count(distinct buyer_address) as purchasers,
    sum(purchasers) over (partition by marketplace_type order by date) as cum_purchasers
FROM ethereum.core.ez_nft_sales
GROUP BY 1,2 
having NOT marketplace_type is NULL
"""

sql2 = f"""
SELECT
	date_trunc('week', block_timestamp)  as date, 
	CASE WHEN PLATFORM_NAME in ('looksrare','x2y2','sudoswap') THEN '0% Marketplace'
  	else 'Royalty Marketplace' END marketplace_type,
  	sum(price_usd) as sales_volume,
    sum(sales_volume) over (partition by marketplace_type order by date) as cum_sales_volume,
	median(price_usd) as median_price,
	count(DISTINCT tx_hash) as sales,
    sum(sales) over (partition by marketplace_type order by date) as cum_sales,
    count(distinct buyer_address) as purchasers,
    sum(purchasers) over (partition by marketplace_type order by date) as cum_purchasers
FROM ethereum.core.ez_nft_sales
GROUP BY 1,2 
having NOT marketplace_type is NULL
"""

sql3 = f"""
SELECT
	date_trunc('month', block_timestamp)  as date, 
	CASE WHEN PLATFORM_NAME in ('looksrare','x2y2','sudoswap') THEN '0% Marketplace'
  	else 'Royalty Marketplace' END marketplace_type,
  	sum(price_usd) as sales_volume,
    sum(sales_volume) over (partition by marketplace_type order by date) as cum_sales_volume,
	median(price_usd) as median_price,
	count(DISTINCT tx_hash) as sales,
    sum(sales) over (partition by marketplace_type order by date) as cum_sales,
    count(distinct buyer_address) as purchasers,
    sum(purchasers) over (partition by marketplace_type order by date) as cum_purchasers
FROM ethereum.core.ez_nft_sales
GROUP BY 1,2 
having NOT marketplace_type is NULL
"""


# In[17]:


st.experimental_memo(ttl=21600)
@st.cache
def compute(a):
    data=sdk.query(a)
    return data

results = compute(sql)
df = pd.DataFrame(results.records)
df.info()

results2 = compute(sql2)
df2 = pd.DataFrame(results2.records)
df2.info()

results3 = compute(sql3)
df3 = pd.DataFrame(results3.records)
df3.info()
#st.subheader('Terra general activity metrics regarding transactions')
#st.markdown('In this first part, we can take a look at the main activity metrics on Terra, where it can be seen how the number of transactions done across the protocol, as well as some other metrics such as fees and TPS.')


# In[18]:


import plotly.express as px

fig1 = px.bar(df, x="date", y="sales", color="marketplace_type", color_discrete_sequence=px.colors.qualitative.Vivid)
fig1.update_layout(
    title='Daily NFT sales by royalties',
    xaxis_tickfont_size=14,
    yaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)


fig2 = px.bar(df2, x="date", y="sales", color="marketplace_type", color_discrete_sequence=px.colors.qualitative.Vivid)
fig2.update_layout(
    title='Weekly NFT sales by royalties',
    xaxis_tickfont_size=14,
    yaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

fig3 = px.bar(df3, x="date", y="sales", color="marketplace_type", color_discrete_sequence=px.colors.qualitative.Vivid)
fig3.update_layout(
    title='Monthly NFT sales by royalties',
    xaxis_tickfont_size=14,
    yaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

tab1, tab2, tab3 = st.tabs(["Daily sales", "Weekly sales", "Monthly sales"])

with tab1:
    st.plotly_chart(fig1, theme="streamlit", use_container_width=True)

with tab2:
    st.plotly_chart(fig2, theme="streamlit", use_container_width=True)

with tab3:
    st.plotly_chart(fig3, theme="streamlit", use_container_width=True)


# In[19]:


import plotly.express as px

fig1 = px.bar(df, x="date", y="cum_sales", color="marketplace_type", color_discrete_sequence=px.colors.qualitative.Vivid)
fig1.update_layout(
    title='Total daily NFT sales by royalties',
    xaxis_tickfont_size=14,
    yaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)


fig2 = px.bar(df2, x="date", y="cum_sales", color="marketplace_type", color_discrete_sequence=px.colors.qualitative.Vivid)
fig2.update_layout(
    title='Total weekly NFT sales by royalties',
    xaxis_tickfont_size=14,
    yaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

fig3 = px.bar(df3, x="date", y="cum_sales", color="marketplace_type", color_discrete_sequence=px.colors.qualitative.Vivid)
fig3.update_layout(
    title='Total monthly NFT sales by royalties',
    xaxis_tickfont_size=14,
    yaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

tab1, tab2, tab3 = st.tabs(["Daily cumulative sales", "Weekly cumulative sales", "Monthly cumulative sales"])

with tab1:
    st.plotly_chart(fig1, theme="streamlit", use_container_width=True)

with tab2:
    st.plotly_chart(fig2, theme="streamlit", use_container_width=True)

with tab3:
    st.plotly_chart(fig3, theme="streamlit", use_container_width=True)


# In[20]:


import plotly.express as px

fig1 = px.bar(df, x="date", y="purchasers", color="marketplace_type", color_discrete_sequence=px.colors.qualitative.Safe)
fig1.update_layout(
    title='Daily purchasers by royalties',
    xaxis_tickfont_size=14,
    yaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)


fig2 = px.bar(df2, x="date", y="purchasers", color="marketplace_type", color_discrete_sequence=px.colors.qualitative.Safe)
fig2.update_layout(
    title='Weekly purchasers by royalties',
    xaxis_tickfont_size=14,
    yaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

fig3 = px.bar(df3, x="date", y="purchasers", color="marketplace_type", color_discrete_sequence=px.colors.qualitative.Safe)
fig3.update_layout(
    title='Monthly purchasers by royalties',
    xaxis_tickfont_size=14,
    yaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

tab1, tab2, tab3 = st.tabs(["Daily purchasers", "Weekly purchasers", "Monthly purchasers"])

with tab1:
    st.plotly_chart(fig1, theme="streamlit", use_container_width=True)

with tab2:
    st.plotly_chart(fig2, theme="streamlit", use_container_width=True)

with tab3:
    st.plotly_chart(fig3, theme="streamlit", use_container_width=True)


# In[21]:


import plotly.express as px

fig1 = px.bar(df, x="date", y="cum_purchasers", color="marketplace_type", color_discrete_sequence=px.colors.qualitative.Safe)
fig1.update_layout(
    title='Daily total purchasers by royalty',
    xaxis_tickfont_size=14,
    yaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)


fig2 = px.bar(df2, x="date", y="cum_purchasers", color="marketplace_type", color_discrete_sequence=px.colors.qualitative.Safe)
fig2.update_layout(
    title='Weekly total purchasers by royalty',
    xaxis_tickfont_size=14,
    yaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

fig3 = px.bar(df3, x="date", y="cum_purchasers", color="marketplace_type", color_discrete_sequence=px.colors.qualitative.Safe)
fig3.update_layout(
    title='Monthly total purchasers by royalty',
    xaxis_tickfont_size=14,
    yaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

tab1, tab2, tab3 = st.tabs(["Total daily purchasers", "Total weekly purchasers", "Total monthly purchasers"])

with tab1:
    st.plotly_chart(fig1, theme="streamlit", use_container_width=True)

with tab2:
    st.plotly_chart(fig2, theme="streamlit", use_container_width=True)

with tab3:
    st.plotly_chart(fig3, theme="streamlit", use_container_width=True)


# In[22]:


import plotly.express as px

fig1 = px.area(df, x="date", y="sales_volume", color="marketplace_type", color_discrete_sequence=px.colors.qualitative.Plotly)
fig1.update_layout(
    title='Daily sales volume by royalties',
    xaxis_tickfont_size=14,
    yaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)


fig2 = px.area(df2, x="date", y="sales_volume", color="marketplace_type", color_discrete_sequence=px.colors.qualitative.Plotly)
fig2.update_layout(
    title='Weekly sales volume by royalties',
    xaxis_tickfont_size=14,
    yaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

fig3 = px.area(df3, x="date", y="sales_volume", color="marketplace_type", color_discrete_sequence=px.colors.qualitative.Plotly)
fig3.update_layout(
    title='Monthly sales volume by royalties',
    xaxis_tickfont_size=14,
    yaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

tab1, tab2, tab3 = st.tabs(["Daily volume (USD)", "Weekly volume (USD)", "Monthly volume (USD)"])

with tab1:
    st.plotly_chart(fig1, theme="streamlit", use_container_width=True)

with tab2:
    st.plotly_chart(fig2, theme="streamlit", use_container_width=True)

with tab3:
    st.plotly_chart(fig3, theme="streamlit", use_container_width=True)


# In[23]:


import plotly.express as px

fig1 = px.area(df, x="date", y="cum_sales_volume", color="marketplace_type", color_discrete_sequence=px.colors.qualitative.Plotly)
fig1.update_layout(
    title='Total daily sales volume by royalties',
    xaxis_tickfont_size=14,
    yaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)


fig2 = px.area(df2, x="date", y="cum_sales_volume", color="marketplace_type", color_discrete_sequence=px.colors.qualitative.Plotly)
fig2.update_layout(
    title='Total weekly sales volume by royalties',
    xaxis_tickfont_size=14,
    yaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

fig3 = px.area(df3, x="date", y="cum_sales_volume", color="marketplace_type", color_discrete_sequence=px.colors.qualitative.Plotly)
fig3.update_layout(
    title='Total monthly sales volume by royalties',
    xaxis_tickfont_size=14,
    yaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

tab1, tab2, tab3 = st.tabs(["Total daily volume (USD)", "Total weekly volume (USD)", "Total monthly volume (USD)"])

with tab1:
    st.plotly_chart(fig1, theme="streamlit", use_container_width=True)

with tab2:
    st.plotly_chart(fig2, theme="streamlit", use_container_width=True)

with tab3:
    st.plotly_chart(fig3, theme="streamlit", use_container_width=True)


# In[24]:


import plotly.express as px

fig1 = px.scatter(df, x="date", y="median_price", color="marketplace_type", color_discrete_sequence=px.colors.qualitative.Light24)
fig1.update_layout(
    title='Daily average NFT price (USD) by royalties',
    xaxis_tickfont_size=14,
    yaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)


fig2 = px.scatter(df2, x="date", y="median_price", color="marketplace_type", color_discrete_sequence=px.colors.qualitative.Light24)
fig2.update_layout(
    title='Weekly average NFT price (USD) by royalties',
    xaxis_tickfont_size=14,
    yaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

fig3 = px.scatter(df3, x="date", y="median_price", color="marketplace_type", color_discrete_sequence=px.colors.qualitative.Light24)
fig3.update_layout(
    title='Monthly average NFT price (USD) by royalties',
    xaxis_tickfont_size=14,
    yaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

tab1, tab2, tab3 = st.tabs(["Daily NFT price by royalties", "Weekly NFT price by royalties", "Monthly NFT price by royalties"])

with tab1:
    st.plotly_chart(fig1, theme="streamlit", use_container_width=True)

with tab2:
    st.plotly_chart(fig2, theme="streamlit", use_container_width=True)

with tab3:
    st.plotly_chart(fig3, theme="streamlit", use_container_width=True)


# In[25]:


st.subheader("0% Marketplace wash sale activity")
st.write("In this final part it can be seen all the information about the wash sales activity regarding 0% royalty fees marketplaces. The analysis displays information about the current sales, purchasers and volume sold in USD in a global basis, as well as the cumulative trends.")


# In[26]:


sql = f"""
WITH tab1 as (
  SELECT 
    buyer_address,
    TOKENID as m1,
    max(block_timestamp) as max_buy,
    min(block_timestamp) as min_buy,
    datediff('day', min(block_timestamp), max(block_timestamp)) buy_time_diff,
  	count(distinct tx_hash) as sales,
  sum(price_usd) as volume
  FROM ethereum.core.ez_nft_sales
  where PLATFORM_NAME in ('looksrare','x2y2','sudoswap') 
  GROUP BY 1,2  
), tab2 as (
  SELECT 
    SELLER_ADDRESS,
    TOKENID as m2,
    max(block_timestamp) as max_sell,
    min(block_timestamp) as min_sell,
    datediff('day', min(block_timestamp), max(block_timestamp)) sell_time_diff
  FROM ethereum.core.ez_nft_sales
  where PLATFORM_NAME in ('looksrare','x2y2','sudoswap') 
  GROUP BY 1,2 
)

SELECT 
  date_trunc('day', min_buy) as date,
  CASE WHEN buy_time_diff < 30 AND sales > 1 THEN 'Wash sales'
  ELSE 'Other sales' END as marketplace_type,
  sum(volume) as sales_volume,
    sum(sales_volume) over (partition by marketplace_type order by date) as cum_sales_volume,
	sum(sales) as saless,
    sum(saless) over (partition by marketplace_type order by date) as cum_sales,
    count(distinct buyer_address) as purchasers,
    sum(purchasers) over (partition by marketplace_type order by date) as cum_purchasers
from tab1
GROUP BY 1,2 
  
"""

sql2 = f"""
WITH tab1 as (
  SELECT 
    buyer_address,
    TOKENID as m1,
    max(block_timestamp) as max_buy,
    min(block_timestamp) as min_buy,
    datediff('day', min(block_timestamp), max(block_timestamp)) buy_time_diff,
  	count(distinct tx_hash) as sales,
  sum(price_usd) as volume
  FROM ethereum.core.ez_nft_sales
  where PLATFORM_NAME in ('looksrare','x2y2','sudoswap') 
  GROUP BY 1,2  
), tab2 as (
  SELECT 
    SELLER_ADDRESS,
    TOKENID as m2,
    max(block_timestamp) as max_sell,
    min(block_timestamp) as min_sell,
    datediff('day', min(block_timestamp), max(block_timestamp)) sell_time_diff
  FROM ethereum.core.ez_nft_sales
  where PLATFORM_NAME in ('looksrare','x2y2','sudoswap') 
  GROUP BY 1,2 
)

SELECT 
  date_trunc('week', min_buy) as date,
  CASE WHEN buy_time_diff < 30 AND sales > 1 THEN 'Wash sales'
  ELSE 'Other sales' END as marketplace_type,
  sum(volume) as sales_volume,
    sum(sales_volume) over (partition by marketplace_type order by date) as cum_sales_volume,
	sum(sales) as saless,
    sum(saless) over (partition by marketplace_type order by date) as cum_sales,
    count(distinct buyer_address) as purchasers,
    sum(purchasers) over (partition by marketplace_type order by date) as cum_purchasers
from tab1
GROUP BY 1,2 
"""

sql3 = f"""
WITH tab1 as (
  SELECT 
    buyer_address,
    TOKENID as m1,
    max(block_timestamp) as max_buy,
    min(block_timestamp) as min_buy,
    datediff('day', min(block_timestamp), max(block_timestamp)) buy_time_diff,
  	count(distinct tx_hash) as sales,
  sum(price_usd) as volume
  FROM ethereum.core.ez_nft_sales
  where PLATFORM_NAME in ('looksrare','x2y2','sudoswap') 
  GROUP BY 1,2  
), tab2 as (
  SELECT 
    SELLER_ADDRESS,
    TOKENID as m2,
    max(block_timestamp) as max_sell,
    min(block_timestamp) as min_sell,
    datediff('day', min(block_timestamp), max(block_timestamp)) sell_time_diff
  FROM ethereum.core.ez_nft_sales
  where PLATFORM_NAME in ('looksrare','x2y2','sudoswap') 
  GROUP BY 1,2 
)

SELECT 
  date_trunc('month', min_buy) as date,
  CASE WHEN buy_time_diff < 30 AND sales > 1 THEN 'Wash sales'
  ELSE 'Other sales' END as marketplace_type,
  sum(volume) as sales_volume,
    sum(sales_volume) over (partition by marketplace_type order by date) as cum_sales_volume,
	sum(sales) as saless,
    sum(saless) over (partition by marketplace_type order by date) as cum_sales,
    count(distinct buyer_address) as purchasers,
    sum(purchasers) over (partition by marketplace_type order by date) as cum_purchasers
from tab1
GROUP BY 1,2 
"""


# In[27]:


results = compute(sql)
df = pd.DataFrame(results.records)
df.info()

results2 = compute(sql2)
df2 = pd.DataFrame(results2.records)
df2.info()

results3 = compute(sql3)
df3 = pd.DataFrame(results3.records)
df3.info()


# In[28]:


import plotly.express as px

fig1 = px.bar(df, x="date", y="saless", color="marketplace_type", color_discrete_sequence=px.colors.qualitative.Vivid)
fig1.update_layout(
    title='Daily 0% Marketplace sales',
    xaxis_tickfont_size=14,
    yaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)


fig2 = px.bar(df2, x="date", y="saless", color="marketplace_type", color_discrete_sequence=px.colors.qualitative.Vivid)
fig2.update_layout(
    title='Weekly 0% Marketplace sales',
    xaxis_tickfont_size=14,
    yaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

fig3 = px.bar(df3, x="date", y="saless", color="marketplace_type", color_discrete_sequence=px.colors.qualitative.Vivid)
fig3.update_layout(
    title='Monthly 0% Marketplace sales',
    xaxis_tickfont_size=14,
    yaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

tab1, tab2, tab3 = st.tabs(["Daily wash sales", "Weekly wash sales", "Monthly wash sales"])

with tab1:
    st.plotly_chart(fig1, theme="streamlit", use_container_width=True)

with tab2:
    st.plotly_chart(fig2, theme="streamlit", use_container_width=True)

with tab3:
    st.plotly_chart(fig3, theme="streamlit", use_container_width=True)


# In[29]:


import plotly.express as px

fig1 = px.bar(df, x="date", y="cum_sales", color="marketplace_type", color_discrete_sequence=px.colors.qualitative.Vivid)
fig1.update_layout(
    title='Total daily 0% Marketplace sales',
    xaxis_tickfont_size=14,
    yaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)


fig2 = px.bar(df2, x="date", y="cum_sales", color="marketplace_type", color_discrete_sequence=px.colors.qualitative.Vivid)
fig2.update_layout(
    title='Total weekly 0% Marketplace sales',
    xaxis_tickfont_size=14,
    yaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

fig3 = px.bar(df3, x="date", y="cum_sales", color="marketplace_type", color_discrete_sequence=px.colors.qualitative.Vivid)
fig3.update_layout(
    title='Total monthly 0% Marketplace sales',
    xaxis_tickfont_size=14,
    yaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

tab1, tab2, tab3 = st.tabs(["Total daily wash sales", "Total weekly wash sales", "Total monthly wash sales"])

with tab1:
    st.plotly_chart(fig1, theme="streamlit", use_container_width=True)

with tab2:
    st.plotly_chart(fig2, theme="streamlit", use_container_width=True)

with tab3:
    st.plotly_chart(fig3, theme="streamlit", use_container_width=True)


# In[30]:


import plotly.express as px

fig1 = px.bar(df, x="date", y="purchasers", color="marketplace_type", color_discrete_sequence=px.colors.qualitative.Safe)
fig1.update_layout(
    title='Daily 0% Marketplace purchasers',
    xaxis_tickfont_size=14,
    yaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)


fig2 = px.bar(df2, x="date", y="purchasers", color="marketplace_type", color_discrete_sequence=px.colors.qualitative.Safe)
fig2.update_layout(
    title='Weekly 0% Marketplace purchasers',
    xaxis_tickfont_size=14,
    yaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

fig3 = px.bar(df3, x="date", y="purchasers", color="marketplace_type", color_discrete_sequence=px.colors.qualitative.Safe)
fig3.update_layout(
    title='Monthly 0% Marketplace purchasers',
    xaxis_tickfont_size=14,
    yaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

tab1, tab2, tab3 = st.tabs(["Daily wash purchasers", "Weekly wash purchasers", "Monthly wash purchasers"])

with tab1:
    st.plotly_chart(fig1, theme="streamlit", use_container_width=True)

with tab2:
    st.plotly_chart(fig2, theme="streamlit", use_container_width=True)

with tab3:
    st.plotly_chart(fig3, theme="streamlit", use_container_width=True)


# In[31]:


import plotly.express as px

fig1 = px.bar(df, x="date", y="cum_purchasers", color="marketplace_type", color_discrete_sequence=px.colors.qualitative.Safe)
fig1.update_layout(
    title='Total daily 0% Marketplace purchasers',
    xaxis_tickfont_size=14,
    yaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)


fig2 = px.bar(df2, x="date", y="cum_purchasers", color="marketplace_type", color_discrete_sequence=px.colors.qualitative.Safe)
fig2.update_layout(
    title='Total weekly 0% Marketplace purchasers',
    xaxis_tickfont_size=14,
    yaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

fig3 = px.bar(df3, x="date", y="cum_purchasers", color="marketplace_type", color_discrete_sequence=px.colors.qualitative.Safe)
fig3.update_layout(
    title='Total monthly 0% Marketplace purchasers',
    xaxis_tickfont_size=14,
    yaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

tab1, tab2, tab3 = st.tabs(["Total daily wash purchasers", "Total weekly wash purchasers", "Total monthly wash purchasers"])

with tab1:
    st.plotly_chart(fig1, theme="streamlit", use_container_width=True)

with tab2:
    st.plotly_chart(fig2, theme="streamlit", use_container_width=True)

with tab3:
    st.plotly_chart(fig3, theme="streamlit", use_container_width=True)


# In[32]:


import plotly.express as px

fig1 = px.area(df, x="date", y="sales_volume", color="marketplace_type", color_discrete_sequence=px.colors.qualitative.Plotly)
fig1.update_layout(
    title='Daily 0% Marketplace volume',
    xaxis_tickfont_size=14,
    yaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)


fig2 = px.area(df2, x="date", y="sales_volume", color="marketplace_type", color_discrete_sequence=px.colors.qualitative.Plotly)
fig2.update_layout(
    title='Weekly 0% Marketplace volume',
    xaxis_tickfont_size=14,
    yaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

fig3 = px.area(df3, x="date", y="sales_volume", color="marketplace_type", color_discrete_sequence=px.colors.qualitative.Plotly)
fig3.update_layout(
    title='Monthly 0% Marketplace volume',
    xaxis_tickfont_size=14,
    yaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

tab1, tab2, tab3 = st.tabs(["Daily wash volume (USD)", "Weekly wash volume (USD)", "Monthly wash volume (USD)"])

with tab1:
    st.plotly_chart(fig1, theme="streamlit", use_container_width=True)

with tab2:
    st.plotly_chart(fig2, theme="streamlit", use_container_width=True)

with tab3:
    st.plotly_chart(fig3, theme="streamlit", use_container_width=True)


# In[33]:


import plotly.express as px

fig1 = px.area(df, x="date", y="cum_sales_volume", color="marketplace_type", color_discrete_sequence=px.colors.qualitative.Plotly)
fig1.update_layout(
    title='Daily total 0% Marketplace volume',
    xaxis_tickfont_size=14,
    yaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)


fig2 = px.area(df2, x="date", y="cum_sales_volume", color="marketplace_type", color_discrete_sequence=px.colors.qualitative.Plotly)
fig2.update_layout(
    title='Weekly total 0% Marketplace volume',
    xaxis_tickfont_size=14,
    yaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

fig3 = px.area(df3, x="date", y="cum_sales_volume", color="marketplace_type", color_discrete_sequence=px.colors.qualitative.Plotly)
fig3.update_layout(
    title='Monthly total 0% Marketplace volume',
    xaxis_tickfont_size=14,
    yaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

tab1, tab2, tab3 = st.tabs(["Total daily wash volume (USD)", "Total weekly wash volume (USD)", "Total monthly wash volume (USD)"])

with tab1:
    st.plotly_chart(fig1, theme="streamlit", use_container_width=True)

with tab2:
    st.plotly_chart(fig2, theme="streamlit", use_container_width=True)

with tab3:
    st.plotly_chart(fig3, theme="streamlit", use_container_width=True)


# In[ ]:




