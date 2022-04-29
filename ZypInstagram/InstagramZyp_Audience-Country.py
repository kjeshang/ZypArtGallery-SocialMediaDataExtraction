import requests
import pandas as pd
import time
import datetime
from dateutil import parser
import json
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

df_old = pd.read_csv(r'data/ZypInstagram_Audience-Country.csv', index_col=False,encoding="utf-8");
lastMostRecentDate = df_old['end_time'][0];
sinceDate = time.mktime(datetime.datetime.strptime(lastMostRecentDate,"%Y-%m-%d").timetuple());
print("Most recent date in the imported dataset: " + str(lastMostRecentDate) + " = " + str(sinceDate));

# ---------------------------------------------------------------

INSIGHT = "audience_country";

results = req_facebook("insights?metric="+INSIGHT+"&period=lifetime").json();

with open("FacebookCountryList.json") as f:
    countryList = json.load(f);
    f.close();

countryKey = [];
countryName = [];
for i in range(len(countryList["data"])):
    countryKey.append(countryList["data"][i].get("key",0));
    countryName.append(countryList["data"][i].get("name",0));

labels = ["end_time","year","week"];
for name in countryName:
    labels.append(name);

def getCountryValues(results,countryKey):
    row = [];
    dateValue = parser.parse(results["data"][0]["values"][0]["end_time"].split("T")[0]);
    row.append(dateValue);
    yearValue = dateValue.isocalendar()[0];
    row.append(yearValue);
    weekValue = dateValue.isocalendar()[1];
    row.append(weekValue);
    for item in countryKey:
        colValue = results["data"][0]["values"][0]["value"].get(item,0);
        row.append(colValue);
    return row;

def getCountryData(results,countryKey):
    data = [];
    data.append(getCountryValues(results,countryKey));
    return data;

data = getCountryData(results,countryKey);

print("Country data extracted");

# ---------------------------------------------------------------

df_temp = pd.DataFrame(data,columns=labels);
df_temp['end_time'] = pd.to_datetime(df_temp['end_time']);

df = pd.concat([df_temp,df_old]);
df['end_time'] = pd.to_datetime(df['end_time']);
df = df.sort_values(by='end_time', ascending=False);
df = df.drop_duplicates(subset=['year','week'], keep="first");

print("All Country data loaded into dataframe");

# ---------------------------------------------------------------

df.to_csv("data/ZypInstagram_Audience-Country.csv",index=False,encoding="utf-8");

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

googleSheetName = "ZypInstagram_Audience-Country";
spreadsheetID = "1E3qUSiiPI0STrw8vMGi-kuoIlDoH4DBzqV2niEtWACg";
csvFilePath = "data/ZypInstagram_Audience-Country.csv";

saveToGoogleSheets(googleSheetName, spreadsheetID, csvFilePath);