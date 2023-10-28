def remove_diacritics(input_str):
    """Replace Czech diacritics with English characters."""
    
    # Dictionary for Czech to English character mapping
    translation_dict = {
        'á': 'a', 'č': 'c', 'ď': 'd', 'é': 'e',
        'ě': 'e', 'í': 'i', 'ň': 'n', 'ó': 'o',
        'ř': 'r', 'š': 's', 'ť': 't', 'ú': 'u',
        'ů': 'u', 'ý': 'y', 'ž': 'z',
        'Á': 'A', 'Č': 'C', 'Ď': 'D', 'É': 'E',
        'Ě': 'E', 'Í': 'I', 'Ň': 'N', 'Ó': 'O',
        'Ř': 'R', 'Š': 'S', 'Ť': 'T', 'Ú': 'U',
        'Ů': 'U', 'Ý': 'Y', 'Ž': 'Z'
    }

    # Create a translation table
    trans_table = str.maketrans(translation_dict)

    # Translate the string using the table
    return input_str.translate(trans_table)


# Example usage:
text = "Dobrý den, jak se máte?"
print(remove_diacritics(text))  # Output: Dobry den, jak se mate?