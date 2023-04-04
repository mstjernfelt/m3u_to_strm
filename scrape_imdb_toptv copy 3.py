def search(original_title, title_list) -> bool:
    # Split the text into individual words
    words = original_title.split()
    movie_title_words = len(words)

    # Create a list of movies that match the words in the text
    matching_movies = []
    for title in title_list:
        num_words = 0

        title_words = len(title.split())

        for word in words:
            # Check if the word is in the movie title (case-insensitive)
            if word.lower() in title.lower():
                num_words += 1
                #break

        if num_words < movie_title_words:
            continue

        if num_words > 0:
            percent = round((num_words / title_words) * 100, 0)
        else:
            percent = 0

        if percent == 100:
            matching_movies.append(title)

    # Check if at least 50% of the words in the text match movie titles
    if len(matching_movies) > 0:
        return(True)
    else:
        return(False)
    
text = 'The Birth of a Nation Two'
movies = [
    'The Chronicle of Narnia: The Lion, the Witch and the Wardrobe',
    'American History X',
    'The Color Purple',
    'The Birth of a Nation',
    'Who We Are: A Chronicle of Racism in America',
    'Who We Are: A man',
    'Malcolm X',
    'The Help',
    '12 Years a Slave',
    'Fruitvale Station',
    'Mississippi Burning'
]

print(search(text, movies))