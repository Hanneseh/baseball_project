# Welcome to the DataScraper Docs

The goal of this documentations is to give a high-level overview of the inner workings of the Data Scraper. We are going from the bigger picture more and more into detail. Additionally, you can find some comments throughout the source code which should help you understand what’s going on. 

## General information:

The DataScraper takes care of collecting all needed data for the dashboard and storing it in our mongoDB. It is designed to run every night and detect changes in documents or insert new ones. Data sources are: 

-	https://www.honkbalsite.com/profhonkballers/
-	The links on the above website are followed to collect links to the player image on the website
-	The main data source is the official, free to use API: https://statsapi.mlb.com/
-	The above API is accessed through the API Wrapper “MLB-StatsAPI” made by “toddrob99”. Learn more about it here: https://github.com/toddrob99/MLB-StatsAPI

## Data Scraper Layout

        app/                                                              
            package/				
                __init__.py						
                createCareerSummaryData.py	# creates data for career table in dashboard
                getRawData.py			    # get all the raw data of all players
                playerScraping.py			# gets general plaer information
            __init__.py
            config.py                       # central database connection provider
        datajob.py                          # entry point of DataScraper
        Dockerfile
        requirements.txt


## Class Diagrams 

The purpose of the following diagram is to give an overview of the relationships between the different files, data sources and database collections:

![dsclasses](img/dsclasses.png)

Although the Diagram is very busy, it is not as complicated as it seems. We are going break down what exactly happens in all those .py files in the next paragraphs.

## dataJob.py

## playerScraping.py

## getRawData.py

## createCareerSummaryData.py
