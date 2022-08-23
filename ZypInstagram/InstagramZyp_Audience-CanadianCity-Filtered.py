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

df_old = pd.read_csv(r'data/ZypInstagram_Audience-CanadianCity-Filtered.csv', index_col=False,encoding="utf-8");
lastMostRecentDate = df_old['end_time'][0];
sinceDate = time.mktime(datetime.datetime.strptime(lastMostRecentDate,"%Y-%m-%d").timetuple());
print("Most recent date in the imported dataset: " + str(lastMostRecentDate) + " = " + str(sinceDate));

# ---------------------------------------------------------------

INSIGHT = "audience_city";

results = req_facebook("insights?metric="+INSIGHT+"&period=lifetime").json();

df_cityNames = pd.read_csv(r'CanadianCitiesFiltered.csv');
cityNames = [];
for i in df_cityNames.index:
    cityNames.append(df_cityNames["City"][i] + ", " + df_cityNames["Province"][i]);

labels = ["end_time","year","week"];
for item in cityNames:
    labels.append(item);

def getCityValues(results,cityNames):
    row = [];
    dateValue = parser.parse(results["data"][0]["values"][0]["end_time"].split("T")[0]);
    row.append(dateValue);
    yearValue = dateValue.isocalendar()[0];
    row.append(yearValue);
    weekValue = dateValue.isocalendar()[1];
    row.append(weekValue);
    for item in cityNames:
        colValue = results["data"][0]["values"][0]["value"].get(item,0);
        row.append(colValue);
    return row;

def getCityData(results,cityNames):
    data = [];
    data.append(getCityValues(results,cityNames));
    return data;

data = getCityData(results,cityNames);

print("Canadian city data extracted");

# ---------------------------------------------------------------

df_temp = pd.DataFrame(data,columns=labels);
df_temp['end_time'] = pd.to_datetime(df_temp['end_time']);

df_old['end_time'] = pd.to_datetime(df_old['end_time']);
df = pd.concat([df_temp,df_old.reindex(columns=df_temp.columns)], ignore_index=True);
df['end_time'] = pd.to_datetime(df['end_time']);
df = df.sort_values(by='end_time', ascending=False);
df = df.drop_duplicates(subset=['year','week'], keep="first");

print("All Canadian city data loaded into dataframe");

# ---------------------------------------------------------------

df.to_csv("data/ZypInstagram_Audience-CanadianCity-Filtered.csv",index=False,encoding="utf-8");
# df_temp.to_csv("data/ZypInstagram_Audience-CanadianCity-Filtered.csv",index=False,encoding="utf-8");

print("Dataframe loaded as CSV");

# ---------------------------------------------------------------

def saveToGoogleSheets(googleSheetName, spreadsheetID, csvFilePath):
    sa = gspread.service_account(filename="zyp-art-gallery-62e00b2be4ff.json");
    sh = sa.open(googleSheetName);
    wks = sh.worksheet(googleSheetName);
    wks.clear();
    content = open(csvFilePath, 'r', encoding="Latin-1").read();
    sa.import_csv(spreadsheetID, content);
    print("Dataframe loaded to Google Sheets");

googleSheetName = "ZypInstagram_Audience-CanadianCity-Filtered";
spreadsheetID = "1jERGg2wuBF6cRH-iX4PNSSIH9Ja4quso0EUCODt5kxg";
csvFilePath = "data/ZypInstagram_Audience-CanadianCity-Filtered.csv";

saveToGoogleSheets(googleSheetName, spreadsheetID, csvFilePath);