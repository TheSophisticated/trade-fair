import streamlit as st

st.set_page_config(page_title="Mayoor Trade Fair", initial_sidebar_state='collapsed')

companies = {
    "XYZ Corp": {"share_price": 10, "shares_bought": 0},
    "ABC Inc": {"share_price": 10, "shares_bought": 0},
    # Add more companies here
}

if 'companies' not in st.session_state:
    st.session_state.companies = {company_name: state for company_name, state in companies.items()}


if 'share_1' not in st.session_state:
    st.session_state.share_1 = 0
    st.session_state.price_1 = 10

def buy_shares(company, shares):
    st.session_state.companies[company]['shares_bought'] += shares
    if st.session_state.companies[company]['shares_bought'] != 0 and st.session_state.companies[company]['shares_bought'] % 10 == 0:
        st.session_state.companies[company]['share_price'] += 2*st.session_state.companies[company]['shares_bought'] // 10

def sell_shares(company, shares):
    st.session_state.companies[company]['shares_bought'] -= shares
    if st.session_state.companies[company]['shares_bought'] != 0:
        st.session_state.companies[company]['share_price'] -= 2       

st.markdown("<div style='text-align: center;'><h1>Mayoor Trade Fair 📈</h1></div>", unsafe_allow_html=True)
st.write("\n")


company = st.selectbox(
    'Chose the Company you want to invest into',
    list(companies.keys())
)

with st.container():
    st.title(company)
    col1, col2 = st.columns(2)

    with col1:
        num_shares = st.number_input("Enter Number of Shares to Buy: ", min_value=0, max_value=20)
        if st.button("Buy Shares"):
            buy_shares(company, num_shares)
    with col2:
        shares_sell = st.number_input("Enter Number of Shares to Sell: ", min_value=0, max_value=st.session_state.companies[company]['shares_bought'])
        if st.button("Sell Shares"):
            sell_shares(company, shares_sell)
    
    with st.container():
        col1, col2, col3 = st.columns(3)

        with col2:
            st.write(f"{company} Shares Owned: {st.session_state.companies[company]['shares_bought']}")
            st.write(f"{company} Share Price: {st.session_state.companies[company]['share_price']}")