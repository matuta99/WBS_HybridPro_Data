import pandas as pd
import time
import random
import os
import sys
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

def generate_stealth_weeks(weeks_ahead=4):
    """Hanya mengambil minggu ini sampai 4 minggu ke depan agar lolos blokir Cloudflare awan"""
    current = datetime.date.today()
    
    # Mundur ke hari Minggu terdekat (Awal minggu bursa Forex Factory)
    while current.weekday() != 6:
        current -= datetime.timedelta(days=1)
        
    months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
    weeks = []
    
    for _ in range(weeks_ahead):
        m_str = months[current.month - 1]
        week_query = f"{m_str}{current.day}.{current.year}"
        label_display = f"Minggu {current.strftime('%d %b %Y')}"
        weeks.append((week_query, label_display))
        current += datetime.timedelta(days=7)
        
    return weeks

def start_cloud_mining():
    print("🌐 STARTING WBS CLOUD WEEKLY STREAM MINER (CHRONOLOGICAL SORT ACTIVE)...")
    
    chrome_options = Options()
    chrome_options.add_argument("--headless=new") 
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--remote-allow-origins=*") 
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")
    
    driver = None
    all_news_extracted = []
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        })
        
        target_weeks = generate_stealth_weeks(4)
        print(f"📅 Tactical Lookout Locked: {target_weeks[0][1]} to {target_weeks[-1][1]}")
        
        for week_query, label_name in target_weeks:
            url = f"https://www.forexfactory.com/calendar?week={week_query}"
            print(f"📡 Radar Scanning: {label_name} -> {url}")
            driver.get(url)
            
            time.sleep(random.uniform(7.0, 10.0))
            
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            table_rows = soup.find_all('tr', class_='calendar__row')
            current_row_date = ""
            
            valid_rows = 0
            for row in table_rows:
                date_item = row.find('td', class_='calendar__date')
                if date_item and date_item.text.strip():
                    current_row_date = date_item.text.strip()
                    
                currency_item = row.find('td', class_='calendar__currency')
                if not currency_item or "USD" not in currency_item.text.strip():
                    continue
                
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
                
                tahun_aktif = week_query.split('.')[-1]
                tanggal_final = f"{current_row_date} {tahun_aktif}".replace('\n', ' ').strip()
                
                all_news_extracted.append({
                    "Date": tanggal_final, "Currency": "USD", "Impact": impact_level,
                    "Event": event_item.text.strip() if event_item else "-",
                    "Actual": actual_item.text.strip() if actual_item and actual_item.text.strip() else "-",
                    "Forecast": forecast_item.text.strip() if forecast_item and forecast_item.text.strip() else "-",
                    "Previous": previous_item.text.strip() if previous_item and previous_item.text.strip() else "-"
                })
                valid_rows += 1
                
            print(f"📊 Extracted {valid_rows} events from {label_name}")
                
    except Exception as e:
        print(f"❌ CRITICAL TIMELINE CRASH: {e}")
        if driver: driver.quit()
        sys.exit(1)
    finally:
        if driver: driver.quit()
            
    os.makedirs("data", exist_ok=True)
    output_file = os.path.join("data", "forex_news_usd_2026.csv")
    
    df_new = pd.DataFrame(all_news_extracted)
    
    # Membaca data induk yang sudah diupload Jenderal agar sejarahnya tidak hilang
    if os.path.exists(output_file):
        try:
            df_old = pd.read_csv(output_file)
            df_final = pd.concat([df_old, df_new]).drop_duplicates(subset=['Date', 'Currency', 'Event'], keep='last')
        except:
            df_final = df_new
    else:
        df_final = df_new

    if not df_final.empty:
        # ⚡ MANTRA KUNCI: Konversi string ke format datetime, urutkan dari masa lalu ke masa depan, lalu kembalikan ke string
        try:
            df_final['temp_sort_date'] = pd.to_datetime(df_final['Date'], format='%a %b %d %Y', errors='coerce')
            df_final = df_final.sort_values(by='temp_sort_date', ascending=True).drop(columns=['temp_sort_date'])
            print("👑 SUCCESS: Database has been chronologically sorted!")
        except Exception as sort_err:
            print(f"⚠️ Sorting Warning: {sort_err}")
            
        df_final.to_csv(output_file, index=False)
        print("👑 BRANKAS BULLETPROOF KRONOLOGIS LEDGER SECURED!")
    else:
        print("⚠️ No data to save.")

if __name__ == "__main__":
    start_cloud_mining()
