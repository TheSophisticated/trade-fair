import streamlit as st
import pandas as pd
from streamlit_extras.stylable_container import stylable_container
import streamlit_shadcn_ui as ui
import streamlit_lottie as st_lottie
import time
import numpy as np


st.set_page_config(page_title="Mayoor Trade Fair", initial_sidebar_state='collapsed')

#Setting User Budget
if 'user_wallet' not in st.session_state:
    st.session_state.user_wallet = 100


companies = {
    "ADNOC": {"share_price": 10, "shares_bought": 0},
    "Aldar": {"share_price": 10, "shares_bought": 0},
    "EMAAR": {"share_price": 10, "shares_bought": 0},
    "Etihad": {"share_price": 10, "shares_bought": 0},
    "ADCB": {"share_price": 10, "shares_bought": 0},
    "FAB": {"share_price": 10, "shares_bought": 0},
    "Etisalat": {"share_price": 10, "shares_bought": 0},
    "Almarai": {"share_price": 10, "shares_bought": 0},
    "Al Ain Agthia": {"share_price": 10, "shares_bought": 0},
    "Al Islamic Bank": {"share_price": 10, "shares_bought": 0},
    "Insurance Market AE": {"share_price": 10, "shares_bought": 0},
    "DAMAC": {"share_price": 10, "shares_bought": 0},
}


if 'companies' not in st.session_state:
    st.session_state.companies = {company_name: state for company_name, state in companies.items()}

def buy_shares(company, shares):
    if st.session_state.companies[company]['share_price']*shares <= st.session_state.user_wallet:
        st.session_state.user_wallet-= st.session_state.companies[company]['share_price']*shares
        st.session_state.companies[company]['shares_bought'] += shares
        if st.session_state.companies[company]['shares_bought'] != 0 and shares != 0:
            st.session_state.companies[company]['share_price'] += 2*(st.session_state.companies[company]['shares_bought']//10 - (st.session_state.companies[company]['shares_bought'] - shares)//10)
    else:
        st.error("You have Insufficient Funds")

def sell_shares(company, shares):   
    if st.session_state.companies[company]['shares_bought'] != 0 and shares != 0:
        st.session_state.companies[company]['shares_bought'] -= shares
        if shares // 10 != 0:
            st.session_state.companies[company]['share_price'] -= 2*(st.session_state.companies[company]['shares_bought']//10 - (st.session_state.companies[company]['shares_bought'] - shares)//10)
        st.session_state.user_wallet += st.session_state.companies[company]['share_price']*shares

#Function to variate data so the graph doesn't look still
def generate_random_data():
    data = pd.DataFrame()
    for company_name, company_state in st.session_state.companies.items():
        share_price = company_state['share_price'] + np.random.randn()*0.1  # Random fluctuation in share price
        data[company_name] = [share_price]
    return data

page = st.sidebar.radio("Navigation", ["Home", "Graphs"])

st.markdown("<div style='text-align: center;'><h1>Mayoor Trade Fair 📈</h1></div>", unsafe_allow_html=True)
st.write("\n")

if page == 'Home':
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
            print(clicked)
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

if page == "Graphs":
    chart_data = pd.DataFrame()

    chart = st.line_chart(chart_data)

    while True:
        new_data = generate_random_data()
        chart_data = pd.concat([chart_data, new_data], ignore_index=True)
        chart.line_chart(chart_data)
        time.sleep(1)  # Update every second