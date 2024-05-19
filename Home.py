#Importing Dependencies
import streamlit as st
import pandas as pd
from streamlit_extras.stylable_container import stylable_container
import streamlit_shadcn_ui as ui
import streamlit_lottie as st_lottie
import time
import numpy as np
from appwrite import *
from appwrite.client import Client
from appwrite.services.databases import Databases


#Initiallsing Connection to Database Service
client = Client()
client.set_endpoint('https://cloud.appwrite.io/v1')
client.set_project('661120831f4c4955bc79')
client.set_key('65250e16b001d108af2b6879ed57b9bb69cd80e20f7855db2d62ed3bc8a6d5670eb9547d2f6de89a68a1dec126dbb8a480f83017253ed54bf3a3f04694a2fe5a9364fa8147604b9754d75049784016adda59d1f0dc112320204ed8f5e523343e32081d1da2642f9696b3e0d2d535f417770baf2116d16aa6dda8c56ca4718477')
database = Databases(Client)

#Simple Page Config
st.set_page_config(page_title="Mayoor Trade Fair", initial_sidebar_state='collapsed')

#Setting User Budget
if 'user_wallet' not in st.session_state:
    st.session_state.user_wallet = 100

#Declaring Basic Compnay Data
companies = {
    "ADNOC": {"share_price": 10, "shares_bought": 0},
    "Aldar": {"share_price": 10, "shares_bought": 0},
    "EMAAR": {"share_price": 10, "shares_bought": 0},
    "Etihad": {"share_price": 10, "shares_bought": 0},
    "ADCB": {"share_price": 10, "shares_bought": 0},
    "FAB": {"share_price": 10, "shares_bought": 0},
    "Etisalat": {"share_price": 10, "shares_bought": 0},
    "Al Marai Farms": {"share_price": 10, "shares_bought": 0},
    "Al Ain Agthia": {"share_price": 10, "shares_bought": 0},
    "Al Islamic Bank": {"share_price": 10, "shares_bought": 0},
    "Insurance Market AE": {"share_price": 10, "shares_bought": 0},
    "DAMAC": {"share_price": 10, "shares_bought": 0},
}

#Generating State Variable Dictionary For the Companies
if 'companies' not in st.session_state:
    st.session_state.companies = {company_name: state for company_name, state in companies.items()}

    
#Defining Function to Update Database in Appwrite
def update_document(document_id, share_price, shares_sold):
    data={"share_price": share_price, "shares_sold": shares_sold}
    document = database.update_document(
      database_id="shares",
      collection_id="stocks",
      document_id=document_id,
      data=data
    )

#Implement ability to Buy Shares
def buy_shares(company, shares):
    if st.session_state.companies[company]['share_price']*shares <= st.session_state.user_wallet:
        st.session_state.user_wallet-= st.session_state.companies[company]['share_price']*shares
        st.session_state.companies[company]['shares_bought'] += shares
        if st.session_state.companies[company]['shares_bought'] != 0 and shares != 0:
            st.session_state.companies[company]['share_price'] += 2*(st.session_state.companies[company]['shares_bought']//10 - (st.session_state.companies[company]['shares_bought'] - shares)//10)
            new_price = st.session_state.companies[company]['share_price']
            Databases(client).update_document("shares", "stocks", get_doc_id(company), data={"share_price": new_price, "shares_sold": st.session_state.companies[company]['shares_bought']})
    else:
        st.error("You have Insufficient Funds")

#Implement ability to Sell Shares
def sell_shares(company, shares):   
    if st.session_state.companies[company]['shares_bought'] != 0 and shares != 0:
        st.session_state.companies[company]['shares_bought'] -= shares
        if shares // 10 != 0:
            st.session_state.companies[company]['share_price'] -= 2*(st.session_state.companies[company]['shares_bought']//10 - (st.session_state.companies[company]['shares_bought'] - shares)//10)
            new_price = st.session_state.companies[company]['share_price']
            Databases(client).update_document("shares", "stocks", get_doc_id(company), data={"share_price": new_price, "shares_sold": st.session_state.companies[company]['shares_bought']})
            #update_document(st.session_state.companies[company], st.session_state.companies[company]['share_price'], st.session_state.companies[company]['shares_bought'])
        st.session_state.user_wallet += st.session_state.companies[company]['share_price']*shares

#Getting Documents
def get_documents():
    documents = Databases(client).list_documents("shares", "stocks")
    return documents["documents"]
    if documents and "documents" in documents:
      return documents["documents"]
    else:
        print("Error retrieving documents")
        return []

#Getting Document id
def get_doc_id(company):
    documents = get_documents()
    for doc in documents:
        if doc['share_name'] == company:
            return doc["$id"]
    return None

#Getting Actual Data from Database
def get_data():
    documents = get_documents()
    if documents:
        latest_document = documents[0]
        return{
            "share_name": latest_document["share_name"],
            "share_price": latest_document["share_price"],
            "shares_sold": latest_document["shares_sold"]
        }
    else:
        return None

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



#Basic Title Configs
st.markdown("<div style='text-align: center;'><h1>Mayoor Trade Fair 📈</h1></div>", unsafe_allow_html=True)
st.write("\n")

if "name" in st.session_state:
    name = st.session_state["name"]
    st.subheader(f"Current User: {name}")


#Adding Main Page
company = st.selectbox(
    'Chose the Company you want to invest into',
    list(companies.keys())
)

with st.container():
    st.title(company)
    col1, col2 = st.columns(2)
    

    with col1:
        num_shares = st.number_input("Enter Number of Shares to Buy: ", min_value=0)
        clicked = ui.button("Buy Shares", key="clk_btn", class_name="bg-green-500 text-white")
        if clicked:
            buy_shares(company, num_shares)
        
            
    with col2:
        shares_sell = st.number_input("Enter Number of Shares to Sell: ", min_value=0, max_value=st.session_state.companies[company]['shares_bought'])
        
        if ui.button("Sell Shares", key="sell_btn", class_name="bg-red-500 text-white"):
            sell_shares(company, shares_sell)


with st.container():
    col1, col2 = st.columns(2)

    with col1:

        ui.metric_card(title="Shares Owned: ", content=st.session_state.companies[company]['shares_bought'], description="Total Shares of this Company bought at the Event", key="card1")
    with col2:
        ui.metric_card(title="Shares Price: ", content=st.session_state.companies[company]['share_price'], description="Current Share Price", key="card2")

st.title(f":blue[Current Balance]: {st.session_state.user_wallet}")

if st.button("New User"):
    st.session_state.user_wallet = 100
    name = ''
    st.session_state["name"] = ''
    st.switch_page("pages/name.py")

#Graph Page
    # chart_data = pd.DataFrame()

    # chart = st.line_chart(chart_data)

    # while True:
    #     latest_data = get_data()
    #     new_data = generate_random_data()
    #     chart_data = pd.concat([latest_data, new_data], ignore_index=True)
    #     chart.line_chart(chart_data)
    #     time.sleep(1)  # Update every second