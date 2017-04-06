#!/usr/bin/env python3

# imdb_alternatives.py

# This script searches for a user given movie name on
# several movie sites and opens them directly in separate
# tabs in the default browser so there is no need to
# search the movies on each site.

__author__ = "Bertalan Ádám"

from lxml import html
import requests
import webbrowser
import json
import logging

# Logging configuration
FORMAT = '%(levelname)s: %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)

# Sites to be scraped (6)
# https://www.themoviedb.org/
# https://letterboxd.com/
# https://www.icheckmovies.com/
# https://www.rottentomatoes.com/
# http://www.allmovie.com/
# http://imdb.com


# This dictionary contaions informations about several movie websites.
# 
# searchUrl: The url which can search for a movie after filled the format out.
# openUrl: The url which after the format supplement, provide the result movie's url.
# nofResults: The xpath expr which will result as many elements as the count of result movies.
#     With this count the result number of movies can be determined.
# movieNames: This is similar to nofResults, except that this will provide the explicit movie names
#     in a list.
# movieUrl: This xpath expression will produce the "index"th result movie's url. The openUrl should
#     be filled with this url.
movieDataDict = {
    "TheMovieDB" :
    {
        "searchUrl" : "https://www.themoviedb.org/search?query={enteredMovieName}",
        "openUrl" : "https://www.themoviedb.org{foundMovieUrl}",
        "nofResults" : "//div[@class='results']/div",
        "movieNames" : "//div[@class='results']/div/div[@class='info']/p[1]/a/text()",
        "movieUrl": "//div[@class='results']/div[{index}]/div[@class='info']/p[1]/a/@href"
    },
    "LetterBoxD" :
    {
        "searchUrl" : "https://letterboxd.com/search/films/{enteredMovieName}/",
        "openUrl" : "https://letterboxd.com{foundMovieUrl}",
        "nofResults" : "//ul[@class='results']/li",
        "movieNames" : "//ul[@class='results']/li/div[@class='film-detail-content']/h2/span/a/text()",
        "movieUrl": "//ul[@class='results']/li[{index}]/div[@class='film-detail-content']/h2/span/a/@href"
    },
    "IChekcMovies":
    {
        "searchUrl" : "https://www.icheckmovies.com/search/movies/?query={enteredMovieName}",
        "openUrl" : "https://www.icheckmovies.com{foundMovieUrl}",
        "nofResults" : "//ol[@id='itemListMovies']/li",
        "movieNames" : "//ol[@id='itemListMovies']/li/h2/a/text()",
        "movieUrl": "//ol[@id='itemListMovies']/li[{index}]/h2/a/@href"
    },
    "IMDB" :
    {
        "searchUrl": "http://www.imdb.com/find?ref_=nv_sr_fn&q={enteredMovieName}&s=tt",
        "openUrl": "http://www.imdb.com{foundMovieUrl}",
        "nofResults" : "//table[@class='findList']/tr",
        "movieNames" : "//table[@class='findList']/tr/td[@class='result_text']/a/text()",
        "movieUrl": "//table[@class='findList']/tr[{index}]/td[@class='result_text']/a/@href"
    },
    "AllMovie" :
    {
        "searchUrl": "http://www.allmovie.com/search/all/{enteredMovieName}",
        "openUrl": "{foundMovieUrl}",
        "nofResults": "//ul[@class='search-results']/li",
        "movieNames": "//ul[@class='search-results']/li/div[@class='info']/div[@class='title']/a/text()",
        "movieUrl": "//ul[@class='search-results']/li[{index}]/div[@class='info']/div[@class='title']/a/@href"
    }
}


def processMovieWebsites(movieName):
    """Process the movieDataDict dictionary.

    parameters:
    movieName: The movie's name to search for.
    """
    
    headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.33 Mobile Safari/537.36'}
    
    for key, value in movieDataDict.items():
        logging.debug("Got movie name: {movieName}".format(movieName=movieName))
        logging.debug("Working on {}".format(key))
        
        page = requests.get(value["searchUrl"].format(enteredMovieName=movieName), headers=headerss)
        tree = html.fromstring(page.content)
        
        results = tree.xpath(value["nofResults"])
        logging.debug("results number: {}".format(len(results)))
        
        movieNotFound = False
        
        if len(results) > 0:
            for index, foundMovieName in enumerate(tree.xpath(value["movieNames"])):
                if foundMovieName.lower().strip().find(movieName.lower().strip()) >= 0:
                    print("{websiteName} says: Movie '{movieName}' FOUND!".format(websiteName=key, movieName=foundMovieName))
                    
                    resultUrl = tree.xpath(value["movieUrl"].format(index=(index+1)))[0]
                    webbrowser.open(value["openUrl"].format(foundMovieUrl=resultUrl), new=2)
                    break
            else:
                movieNotFound = True
        else:
            movieNotFound = True
        
        if movieNotFound:
            print("{websiteName} says: Movie '{movieName}' NOT found!".format(websiteName=key, movieName=movieName))
        logging.debug("-"*10)


def processRottenTomatoes(movieName):
    """Process the RottenTomatoes website.
    
    It needs to be in a separate function because
    the logic in the processMovieWebsites is different
    in the RottenTomatoes case.
    
    The page itself does not contains the result in a html
    structure, but a script does
    so the logic in this function processes the script'a
    content as a json.
    
    parameters:
    movieName: The movie's name to search for.
    """
    
    logging.debug("Working on RottenTomatoes")
    page = requests.get("https://www.rottentomatoes.com/search/?search={enteredMovieName}".format(enteredMovieName=movieName))
    tree = html.fromstring(page.content)
    results = tree.xpath('//div[@id="main_container"]/div[1]/script/text()')
    
    logging.debug("results number: {}".format(results))
    
    movieNotFound = False
    
    if len(results) > 0:
        resultJSON = results[0]
        jsonStart = resultJSON.find("{",resultJSON.find("{")+1)
        jsonEnd = resultJSON.find(";")
        
        jsonDict=json.loads(resultJSON[jsonStart:jsonEnd-1])
        logging.debug("json: {}".format(jsonDict))
        
        if jsonDict['movieCount'] > 0:
            for movie in jsonDict["movies"]:
                if movie["name"].lower().strip().find(movieName.lower().strip()) >= 0:
                    print("RottenTomatoes says: Movie '{movieName}' FOUND!".format(movieName=movieName))
                    
                    webbrowser.open("https://www.rottentomatoes.com{}".format(movie["url"]), new=2)
                    break
        else:
            movieNotFound = True
    else:
        movieNotFound = True
    
    if movieNotFound:
        print("RottenTomatoes says: Movie '{movieName}' not found!".format(movieName=movieName))


def getMovieNameFromUser():
    """Prompt the user to enter a movie name to search for.
    
    Returns the entered movie's name, or None upon user interruption.
    """
    
    validInput = False
    movieName = ""
    try:
        while not validInput:
            movieName = input("Enter movie name: ")
            if len(movieName) <= 0:
                print("Enter a valid movie name!")
            else:
                validInput = True
        return movieName
    except KeyboardInterrupt as ki:
        logging.debug("User interruption")
        return None


def main():
    logging.debug("main started")
    movieName = getMovieNameFromUser()
    if movieName:
        processMovieWebsites(movieName)
        processRottenTomatoes(movieName)


if __name__ == "__main__":
    main()