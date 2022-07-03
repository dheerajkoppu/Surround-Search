# Surround Search

This program will suggests attractions to visit to potential visitors based on attributes that the visitor would enter.

This program was created for the 2022 FBLA Coding and Programming Event.

Written in Python (Following the PEP-8 Style Guide), HTML, CSS, and JSON

#### Created By: Dheeraj Koppu

## The Project

### Back End:

- the app starts at `server.py` which is the python program of the code.
- add frameworks and packages in `requirements.txt`

#### Functions Used:

- <b>gfg</b>: pulls user inputs from HTML file into python program
- <b>surround_search</b>: Filters locations by users desired attributes and returns them
- <b>get_geo_coord</b>: converts users locations into geocoordinates

### Front End:

- the first site the user sees is `index.html` which is where the user would enter their desired attributes
- `faq.html` is the webstie the users would go to if they have any questions about the program
- `common.css` is the css used for the HTML pages
- `output.html` is the website where the users would see the output of their entry, which would show possible locations to visit

### Overall Method:

1. The user inputs the desired attributes that they would prefer in their location
2. Filter the data by the users desired attributes
3. Return the top 5 locations the user could visit

### Run the Program:

Go to [https://surroundsearch.glitch.me](https://surroundsearch.glitch.me)
