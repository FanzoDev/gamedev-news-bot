from database.database import get_subscribers


def get_recipients(category):
    return get_subscribers(category)


if __name__ == "__main__":

    category = "ENGINE"

    recipients = get_recipients(category)

    print("==============================")
    print("     NEWS DISPATCHER")
    print("==============================")

    print(f"Kategori: {category}")
    print()

    if not recipients:
        print("Tidak ada subscriber.")
    else:
        print("Berita akan dikirim kepada:")

        for phone in recipients:
            print(f"→ {phone}")
