import streamlit as st
import asyncio
from aiohttp.client import ClientSession
from pylnbits.config import Config
from pylnbits.user_wallet import UserWallet
from utils import *

c = Config(config_file="config.yml")

async def main():
    
    st.set_page_config(page_title="LN WALLET API", page_icon="🤖")
    st.title("LNBITs Invoicer")
    btc_price = get_btc_price()
    dollar_price = get_dollar_price(btc_price)
    col1, col2 = st.columns(2)
    col1.metric(label='BTC price', value=f"{btc_price} $")
    col2.metric(label='Dollar price', value=f"{dollar_price} SAT")
    
    st.subheader("Generate Invoice") 
    
    async with ClientSession() as session:
        uw = UserWallet(c, session)
        user_wallet = await uw.get_wallet_details()
        
        st.write(f"User Wallet: {user_wallet}")
        with st.container():
    
            amount_option = st.radio("Invoice type", ["SAT", "DOLLAR"])
            if amount_option == "SAT":
                st.header("Price in SAT")
                tot_sats = st.number_input("Set Invoice Amount in sat", min_value=50, step=50)
                dollar_value = tot_sats / int(dollar_price)
                st.metric(label='Dollar Value', value=f"{dollar_value:.4f} $")
            
                
            if amount_option == "DOLLAR":
                st.header("Price in Dollar")
                tot_dollar = st.number_input("Set Invoice Amount in $", min_value=0.01, step=0.01)
                tot_sats = int(tot_dollar * int(dollar_price))
                st.metric(label='Tot Sats', value=f"{tot_sats} SAT")
              
            memo = st.text_input("Memo", value="Demo Invoice")
                
            submitted = st.button("Request")
            if submitted:
                invoice = await uw.create_invoice(direction=False, amt=tot_sats, memo=memo, webhook="")
                st.json(invoice)
                bolt11 = invoice["payment_request"]
                qr_image = create_qr_image(bolt11)
                image_caption = f"INVOICE OF {tot_sats} SATS, {dollar_value:.2f} $ - MEMO: {memo}"
                st.image(qr_image, caption=image_caption, width=600)

                
if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())