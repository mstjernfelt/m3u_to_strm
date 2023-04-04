import re
import requests
from bs4 import BeautifulSoup

class Imdb:

    tv_shows = {'': {'Year': '', 'IMDb Rating': ''}}
    movies = {'': {'Year': '', 'IMDb Rating': ''}}

    def __init__(self):
        self.add_to_tv_shows(self.scrape('https://www.imdb.com/chart/tvmeter'))
        self.add_to_tv_shows(self.scrape('https://www.imdb.com/chart/toptv/'))
        self.tv_shows.pop('', None)

        self.add_to_movies(self.scrape('https://www.imdb.com/chart/boxoffice'))
        self.add_to_movies(self.scrape('https://www.imdb.com/chart/moviemeter'))
        self.add_to_movies(self.scrape('https://www.imdb.com/chart/top'))
        
        self.movies.pop('', None)

    def add_to_tv_shows(self, scrape_result):
        for key, value in scrape_result.items():
            if key not in self.tv_shows:
                self.tv_shows[key] = value

    def add_to_movies(self, scrape_result):
        for key, value in scrape_result.items():
            if key not in self.movies:
                self.movies[key] = value

    def scrape(self, url):
        response = requests.get(url)

        soup = BeautifulSoup(response.text, 'html.parser')

        tv_shows = soup.select('td.titleColumn')
        ratings = soup.select('td.ratingColumn.imdbRating')

        top_tv_shows = {}

        for i in range(len(tv_shows)):
            title = tv_shows[i].find('a').text

            try:
                year = tv_shows[i].find('span').text
                year = re.sub(r'\((.*?)\)', r'\1', year)
            except:
                year = ""

            try:
                rating = ratings[i].find('strong').text
            except:
                rating = ""

            top_tv_shows[title] = {'Year': year, 'IMDb Rating': rating}

        return top_tv_shows

    # def toptv(self):
    #     url = 'https://www.imdb.com/chart/toptv/'

    #     response = requests.get(url)

    #     soup = BeautifulSoup(response.text, 'html.parser')

    #     tv_shows = soup.select('td.titleColumn')
    #     ratings = soup.select('td.ratingColumn.imdbRating')

    #     top_tv_shows = {}

    #     for i in range(len(tv_shows)):
    #         title = tv_shows[i].find('a').text
    #         rating = ratings[i].find('strong').text
    #         top_tv_shows[title] = {'IMDb Rating': rating}

    #     return top_tv_shows