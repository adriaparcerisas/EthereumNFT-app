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


st.title('NFT purchasing behavior')


# In[3]:


st.markdown('The user behavior on the major of the blockchains are different. The same occurs with the NFT purchases over the entire ecosystem. In this section we are gonna analyze the distribution of Ethereum NFT sales and the purchases above and below some specific prices to determine the trends.') 


# In[4]:


st.markdown('First of all, we will take a look at the distribution of both sales and purchasers by the price of the sales, and we will find some correlation between both metrics. The prices are grouped in different buckets such as:')
st.write('- Price above 500 USD')
st.write('- Between 100 and 500 USD')
st.write('- Between 10 and 50 USD')
st.write('- Between 5 and 10 USD')
st.write('- Between 2 and 5 USD')
st.write('- Between 0.5 and 2 USD')
st.write('- Below 0.5 USD')
st.write('')


# In[5]:


sql = f"""
SELECT
case when price_usd >500 then 'a. >500 USD'
  when price_usd between 100 and 500 then 'b. 100-500 USD'
  when price_usd between 50 and 100 then 'c. 50-100 USD'
  when price_usd between 10 and 50 then 'd. 10-50 USD'
  when price_usd between 5 and 10 then 'e. 5-10 USD'
  when price_usd between 2 and 5 then 'f. 2-5 USD'
  when price_usd between 0.5 and 2 then 'g. 0.5-2 USD'
  else 'h. <0.5 USD' end as "Price Range",
  count(distinct tx_hash) as "Number of sales",
  count(distinct buyer_address) as "Number of purchasers"
from ethereum.core.ez_nft_sales
group by 1
order by 1
"""

sql2 = f"""
WITH
  table1 as (
  SELECT
  count(distinct tx_hash) as all_sales
  from ethereum.core.ez_nft_sales
  ),
  table2 as (
SELECT
count(case when price_usd >100 then 1 end) as n_sales_above_100,
count(case when price_usd >1000 then 1 end) as n_sales_above_1000
from ethereum.core.ez_nft_sales
)
SELECT
all_sales as "Total Ethereum NFT sales",
n_sales_above_100 as "Sales above 100 USD",
n_sales_above_1000 as "Sales above 1000 USD",
(n_sales_above_100/all_sales)*100 as "Percentage of sales above 100 USD",
(n_sales_above_1000/all_sales)*100 as "Percentage of sales above 1000 USD"
from table1, table2
"""

sql3 = f"""
WITH
  table1 as (
  SELECT
  count(distinct buyer_address) as total_purchasers
  from ethereum.core.ez_nft_sales
  ),
  table2 as (
SELECT
count(distinct buyer_address) as n_purchasers_above_100
from ethereum.core.ez_nft_sales
  where price_usd >100
),
  table3 as (
SELECT
count(distinct buyer_address) as n_purchasers_above_1000
from ethereum.core.ez_nft_sales
  where price_usd >1000
)
SELECT
total_purchasers as "Total Ethereum NFT purchasers",
n_purchasers_above_100 as "Purchasers buying above 100 USD",
n_purchasers_above_1000 as "Purchasers buying above 1000 USD",
(n_purchasers_above_100/total_purchasers)*100 as "Percentage of purchasers that bought above 100 USD",
(n_purchasers_above_1000/total_purchasers)*100 as "Percentage of purchasers that bought above 1000 USD"
from table1, table2, table3
"""


# In[6]:


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


# In[7]:


import plotly.graph_objects as go
fig1 = go.Figure([go.Bar(x=df['price range'], y=df['number of sales'],marker_color=px.colors.qualitative.Plotly)])
fig1.update_layout(
    title='Distribution of sales by NFT price range',
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

fig2 = go.Figure([go.Bar(x=df['price range'], y=df['number of purchasers'],marker_color=px.colors.qualitative.Vivid)])
fig2.update_layout(
    title='Distribution of purchasers by NFT price range',
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


st.plotly_chart(fig1, theme="streamlit", use_container_width=True)
st.plotly_chart(fig2, theme="streamlit", use_container_width=True)


# In[8]:


fig3 = go.Figure([go.Scatter(x=df['number of purchasers'], y=df['number of sales'],marker_color=px.colors.qualitative.Plotly)])
fig3.update_layout(
    title='Number of sales vs number of purchasers',
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
st.plotly_chart(fig3, theme="streamlit", use_container_width=True)


# In[9]:


st.write('')


# In[10]:


import math

millnames = ['',' k',' M',' B',' T']

def millify(n):
    n = float(n)
    millidx = max(0,min(len(millnames)-1,
                        int(math.floor(0 if n == 0 else math.log10(abs(n))/3))))

    return '{:.0f}{}'.format(n / 10**(3 * millidx), millnames[millidx])


# In[11]:


st.markdown(""" <style> div.css-12w0qpk.e1tzin5v2{
 background-color: #f5f5f5;
 border: 2px solid;
 padding: 10px 5px 5px 5px;
 border-radius: 10px;
 color: #ffc300;
 box-shadow: 10px;
}
div.css-1r6slb0.e1tzin5v2{
 background-color: #f5f5f5;
 border: 2px solid; /* #900c3f */
 border-radius: 10px;
 padding: 10px 5px 5px 5px;
 color: green;
}
div.css-50ug3q.e16fv1kl3{
 font-weight: 900;
} 
</style> """, unsafe_allow_html=True)

col1,col2,col3 =st.columns(3)
with col1:
    st.metric('Number of NFT sales', millify(df2['total ethereum nft sales'][0]))
col2.metric('Number of sales above 100 USD', millify(df2['sales above 100 usd'][0]))
col3.metric('Number of sales above 1000 USD', millify(df2['sales above 1000 usd'][0]))

col4,col5=st.columns(2)
with col4:
    st.metric('Percentage of sales above 100 USD',df2['percentage of sales above 100 usd'][0])
col5.metric('Percentage of sales above 1000 USD',df2['percentage of sales above 1000 usd'][0])


# In[12]:


col1,col2,col3 =st.columns(3)
with col1:
    st.metric('Number of NFT purchasers', millify(df3['total ethereum nft purchasers'][0]))
col2.metric('Purchasers buying above 100 USD', millify(df3['purchasers buying above 100 usd'][0]))
col3.metric('Purchasers buying above 1000 USD', millify(df3['purchasers buying above 1000 usd'][0]))

col4,col5=st.columns(2)
with col4:
    st.metric('% of purchasers buying above 100 USD',df3['percentage of purchasers that bought above 100 usd'][0])
col5.metric('% of purchasers buying above 1000 USD',df3['percentage of purchasers that bought above 1000 usd'][0])


# In[17]:


sql4 = f"""
WITH
  ethereum_sales as (
SELECT
trunc(block_timestamp,'month') as date,
  max(price_usd) as high_NFT_price_sale
from ethereum.core.ez_nft_sales where price_usd is not null
group by 1
order by 1 asc
  )
SELECT
x.date,
x.high_NFT_price_sale as "High Ethereum NFT price sale",
lag(x.high_NFT_price_sale,1) over (order by x.date) as lasts,
((x.high_NFT_price_sale-lasts)/lasts)*100 as "High Ethereum NFT price sale % growth"
from ethereum_sales x
order by 1 asc
"""

sql5="""
WITH
  ethereum_sales as (
SELECT
trunc(block_timestamp,'month') as date,
  max(price_usd) as high_NFT_price_sale
from ethereum.core.ez_nft_sales where price_usd is not null
group by 1
order by 1 asc
  ),
  final_data as (
SELECT
x.date,
x.high_NFT_price_sale as "High Ethereum NFT price sale",
lag(x.high_NFT_price_sale,1) over (order by x.date) as lasts,
((x.high_NFT_price_sale-lasts)/lasts)*100 as "High Ethereum NFT price sale % growth"
from ethereum_sales x
order by 1 asc
  )
SELECT
date,
  "High Ethereum NFT price sale % growth",
  sum("High Ethereum NFT price sale % growth") over (order by date) as "Cumulative growth of Highest Ethereum NFT price sale"
from final_data 
order by 1 asc
"""


# In[18]:


results4 = compute(sql4)
df4 = pd.DataFrame(results4.records)
df4.info()

results5 = compute(sql5)
df5 = pd.DataFrame(results5.records)
df5.info()


# In[19]:


fig1 = px.line(df4, x="date", y="high ethereum nft price sale", color_discrete_sequence=px.colors.qualitative.Plotly)
fig1.update_layout(
    title='Highest Ethereum NFT price sale evolution',
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
st.plotly_chart(fig1, theme="streamlit", use_container_width=True)
st.write('')


# In[20]:


import altair as alt
base=alt.Chart(df5).encode(x=alt.X('date:O', axis=alt.Axis(labelAngle=325)))
line=base.mark_line(color='darkgreen').encode(y=alt.Y('high ethereum nft price sale % growth:Q', axis=alt.Axis(grid=True)))
bar=base.mark_bar(color='green',opacity=0.5).encode(y='cumulative growth of highest ethereum nft price sale:Q')

st.altair_chart((bar + line).resolve_scale(y='independent').properties(title='Monthly Highest Ethereum NFT price sale (USD)',width=600))


# In[ ]:




