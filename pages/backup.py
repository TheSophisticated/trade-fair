import streamlit as st
import pandas as pd
from streamlit_extras.stylable_container import stylable_container
import streamlit_shadcn_ui as ui
from streamlit_lottie import st_lottie


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
    # Add more companies here
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

st.markdown("<div style='text-align: center;'><h1>Mayoor Trade Fair 📈</h1></div>", unsafe_allow_html=True)
st.write("\n")
  

with st.container():
    col1, second_col = st.columns(2)

    with col1:
        company = st.selectbox(
            'Chose the Company you want to invest into',
            list(companies.keys())
        )


        with st.container():
            st.title(company)
            col1, col2 = st.columns(2)

            with col1:
                num_shares = st.number_input("Enter Number of Shares to Buy: ", min_value=0, max_value=10)
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

with second_col:
    url = "https://lottie.host/3516d402-ca03-4261-a562-dcd98ad9b177/AqFA1YyMLU.json" #Lottie Retrieval Code
    st_lottie(url, loop=True,height = 300, width = 300)

