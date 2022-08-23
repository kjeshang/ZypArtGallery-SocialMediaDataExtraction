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

df_old = pd.read_csv(r'data/ZypInstagram_Insights1.csv', index_col=False);
lastMostRecentDate = df_old['end_time'][0];
sinceDate = time.mktime(datetime.datetime.strptime(lastMostRecentDate,"%Y-%m-%d").timetuple());
print("Most recent date in the imported dataset: " + str(lastMostRecentDate) + " = " + str(sinceDate));

# ---------------------------------------------------------------

INSIGHT = "impressions,reach,email_contacts,phone_call_clicks,text_message_clicks,get_directions_clicks,website_clicks,profile_views";

results = req_facebook("insights?metric="+INSIGHT+"&period=day&since="+str(sinceDate-172800)).json();
# results = req_facebook("insights?metric="+INSIGHT+"&period=day").json();

metrics = INSIGHT.split(",");

labels = [];
labels.append("end_time");
for item in metrics:
    labels.append(item);

def getInsightMetricValues(results,index):
    row = [];
    date = parser.parse(results["data"][0]["values"][index].get("end_time").split(":")[0][0:10]);
    row.append(date);
    for i in range(len(results["data"])):
        value = results["data"][i]["values"][index].get("value",0);
        row.append(value);
    return row;

def getHistoricalInsightsData(results):
    data = [];
    while True:
        try:
            data.append(getInsightMetricValues(results,1));
            data.append(getInsightMetricValues(results,0));
            results = paginate(results,"previous").json();
        except:
            print("done");
            break;
    return data;

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
# data = getHistoricalInsightsData(results);

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

df.to_csv("data/ZypInstagram_Insights1.csv",index=False);

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

googleSheetName = "ZypInstagram_Insights1";
spreadsheetID = "1_K3nL_F7TZBhEF4FbGZNPu9WVDIISgeR8flw2ZKtDJg";
csvFilePath = "data/ZypInstagram_Insights1.csv";

saveToGoogleSheets(googleSheetName, spreadsheetID, csvFilePath);