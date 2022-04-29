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

df_old = pd.read_csv(r'data/ZypInstagram_Insights2.csv', index_col=False);
lastMostRecentDate = df_old['end_time'][0];
sinceDate = time.mktime(datetime.datetime.strptime(lastMostRecentDate,"%Y-%m-%d").timetuple());
print("Most recent date in the imported dataset: " + str(lastMostRecentDate) + " = " + str(sinceDate));

# ---------------------------------------------------------------

INSIGHT = "follower_count";

results = req_facebook("insights?metric="+INSIGHT+"&period=day&since="+str(sinceDate-172800)).json();

labels = ["end_time",INSIGHT];

def getInsightMetricValues(results,index):
    date = parser.parse(results["data"][0]["values"][index].get("end_time").split(":")[0][0:10]);
    insightValue = results["data"][0]["values"][index].get("value",0);
    return [date, insightValue];

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

print("Insights data extracted");

# ---------------------------------------------------------------

df_temp = pd.DataFrame(data,columns=labels);
df_temp['end_time'] = pd.to_datetime(df_temp['end_time']);
df_temp = df_temp.sort_values(by='end_time', ascending=False);

df = pd.concat([df_temp,df_old]);
df['end_time'] = pd.to_datetime(df['end_time']);
df = df.drop_duplicates(subset='end_time', keep="first");
df = df.sort_values(by='end_time', ascending=False);

print("All extracted insights data loaded into dataframe");

# ---------------------------------------------------------------

df.to_csv("data/ZypInstagram_Insights2.csv",index=False);

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

googleSheetName = "ZypInstagram_Insights2";
spreadsheetID = "1vpKPzH8D0blZArJbCkBQnOd4slO-Yj0FYS_yMjFyClo";
csvFilePath = "data/ZypInstagram_Insights2.csv";

saveToGoogleSheets(googleSheetName, spreadsheetID, csvFilePath);