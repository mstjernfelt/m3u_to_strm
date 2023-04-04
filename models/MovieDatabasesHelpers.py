import re
import requests
import datetime
# from bs4 import BeautifulSoup

# class Imdb:

#     tv_shows = {'': {'Year': '', 'IMDb Rating': ''}}
#     movies = {'': {'Year': '', 'IMDb Rating': ''}}

#     def __init__(self):
#         self.add_to_tv_shows(self.scrape('https://www.imdb.com/chart/tvmeter'))
#         self.add_to_tv_shows(self.scrape('https://www.imdb.com/chart/toptv/'))
#         self.tv_shows.pop('', None)

#         self.add_to_movies(self.scrape('https://www.imdb.com/chart/boxoffice'))
#         self.add_to_movies(self.scrape('https://www.imdb.com/chart/moviemeter'))
#         self.add_to_movies(self.scrape('https://www.imdb.com/chart/top'))
        
#         self.movies.pop('', None)

#     def add_to_tv_shows(self, scrape_result):
#         for key, value in scrape_result.items():
#             if key not in self.tv_shows:
#                 self.tv_shows[key] = value

#     def add_to_movies(self, scrape_result):
#         for key, value in scrape_result.items():
#             if key not in self.movies:
#                 self.movies[key] = value

#     def scrape(self, url):
#         response = requests.get(url)

#         soup = BeautifulSoup(response.text, 'html.parser')

#         tv_shows = soup.select('td.titleColumn')
#         ratings = soup.select('td.ratingColumn.imdbRating')

#         top_tv_shows = {}

#         for i in range(len(tv_shows)):
#             title = tv_shows[i].find('a').text

#             try:
#                 year = tv_shows[i].find('span').text
#                 year = re.sub(r'\((.*?)\)', r'\1', year)
#             except:
#                 year = ""

#             try:
#                 rating = ratings[i].find('strong').text
#             except:
#                 rating = ""

#             top_tv_shows[title] = {'Year': year, 'IMDb Rating': rating}

#         return top_tv_shows

class TheMovieDB:

    def __init__(self):
        pass

    def get_popular_movies(self, from_year, pages = 1):
        # set up the URL and parameters for the API request
        url = "https://api.themoviedb.org/3/discover/movie"
        params = {
            "sort_by": "vote_average.desc",
            "api_key": "aa95d4206fa2616cf5a2ea5053a1f567",
            "vote_count.gte": "50"
        }

        # initialize an empty list to store the results
        # get the current year
        current_year = datetime.datetime.now().year

        results = []

        # loop through the years from 2000 to the current year
        for year in range(from_year, current_year + 1):
            # add the primary_release_year parameter to the API request
            params["primary_release_year"] = str(year)
            
            for page in range(1, pages):
                params["page"] = str(page)
                
                # make the API request and store the response
                response = requests.get(url, params=params)
                
                # parse the JSON data from the response into a dictionary
                data = response.json()
                
                # add the dictionary to the list of results
                #results.extend(data["results"])
                for movie in data["results"]:
                    results.append(movie["original_title"])
            
        # print the list of results to see the data for all years
        return(results)

    def get_popular_tvshows(self, from_year, pages = 1):
        # set up the URL and parameters for the API request
        url = "https://api.themoviedb.org/3/discover/tv"
        params = {
            "sort_by": "vote_average.desc",
            "api_key": "aa95d4206fa2616cf5a2ea5053a1f567",
            "vote_count.gte": "50"
        }

        # initialize an empty list to store the results
        # get the current year
        current_year = datetime.datetime.now().year

        results = []

        # loop through the years from 2000 to the current year
        for year in range(from_year, current_year + 1):
            # add the primary_release_year parameter to the API request
            params["first_air_date_year"] = str(year)
            
            for page in range(1, pages):
                params["page"] = str(page)

                # make the API request and store the response
                response = requests.get(url, params=params)
                
                # parse the JSON data from the response into a dictionary
                data = response.json()
                
                # add the dictionary to the list of results
                #results.extend(data["results"])
                for show in data["results"]:
                    results.append(show["original_name"])               
            
        # print the list of results to see the data for all years
        return(results)

    def search(self, original_title, title_list) -> bool:
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

            if num_words < movie_title_words:
                continue

            if num_words > 0:
                percent = round((num_words / title_words) * 100, 0)
            else:
                percent = 0

            if percent == 100:
                matching_movies.append(title)
                break

        # Check if at least 50% of the words in the text match movie titles
        if len(matching_movies) > 0:
            return(True)
        else:
            return(False)