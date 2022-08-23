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

FIELDS = "timestamp,id,caption,media_url,comments_count,like_count,media_product_type,media_type";

results = req_facebook("media?fields="+FIELDS).json();

metrics = FIELDS.split(",");

labels = [];
for item in metrics:
    labels.append(item);
for item in ["datetime","date","time","shortened_caption"]:
    labels.append(item);

def getPostMetricValues(results,metrics,index):
    row = [];
    for item in metrics:
        row.append(results["data"][index].get(item));
    date_str = results["data"][index].get("timestamp").split(":")[0][0:10];
    time_str = results["data"][index].get("timestamp").split("T")[1].split("+")[0];
    dateTime = datetime.datetime.strptime(date_str + " " + time_str, '%Y-%m-%d %H:%M:%S');
    row.append(dateTime);
    date = datetime.datetime.strptime(date_str, "%Y-%m-%d");
    row.append(date);
    time = str(datetime.datetime.strptime(time_str, "%H:%M:%S")).split(" ")[1];
    row.append(time);
    shortedCaption = results["data"][index].get("caption")[0:20];
    row.append(shortedCaption);
    return row;

def getPostsData(results,i=0):
    data = [];
    while True:
        try:
            if(i <= len(results["data"])):
                data.append(getPostMetricValues(results,metrics,i));
                i += 1;
            else:
                results = paginate(results,"next").json();
                i = 0;
        except:
            print("done");
            break;
    return data;

data = getPostsData(results);

print("Posts data extracted");

# ---------------------------------------------------------------

df = pd.DataFrame(data,columns=labels);
df = df.sort_values(by='datetime', ascending=False);

print("All extracted posts data loaded into dataframe");

# ---------------------------------------------------------------

df.to_csv("data/ZypInstagram_Posts.csv",index=False);

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

googleSheetName = "ZypInstagram_Posts";
spreadsheetID = "1x1x4Mbz0LrKz_o_h-Nq37O4NJGAMjstB7I2ZLaMiPUg";
csvFilePath = "data/ZypInstagram_Posts.csv";

saveToGoogleSheets(googleSheetName, spreadsheetID, csvFilePath);