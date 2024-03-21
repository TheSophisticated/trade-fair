#Import Dependencies
import streamlit as st

# set_page_config
st.set_page_config(page_title="Mayoor Trade Fair", layout='centered',
                   initial_sidebar_state='collapsed')

st.markdown("<div style='text-align: center;'><h1>Mayoor Trade Fair 📈</h1></div>", unsafe_allow_html=True)
st.write("\n")

stocks = {'Company 1': 10,'Company 2': 10,'Company 3': 10,'Company 4': 10,'Company 5': 10,'Company 6': 10,'Company 7': 10,'Company 8': 10,}
shares = [10]
with st.container():
    col1, col2 = st.columns(2)

    with col1: 
        st.subheader("Company 1")
        st.write("Current Share Price:", shares[0])
        if (st.button("Buy Share")):
            shares[0] = shares[0]+1
            print(shares[0])
        st.button("Sell Share")