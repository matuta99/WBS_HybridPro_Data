import pandas as pd
import os
import sys
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

def start_vip_selenium_mining():
    print("🌐 STARTING WEB SCRAPER (SELENIUM ANTI-ZONK MODE)...")
    
    # ⚡ 1. Setup Browser Chrome Tak Kasat Mata (Headless)
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    # Menyamar jadi manusia asli
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        print(f"❌ Error Setup ChromeDriver: {e}")
        sys.exit(1)
        
    url = "https://www.forexfactory.com/calendar?week=this"
    print(f"📡 Membobol HTML Website Langsung: {url}")
    
    driver.get(url)
    # Tunggu 5 detik agar sistem Cloudflare dan Javascript Forex Factory selesai loading
    time.sleep(5)  
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()
    
    # ⚡ 2. Mencari Tabel Kalender Utama
    table = soup.find('table', class_='calendar__table')
    if not table:
        print("❌ Gagal menemukan tabel kalender! Diblokir Cloudflare atau struktur web berubah.")
        sys.exit(1)
        
    all_news = []
    current_date = ""
    current_year = datetime.now().year
    
    # ⚡ 3. Menyisir setiap baris data (Merampok angka Actual)
    rows = table.find_all('tr', class_='calendar__row')
    for row in rows:
        # Ambil Tanggal (Forex Factory kadang menggabung tanggal untuk hari yang sama)
        date_td = row.find('td', class_='calendar__date')
        if date_td and date_td.text.strip():
            raw_date = date_td.text.strip() # Contoh: "Tue Jun 9"
            current_date = f"{raw_date} {current_year}"
        
        currency_td = row.find('td', class_='calendar__currency')
        currency = currency_td.text.strip() if currency_td else ""
        
        # HANYA AMBIL BERITA USD
        if currency == "USD":
            # Bedah Impact Berdasarkan Warna
            impact = "Low"
            impact_td = row.find('td', class_='calendar__impact')
            if impact_td:
                span = impact_td.find('span')
                if span:
                    class_list = span.get('class', [])
                    class_str = " ".join(class_list).lower()
                    if 'red' in class_str: impact = "High"
                    elif 'ora' in class_str: impact = "Medium"
                    
            event_td = row.find('td', class_='calendar__event')
            event = event_td.text.strip() if event_td else "-"
            
            # INI DIA HARTA KARUNNYA!
            actual_td = row.find('td', class_='calendar__actual')
            actual = actual_td.text.strip() if actual_td else "-"
            
            forecast_td = row.find('td', class_='calendar__forecast')
            forecast = forecast_td.text.strip() if forecast_td else "-"
            
            previous_td = row.find('td', class_='calendar__previous')
            previous = previous_td.text.strip() if previous_td else "-"
            
            all_news.append({
                "Date": current_date,
                "Currency": "USD",
                "Impact": impact,
                "Event": event,
                "Actual": actual if actual else "-",
                "Forecast": forecast if forecast else "-",
                "Previous": previous if previous else "-"
            })
    
    # ⚡ 4. Simpan ke CSV dengan Timestamp (Taktik Membodohi Git tetap dipakai)
    os.makedirs("data", exist_ok=True)
    output_file = os.path.join("data", "forex_news_usd_2015_2026.csv")
    df_new = pd.DataFrame(all_news)
    
    if not df_new.empty:
        df_new['Scrape_Time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        df_new.to_csv(output_file, index=False)
        print(f"👑 SELENIUM SUCCESS: {len(df_new)} baris berita (TERMASUK ACTUAL) diamankan!")
    else:
        print("⚠️ Gawat! Robot tidak menemukan data USD satupun.")
        sys.exit(1)

if __name__ == "__main__":
    start_vip_selenium_mining()
