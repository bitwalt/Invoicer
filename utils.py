import requests
import qrcode
import io


def create_qr_image(bolt11: str):
    qr = qrcode.QRCode()
    qr.add_data(bolt11)
    qr.make()
    img = qr.make_image()
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='JPEG')
    img_byte_arr = img_byte_arr.getvalue()
    return img_byte_arr 

parse_price = lambda price: float(price.replace(',', ''))

def get_btc_price() -> float:    
    response = requests.get('https://api.coindesk.com/v1/bpi/currentprice.json')
    data = response.json()
    return data["bpi"]["USD"]["rate"].split('.')[0]

def get_dollar_price(btc_price) -> str: 
    btc_float = parse_price(btc_price)
    dollar_sat = dollar_to_sat(btc_float)
    return str(dollar_sat)


def get_dollar_sats_data(daily_price):
    daily_price['sat_price'] = daily_price['price_btc'].apply(lambda d: dollar_to_sat(d))
    return daily_price['sat_price']
       


dollar_to_sat = lambda usd_price: int(1 / usd_price * (10 ** 8))
sats_to_dollar = lambda tot_sats, dollar_in_sat: tot_sats / int(dollar_in_sat)

    
