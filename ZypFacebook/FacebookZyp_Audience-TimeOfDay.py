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

URL = "https://graph.facebook.com/" + VERSION + "/";

with open('AccessToken.txt') as f:
    ACCESS_TOKEN = f.readlines();
    f.close();

# ------------------------------------------------------------

df_old = pd.read_csv(r'data/ZypFacebook_Audience-TimeOfDay.csv', index_col=False, encoding='utf-8');
lastMostRecentDate = df_old['end_time'][0];
sinceDate = time.mktime(datetime.datetime.strptime(lastMostRecentDate,"%Y-%m-%d").timetuple());
print("Most recent date in the imported dataset: " + str(lastMostRecentDate) + " = " + str(sinceDate));
# sinceDate = 1523948400;

# ------------------------------------------------------------

results = req_facebook("zypgallery/insights?metric=page_fans_online&period=day&since=" + str(sinceDate)).json();

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

labels = [];
labels.append("end_time");
for range in timeRange:
    labels.append(range);

def getTimeOfDayValues(results,timeAbbreviation,index):
    row = [];
    dateValue = parser.parse(results['data'][0]['values'][index].get('end_time',0).split(":")[0][0:10]);
    row.append(dateValue)
    for lbl in timeAbbreviation:
        colValue = results['data'][0]['values'][index]['value'].get(str(lbl),0)
        row.append(colValue);
    return row;

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

print("Time of Day insights data extracted");

# ------------------------------------------------------------

df_temp = pd.DataFrame(data,columns=labels);
df_temp = df_temp.sort_values(by='end_time', ascending=False);

df = pd.concat([df_temp,df_old.reindex(columns=df_temp.columns)], ignore_index=True);
df['end_time'] = pd.to_datetime(df['end_time']);
df = df.drop_duplicates();
df = df.sort_values(by='end_time', ascending=False);

print("All extracted Time of Day insights data loaded into a dataframe");

# ------------------------------------------------------------

df.to_csv("data/ZypFacebook_Audience-TimeOfDay.csv", index=False, encoding='utf8')

print("Dataframe loaded as CSV");

# ------------------------------------------------------------

def saveToGoogleSheets(googleSheetName, spreadsheetID, csvFilePath):
    sa = gspread.service_account(filename="zyp-art-gallery-service_account.json");
    sh = sa.open(googleSheetName);
    wks = sh.worksheet(googleSheetName);
    wks.clear();
    content = open(csvFilePath, 'r', encoding="Latin-1").read();
    sa.import_csv(spreadsheetID, content);
    print("Dataframe loaded to Google Sheets");

googleSheetName = "ZypFacebook_Audience-TimeOfDay";
spreadsheetID = "188yyzZiKwo3a-vDhWUtkkKH7fN1Rx0uXWGvTf-3uee0";
csvFilePath = "data/ZypFacebook_Audience-TimeOfDay.csv";

saveToGoogleSheets(googleSheetName, spreadsheetID, csvFilePath);