import requests

# set up the URL and parameters for the API request
url = "https://api.themoviedb.org/3/discover/movie"
params = {
    "sort_by": "vote_average.desc",
    "api_key": "aa95d4206fa2616cf5a2ea5053a1f567",
    "vote_count.gte": "50"
}

# initialize an empty list to store the results
results = []

# loop through the years from 2000 to the current year
for year in range(2000, 2023):
    # add the primary_release_year parameter to the API request
    params["primary_release_year"] = str(year)
    
    # make the API request and store the response
    response = requests.get(url, params=params)
    
    # parse the JSON data from the response into a dictionary
    data = response.json()
    
    # add the dictionary to the list of results
    results.extend(data["results"])
    
# print the list of results to see the data for all years
print(len(results))
