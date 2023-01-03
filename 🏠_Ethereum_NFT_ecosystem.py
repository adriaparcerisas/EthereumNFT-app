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
import altair as alt
sdk = ShroomDK("7bfe27b2-e726-4d8d-b519-03abc6447728")


# In[2]:


st.title('Ethereum NFT ecosystem')


# In[3]:


st.markdown("**Ethereum** is the community-run technology powering the cryptocurrency ether (ETH) and thousands of decentralized applications [1](https://ethereum.org/en/).")
st.write("")
st.markdown("One of the main characteristics of Ethereum network are the **_Non-Fungible Tokens (NFTs)_**. Last year, the market growth exponentially and consequently, the number of marketplaces related to NFT to be purchased increased as well.")
st.markdown("NFTs have been the trending topic of cryptowolrd over the past year. In fact, emblematic persons like _Mark Zuckenberg_ told about that and basically, put their enterprise name Facebook a different name so called _Meta_ in reference to Metaverse, the world of NFTs. Thanks to that, the growth of this type of tokens increased exponentially in all the blockchain networks. One of the main networks have been Ethereum and in this dashboard we are gonna analyze several metrics about their growth. ")
st.write("")
st.markdown("This dashboard represents an **Ethereum NFT Market** trends. It is intended to provide an overview of the current market for NFTs in **Ethereum**. The idea is that readers can have at their disposal a tool to see the current volume of NFT sales, which are the most popular secondary markets, as well as to see other metrics such as the number of users, the average price per sale of NFTs, etc. All the metrics are displayed in a daily, weekly and monthly basis in both, global and by each marketplace ways.")
st.markdown("Finally, a current metrics about each Ethereum NFT collection is displayed. The metrics corresponds to volume, popularity, sales, and percentage growth daily and weekly.")
            


# In[4]:


st.markdown("To display all the information properly and make the app more readable and user-friendly, it has been divided in several parts. You can find information about each different section by navigating on the sidebar pages.")


# In[5]:


st.markdown("These includes:") 
st.markdown("1. **_General NFT trends_**")
st.markdown("2. **_NFT sector growth_**")
st.markdown("3. **_Marketplaces competition_**")
st.markdown("4. **_NFT royalties_**")
st.markdown("5. **_NFT purchasing behavior_**")
st.markdown("6. **_Collection trends_**")


# In[ ]:




