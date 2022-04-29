import requests
import pandas as pd
import time
import datetime
from dateutil import parser
import gspread

def req_facebook(req):
    r = requests.get(URL + req, {'access_token': ACCESS_TOKEN});
    return r;

def paginate(r, direction):
    return requests.get(r['paging'][direction]);

VERSION = "v12.0";

text_file = open("IGMediaID.txt", "r");
IG_MEDIA_ID = text_file.read();
text_file.close();

URL = "https://graph.facebook.com/" + VERSION + "/" + IG_MEDIA_ID + "/";

with open('AccessToken.txt') as f:
    ACCESS_TOKEN = f.readlines();
    f.close();

# ---------------------------------------------------------------

df_old = pd.read_csv(r'data/ZypInstagram_Audience-TimeOfDay.csv', index_col=False,encoding="utf-8");
lastMostRecentDate = df_old['end_time'][0];
sinceDate = time.mktime(datetime.datetime.strptime(lastMostRecentDate,"%Y-%m-%d").timetuple());
print("Most recent date in the imported dataset: " + str(lastMostRecentDate) + " = " + str(sinceDate));

# ---------------------------------------------------------------

INSIGHT = "online_followers";

results = req_facebook("insights?metric="+INSIGHT+"&period=lifetime").json();

timeAbbreviation = [];
for i in range(24):
    timeAbbreviation.append(i);

timeRange = [];
count = 0;
while count < 23:
    startTime = str(timeAbbreviation[count]) + ":00";
    endTime = str(timeAbbreviation[count+1]) + ":00";
    timeRange.append(startTime + " - " + endTime);
    count += 1;
timeRange.append(str(timeAbbreviation[23]) + ":00 - " + "24:00");

labels = ["end_time","year","week"];
for range in timeRange:
    labels.append(range);

def getTimeOfDayValues(results,timeAbbreviation,index):
    row = [];
    dateValue = parser.parse(results["data"][0]["values"][index]["end_time"].split(":")[0][0:10]);
    row.append(dateValue);
    yearValue = dateValue.isocalendar()[0];
    row.append(yearValue);
    weekValue = dateValue.isocalendar()[1];
    row.append(weekValue);
    for lbl in timeAbbreviation:
        colValue = results['data'][0]['values'][index]['value'].get(str(lbl),0)
        row.append(colValue);
    return row;

def getHistoricalTimeOfDayData(results):
    data = [];
    while True:
        try:
            data.append(getTimeOfDayValues(results,timeAbbreviation,1));
            data.append(getTimeOfDayValues(results,timeAbbreviation,0));
            results = paginate(results,"previous").json();
        except:
            print("done");
            break;
    return data;

def getTimeOfDayData(results,i=0):
    data = [];
    while True:
        try:
            if(i <= len(results["data"][0]["values"])):
                data.append(getTimeOfDayValues(results,timeAbbreviation,i));
                i += 1;
            else:
                results = paginate(results,"previous").json();
                i = 0;
        except:
            print("done");
            break;
    return data;

data = getTimeOfDayData(results);
# data = getHistoricalTimeOfDayData(results)

print("Time of Day data extracted");

# ---------------------------------------------------------------

df_temp = pd.DataFrame(data,columns=labels);
df_temp['end_time'] = pd.to_datetime(df_temp['end_time']);

df = pd.concat([df_temp,df_old]);
df['end_time'] = pd.to_datetime(df['end_time']);
df = df.sort_values(by='end_time', ascending=False);
df = df.drop_duplicates(subset=['year','week'], keep="first");

print("All Time of Day data loaded into dataframe");

# ---------------------------------------------------------------

df.to_csv("data/ZypInstagram_Audience-TimeOfDay.csv",index=False);

print("Dataframe loaded as CSV");

# ---------------------------------------------------------------

def saveToGoogleSheets(googleSheetName, spreadsheetID, csvFilePath):
    sa = gspread.service_account(filename="zyp-art-gallery-service_account.json");
    sh = sa.open(googleSheetName);
    wks = sh.worksheet(googleSheetName);
    wks.clear();
    content = open(csvFilePath, 'r', encoding="Latin-1").read();
    sa.import_csv(spreadsheetID, content);
    print("Dataframe loaded to Google Sheets");

googleSheetName = "ZypInstagram_Audience-TimeOfDay";
spreadsheetID = "1GxrrByhjKPT2SC8RzHTPlqu0VpMv3ISaMAMx2Muivrs";
csvFilePath = "data/ZypInstagram_Audience-TimeOfDay.csv";

saveToGoogleSheets(googleSheetName, spreadsheetID, csvFilePath);