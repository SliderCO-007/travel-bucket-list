import requests
from dotenv import load_dotenv

from flask import redirect, render_template, session
from functools import wraps


def apology(message, code=400):
    """Render message as an apology to user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s

    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


# def lookup(symbol):
#     """Look up quote for symbol."""
#     url = f"https://finance.cs50.io/quote?symbol={symbol.upper()}"
#     try:
#         response = requests.get(url)
#         response.raise_for_status()  # Raise an error for HTTP error responses
#         quote_data = response.json()
#         return {
#             "name": quote_data["companyName"],
#             "price": quote_data["latestPrice"],
#             "symbol": symbol.upper()
#         }
#     except requests.RequestException as e:
#         print(f"Request error: {e}")
#     except (KeyError, ValueError) as e:
#         print(f"Data parsing error: {e}")
#     return None

# Wikipedia API
# https://api.wikimedia.org/wiki/Core_REST_API

# Troubleshooting research
# https://www.sqlpey.com/python/solved-how-to-pass-authorization-header/


def lookup(searchText):
    """Look up quote for symbol."""
    language_code = 'en'
    search_query = searchText
    number_of_results = 1
    headers = {
        'User-Agent': 'Travel Bucket List'
    }
    base_url = 'https://api.wikimedia.org/core/v1/wikipedia/'
    endpoint = '/search/page'
    url = base_url + language_code + endpoint
    parameters = {'q': search_query, 'limit': number_of_results, 'pithumbsize': 400}
    response = requests.get(url, params=parameters, headers=headers)
    my_list = response.json()
    my_dict = my_list["pages"][0]
    print(f'my_dict: {my_dict}')
    my_title = my_dict['title']
    
    # Use title to get better image
    headers = {
        'User-Agent': 'TravelBucketListApp/1.0 (https://your-website.com or your-email@example.com)'
    }
    api_url = f'https://en.wikipedia.org/w/api.php?action=query&prop=pageimages&pithumbsize=300&titles={my_title}&format=json&formatversion=2'
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status() # This will raise an exception for a 403 error
    # ... rest of your code ...
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
        print(response.text) # Check the server's error message
    except Exception as err:
        print(f"An unexpected error occurred: {err}")
    img_response = response.json()
    print(f'img_response: {img_response}')
    pages = img_response["query"]["pages"]
    img_url = pages[0]["thumbnail"]["source"]

    my_key = my_dict['key']
    my_description = my_dict['description']
    # Uses thumbnail from the initial search API which is of a very low quality
    # my_url = my_dict['thumbnail']['url']
    my_url = img_url

    new_dict = {
        'key': my_key,
        'description': my_description,
        'url': my_url
    }

    ### Need to Extract the values from the results to display to the user
    return {
        "key_value": new_dict['key'],
        "description_value": new_dict['description'],
        "url_value": new_dict['url']
    }
