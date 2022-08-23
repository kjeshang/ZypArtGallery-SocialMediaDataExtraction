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

# -----------------------------------------------------------------

df_old = pd.read_csv(r'data/ZypFacebook_Posts.csv', index_col=False);
lastMostRecentDate = df_old['date'][0];
sinceDate = time.mktime(datetime.datetime.strptime(lastMostRecentDate,"%Y-%m-%d").timetuple());
print("Most recent date in the imported dataset: " + str(lastMostRecentDate) + " = " + str(sinceDate));
# sinceDate = 1523948400;

# -----------------------------------------------------------------

results_posts = req_facebook("zypgallery/feed?fields=id,message,created_time&since="+str(sinceDate)).json();

metrics = ["id","message","created_time"];
def getPostMetricValues(results,metrics,index):
    row = [];
    for metric in metrics:
        row.append(results["data"][index].get(metric));
    return row;

def getPostsData(results,i=0):
    data = [];
    while True:
        try:
            if(i < len(results["data"])):
                data.append(getPostMetricValues(results,metrics,i));
                i += 1;
            else:
                results = paginate(results,"next").json();
                i = 0;
        except:
            print("done");
            break;
    return data;

data = getPostsData(results_posts);

print("Posts data extracted");

# -----------------------------------------------------------------

df_posts = pd.DataFrame(data,columns=metrics);

df_posts['date'] = df_posts['created_time'];
df_posts['time'] = df_posts['created_time'];
df_posts['post'] = df_posts['message'];
for index in df_posts.index:
    df_posts.loc[index,'date'] = df_posts.loc[index,'created_time'].split("T")[0];
    df_posts.loc[index,'time'] = df_posts.loc[index,'created_time'].split("T")[1].split("+")[0];
    df_posts.loc[index,'post'] = str(df_posts.loc[index,'message'])[0:20];

# -----------------------------------------------------------------

def getPostInsightValues(postID):
    row = [];
    
    # PAGE POST ENGAGEMENT

    # Engagement Metric 1:
    results = req_facebook(str(postID)+"/insights?metric=post_engaged_users,post_negative_feedback,post_negative_feedback_unique,post_engaged_fan,post_clicks,post_clicks_unique").json();
    try:
        for j in range(len(results["data"])):
            row.append(results["data"][j]["values"][0].get("value",0));
    except KeyError:
        for j in range(0,6):
            row.append(0);

    # Engagmenet Metric 2:
    results = req_facebook(str(postID)+"/insights?metric=post_clicks_by_type,post_clicks_by_type_unique").json();
    try:
        for j in range(len(results["data"])):
            valueType = ["other clicks","photo view","link clicks"];
            for type in valueType:
                row.append(results["data"][j]["values"][0].get("value").get(type,0));
    except KeyError:
        for j in range(0,6):
            row.append(0);
    
    # Engagement Metric 3:
    results = req_facebook(str(postID)+"/insights?metric=post_activity_by_action_type").json();
    try:
        for j in range(len(results["data"])):
            valueType = ["share","like","comment"];
            for type in valueType:
                row.append(results["data"][j]["values"][0].get("value").get(type,0));
    except KeyError:
        for j in range(0,3):
            row.append(0);

    # PAGE POST IMPRESSIONS

    # Impressions Metric 1:
    results = req_facebook(str(postID)+"/insights?metric=post_impressions,post_impressions_unique,post_impressions_paid,post_impressions_paid_unique,post_impressions_fan,post_impressions_fan_unique,post_impressions_fan_paid,post_impressions_fan_paid_unique,post_impressions_organic,post_impressions_organic_unique,post_impressions_viral,post_impressions_viral_unique,post_impressions_nonviral,post_impressions_nonviral_unique").json();
    try:
        for j in range(len(results["data"])):
            row.append(results["data"][j]["values"][0].get("value",0));
    except KeyError:
        for j in range(0,14):
            row.append(0);

    # Impressions Metric 2:
    results = req_facebook(str(postID)+"/insights?metric=post_impressions_by_story_type,post_impressions_by_story_type_unique").json();
    try:
        for j in range(len(results["data"])):
            row.append(results["data"][j]["values"][0].get("value").get("other",0));
    except KeyError:
        for j in range(0,2):
            row.append(0);
    
    # PAGE POST REACTIONS

    # Reactions Metric:
    results = req_facebook(str(postID)+"/insights?metric=post_reactions_like_total,post_reactions_love_total,post_reactions_wow_total,post_reactions_haha_total,post_reactions_sorry_total,post_reactions_anger_total").json();
    try:
        for j in range(len(results["data"])):
            row.append(results["data"][j]["values"][0].get("value",0));
    except KeyError:
        for j in range(0,6):
            row.append(0);
    
    return row;

def getPostInsightsData(df_posts):
    data_posts_insights = [];
    for index in df_posts.index:
        row = getPostInsightValues(df_posts.loc[index,"id"]);
        data_posts_insights.append(row);
    return data_posts_insights;

data_posts_insights = getPostInsightsData(df_posts);

print("Posts insights data extracted");

# -----------------------------------------------------------------

labels = [
    # PAGE POST ENGAGEMENTS
    "post_engaged_users",
    "post_negative_feedback",
    "post_negative_feedback_unique",
    "post_engaged_fan",
    "post_clicks",
    "post_clicks_unique",
    "post_clicks_by_type - other clicks",
    "post_clicks_by_type - photo view",
    "post_clicks_by_type - link clicks",
    "post_clicks_by_type_unique - other clicks",
    "post_clicks_by_type_unique - photo view",
    "post_clicks_by_type_unique - link clicks",
    "post_activity_by_action_type - share",
    "post_activity_by_action_type - like",
    "post_activity_by_action_type - comment",
    # PAGE POST IMPRESSIONS
    "post_impressions",
    "post_impressions_unique",
    "post_impressions_paid",
    "post_impressions_paid_unique",
    "post_impressions_fan",
    "post_impressions_fan_unique",
    "post_impressions_fan_paid",
    "post_impressions_fan_paid_unique",
    "post_impressions_organic",
    "post_impressions_organic_unique",
    "post_impressions_viral",
    "post_impressions_viral_unique",
    "post_impressions_nonviral",
    "post_impressions_nonviral_unique",
    "post_impressions_by_story_type",
    "post_impressions_by_story_type_unique",
    # PAGE POST REACTIONS
    "post_reactions_like_total",
    "post_reactions_love_total",
    "post_reactions_wow_total",
    "post_reactions_haha_total",
    "post_reactions_sorry_total",
    "post_reactions_anger_total"
];

df_posts_insights = pd.DataFrame(data_posts_insights,columns=labels);

# -----------------------------------------------------------------

df = pd.concat([df_posts,df_posts_insights],axis=1);

df = pd.concat([df,df_old]);
df = df.drop_duplicates(subset='id', keep="first");

print("All extracted posts-related data loaded into a dataframe");

# -----------------------------------------------------------------

df.to_csv("data/ZypFacebook_Posts.csv",index=False);

print("Dataframe loaded as CSV");

# -----------------------------------------------------------------

def saveToGoogleSheets(googleSheetName, spreadsheetID, csvFilePath):
    sa = gspread.service_account(filename="zyp-art-gallery-62e00b2be4ff.json");
    sh = sa.open(googleSheetName);
    wks = sh.worksheet(googleSheetName);
    wks.clear();
    content = open(csvFilePath, 'r', encoding="Latin-1").read();
    sa.import_csv(spreadsheetID, content);
    print("Dataframe loaded to Google Sheets");

googleSheetName = "ZypFacebook_Posts";
spreadsheetID = "1tImuEz2IauWtc6kfzbduKitMZwE8vNeruvD25BzGxuI";
csvFilePath = "data/ZypFacebook_Posts.csv";

saveToGoogleSheets(googleSheetName, spreadsheetID, csvFilePath);