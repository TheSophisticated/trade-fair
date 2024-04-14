import pandas as pd
import numpy as np
from appwrite.client import Client
from appwrite.services.databases import Databases
import streamlit as st
import time

#Initiallsing Connection to Database Service
client = Client()
client.set_endpoint('https://cloud.appwrite.io/v1')
client.set_project('661120831f4c4955bc79')
client.set_key('65250e16b001d108af2b6879ed57b9bb69cd80e20f7855db2d62ed3bc8a6d5670eb9547d2f6de89a68a1dec126dbb8a480f83017253ed54bf3a3f04694a2fe5a9364fa8147604b9754d75049784016adda59d1f0dc112320204ed8f5e523343e32081d1da2642f9696b3e0d2d535f417770baf2116d16aa6dda8c56ca4718477')
database = Databases(Client)


# Function to retrieve latest share prices from Appwrite for all companies
def get_latest_share_prices():
    database = Databases(client)
    response = database.list_documents(
        collection_id='stocks',
        database_id="shares"
    )
    documents = response['documents']
    share_prices = {}
    for doc in documents:
        share_prices[doc['share_name']] = doc['share_price']
    return share_prices

# Function to generate random data for each company using the latest share prices
def generate_random_data():
    latest_share_prices = get_latest_share_prices()
    data = pd.DataFrame(columns=latest_share_prices.keys())
    for company_name, share_price in latest_share_prices.items():
        fluctuated_price = share_price + np.random.randn() * 0.1  # Random fluctuation in share price
        data[company_name] = [fluctuated_price]
    return data


chart_data = pd.DataFrame()

chart = st.line_chart(chart_data)

while True:
    new_data = generate_random_data()
    chart_data = pd.concat([chart_data, new_data], ignore_index=True)
    chart.line_chart(chart_data)
    time.sleep(1)  # Update every second