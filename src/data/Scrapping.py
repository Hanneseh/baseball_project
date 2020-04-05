import requests
import re
from urllib.parse import urljoin
from urllib.request import urlopen
from bs4 import BeautifulSoup as soup
import pandas as pd

BBref_URLs = []

Honkbalsite_url = "https://www.honkbalsite.com/profhonkballers/"

# Reading HTML from above URL, using the BeautifulSoup4 library. 
page_html = urlopen(Honkbalsite_url).read()
page_soup = soup(page_html, "html.parser")

# Searching the HTML for all tables with ID = tablepress-1
RawHTML = page_soup.findAll("table",{"id":"tablepress-1"})

# Converting variable into a string.
RawHTML = str(RawHTML)

# Using the Pandas read_html function to convert HTML to a DataFrame in a list.
Table = pd.read_html(RawHTML)
print(Table)
# As the DataFrame is still in a list, next line takes the first (and only) item out of the list.
Table = Table[0]
print(Table)
# This line removes all rows with a 'NaN' value and then resets the indexes.
Table = Table.dropna().reset_index(drop=True)

# This replaces the column-names with the values in this list.
Table.columns = ["Pos", "PlayerName", "Team", "BirthPlace"]

# Placing all Player Names from the DataFrame column into a list which we can then loop through.
dfPlayerName = Table["PlayerName"].to_list()


for PlayerName in dfPlayerName:
    # Replace all whitespaces in a players name with a "+".
    PlayerName_search = PlayerName.replace(" ", "+")

    # Next 2 if-statements were necessary because results were not right.
    if PlayerName_search == "Mike+Kelkboom":
        PlayerName_search = "Makesiondon+Kelkboom"

    if PlayerName_search == "Cal+Maduro":
        BBref_URLs.append("https://www.baseball-reference.com/register/player.fcgi?id=maduro001cal")
    
    # If PlayerName is not "Cal+Maduro" then this part wil run:
    else:
        # Defining the URL used for the search.
        BBref_search = "https://www.baseball-reference.com/search/search.fcgi?search=" + PlayerName_search

        BBref_search_html = urlopen(BBref_search).read()
        BBref_search_soup = soup(BBref_search_html, "html.parser")

        BBref_search_results = BBref_search_soup.findAll("div",{"class":"search-item-name"})

        # If results are found (not zero) the first part runs. 
        # If results are not found, this often means you're redirected to the player immediately or no hits are found (the last is filtered out later).
        if len(BBref_search_results) > 0:
            BBref_search_results = str(BBref_search_results)
            
            # Searching the result for the entered player name. If found this removes all text after the result.
            BBref_search_href = BBref_search_results[:BBref_search_results.find(PlayerName)]
            
            # Searching from right to left for "href=" (indicating a part of a URL). If found this removes all text *before* the result.
            BBref_search_href = BBref_search_href[BBref_search_href.rfind("href=")+6:]
            
            # Searching from left to right for a " indicating the end of the URL-part. If found this removes all text after the result.
            BBref_search_href = BBref_search_href[:BBref_search_href.find('"')]

            # Previous result (part of URL) is pasted after the base URL resulting in a full URL directing to the player's page.
            BBref_PlayerURL = "https://www.baseball-reference.com" + BBref_search_href
            
            # Adding the full URL to the list of Player URLs.
            BBref_URLs.append(BBref_PlayerURL)
        

        # This loop runs if you're redirected to the player's page directly or if no results are found.
        else:
            # This part defines formulas used for finding all URL's on a page and stores them in list called 'links' (found on the internet).
            def make_soup(url):
                r = requests.get(BBref_search)
                main_soup = soup(r.text, "html.parser")
                return main_soup

            def get_links(url):
                main_soup = make_soup(BBref_search)
                a_tags = main_soup.find_all("a", href=re.compile(r''))
                links = [urljoin(BBref_search, a["href"])for a in a_tags]  # convert relative url to absolute url
                return links

            links = get_links(BBref_search)
            
            # This loops through all items in the list 'links'.
            for Item in links:
                # Only links containing this base URL are player links.
                # All links containing "&type=" are sub-pages, thus not necessary for us (if sub-page is present, main page is present as well).
                if "https://www.baseball-reference.com/register/player.fcgi?id=" in Item and "&type=" not in Item:
                    BBref_URLs.append(Item)


# This line removes all duplicate links, remaining links are only unique values.
BBref_URLs = list(dict.fromkeys(BBref_URLs))



# This line saves the BBref_URLs list to a text file.
with open("BBref_IDs.txt", "w") as f:
    for item in BBref_URLs:
        f.write("%s\n" % item)


