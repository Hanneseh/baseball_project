# NL Baseball

This Application allows looking at and comparing the career and splits stats of professional Dutch baseball players.

Watch a screen capture: https://drive.google.com/file/d/1P-BC9HYBphJrzvLAeQbN_sP6iP6MyZAM/view?usp=sharing

Its creation was part of the thematic semester on Big Data at the Hogeschool van Amsterdam. 

## Getting Started

The project consists out of a dashboard application (“Dashboard” folder) and a data scraper (“DataScraper” folder). 
-	The Dashboard is made with Plotly-Dash (https://dash.plotly.com/)
-	The Data Scraper is written in python 
-	MongoDB is used to persist the data

### Prerequisites / Installing

This Application can be installed using docker or just pip (the default python package manager)

**In depth installation guides can be found in "installation.md" file in the “docs” folder**


## Documentation

The Project is documented with MkDocs. You can look at the documentation by either
-	browsing through the above “docs” folder 
-	or installing MkDocs (https://www.mkdocs.org/), dowloading this repository and running the “mkdocs serve” command in the “baseballmd” folder

## Contributors

The MegaData Team: August Carlsson, Basit Kazimi, Marcus Åqvist, Hannes Ehringfeld

## Contact Info
For further questions: 

- hannes.ehringfeld@hva.nl
- august.carlsson@hva.nl
- basit.kazimi@hva.nl
- marcus.aqvist@hva.nl


## License

This project is licensed under the MIT License - see the LICENSE file for details

The data used in this project is protected as followed:

"Copyright 2020 MLB Advanced Media, L.P.  Use of any content on this page acknowledges agreement to the terms posted here http://gdx.mlb.com/components/copyright.txt"
