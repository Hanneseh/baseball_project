# imports
import pandas as pd
from pymongo import MongoClient

client = MongoClient("localhost:27017")
db=client['baseballmd']


{"type" : "career", "statGroupe" : "hitting", "id":642720}

# this goes in the function
collection = db.careerStats

rawData = pd.DataFrame(list(collection.find({"type" : "career", "statGroupe" : "hitting"})))
rawData=rawData.drop(columns=['_id'])
rawData

playerDataOzzi = rawData.loc[lambda df: df['id'] == 645277]
playerDataOzzi

playerDataRay = rawData.loc[lambda df: df['id'] == 642720]
playerDataRay

# bookingLongEnoughReviews = (
#     dataBooking
#         .loc[lambda df: df['Review_Total_Negative_Word_Counts'] >= 5]
#         .loc[lambda df: df['Review_Total_Positive_Word_Counts'] >= 5]
# )

