import pandas as pd
import time
import random
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service # ⚡ SUNTIKAN BARU
from webdriver_manager.chrome import ChromeDriverManager # ⚡ SUNTIKAN BARU
from bs4 import BeautifulSoup

def generate_monthly_ranges(start_year, end_year):
    months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
    ranges = []
    current_month_idx = datetime.now().month - 1
    current_year = datetime.now().year
    
    for year in range(start_year, end_year + 1):
        for m_idx in range(12):
            if year == current_year and m_idx > current_month_idx:
                break
            start_m = months[m_idx]
            start_date = f"{start_m}1.{year}"
            if m_idx == 11:
                end_m = months[0]
                end_year_val = year + 1
            else:
                end_m = months[m_idx + 1]
                end_year_val = year
            ranges.append((f"{start_date}-{end_date}", f"{start_m.upper()} {year}"))
    return ranges

def start_cloud_mining():
    print("🌐 STARTING WBS GLOBAL CLOUD NEWS MINER (ALL CURRENCIES & ALL IMPACTS)...")
    
    chrome_options = Options()
    chrome_options.add_argument("--headless") 
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    
    # ⚡ PERBAIKAN UTAMA: Menggunakan Service dari WebDriver Manager agar auto-singkron di Linux
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    # 💡 TIPS TRADING: Untuk run harian, mulailah dari tahun berjalan (misal 2026) 
    # agar tidak terkena blokir Cloudflare karena melakukan 130+ request sekaligus setiap hari.
    target_ranges = generate_monthly_ranges(2026, datetime.now().year)
    all_news_extracted = []
    
    try:
        for range_query, label_name in target_ranges:
            print(f"📡 Cloud Scrape: {label_name}...")
            url = f"https://www.forexfactory.com/calendar?range={range_query}"
            driver.get(url)
            time.sleep(random.uniform(4.0, 6.0))
            
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            table_rows = soup.find_all('tr', class_='calendar__row')
            current_row_date = ""
            
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
                
                tahun_aktif = range_query.split('-')[0].split('.')[-1]
                tanggal_final = f"{current_row_date} {tahun_aktif}".replace('\n', ' ').strip()
                
                all_news_extracted.append({
                    "Date": tanggal_final, "Currency": currency_txt, "Impact": impact_level,
                    "Event": event_item.text.strip() if event_item else "-",
                    "Actual": actual_item.text.strip() if actual_item and actual_item.text.strip() else "-",
                    "Forecast": forecast_item.text.strip() if forecast_item and forecast_item.text.strip() else "-",
                    "Previous": previous_item.text.strip() if previous_item and previous_item.text.strip() else "-"
                })
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        driver.quit()
        if all_news_extracted:
            df_new = pd.DataFrame(all_news_extracted)
            os.makedirs("data", exist_ok=True)
            output_file = os.path.join("data", "forex_news_usd_2015_2026.csv")
            
            # Jika file sudah ada, gabungkan datanya agar sejarah lama tidak hilang
            if os.path.exists(output_file):
                try:
                    df_old = pd.read_csv(output_file)
                    df_new = pd.concat([df_old, df_new]).drop_duplicates(subset=['Date', 'Currency', 'Event'], keep='last')
                except: pass
                
            df_new.to_csv(output_file, index=False)
            print(f"👑 GLOBAL CLOUD MINING SUCCESS: Database Multi-Currency Berhasil Diperbarui!")

if __name__ == "__main__":
    start_cloud_mining()
