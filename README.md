# travel-bucket-list

A travel bucket list site

### References

https://flask.palletsprojects.com/en/stable/quickstart/

_Simple project structure_
https://www.geeksforgeeks.org/python/how-to-build-a-web-app-using-flask-and-sqlite-in-python/

---

Question (prompt to AI) :

> Do I always have to close a cursor using cursor.close()?

GitHub CoPilot (code block from Google Gemini):

No, you don't always have to explicitly close a cursor in Python's sqlite3 module. When you use a `with` statement for the connection, the connection is properly closed, but cursors are not automatically closed. However, cursors are lightweight and usually closed when they are garbage collected. For best practice, you can use a `with` statement for the cursor as well (Python 3.6+):

```shell
# Automatic resource management using `with`
import sqlite3

conn = sqlite3.connect('example.db')
with conn:
    # A cursor object is automatically created and closed for you
    for row in conn.execute("SELECT * FROM some_large_table"):
        # Process each row, one by one
        print(row)

```

If you don't use a `with` statement for the cursor, it's good practice to call `cursor.close()` when you're done.
