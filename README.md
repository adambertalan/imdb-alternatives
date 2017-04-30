# imdb-alternatives

This Python script looks up a given movie title on several
webpages and opens them in your browser's tabs.

## Requirements
* Python 3
* pip (for installing the required modules)
* virtualenv (installed with pip)

## Usage
1. `git clone https://github.com/AdamTakeow/imdb-alternatives.git imdb-alternatives`
2. `cd imdb-alternatives`
3. create venv folder here (`virtualenv -p python3 venv`)
5. activate the virtual environment
6. `pip install -r requirements.txt`
7. `python imdb_alternatives.py`

![running example](https://github.com/AdamTakeow/imdb-alternatives/blob/master/readme_pictures/imdb_alternatives_example.png "Example run of the script")

When the script starts, the user is asked to enter a movie title.
The movie is searched on these websites:
* https://www.themoviedb.org/
* https://letterboxd.com/
* https://www.icheckmovies.com/
* https://www.rottentomatoes.com/
* http://www.allmovie.com/
* http://imdb.com

The first match will be opened in a new tab in your default browser.

## Contributions

* [Jabba Laci](https://github.com/jabbalaci) (project idea)
