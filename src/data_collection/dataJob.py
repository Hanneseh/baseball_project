# Cron job implementation
from app.package.playerScraping import getPlayerInfo
from app.package.getRawData import getRawDartaFromAPI
from app.package.createCareerSummaryData import getCareerSummaryData
from app.config import getDB
import datetime
import schedule
import time

client = getDB()
db = client['baseballmd']

def dataCollection():
    print('main start ')
    updateMeta = {}
    collectionNames = db.list_collection_names()
    if len(collectionNames) > 0 and 'metaData' in collectionNames:
        docs = list(db.metaData.find({},{"_id" : 0}))
        seq = [x['fetchCycle'] for x in docs]
        fetchNumberMax = max(seq)
        updateMeta['fetchCycle'] = fetchNumberMax +1
    else:
        updateMeta['fetchCycle'] = 1  

    now = datetime.datetime.now()
    updateMeta['fetchStartTime'] = now.strftime("%H:%M %d.%m.%Y")
    playerInfoChange = getPlayerInfo()
    rawDataChange = getRawDartaFromAPI()
    careerSummaryChange = getCareerSummaryData()

    updateMeta['totalNumberOfDocUpdates'] = playerInfoChange['updates'] + rawDataChange['updates'] + careerSummaryChange['updates']
    updateMeta['totalNumberOfDocInserts'] = playerInfoChange['inserts'] + rawDataChange['inserts'] + careerSummaryChange['inserts']

    now = datetime.datetime.now()
    updateMeta['fetchEndTime'] = now.strftime("%H:%M %d.%m.%Y")

    updateMeta.pop('_id', None)
    db['metaData'].insert_one(updateMeta)
    print('main end ')



# execute data gethering scrips: uncomment the one line accordingly
# testing the scedualer
schedule.every(15).minutes.do(dataCollection)

# implementation on server
# schedule.every().day.at("3:00").do(job)

# running the script just once
# dataCollection()

while True:
    schedule.run_pending()
    now = datetime.datetime.now()
    nextRun = schedule.next_run()
    print('Current Time: ', now.strftime("%H:%M:%S"), 'Next Run at: ', nextRun.strftime("%H:%M:%S"))
    time.sleep(60)