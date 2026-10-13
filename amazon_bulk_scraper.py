import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
}

today = datetime.now().strftime("%Y-%m-%d")
save_path = r"C:\Users\Anusha\Downloads\freelancing\amazon_bata_bulk.csv"

with open(save_path, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Date", "Product Name", "Price (INR)", "Page Number"])
    
    total_count = 0
    
    # Page 1 nundi 3 varaku loop chesthunnam (range(1, 4) ante 1, 2, 3)
    for page_num in range(1, 4):
        print(f"Page {page_num} nundi data lagutunnam...")
        
        # URL lo page_num dynamic ga marutundi
        url = f"https://www.amazon.in/s?k=bata+women+sandals&page={page_num}"
        
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")
        products = soup.find_all("div", {"data-component-type": "s-search-result"})
        
        for item in products:
            img_tag = item.find("img", class_="s-image")
            peru = img_tag["alt"] if img_tag else "Peru kanipinchaledu"
            peru = peru.replace("Sponsored Ad - ", "")
            
            price_tag = item.find("span", class_="a-price-whole")
            dhara = price_tag.get_text().strip() if price_tag else "Price ledu"
            
            # Ye page nundi vachindo aa page number kuda save chesthunnam
            writer.writerow([today, peru, dhara, page_num])
            total_count += 1
            
        # Modati page aipoyaka 2 seconds wait chesi next page ki velthundi
        time.sleep(2)

print(f"\nBoom! 3 pages kalipi total {total_count} products data CSV lo save aypoyindi.")