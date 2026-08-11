CATEGORIES = {
    "ENGINE": [
        "unity",
        "unreal",
        "godot",
        "gamemaker",
        "game engine",
        "engine update"
    ],

    "PROGRAMMING": [
        "c++",
        "c#",
        "programming",
        "shader",
        "scripting",
        "optimization",
        "code"
    ],

    "ART": [
        "3d",
        "2d",
        "animation",
        "modeling",
        "texture",
        "vfx",
        "visual effects",
        "game art"
    ],

    "AI": [
        "artificial intelligence",
        "ai",
        "machine learning",
        "generative ai",
        "llm"
    ],

    "INDIE": [
        "indie game",
        "indie developer",
        "independent developer",
        "solo developer"
    ],

    "TOOLS": [
        "plugin",
        "tool",
        "sdk",
        "software",
        "asset"
    ],

    "INDUSTRY": [
        "game studio",
        "developer studio",
        "games industry",
        "game industry",
        "funding",
        "acquisition"
    ],

    "RELEASE": [
        "release",
        "released",
        "available",
        "launch",
        "version"
    ]
}


def classify_news(title):
    title_lower = title.lower()

    for category, keywords in CATEGORIES.items():

        for keyword in keywords:

            if keyword in title_lower:
                return category

    return "OTHER"

if __name__ == "__main__":

    test_titles = [
        "Unity 7 is Back",
        "Unreal Engine 5.8 is now available",
        "New AI Tool for Game Developers",
        "C++ Optimization Techniques for Games",
        "New 3D Animation Workflow"
    ]

    for title in test_titles:
        category = classify_news(title)

        print(f"{title}")
        print(f"Category: {category}")
        print()
