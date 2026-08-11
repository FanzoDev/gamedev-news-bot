import feedparser
import re
import html

from database.database import (
    initialize_database,
    news_exists,
    save_news,
    source_exists,
    is_source_initialized,
    initialize_source,
    mark_source_initialized
)

from news.filter import classify_news


SOURCES = [
    {
        "name": "GameFromScratch",
        "url": "https://gamefromscratch.com/feed/"
    },
    {
        "name": "Unreal Engine",
        "url": "https://www.unrealengine.com/rss"
    },
    {
        "name": "Godot",
        "url": "https://godotengine.org/rss.xml"
    },
    {
        "name": "Game Developer",
        "url": "https://www.gamedeveloper.com/rss.xml"
    },
    {
        "name": "GamesIndustry.biz",
        "url": "https://www.gamesindustry.biz/feed"
    }
]

def clean_html(text):
    text = html.unescape(text)
    text = re.sub(r"<[^>]+>", "", text)
    return text.strip()


def collect_news():

    initialize_database()

    new_articles = []

    for source in SOURCES:

        source_name = source["name"]

        print(f"\nMengambil berita dari: {source_name}")

        # ==========================================
        # CEK APAKAH SUMBER SUDAH DIKENAL BOT
        # ==========================================

        if not source_exists(source_name):

            initialize_source(source_name)

            first_run = True

            print(
                f"[SUMBER BARU] {source_name}"
            )

        else:

            first_run = not is_source_initialized(
                source_name
            )

        # ==========================================
        # AMBIL RSS
        # ==========================================

        try:

            feed = feedparser.parse(
                source["url"]
            )

        except Exception as error:

            print(
                f"[ERROR] Gagal mengambil {source_name}: {error}"
            )

            continue

        print(
            f"Ditemukan {len(feed.entries)} berita"
        )

        # ==========================================
        # RSS KOSONG
        # ==========================================

        if len(feed.entries) == 0:

            print(
                f"[KOSONG] Tidak ada berita dari {source_name}"
            )

            continue

        # ==========================================
        # PROSES BERITA
        # ==========================================

        for article in feed.entries[:10]:

            title = clean_html(
                article.get(
                    "title",
                    "Tidak ada judul"
                )
            )

            category = classify_news(title)

            link = article.get(
                "link",
                ""
            )

            published = article.get(
                "published",
                ""
            )

            summary = clean_html(
                article.get(
                    "summary",
                    ""
                )
            )

            image_url = ""

            if "media_content" in article:

                media = article.media_content

                if media:

                    image_url = media[0].get(
                        "url",
                        ""
                    )

            elif "media_thumbnail" in article:

                thumbnail = article.media_thumbnail

                if thumbnail:

                    image_url = thumbnail[0].get(
                        "url",
                        ""
                    )

            # ======================================
            # CEK DUPLIKAT
            # ======================================

            if news_exists(link):

                print(
                    f"[SUDAH ADA] {title}"
                )

                continue

            # ======================================
            # SUMBER BARU
            # ======================================

            if first_run:

                saved = save_news(
                    source_name,
                    title,
                    link,
                    published,
                    category,
                    summary
                )

                if saved:

                    print(
                        f"[BASELINE] {title}"
                    )

                continue

            # ======================================
            # BERITA BARU
            # ======================================

            saved = save_news(
                source_name,
                title,
                link,
                published,
                category,
                summary
            )

            if saved:

                print(
                    f"[BERITA BARU] "
                    f"[{category}] {title}"
                )

                new_articles.append({

                    "source": source_name,

                    "title": title,

                    "link": link,

                    "published": published,

                    "category": category,

                    "summary": summary,

                    "image_url": image_url

                })

        # ==========================================
        # SUMBER SELESAI DIINISIALISASI
        # ==========================================

        if first_run:

            mark_source_initialized(
                source_name
            )

            print(
                f"[SELESAI BASELINE] {source_name}"
            )


    print()
    print("==============================")
    print(
        f"Berita baru: {len(new_articles)}"
    )
    print("==============================")


    return new_articles


if __name__ == "__main__":

    collect_news()
