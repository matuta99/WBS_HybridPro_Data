import pandas as pd
import time
import random
import os
import sys
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

def generate_forward_months(months_ahead=13):
    """Menghasilkan list biner bulan dan tahun dari sekarang hingga 13 bulan ke depan"""
    months_names = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
    current_date = datetime.now()
    
    y = current_date.year
    m = current_date.month
    
    future_list = []
    for _ in range(months_ahead):
        m_str = months_names[m - 1]
        future_list.append((m_str, str(y)))
        m += 1
        if m > 12:
            m = 1
            y += 1
    return future_list

def start_cloud_mining():
    print("🌐 STARTING WBS GLOBAL 13-MONTH FORWARD VISION RADAR ENGINE...")
    
    chrome_options = Options()
    chrome_options.add_argument("--headless=new") 
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--remote-allow-origins=*") 
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36")
    
    driver = None
    all_news_extracted = []
    
    try:
        print("🏗️ Launching Multi-Month Stealth Chrome inside GitHub Runner...")
        driver = webdriver.Chrome(options=chrome_options)
        
        # Ambil cetak biru target 13 bulan kedepan (Juni 2026 - Juni 2027)
        target_months = generate_forward_months(13)
        print(f"📅 Target Timeline Coordinates Locked: {target_months[0][0].upper()} {target_months[0][1]} to {target_months[-1][0].upper()} {target_months[-1][1]}")
        
        for m_str, y_str in target_months:
            label_name = f"{m_str.upper()} {y_str}"
            url = f"https://www.forexfactory.com/calendar?month={m_str}.{y_str}"
            
            print(f"📡 Radar Scanning: {label_name} -> {url}")
            driver.get(url)
            
            # Beri delay acak agak panjang agar aman dari blokir Cloudflare
            time.sleep(random.uniform(5.5, 7.5))
            
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            table_rows = soup.find_all('tr', class_='calendar__row')
            current_row_date = ""
            
            valid_rows = 0
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
                
                tanggal_final = f"{current_row_date} {y_str}".replace('\n', ' ').strip()
                
                all_news_extracted.append({
                    "Date": tanggal_final, "Currency": currency_txt, "Impact": impact_level,
                    "Event": event_item.text.strip() if event_item else "-",
                    "Actual": actual_item.text.strip() if actual_item and actual_item.text.strip() else "-",
                    "Forecast": forecast_item.text.strip() if forecast_item and forecast_item.text.strip() else "-",
                    "Previous": previous_item.text.strip() if previous_item and previous_item.text.strip() else "-"
                })
                valid_rows += 1
                
            print(f"📊 Extracted {valid_rows} events from {label_name}")
                
    except Exception as e:
        print(f"❌ CRITICAL TIMELINE CRASH DETECTED: {e}")
        if driver: driver.quit()
        sys.exit(1)
    finally:
        if driver: 
            driver.quit()
            print("🔒 Multi-Month session closed safely.")
            
    os.makedirs("data", exist_ok=True)
    output_file = os.path.join("data", "forex_news_usd_2015_2026.csv")
    
    if all_news_extracted:
        df_new = pd.DataFrame(all_news_extracted)
        print(f"🎉 GRAND TOTAL: Successfully harvested {len(df_new)} future economic events!")
        
        if os.path.exists(output_file):
            try:
                df_old = pd.read_csv(output_file)
                df_new = pd.concat([df_old, df_new]).drop_duplicates(subset=['Date', 'Currency', 'Event'], keep='last')
            except: pass
            
        df_new.to_csv(output_file, index=False)
        print("👑 BRANKAS BULLETPROOF FUTURE LEDGER SECURED SUCCESSFULLY!")
    else:
        print("⚠️ Failed to parse any data across the timeline. Check block configurations.")

if __name__ == "__main__":
    start_cloud_mining()
