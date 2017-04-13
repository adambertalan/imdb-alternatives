# imdb-alternatives

This small project contains only a python script file which the user can run and search for movies with it.

The project idea and more details about the requirement description can be found on my teacher's website [here](https://arato.inf.unideb.hu/szathmary.laszlo/pmwiki/index.php?n=Py3.20170313a).

## Requirements:
* python 3
* pip for installing required modules
* virtualenv (installed with pip)

## Usage:
1. ```git clone https://github.com/AdamTakeow/imdb-alternatives.git imdb-alternatives```
2. ```cd imdb-alternatives```
3. create venv folder here
4. ```virtualenv -p *path-to-python-executable* venv```
5. activate virtual environment
6. ```pip install -r requirements.txt```
7. ```python imdb_alternatives.py```

![running example](https://github.com/AdamTakeow/imdb-alternatives/blob/master/readme_pictures/imdb_alternatives_example.png "Example run of the script")

When the script starts, the user can enter a movie name that will be searched on these websites:
* https://www.themoviedb.org/
* https://letterboxd.com/
* https://www.icheckmovies.com/
* https://www.rottentomatoes.com/
* http://www.allmovie.com/
* http://imdb.com

The first match will be opened on a new tab in the default browser and some information will also be printed on the command line interface too about wether the movie could be found on the page or not.
