
import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_mytek_informatique():
    base_url = "https://www.mytek.tn/informatique/ordinateurs-portables/pc-portable.html"
    category_url = f"{base_url}/informatique.html"
    products = []
    page = 1

    while True:
        # Fetch the page with pagination
        url = f"{category_url}?p={page}" if page > 1 else category_url
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            print(f"Failed to fetch page {page}. Status code: {response.status_code}")
            break

        soup = BeautifulSoup(response.text, 'html.parser')
        product_items = soup.find_all('div', class_='product-item-info')  # Adjust class based on actual HTML

        if not product_items:
            print(f"No more products found on page {page}. Exiting.")
            break

        for item in product_items:
            try:
                name = item.find('a', class_='product-item-link').text.strip()
                price = item.find('span', class_='price').text.strip()
                product_url = item.find('a', class_='product-item-link')['href']
                products.append({
                    "Product": name,
                    "Price": price,
                    "URL": product_url
                })
            except Exception as e:
                print(f"Error parsing product: {e}")

        print(f"Scraped page {page} with {len(product_items)} products.")
        page += 1

    # Save to CSV
    df = pd.DataFrame(products)
    df.to_csv("mytek_informatique_products.csv", index=False)
    print(f"Saved {len(products)} products to 'mytek_informatique_products.csv'.")

if __name__ == "__main__":
    scrape_mytek_informatique()