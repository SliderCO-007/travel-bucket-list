# Travel Bucket List

#### Video Demo: [URL HERE](https://link.com/)

#### Description:

Travel Bucket List is a website where registered users can create a bucket list of dream destinations
that they aspire to visit before their time on Earth expires. Visitors can register as users
then search for destinations and add them to their personal travel bucket list. Once a destination is saved to their list, they can view all of their
destinations on the main page or on an interactive map. Using the street view, users can see actual images of their destination
and visualize themselves being there! Finally, users can check the bucket list item off their list and mark it done
by creating a journal entry to describe the many sites, sounds and adventures they experienced
while reaching their destination.

#### Creative Process:

The initial concept came to me while brainstorming ideas for what I was interested in. Having visited
many countries and locations, I recognize the value of travel and learning about new cultures. I've created
an application to make a difference in other people's lives encouraging them to travel and experience the world
knowing that they will grow and learn about themselves and the world.

The first step was to find an API that would return information about places in the world. Trip Advisor was the first
choice but I quickly recognized that the Trip Advisor data was very focused on commercial concerns such as restaurants, tours and
expeditions. While this is exciting, it is not the type of site I wanted to create. Then I found Wikipedia's
APIs.

Wikipedia data is vast and more like an online encyclopedia with many API endpoints for
different types of data. Initially the general search endpoint provided the required data in the response.
It returns a short description, a thumbnail and a page title. Upon implementing this API call, it was apparent that
the returned thumbnail image was unacceptable. Since it is a "thumbnail", the image is such a low resolution that most were
pixelated and grainy when displayed in the Bootstrap card. Further research revealed that Wikipedia provided another endpoint which can be
called with parameters defining the size of an image needed. So I learned how to stack API calls, or call them
sequentially. The application now makes a call to the search API then uses the page title in the response to make a
second API call to retrieve a higher quality image which is displayed to the user.

I leveraged many sources to get the API calls working. Wikipedia's documentation for the APIs includes Python
examples which provided a great starting point. Then Google's Gemini helped me to manage the data types in the API
responses. Dealing with lists and dictionaries made sense to me but I didn't know how to reference, convert and
create them in some cases. Fortunately, the Python community is vast and I quickly found examples which could be
converted to my specific use case. Between the Copilot responses embedded in Bing and Gemini,
I found that good prompts lead to good responses. There was also some Stack Overflow and
[GeeksforGeeks](https://www.geeksforgeeks.org/) sprinkled in which I have used many times in the past.

Now that we have locations it is time to save them and present them to the user. The "list.html" page is the main
page of the site which displays the records (locations) that have been saved to a user's bucket list. SQLite is
"da bomb" so to speak. It is easy to use and only requires a file rather than an addition external folder structure.
The projects from previous problem sets taught me enough to create tables for users and their saved locations which
provided the source for the list page to display the records in the Bootstrap card component.

The "Add" button on the search response card invokes yet another Wikipedia API call to retrieve coordinates
which along with the brief description, the image URL and the title are saved to the database to fulfill the
requirement to map the locations on an interactive map.
The project leverages Google Maps to bring the locations to life. The interactive functionality of Google Maps
is tremendous. Having used maps in previous projects, I knew this would be a great addition to the project.
Google's documentation is exceptional as it is thorough, accurate and current. It didn't take long to implement
and customize the map to look and behave as I envisioned.

Next, users need the ability to check items off their bucket list. Once they visit their destination or even as they travel to
reach it, they can create journal entries to record their thoughts and life events. A single journal entry marks the
location as visited both on the main list page and changes the color of the marker on the map. The third table in the
database, "journal" stores these entries and has a foreign key relationship to the bucket_lists table to tie them all
together. Users can use this feature as a running journal and make multiple entries for each location as they
progress or remember additional details.

Finally, once all of the functional requirements have been addressed it is time to improve the design. I tapped Google's
Gemini by submitting my login page template code and asking Gemini to improve my template to be more "professional and
contemporary". I was shocked by the recommendation to use a two column structure with a dark overlay and white text
to improve readability. While Gemini's code didn't properly render the stock image from Unsplash, I know both
CSS and Unsplash and was able to find an image then implement it using CSS in the style.css file. I experimented with
some variants of this design while updating the rest of the site but landed on the same basic principles for consistency.
The end result is a semi-professional looking site that I am proud to submit and share with friends and colleagues.

Time will tell if I take this to the next level. The domain, travelbucketlist.com has been purchased and while there
is not currently a site at the domain, it is priced at $29,999.00. I could search for a variant of
the domain and take it further. My initial research reveals that a Flask project can be hosted on Google Cloud using
the Google Run technology. What I've created so far is a good start but to pursue something further will require
additional features. The first one is likely an external database to handle the volume of users with their many destinations.
Even the few users that I've created while developing the project reveals that the bucket_lists table could grow to be
quite large. While I like SQLite, I would look at GCP's Firebase or Firestore technologies as I've found them easy to implement and
very cost effective in past projects. The Firebase Authentication service also offers the many authentication options that users
expect in today's modern websites like the ability to log in using Facebook or Google. Next, users should be able to upload
their own images. Everyone has smartphones and I know my Google account has a running history of my travels, this site should
provide the functionality for users to upload their images (perhaps from Google drive) to add them to their journal.

```
|-- README.md
|-- app.py
|-- database.db
|-- helpers.py
|-- requirements.txt
|-- static
|   |-- cristian-macovei-af7YjaPMce0-unsplash.jpg
|   |-- favicon.ico
|   |-- pietro-de-grandi-T7K4aEPoGGk-unsplash.jpg
|   |-- reisetopia-6qfaxB-cm0o-unsplash.jpg
|   |-- secret-travel-guide-VNjnidGrH4w-unsplash.jpg
|   `-- styles.css
`-- templates
    |-- apology.html
    |-- join.html
    |-- layout.html
    |-- list.html
    |-- login.html
    |-- map.html
    `-- search.html
```

| File/Directory                               | Summary                                                                                                                                                                                                              |
| -------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| README.md                                    | Provides detailed information about the project. This includes an overview along with instructions on how to set up and run the application.                                                                         |
| app.py                                       | This is the main Python script for the Flask application. It defines the application's routes (/, /login, /list, /search, etc.), handles user requests, interacts with the database, and renders the HTML templates. |
| database.db                                  | A file that stores the project's data. This SQLite database contains tables for users (PARTICIPANTS), bucket list items (bucket_lists), and journal entries (journal).                                               |
| helpers.py                                   | A Python module containing helper functions. These are utility functions designed to make the main application code cleaner by abstracting common tasks, such as database queries, API calls, or input validation.   |
| requirements.txt                             | Lists the Python libraries and their versions required to run the application. This file is used to install all dependencies by running pip install -r requirements.txt.                                             |
| static/                                      | A directory for static files that are served directly to the user's browser.                                                                                                                                         |
| cristian-macovei-af7YjaPMce0-unsplash.jpg    | A stock photo, used as the background image on the map page of the application.                                                                                                                                      |
| favicon.ico                                  | The custom icon with the letters TBL for Travel Bucket List that appears in a browser's tab or bookmarks bar.                                                                                                        |
| pietro-de-grandi-T7K4aEPoGGk-unsplash.jpg    | Another stock photo, used on the login page which is the first thing displayed when visiting the site.                                                                                                               |
| reisetopia-6qfaxB-cm0o-unsplash.jpg          | Another stock photo, used as the background for both the registration page (join.html) and the main page (list.html).                                                                                                |
| secret-travel-guide-VNjnidGrH4w-unsplash.jpg | Another stock photo, used as the background for the search page.                                                                                                                                                     |
| styles.css                                   | The stylesheet for the project. It defines the visual appearance of the HTML elements, including fonts, colors, and layout, and contains custom styles in addition to Bootstrap styling.                             |
| templates/                                   | A directory containing the HTML templates used by the Flask application. Jinja is the template engine used to dynamically render these pages.                                                                        |
| apology.html                                 | A template for displaying error messages to the user.                                                                                                                                                                |
| join.html                                    | The template for the user registration page, where new users can create an account.                                                                                                                                  |
| layout.html                                  | The base template that other pages extend. It defines the common structure, like the navigation bar, footer, and overall page layout.                                                                                |
| list.html                                    | The template that displays the user's bucket list items. This page uses Jinja to iterate over data passed from app.py to display Bootstrap cards for each destination.                                               |
| login.html                                   | The template for the user login page.                                                                                                                                                                                |
| map.html                                     | A template for displaying a map view of the bucket list destinations using the Google Maps API.                                                                                                                      |
| search.html                                  | The template for the search page, where users can search for new destinations to add to their list. The search results are provided by the Wikipedia API.                                                            |

## References

[Google's Gemini](https://gemini.google.com/) was used as the primary AI tool to expedite code syntax
debugging and for design recommendations.

[Wikipedia APIs](https://api.wikimedia.org/wiki/API_catalog) leveraged for searching and images. One API is first used to search then a
second API is called to get a better quality image for the site. The same endpoint that is used for the image is called to request coordinates
when the function to add the location to the database is executed.

[Google Maps API](https://developers.google.com/maps/documentation/javascript/) enables users to interactively view their destinations.
A high level view displaying all locations on their list is their starting point. Then users can zoom in
and use Google's street view to explore a city, town or village.

## Run app

In Dev workspace

Install Python (version used is `Python 3.13.7`)

Clone the repository to your local workspace.

Create Virtual Environment

```shell
$ python -m venv venv
```

Activate the Virtual Environment (using Git Bash on Windows)

```shell
$ source ./venv/bin/activate
```

Install project dependencies

```shell
$ pip install -r requirements.txt
```

Start Flask to run locally

```shell
$ flask run --debug
```

Expected output

```shell
$ flask run --debug
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 102-007-695
```

Load `http://127.0.0.1:5000` in a browser to view the site.
