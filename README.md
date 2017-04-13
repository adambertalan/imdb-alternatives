# imdb-alternatives

This small project contains only a python script file which the user can run and search for movies with it.

The project idea and more details about the requirement description can be found on my teacher's website [here](https://arato.inf.unideb.hu/szathmary.laszlo/pmwiki/index.php?n=Py3.20170313a).

## Requirements:
* python 3
* pip for installing required modules
* lxml 3.7.3 (can be installed with pip)
* requests 2.13.0 (can be installed with pip)

## Usage:
After installing every required module the user can simply run the script with the following command:
```
python3 imdb_alternatives.py
```

![running example](https://github.com/AdamTakeow/imdb-alternatives/blob/master/readme_pictures/imdb_alternatives_example.png "Example run of the script")

When the script starts, the user can enter a movie name that will be searched on these websites:
* https://www.themoviedb.org/
* https://letterboxd.com/
* https://www.icheckmovies.com/
* https://www.rottentomatoes.com/
* http://www.allmovie.com/
* http://imdb.com

The first match will be opened on a new tab in the default browser and some information will also be printed on the command line interface too about wether the movie could be found on the page or not.
