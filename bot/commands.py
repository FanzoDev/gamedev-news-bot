from database.database import (
    initialize_database,
    add_subscriber,
    remove_subscriber,
    update_subscriber_category
)


VALID_CATEGORIES = [
    "ALL",
    "ENGINE",
    "PROGRAMMING",
    "ART",
    "AI",
    "INDIE",
    "TOOLS",
    "INDUSTRY",
    "RELEASE"
]


def process_command(phone, message):

    message = message.strip().upper()

    # START
    if message == "START":

        add_subscriber(phone, "ALL")

        return (
            "✅ Kamu sudah berlangganan GameDev Update.\n\n"
            "Topik: ALL\n\n"
            "Ketik TOPIC untuk melihat pilihan topik."
        )

    # STOP
    if message == "STOP":

        removed = remove_subscriber(phone)

        if removed:
            return "🔕 Berlangganan GameDev Update dihentikan."

        return "Kamu belum terdaftar sebagai subscriber."

    # TOPIC
    if message == "TOPIC":

        topics = "\n".join(
            f"• {category}"
            for category in VALID_CATEGORIES
        )

        return (
            "📚 TOPIK GAMEDEV UPDATE\n\n"
            f"{topics}\n\n"
            "Contoh:\n"
            "TOPIC ENGINE"
        )

    # TOPIC <CATEGORY>
    if message.startswith("TOPIC "):

        category = message.replace("TOPIC ", "").strip()

        if category not in VALID_CATEGORIES:

            return (
                "❌ Topik tidak ditemukan.\n\n"
                "Ketik TOPIC untuk melihat daftar topik."
            )

        updated = update_subscriber_category(
            phone,
            category
        )

        if updated:

            return (
                f"✅ Topik berhasil diubah menjadi "
                f"{category}."
            )

        return (
            "Kamu belum berlangganan.\n\n"
            "Ketik START terlebih dahulu."
        )

    # HELP
    if message == "HELP":

        return (
            "🎮 GAMEDEV UPDATE\n\n"
            "START - Mulai berlangganan\n"
            "STOP - Berhenti berlangganan\n"
            "TOPIC - Lihat topik\n"
            "TOPIC ENGINE - Pilih topik\n"
            "HELP - Bantuan"
        )

    return (
        "❓ Perintah tidak dikenali.\n\n"
        "Ketik HELP untuk melihat daftar perintah."
    )


if __name__ == "__main__":

    initialize_database()

    phone = "628123456789"

    commands = [
        "START",
        "TOPIC",
        "TOPIC ENGINE",
        "HELP",
        "STOP"
    ]

    for command in commands:

        print()
        print("USER:", command)
        print("BOT:", process_command(phone, command))
