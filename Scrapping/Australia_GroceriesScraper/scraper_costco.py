from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
from datetime import datetime
import os, requests, sys, random, json
import pandas as pd
from urllib.parse import quote_plus

# def setup_mongo():
#     # Load environment variables from .env file if it exists
#     load_dotenv()
    
#     # MongoDB credentials
#     username = os.getenv('MONGO_USERNAME', 'discountmate')
#     password = os.getenv('MONGO_PASSWORD', 'discountmate1')
    
#     # Encode credentials for MongoDB URI
#     encoded_username = quote_plus(username)
#     encoded_password = quote_plus(password)
    
#     # MongoDB URI construction
#     uri = f'mongodb+srv://{encoded_username}:{encoded_password}@discountmatecluster.u80y7ta.mongodb.net/?retryWrites=true&w=majority&appName=DiscountMateCluster'
    
#     # Initialize MongoDB client
#     client = MongoClient(uri, server_api=ServerApi('1'))
    
#     try:
#         client.admin.command('ping')
#         print("Pinged your deployment. You successfully connected to MongoDB!")
#     except Exception as e:
#         print(e)
#         sys.exit()
    
#     # MongoDB database and collection
#     db = client['ScrappedData']
    
#     # Generate the custom string with the current date and time
#     current_date_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
#     custom_string = f"{current_date_time}_Woolies"
    
#     # Define collection based on the custom string
#     collection = db[custom_string]
#     return collection


consonants = "bcdfghjklmnpqrstvwxyz"
vowels = "aeiou"

def generate_fake_word():
    """
    generate a random fake word for the user agent
    """
    word = ""
    length = random.choice([3, 4, 5, 6])
    for i in range(length):
        word += random.choice(consonants)
        word += random.choice(vowels)
    return word

def generate_random_version():
    """
    generate a random version for the user agent
    """
    first_digit = random.choice(['0', '1', '2', '3'])
    second_digit = random.choice(['0', '1', '2', '3','4','5','6','7','8','9'])
    return first_digit + "." + second_digit

def random_tld():
    tlds = ['com', 'net', 'co', 'mil', 'biz', 'info', 'name', 'mobi', 'pro',
            'travel', 'museum', 'coop', 'aero', 'xxx', 'idv', 'int', 'jobs', 'post', 'rec']
    return random.choice(tlds)

def get_fake_user_agent():
    fake_site = generate_fake_word()
    version = generate_random_version()
    domain = random_tld()
    return f'{fake_site}/{version} (http://{fake_site}.{domain})'


def safe_get(dictionary, keys, default=''):
    """
    Safely get the value from a nested dictionary using a list of keys.
    """
    current = dictionary
    for key in keys:
        try:
            current = current[key]
        except (KeyError, TypeError):
            return default
    return current


scraped_data = []
base_url = 'https://www.costco.com.au/rest/v2/australia/products/search'

headers = {
    "accept": "application/json, text/plain, */*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "en-US,en;q=0.9",
    "connection": "keep-alive",
    "content-type": "application/json",
    # "cookie": "session_uuid=912c2954-f984-4645-9ccc-94b3b7c12a65; ROUTEID=.app12; HAPC=fe06; GCLB=COmVuIjdicP5FRAD; UserPreferences=visited-analyticsEnabled-preferencesEnabled; tire-search-criteria=dGV4dA==; bm_mi=CA5CDA8EA17AA3DF49F89382DDAE1A0A~YAAQHyraF5qehjCTAQAA3r74PBmGlK6voPTFXuDSM6AyggnU2qAtSE0Plqka4FbPKiv5zLBVP/kIJFEhMTrcYlXLvVeqNwTSN0vCHXoU6ASgqljHwto/J3g17KmbICccdOnhQPqR/jgtlCL5YVh4rUq2v2DfSpJlImz/cnrOxKtji02xazFwLyeGvgJYx7WTIcQ/aFS1rMWLgZVpYI6o6NORqZE2czFIs8fzkeE/van15BrMN2WPrJyohIA3HvCd6wY5YR9/BK014pxWCGaJoTgxHQFSOnlMgwsIxM29m3JBznlKFUth7bfS10kCFgPZijLe4djqPuVSSw==~1; JSESSIONID=Y12-09d01e3e-fa87-481e-97e3-4732b97b192a; SF_SESSION_ID=WTEyLTA5ZDAxZTNlLWZhODctNDgxZS05N2UzLTQ3MzJiOTdiMTkyYQ==; ak_bmsc=AB53304CA524E20468369A974D735C35~000000000000000000000000000000~YAAQHSraF5xqty+TAQAAB8P4PBnfqO76ZuF9tBoZ6zNHXZO8OkEr68l2Y4K33k5ySge6VKYR93aF7UrevvtrVIAWB6MMm+MNdHUO9CMi2Az2hMZu0Z7CrW35IHeN7T+v08jbUBNHljMGsHxMxKSik+nNw+Oa5fBNk7uEgO9bQlD9lSDUOHRVIwwsHbNiXcEij/iwKlSiq25hJ1IqRPDarzxCr0fGHtCWpV9Yn4dLlVf7mQRSiEjfe2IpjGL3vlhJXFMtyb0X8CkRYftlX/jhI+1jzq1YxUTyqrVQ9JT/2Nm2zrrK67o8cP43NXipIpgsEqven8sfpMHt6msHQwjTUkuTfmgyRPwhDCDFy5NOoBLb0S6IGvvZh7zVi1vag//GePEkpCQyVLuE3eUKFCVIn/dYNq+dvgRcoh7jqn1A9wfuI2n3Xw2dppP2d0wY+07Vp5kT/+9R3yz2of4ig5B57nJgy00ftiBjbyChl3a7pZ0d7ArnNovE244x+mDd; tire-search-filters=L2MvaG90LWJ1eXM%3D; bm_sv=35F74BAF74536ADBB042772BC9290C20~YAAQHSraF+Fsty+TAQAAp8j4PBltbPGLBVYN8WApT1m3mjHV/hnkDsnN8z6kglJQW9wXzJWkcQ4Xb9sOgA8V3ravJtdcTEm1AnVryNheldu9Ot5KxfKFGEefhSLLJv9Xle5dlU3TZiM6kIBTV8IE6VWi6o+1gbUzkIxsIivcLTlmDArmEbMrLNzSZUy8RXA8vb+1fouj0cmHLt9yA+4k6OHZbegMP74MB4ksvcPIl8BJXQ40onG9Hi1whIfC+3XJs38jvg==~1",
    "host": "www.costco.com.au",
    # "if-none-match": '"07204a0f8775e6cc537658f9322fb5dd7-gzip"',
    "referer": "https://www.costco.com.au/c/hot-buys",
    # "sec-ch-ua": '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": get_fake_user_agent()
}


page = 1
while True:
    print(page)
    query_params = {
        "fields": "FULL",
        "query": "",
        "pageSize": 48,
        "category": "hot-buys",
        "lang": "en_AU",
        "curr": "AUD"
    }
    
    if page > 1:
        query_params.update({'currentPage': page-1})

    print(query_params)
    response = requests.get(base_url, headers=headers, params=query_params)
    data = response.json()


    for product in data['products']:
        product_info = {
            'name': product.get('englishName', 'N/A'),
            'value': safe_get(product, ['price', 'value'], 0),
            'product_link': 'https://www.costco.com.au' + product.get('url', 'N/A'),
            'code': product.get('code', 'N/A'),
            'averageRating': product.get('averageRating', 0),
            'discount_value': safe_get(product, ['couponDiscount', 'discountValue'], 0),
            'discount_end_date': product.get('discountEndDate', 'N/A'),
            'discount_start_date': product.get('discountStartDate', 'N/A'),
            'in_stock': product.get('stock', {}).get('stockLevelStatus', 'N/A'),
            'images_link': ['https://www.costco.com.au' + img['url'] for img in product.get('images', [])]
        }
        scraped_data.append(product_info)

    totalPages = data['pagination']['totalPages']
    if page >= totalPages:
        break
    page += 1


df = pd.DataFrame(scraped_data)
df.to_csv('costco_products.csv', index=False)