import re

class TitleManagment:
    def __init__(self):
        pass

    def get_Title_Year(title):
        year_pattern = r"\[(\d{4})\]"  # matches a four-digit year

        # find the year in the modified string
        year_match = re.search(year_pattern, title)

        if year_match:
            year = year_match.group(1)
        else:
            year = 0
            
        return(year)

    def get_Cleaned_Title(title):

        pattern = r"\[[^\]]*\]"  # matches any square brackets and the characters inside them
        year_pattern = r"\b\d{4}\b"  # matches a four-digit year

        # find all matches of the pattern in the string and replace them with an empty string
        string_without_brackets = re.sub(pattern, "", title)

        return string_without_brackets