import pandas as pd
import requests
import os
import sys
import time
from datetime import datetime

def start_vip_cloud_mining():
    print("🌐 STARTING WBS HOURLY LIVE TRACKER (VIP API AMNESIA MODE)...")
    
    # Jalur VIP langsung ke brankas database Forex Factory (Anti-Cloudflare)
    urls = [
        "https://nfs.faireconomy.media/ff_calendar_thisweek.json",
        "https://nfs.faireconomy.media/ff_calendar_nextweek.json"
    ]
    
    all_news_extracted = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    for url in urls:
        print(f"📡 Menembak Jalur VIP: {url}")
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                for item in data:
                    # Filter ketat hanya berita USD
                    if item.get('country') == 'USD':
                        # Ubah waktu rilis bursa ke format kalender sistem Jenderal
                        try:
                            dt = pd.to_datetime(item.get('date'))
                            # Format sakti anti angka nol di depan (Contoh: Tue Jun 9 2026)
                            date_str = f"{dt.strftime('%a %b')} {dt.day} {dt.strftime('%Y')}"
                        except:
                            date_str = item.get('date')
                            
                        actual = str(item.get('actual', '')).strip()
                        forecast = str(item.get('forecast', '')).strip()
                        previous = str(item.get('previous', '')).strip()
                        
                        all_news_extracted.append({
                            "Date": date_str,
                            "Currency": "USD",
                            "Impact": item.get('impact', 'Low'),
                            "Event": item.get('title', '-'),
                            "Actual": actual if actual else "-",
                            "Forecast": forecast if forecast else "-",
                            "Previous": previous if previous else "-"
                        })
                print("✅ Sukses menyedot data dari target.")
            else:
                print(f"❌ Gagal menembus API, Status: {response.status_code}")
        except Exception as e:
            print(f"❌ Error API: {e}")

    os.makedirs("data", exist_ok=True)
    # Sesuaikan dengan nama file di GitHub Jenderal
    output_file = os.path.join("data", "forex_news_usd_2015_2026.csv")
    
    df_new = pd.DataFrame(all_news_extracted)
    
    if not df_new.empty:
        # Hancurkan sejarah lama, simpan data segar hari ini!
        df_new.to_csv(output_file, index=False)
        print(f"👑 VIP AMNESIA MODE SUCCESS: {len(df_new)} baris berita berhasil diamankan!")
    else:
        # Jika gagal, bunyikan alarm error di GitHub agar Jenderal tahu robotnya mogok!
        print("⚠️ Gawat! Robot tidak menemukan data USD satupun.")
        sys.exit(1)

if __name__ == "__main__":
    start_vip_cloud_mining()
