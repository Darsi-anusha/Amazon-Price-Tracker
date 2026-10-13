import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import time

# Headers to mimic a real browser and bypass basic bot detection
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
}

today = datetime.now().strftime("%Y-%m-%d")
save_path = r"C:\Users\Anusha\Downloads\freelancing\amazon_bata_bulk.csv"

# Open CSV file in append mode for daily automation
with open(save_path, mode="a", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    
    total_count = 0
    
    # Loop through multiple pages (e.g., Pages 1 to 3)
    for page_num in range(1, 4):
        print(f"Scraping Page {page_num}...")
        
        url = f"https://www.amazon.in/s?k=bata+women+sandals&page={page_num}"
        
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")
        products = soup.find_all("div", {"data-component-type": "s-search-result"})
        
        for item in products:
            img_tag = item.find("img", class_="s-image")
            product_name = img_tag["alt"] if img_tag else "Name not found"
            
            # Clean up "Sponsored Ad" tags from the product name
            product_name = product_name.replace("Sponsored Ad - ", "")
            
            price_tag = item.find("span", class_="a-price-whole")
            product_price = price_tag.get_text().strip() if price_tag else "Price not available"
            
            # Save extracted data to CSV
            writer.writerow([today, product_name, product_price, page_num])
            total_count += 1
            
        # Sleep for 2 seconds to prevent getting blocked by the server
        time.sleep(2)

print(f"\nTask Completed: Successfully extracted and saved {total_count} products.")