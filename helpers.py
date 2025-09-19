import requests
import sqlite3
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
    # print(f'my_dict: {my_dict}')
    my_title = my_dict['title']
    
    # Use title to get better image
    headers = {
        'User-Agent': 'TravelBucketListApp/1.0 (https://your-website.com or your-email@example.com)'
    }
    api_url = f'https://en.wikipedia.org/w/api.php?action=query&prop=pageimages&pithumbsize=300&titles={my_title}&format=json&formatversion=2'
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status() # This will raise an exception for a 403 error
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
        # print(response.text) # Check the server's error message
    except Exception as err:
        print(f"An unexpected error occurred: {err}")
    img_response = response.json()
    # print(f'img_response: {img_response}')
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

def add(bucketItemData):
    # get form data
    title = bucketItemData.get('key_value')
    description = bucketItemData.get('description_value')
    url = bucketItemData.get('url_value')
    # user_id from session
    current_user = session["user_id"]

    # get location - long/latitude for item
    headers = {
        'User-Agent': 'TravelBucketListApp/1.0 (https://your-website.com or your-email@example.com)'
    }
    api_url = f'https://en.wikipedia.org/w/api.php?action=query&prop=coordinates&titles={title}&format=json&formatversion=2'
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status() # This will raise an exception for a 403 error
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
        # print(response.text) # Check the server's error message
    except Exception as err:
        print(f"An unexpected error occurred: {err}")
    response = response.json()
    # print(f'response: {response}')
    pages = response["query"]["pages"]
    title = pages[0]["title"]
    # Raise ValueError if 'coordinates' key is missing
    page_data = pages[0]
    if "coordinates" not in page_data:
        raise ValueError(f"No coordinates found for '{title}'. \
                        Try a more specific search term. There may be more than one {title}")
    latitude = pages[0]["coordinates"][0]["lat"]
    longitude = pages[0]["coordinates"][0]["lon"]

    # insert all into db
    # print(f'bucketItemData: {current_user}, {title}, {description}, {url}, {latitude}, {longitude}')
    with sqlite3.connect("database.db") as bucket:
        cursor = bucket.cursor()
        cursor.execute("INSERT INTO bucket_lists \
        (user_id,name,description,url,latitude,longitude) VALUES (?,?,?,?,?,?)",
                        (current_user, title, description, url, latitude, longitude))
        bucket.commit()


    # Redirect user to home page
    return redirect("/")


def delete_item_from_db(item_id):
    """
    Deletes an item from the bucket_lists table based on its ID.
    """
    try:
        # Use a 'with' statement for the database connection
        with sqlite3.connect("database.db") as bucket:
            cursor = bucket.cursor()
            
            # Enable foreign key support
            cursor.execute('PRAGMA foreign_keys = ON;')

            # Execute the DELETE statement with a placeholder
            # for the item_id to prevent SQL injection.
            cursor.execute("DELETE FROM bucket_lists WHERE id = ?", (item_id,))
            
            # The 'with' statement automatically handles the commit,
            # but it is good practice to include it explicitly.
            bucket.commit()

            # Optional: Check if a row was actually deleted.
            if cursor.rowcount > 0:
                print(f"Successfully deleted item with ID: {item_id}")
                return True
            else:
                print(f"No item found with ID: {item_id}")
                return False

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False

def is_text_only(user_input):
    """Returns True if the string contains only letters and spaces, and is not empty."""
    if not user_input or user_input.isspace():
        return False
    else:
        return all(char.isalpha() or char.isspace() for char in user_input)