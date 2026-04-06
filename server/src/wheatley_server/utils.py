def snake_to_pascal(text):
    return "".join(word.capitalize() for word in text.split("_"))
