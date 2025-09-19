# Travel Bucket List

#### Video Demo: [URL HERE](https://link.com/)

#### Description:

Travel Bucket List is a website where registered users can create a bucket list of dream destinations
that they aspire to visit before their time on this Earth expires. Visitors can register as users
then search for destinations. Once a destination is saved to their list, they can view all of their
destinations on an interactive map. Using the street view they can see exactly what the place looks
like and visualize themselves in the place! Finally, users can check it off their list and mark it done
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

```shell
$ flask run --debug
```
