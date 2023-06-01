# Importing the modules
from bs4 import BeautifulSoup
import requests
import pandas as pd
from sellers import get_seller_names


# Scraping all the content from the url
url = "https://www.amazon.in/s?rh=n%3A6612025031&fs=true&ref=lp_6612025031_sar"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
    'Upgrade-Insecure-Requests': '1',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
    }
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")


### Scraping the Product name
product_name_tags = soup.find_all('span', attrs={'class':'a-size-base-plus a-color-base a-text-normal'})

### Scraping the Price
price_tags = soup.find_all('span', attrs={'class':'a-price-whole'})


### Scraping the Rating
rating_tags = soup.find_all('span', attrs={'class':'a-icon-alt'})
# Removing Demo stars(Avg.customer review ratings)
rating_tags = rating_tags[:-4]

### Scraping the Seller Names
seller_names = get_seller_names(url)

# converting all the tags into lists
products, prices, ratings = [], [], []
for i in range(len(product_name_tags)):
    products.append(product_name_tags[i].text)
    # Filtering Prices
    price = price_tags[i].text.replace(",","")
    prices.append(int(price))
    # Filtering ratings
    rating = rating_tags[i].text
    ratings.append(rating.split()[0])

# Product Name, Price, Rating, Seller Name (If not out of stock)
dataframe = pd.DataFrame({"Product Name":products, "Price (in Rupees)": prices, "Rating":ratings, "Seller":seller_names})
dataframe.to_csv("products_data.csv")