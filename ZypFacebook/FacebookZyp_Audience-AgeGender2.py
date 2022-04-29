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

# --------------------------------------------------------------

df_old = pd.read_csv(r'data/ZypFacebook_Audience-Age&Gender2.csv', index_col=False);
lastMostRecentDate = df_old['end_time'][0];
sinceDate = time.mktime(datetime.datetime.strptime(lastMostRecentDate,"%Y-%m-%d").timetuple());
print("Most recent date in the imported dataset: " + str(lastMostRecentDate) + " = " + str(sinceDate));
# sinceDate = 1523948400;

# ---------------------------------------------------------------

results = req_facebook("zypgallery/insights?metric=page_impressions_by_age_gender_unique&period=day&since=" + str(sinceDate)).json();

genderAge = ['F.13-17','F.18-24','F.25-34','F.35-44','F.45-54','F.55-64','F.65+','M.13-17','M.18-24','M.25-34','M.35-44','M.45-54','M.55-64','M.65+','U.13-17','U.18-24','U.25-34','U.35-44','U.45-54','U.55-64','U.65+'];

labels = [];
labels.append("end_time");
for lbl in genderAge:
    labels.append(lbl);

def getGenderAgeValues(results,genderAge,index):
    row = [];
    dateValue = parser.parse(results['data'][0]['values'][index].get('end_time',0).split(":")[0][0:10]);
    row.append(dateValue)
    for lbl in genderAge:
        colValue = results['data'][0]['values'][index]['value'].get(lbl,0)
        row.append(colValue);
    return row;

def getGenderAgeData(results,i=0):
    data = [];
    while True:
        try:
            if(i <= len(results["data"][0]["values"])):
                data.append(getGenderAgeValues(results,genderAge,i));
                i += 1;
            else:
                results = paginate(results,"previous").json();
                i = 0;
        except:
            print("done");
            break;
    return data;

data = getGenderAgeData(results);

print("Age & gender insights data extracted");

# ---------------------------------------------------------------

df_temp = pd.DataFrame(data,columns=labels);
df_temp = df_temp.sort_values(by='end_time', ascending=False);

df = pd.concat([df_temp,df_old]);
df['end_time'] = pd.to_datetime(df['end_time']);
df = df.drop_duplicates(subset='end_time', keep="first");
df = df.sort_values(by='end_time', ascending=False);

print("All extracted age & gender insights data loaded into a dataframe");

# ---------------------------------------------------------------

df.to_csv("data/ZypFacebook_Audience-Age&Gender2.csv",index=False);

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

googleSheetName = "ZypFacebook_Audience-Age&Gender2";
spreadsheetID = "1Lwc4zcK5rXxCyC6BYnlhw1Ny2c1sfri_qtlETRUwKlc";
csvFilePath = "data/ZypFacebook_Audience-Age&Gender2.csv";

saveToGoogleSheets(googleSheetName, spreadsheetID, csvFilePath);