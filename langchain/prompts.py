def get_user_input():

    print("Welcome to the Personalized Story Generator!")

    character = input("Enter character name: ")

    setting = input("Enter setting: ")

    genre = input("Enter genre: ")

    theme = input("Enter theme: ")

    return character, setting, genre, theme


def build_story_prompt(character,setting,genre,theme):

    return f"""
Generate a {genre} story about {character}
in {setting} with the theme of {theme}.
Keep it under 300 words.
"""