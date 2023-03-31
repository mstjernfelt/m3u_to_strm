import requests

class ImdbManagement:

    def __init__(self, title = None):
        # Send a request to the imdb-api.com API to search for the movie or TV show
        response = requests.get(f"https://imdb-api.com/en/API/Search/k_bac4m5jr/{title}")

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response and retrieve the first search result
            data = response.json()
            search_results = data.get("results")
            
            if search_results:
                first_result = search_results[0]

                response = requests.get(f"https://imdb-api.com/en/API/Ratings/k_bac4m5jr/{first_result.get('id')}")

                data = response.json()
                
                if data:
                    return(data.get('theMovieDb'))
                
        return 0
