import schedule
import time

from news.collector import collect_news


def job():
    print("\n==============================")
    print("Memeriksa berita terbaru...")
    print("==============================")

    collect_news()


# Jalankan setiap 5 menit
schedule.every(5).minutes.do(job)


print("================================")
print("   GAMEDEV NEWS BOT STARTED")
print("================================")
print("Collector akan berjalan setiap 5 menit.")
print("Tekan CTRL + C untuk menghentikan bot.")

# Jalankan sekali saat program pertama dimulai
job()


while True:
    schedule.run_pending()
    time.sleep(1)
