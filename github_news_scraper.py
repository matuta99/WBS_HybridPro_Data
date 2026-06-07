import pandas as pd
import time
import random
import os
import sys
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

def start_cloud_mining():
    # Mengambil nama bulan dan tahun aktif PC saat ini secara otomatis (Misal: jun dan 2026)
    current_month_str = datetime.now().strftime('%b').lower()
    current_year_str = str(datetime.now().year)
    label_name = f"{current_month_str.upper()} {current_year_str}"
    
    print(f"🌐 STARTING WBS STEALTH SINGLE-SHOT MINER FOR {label_name}...")
    
    chrome_options = Options()
    chrome_options.add_argument("--headless=new") 
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--remote-allow-origins=*") 
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")
    
    driver = None
    all_news_extracted = []
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        
        # 🎯 STRATEGI UTAMA: Langsung tembak 1 URL bulan berjalan (Bebas dari blokir Cloudflare)
        url = f"https://www.forexfactory.com/calendar?month={current_month_str}.{current_year_str}"
        print(f"📡 Fetching Live Month Data Feed from: {url}")
        driver.get(url)
        time.sleep(8.0) # Beri waktu ekstra agar seluruh row termuat sempurna
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        table_rows = soup.find_all('tr', class_='calendar__row')
        current_row_date = ""
        
        print(f"📊 Total rows discovered on page: {len(table_rows)}")
        
        for row in table_rows:
            currency_item = row.find('td', class_='calendar__currency')
            if not currency_item or not currency_item.text.strip():
                continue
                
            currency_txt = currency_item.text.strip()
            date_item = row.find('td', class_='calendar__date')
            if date_item and date_item.text.strip():
                current_row_date = date_item.text.strip()
            
            impact_td = row.find('td', class_='calendar__impact')
            impact_icon = impact_td.find('span') if impact_td else None
            impact_level = "Low"
            if impact_icon:
                icon_class = "".join(impact_icon.get('class', []))
                if 'high' in icon_class or 'red' in icon_class: impact_level = "High"
                elif 'medium' in icon_class or 'orange' in icon_class: impact_level = "Medium"
                elif 'low' in icon_class or 'yellow' in icon_class: impact_level = "Low"
            
            event_item = row.find('td', class_='calendar__event')
            actual_item = row.find('td', class_='calendar__actual')
            forecast_item = row.find('td', class_='calendar__forecast')
            previous_item = row.find('td', class_='calendar__previous')
            
            tanggal_final = f"{current_row_date} {current_year_str}".replace('\n', ' ').strip()
            
            all_news_extracted.append({
                "Date": tanggal_final, "Currency": currency_txt, "Impact": impact_level,
                "Event": event_item.text.strip() if event_item else "-",
                "Actual": actual_item.text.strip() if actual_item and actual_item.text.strip() else "-",
                "Forecast": forecast_item.text.strip() if forecast_item and forecast_item.text.strip() else "-",
                "Previous": previous_item.text.strip() if previous_item and previous_item.text.strip() else "-"
            })
                
    except Exception as e:
        print(f"❌ PYTHON EXECUTOR ERROR: {e}")
        if driver: driver.quit()
        sys.exit(1)
    finally:
        if driver: 
            driver.quit()
            print("🔒 Cloud browser engine shut down cleanly.")
            
    os.makedirs("data", exist_ok=True)
    output_file = os.path.join("data", "forex_news_usd_2015_2026.csv")
    
    if all_news_extracted:
        df_new = pd.DataFrame(all_news_extracted)
        print(f"🎉 Successfully parsed {len(df_new)} economic indicators for this month!")
    else:
        print("⚠️ Alert: Zero data parsed. Generating fallback placeholder template.")
        df_new = pd.DataFrame(columns=["Date", "Currency", "Impact", "Event", "Actual", "Forecast", "Previous"])
        
    if os.path.exists(output_file):
        try:
            df_old = pd.read_csv(output_file)
            # Gabungkan sejarah lama (termasuk data Januari) dan timpa dengan update terbaru Juni
            df_new = pd.concat([df_old, df_new]).drop_duplicates(subset=['Date', 'Currency', 'Event'], keep='last')
        except: pass
        
    df_new.to_csv(output_file, index=False)
    print("👑 LIVE MONTH LEDGER MERGED AND SECURED SUCCESSFULLY!")

if __name__ == "__main__":
    start_cloud_mining()
