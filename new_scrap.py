
import pandas as pd
import requests
from bs4 import BeautifulSoup

def scrape_flipkart_product(goods_name):
    Product_Name = []
    Prices = []
    Description = []
    Reviews = []

    page = 1
    while True:
        try:
            url = f"https://www.flipkart.com/search?q={goods_name}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=off&as=off&page={page}"
            r = requests.get(url)
            soup = BeautifulSoup(r.text, 'html.parser')
            particular = soup.find('div', class_="_1YokD2 _3Mn1Gg")
            
            n_o_p = particular.find_all('a', class_='s1Q9rs')
            if not n_o_p:
                n_o_p = particular.find_all('a', class_='IRpwTa')
            if not n_o_p:
                n_o_p = particular.find_all('div', class_='_4rR01T')
            for item in n_o_p:
                n = item.text
                Product_Name.append(n)

            get_price = particular.find_all('div', class_='_30jeq3')
            if not get_price:
                get_price = particular.find_all('div', class_='_1vC4OE')
            if not get_price:
                get_price = particular.find_all('div', class_='_30jeq3 _1_WHN1')
            for item in get_price:
                n = item.text
                Prices.append(n)

            get_desc = particular.find_all('div', class_='_3Djpdu')
            if not get_desc:
                get_desc = particular.find_all('a', class_='_2mylT6')
            if not get_desc:
                get_desc = particular.find_all('ul', class_='_1xgFaf')
            for item in get_desc:
                n = item.text
                Description.append(n)

            o_p_r = particular.find_all('div', class_='_3LWZlK')
            if not o_p_r:
                o_p_r = particular.find_all('div', class_='_2_R_DZ')
            for item in o_p_r:
                n = item.text
                Reviews.append(n)
            
            next_button = particular.find('a', class_="_1LKTO3")
            if not next_button:
                break

            page += 1

        except requests.exceptions.RequestException as e:
            print("Error occurred while requesting the page:", e)
            
    max_length = max(len(Product_Name), len(Prices), len(Description), len(Reviews))
    fill_value = 'not available'

    # Extend lists to have the same length
    Product_Name += [fill_value] * (max_length - len(Product_Name))
    Prices += [fill_value] * (max_length - len(Prices))
    Description += [fill_value] * (max_length - len(Description))
    Reviews += [fill_value] * (max_length - len(Reviews))

    # Create DataFrame
    data = {
        'Product Name': Product_Name,
        'Price': Prices,
        'Description': Description,
        'Reviews': Reviews
    }
    df = pd.DataFrame(data)
    
    return df

goods_name = input("Enter the product you want to search for: ")
df = scrape_flipkart_product(goods_name)
print(df)
print()
print("Scraping done.")