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

df_old = pd.read_csv(r'data/ZypInstagram_Audience-Age&Gender.csv', index_col=False);
lastMostRecentDate = df_old['end_time'][0];
sinceDate = time.mktime(datetime.datetime.strptime(lastMostRecentDate,"%Y-%m-%d").timetuple());
print("Most recent date in the imported dataset: " + str(lastMostRecentDate) + " = " + str(sinceDate));

# ---------------------------------------------------------------

INSIGHT = "audience_gender_age";

results = req_facebook("insights?metric="+INSIGHT+"&period=lifetime").json();

genderAge = ['F.13-17','F.18-24','F.25-34','F.35-44','F.45-54','F.55-64','F.65+','M.13-17','M.18-24','M.25-34','M.35-44','M.45-54','M.55-64','M.65+','U.13-17','U.18-24','U.25-34','U.35-44','U.45-54','U.55-64','U.65+'];

labels = ["end_time","year","week"];
for item in genderAge:
    labels.append(item);

def getGenderAgeValues(results,genderAge):
    row = [];
    dateValue = parser.parse(results["data"][0]["values"][0]["end_time"].split("T")[0]);
    row.append(dateValue);
    yearValue = dateValue.isocalendar()[0];
    row.append(yearValue);
    weekValue = dateValue.isocalendar()[1];
    row.append(weekValue);
    for item in genderAge:
        colValue = results["data"][0]["values"][0]["value"].get(item,0);
        row.append(colValue);
    return row;

def getGenderAgeData(results,genderAge):
    data = [];
    data.append(getGenderAgeValues(results,genderAge));
    return data;

data = getGenderAgeData(results,genderAge);

print("Age & gender data extracted");

# ---------------------------------------------------------------

df_temp = pd.DataFrame(data,columns=labels);
df_temp['end_time'] = pd.to_datetime(df_temp['end_time']);

df = pd.concat([df_temp,df_old]);
df['end_time'] = pd.to_datetime(df['end_time']);
df = df.sort_values(by='end_time', ascending=False);
df = df.drop_duplicates(subset=['year','week'], keep="first");

print("All Age & gender data loaded into dataframe");

# ---------------------------------------------------------------

df.to_csv("data/ZypInstagram_Audience-Age&Gender.csv",index=False);

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

googleSheetName = "ZypInstagram_Audience-Age&Gender";
spreadsheetID = "13I_PfmAQ5DWwxY0AEsH1OMvn7wcpzfanLgiFcG2et5A";
csvFilePath = "data/ZypInstagram_Audience-Age&Gender.csv";

saveToGoogleSheets(googleSheetName, spreadsheetID, csvFilePath);