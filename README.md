# Travel Bucket List

#### Video Demo: [URL HERE](https://link.com/)

#### Description:

Travel Bucket List is a website where registered users can create a bucket list of dream destinations
that they aspire to visit before their time on this Earth expires. Visitors can register as users
then search for destinations. Once a destination is saved to their list, they can view all of their
destinations on an interactive map. Using the street view, users can see actual images of their destination
and visualize themselves being there! Finally, users can check the bucket list item off their list and mark it done
by creating a journal entry where they can describe the sites, sounds and adventure they experienced
while reaching their destination.
Users will also be able to upload their own images in a future version of the site.

## References

[Google's Gemini](https://gemini.google.com/) was used as the primary AI tool to expedite code syntax
debugging and for design recommendations.

[Wikipedia APIs](https://api.wikimedia.org/wiki/API_catalog) leveraged for searching and images. One API is first used to search then a
second API is called to get a better quality image for the site.

[Google Maps API](https://developers.google.com/maps/documentation/javascript/) enables users to interactively view their destinations.
A high level view displaying all locations on their list is their starting point. Then users can zoom in
and use Google's street view to explore a city, town or village.

## Run app

In Dev workspace

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
