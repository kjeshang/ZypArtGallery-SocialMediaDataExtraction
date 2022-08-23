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

# ---------------------------------------------------------------

df_old = pd.read_csv(r'data/ZypFacebook_Insights3.csv', index_col=False);
lastMostRecentDate = df_old['end_time'][0];
sinceDate = time.mktime(datetime.datetime.strptime(lastMostRecentDate,"%Y-%m-%d").timetuple());
print("Most recent date in the imported dataset: " + str(lastMostRecentDate) + " = " + str(sinceDate));
# sinceDate = 1523948400;

# ---------------------------------------------------------------

results = req_facebook("zypgallery/insights?metric=page_fans&period=day&since=" + str(sinceDate)).json();

metrics = ["end_time","page_fans"];

def getInsightMetricValues(results,index):
    row = [];
    date = parser.parse(results["data"][0]["values"][index].get("end_time").split(":")[0][0:10]);
    row.append(date);
    colValue = results["data"][0]["values"][index].get("value",0);
    row.append(colValue);
    return row;

def getInsightsData(results,i=0):
    data = [];
    while True:
        try:
            if(i <= len(results["data"][0]["values"])):
                data.append(getInsightMetricValues(results,i));
                i += 1;
            else:
                results = paginate(results,"previous").json();
                i = 0;
        except:
            print("done");
            break;
    return data;

data = getInsightsData(results);

print("Page insights data extracted");

# ---------------------------------------------------------------

df_temp = pd.DataFrame(data,columns=metrics);
df_temp = df_temp.sort_values(by='end_time', ascending=False);

df = pd.concat([df_temp,df_old]);
df['end_time'] = pd.to_datetime(df['end_time']);
df = df.drop_duplicates(subset='end_time', keep="first");
df = df.sort_values(by='end_time', ascending=False);

print("All extracted page insights data loaded into a dataframe");

# ---------------------------------------------------------------

df.to_csv("data/ZypFacebook_Insights3.csv",index=False);

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

googleSheetName = "ZypFacebook_Insights3";
spreadsheetID = "1GL_oPi0nrwV8FE9dBVtRF8GzWkG6avoMtOUmGxfTfU4";
csvFilePath = "data/ZypFacebook_Insights3.csv";

saveToGoogleSheets(googleSheetName, spreadsheetID, csvFilePath);