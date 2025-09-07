import requests
from dotenv import load_dotenv
import os

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

# TripAdvisor API Key
api_key = os.getenv("API_KEY")


def lookup(searchText):
    """Look up quote for symbol."""
    url = f"https://api.content.tripadvisor.com/api/v1/location/search?searchQuery={searchText}&language=en&key={api_key}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for HTTP error responses
        location_data = response.json()
        return {
            "locationId": location_data["location_id"],
            "price": quote_data["latestPrice"],
            "symbol": symbol.upper()
        }
    except requests.RequestException as e:
        print(f"Request error: {e}")
    except (KeyError, ValueError) as e:
        print(f"Data parsing error: {e}")
    return None
