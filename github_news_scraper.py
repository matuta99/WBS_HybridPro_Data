import pandas as pd
import requests
import os
import sys
from datetime import datetime, timedelta

def start_tradingview_news_mining():
    print("🌐 STARTING WBS FUNDAMENTAL TRACKER (TRADINGVIEW REAL-TIME API)...")
    
    # ⚡ 1. Ambil jangkauan tanggal: 7 hari lalu s/d 7 hari ke depan agar data historis minggu ini aman!
    now = datetime.utcnow()
    start_date = (now - timedelta(days=7)).strftime("%Y-%m-%dT00:00:00Z")
    end_date = (now + timedelta(days=7)).strftime("%Y-%m-%dT23:59:59Z")
    
    url = f"https://economic-calendar.tradingview.com/events?from={start_date}&to={end_date}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://www.tradingview.com/'
    }
    
    print(f"📡 Menembak API Institusional TradingView: {url}")
    all_news_extracted = []
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            data = response.json()
            
            # Pengaman struktur array/object JSON
            events = []
            if isinstance(data, list): events = data
            elif isinstance(data, dict): events = data.get('result', data.get('events', []))
                
            for item in events:
                # Filter ketat hanya berita Amerika Serikat (USD)
                if item.get('country') == 'US':
                    
                    # ⚡ 2. Format tanggal disamakan dengan selera UI Jenderal (Contoh: Tue Jun 9 2026)
                    try:
                        raw_time = item.get('time')
                        dt = pd.to_datetime(raw_time)
                        date_str = f"{dt.strftime('%a %b')} {dt.day} {dt.strftime('%Y')}"
                    except:
                        date_str = datetime.now().strftime("%a %b %d %Y")
                    
                    # ⚡ 3. Mapping Kasta Dampak (Importance)
                    # TradingView: -1 = Low, 0 = Medium, 1 = High
                    importance = item.get('importance', -1)
                    if importance == 1: impact = "High"
                    elif importance == 0: impact = "Medium"
                    else: impact = "Low"
                    
                    # Fungsi pembersih angka Zonk
                    def clean_val(val):
                        if val is None or str(val).strip().lower() in ['nan', 'none', '']:
                            return "-"
                        return str(val).strip()

                    # ⚡ 4. RAMPAS HARTA KARUN UTAMA (ACTUAL VALUE!)
                    actual = clean_val(item.get('actual'))
                    forecast = clean_val(item.get('forecast'))
                    previous = clean_val(item.get('previous'))
                    
                    all_news_extracted.append({
                        "Date": date_str,
                        "Currency": "USD",
                        "Impact": impact,
                        "Event": item.get('title', '-'),
                        "Actual": actual,
                        "Forecast": forecast,
                        "Previous": previous
                    })
            print(f"✅ Berhasil mengamankan {len(all_news_extracted)} data berita USD.")
        else:
            print(f"❌ API TradingView menolak! Status: {response.status_code}")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Gagal Total mengekstrak API: {e}")
        sys.exit(1)

    # ⚡ 5. Bangun ulang folder data dan simpan hasilnya
    os.makedirs("data", exist_ok=True)
    output_file = os.path.join("data", "forex_news_usd_2015_2026.csv")
    
    df_new = pd.DataFrame(all_news_extracted)
    
    if not df_new.empty:
        df_new['Scrape_Time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        df_new.to_csv(output_file, index=False)
        print(f"👑 GOD MODE SUCCESS: {len(df_new)} Berita Fundamental REAL-TIME + ACTUAL berhasil dijinakkan!")
    else:
        print("⚠️ Alarm! Tidak ada berita USD yang tersaring.")
        sys.exit(1)

if __name__ == "__main__":
    start_tradingview_news_mining()
