# ZypArtGallery-SocialMediaDataExtraction

## Description

This project repository contains a collection of scripts and related files that were used to extract unaggregated social media data of Zyp Art Gallery's Facebook & Instagram profiles from Facebook Graph API. The purpose of this project was to assist Zyp Art Gallery to extract social media data that was previously available to download directly as CSV files on Facebook and Instagram webpages. In the context of Facebook, the company decided to remove the feature for Facebook page creators & contributors to download unaggregated data, and replaced that feature with the _Facebook for Business_ page which provided concise yet limited data but was already aggregated, which in turn, hindered the organization to derive accurate social media insights. Deriving accurate social media insights is important as it helps Zyp Art Gallery to make optimal business decisions for the purpose of planning community endeavors, charity events, volunteer programs, and showcase art to give a voice to the voiceless. This can then help contribute to receiving donations and other forms of monetary support to help maintain the financial longevity of Zyp Art Gallery. Thus, the social media data extraction performed using the scripts in this repository greatly assisted Zyp Art Gallery to maintain access to unaggreated data, and create detailed & accurate PowerBI and Google Data Studio dashboards to help derive social media insights. For further context, the social media data extraction scripts were executed on a weekly basis.

The scripts were created using the **Python** programming language with the help of the **_Pandas_**, **_Time_**, **_Datetime_**, **_Requests_**, and **_Gspread_** packages, along with the incorporation of **Facebook Graph API**, **Google Drive API**, and **Google Sheets API**. The extracted, transformed, and cleaned data would be saved in both CSV files whereby the content is updated to combine the past data with the most curren week's data each time the Python scripts are run. This makes sure that the social media data is up-to-date. Then the contents of the CSV files is programmatically copied and pasted into pre-specified Google Sheets files on the organization's Google Drive. The other necessary requirements to utilize these scripts are the following:
* A **Facebook Account** that is added to the Zyp Art Gallery Facebook Page as a role type/contributor. The Facebook Account could be a personal one, or a new one preferably created using the organization email.
* A **Facebook for Developers** Account that is accessed using the Facebook Account and the email address associated with the respective Facebook Account.
* The **Facebook Graph API Access Token** which serves as an authentication key to make API requests to retrieve Facebook & Instagram data. Without the Access Token, one would not be able to make API requests to retrieve social media data.
* A **Google Services Account** that is created using the organization email account and the Google Cloud Console. With the Google Services Account, one will be able to access the Google Drive and Google Sheets API. The Google Services Account is also utilized in actual codebase, and it takes the form of a Gmail address.
* The **Google Services Account Private Key** which authenticates the user to take the contents of the social media data within the CSV files and paste it in the appropriate Google Sheets files so that other members of the organization can access it. Without the Private Key, one would not be able to programmatically save the social media data on the organization Google Drive.
* The **Name of the Zyp Art Gallery Facebook Page** and the **Media ID of the Zyp Art Gallery Instagram Page** are necessary to tell the API request conduction by Python code which social media page to retrieve data from.

Microsoft Visual Studio Code (VS Code) was the IDE used to construct the Python scripts. The Python version used was 3.10.1.

There are three sub-categories of Facebook & Instagram data that is retrieved from Facebook Graph API.

|Data|Explanation|
|--|--|
|Posts|Data describing the performance of the Social Media Account's posts.|
|Page|Data describing the performance of the Social Media Account's page.|
|Audience|Data describing the performance of Social Media Account in terms of Age & Gender, Country, Canadian City, and Time of Day.|

## Important Note

This GitHub repository was created for the purpose of viewing the codebase and documentation. However, the social media data files, Facebook Graph API Access Token, Google Service Account Address, and Google Services Account Private Key are not provided in this repository to protect the privacy of the Zyp Art Gallery organization and the followers of the organization's social media accounts.

## How the Project works
> This section explains in detail what was explained in the Description section. In addition, explains the flow of data in terms of extraction, transformation, and loading, which is performed by the Python scripts.

### Environment Setup
As explained in the prior section, the social media data itself was extracted using Python programming with the help of Facebook Graph API. In order to make requests to Facebook Graph API, I needed to have a Facebook account and have a page role in the organization’s Facebook page. I ended up making a Facebook account using my organization email. After creating a Facebook account, the executive director then assigned my Facebook profile to have a page role on the organization’s Facebook page. I was then able to create a ‘Facebook for Developers’ account. I then had to create an ‘app’ on Facebook for Developers, and then state the purpose of it which was simply to make requests. To gain full access to information provided by various metrics, I had to provide Zyp Art Gallery’s privacy policy for approval before gaining full access.

Even though Facebook for Developers allows for making requests within the Graph Explorer, the drawback was that some request output was too long thus pagination would occur. In other words, the entire output would not be accessible within the explorer without further manipulation. This is further exemplified by the fact that the data output is in JSON format. Thus, making the API request with the help of Python programming was easier because I could code a loop that would paginate through the JSON output. In order to make requests to Graph API via a Python script, I needed to have an access token. Although, an access token is required overall to make requests to Graph API. Within Graph Explorer, an access token is provided by default but it is only valid for approximately two hours. Thus, using a short-lived access token is not ideal when running social media data extraction code on a weekly basis. And so, I extended the access token to last approximately two months. Unfortunately, Facebook for Developers do not provide lifelong access tokens. Thus, after the current token expires, I generate a new token and extend its lifetime. An access token with a longer lifetime was more ideal for me to create the social media data extraction code. This makes the act of running the social media data extraction code easily executable on a weekly basis as I not have to keep on generating a new access token via the Graph Explorer. I only need to generate an access token with an extended lifetime every so often.

The organization utlilzes Google Drive as the primary office suite and data storage space at this current time. During the early days after I completed creating social media data extraction scripts for posts, page, & demographic insights, my final output would be a collection of data files in ‘CSV’ format. I used to manually upload them to a folder on the organization’s Google Drive. This used to be quite a tedious task. Thus, I decided to create a Google Service Account via the Google Cloud console. I then added the Google Drive and Google Sheets API. I then was able to acquire a private service account key which allows me to interact with Google Drive & Google Sheets. The next step was to create a dedicated Google Sheets file with a singular sheet that corresponds with the name of the data files in ‘CSV’ file format. The name of the Google Sheets file, sheet name, and identification value of the Google Sheets file (which is found in the URL), are utilized with the Google service account private key to take the contents of the data files in ‘CSV’ file format, and paste it into the respective Google Sheets files. The Python package called ‘gspread’ is imperative to auto-inserting the data to Google Sheets files.

### How the Project Runs
As aforementioned, the social media data extraction code was created using Python. It was coded using VS Code. There are multiple scripts that are dedicated to extracting different types of metrics, yet they all follow a similar process with slight variations in terms of data cleaning & transformation. In practice, there is another Python script that runs all of the other extraction code scripts all at once. In essence, the Python scripts I wrote go through the following stages.

1. Setup
    * Import the following packages: requests, pandas, time, datetime, dateutil, gspread.
    * Create function to make request to Facebook Graph API.
    * Create function that paginates through API request output if all output is not visible at once.
    * Instantiate variables for API version and request URL.
    * Retrieve current long-lived access token from text file.
2. Import Data
    * a. Retrieve social media data file which is in CSV format. The file consists of data that is until the last time the extraction code was run which is typically the week prior. It would take the form of a pandas dataframe.
    * As there is a date column in the data file, the script takes the most recent date in the column (which is in the first row), and then instantiates as a variable to be used for the request made in the forthcoming stage.
    * The recent date is then converted from datetime format into unix time format.
3. Extraction
    * Using the API request function along with the request URL & API version variables, and the variable holding the recent date, a request is made to Facebook Graph API to retrieve data of the specified metrics in the request. The output is instantiated to a variable and is of a JSON structure.
    * Create column heading labels that would be used for the dataframe for the eventual dataframe.
    * Create function that is able to extract the date and metric values from a JSON object and appends to a list. There is a nested JSON object per date.
    * Create function that applies the aforementioned function throughout the request output per nested JSON object in the form of a loop.
    * Instantiate the aforementioned function to variable that would be used as the basis to create a dataframe of the newly extracted data.
4. Transformation
    * The newly extracted data and column labels (created in the prior stage) are used to create a dataframe. The dataframe rows would be in descending order by date (i.e., the most latest date to earliest date).
    * The dataframes of the imported data and newly extracted data are then combined together.
    * Some data cleaning is performed to the combined dataframe such as dropping duplicates.
5. Loading
    * The combined dataframe is then saved as a CSV file. In turn, overwriting the earlier imported social media data file.
    * Then, the newly saved social media data file’s contents are saved to the corresponding Google Sheets file on the organization’s Google Drive. Specifically, the existing data in the Google Sheets file is deleted, and then the data in the CSV file are then copied and pasted in the Google Sheets file. This is accomplished through a function that takes parameters consisting of Google Sheets file name, sheet name, and spreadsheet ID, along with authentication via the Google service account private key.

## Credits
> The References section

Despite working on this project independently, I referred to many online resources to craft the social media data extraction code, and update it reasonable increments over a period of time. Below is a list of resources that were imperative to setting up an environment to retrieve social media data of the organization’s Facebook and Instagram pages.
*  Setting up Facebook for Developers and working with Graph Explorer
    * [Lesson-01 :Introduction & Understanding Graph API - Facebook Data Analysis with Python](https://www.youtube.com/watch?v=LmhjVT9gIwk&list=PLhpgLgFy42uVqkUa_5P0HZIg0dwbVm96D&index=2) - Nour Galaby (YouTube)
    * [Using Facebook's Graph API Explorer to retrieve Insights data](https://www.klipfolio.com/blog/facebook-graph-api-explorer) - Jonathan Taylor (Klipfolio)
*  Facebook Graph API access tokens
    * [Facebook access token - Error validating access token: Session has expired](https://www.igorkromin.net/index.php/2020/10/02/facebook-access-token-error-validating-access-token-session-has-expired/) - Igor Kromin
    * [How To Get Facebook Long-Lived User Access Token?](https://www.sociablekit.com/get-facebook-long-lived-user-access-token/) - Mike (SociableKIT)
* Wrangling data from Facebook Graph API
    * [Python in Digital Analytics: Automating Facebook metric reports](https://bubbletao.com/2017/05/31/python-in-digital-analytics-automating-facebook-metric-reports/) - Tom Tao (BubbleTao)
* Metrics
    * [Field list for Facebook Insights](https://supermetrics.com/api/getFields?ds=FB&amp;fieldType=met) - _Supermetrics_
    * [Page Insights](https://developers.facebook.com/docs/graph-api/reference/v11.0/insights#post_impressions) - _Meta for Developers_
    * [&quot;name&quot;:&quot;page_fans_country&quot,,](https://prezi.com/acd742tobfjg/quotnamequot-quotpage_fans_countryquot/) - Milan Lepík (Prezi)
    * [IG Media Insights](https://developers.facebook.com/docs/instagram-api/reference/ig-media/insights/) - _Meta for Developers_
* Requests to Facebook Graph API and Python
    * [Difference in Engaged Users (Facebook page) and Engaged Users (Insights API)](https://stackoverflow.com/questions/37419788/difference-in-engaged-users-facebook-page-and-engaged-users-insights-api) - _StackOverflow_
    * [Get Post Insights for multiple posts in one call using Graph Api 2.7](https://stackoverflow.com/questions/38924707/get-post-insights-for-multiple-posts-in-one-call-using-graph-api-2-7/39104504) - _StackOverflow_
    * [Facebook Page insights API to retrieve different insight metrics using python](https://stackoverflow.com/questions/44491319/facebook-page-insights-api-to-retrieve-different-insight-metrics-using-python) - _StackOverflow_
    * [Get Post Insights for multiple posts in one call using Graph Api 2.7](https://stackoverflow.com/questions/38924707/get-post-insights-for-multiple-posts-in-one-call-using-graph-api-2-7) - _StackOverflow_
    * [List of countries and cities to be used in Facebook Graph API for targeting](https://stackoverflow.com/questions/7227498/list-of-countries-and-cities-to-be-used-in-facebook-graph-api-for-targeting) - _StackOverflow_
* The full analysis process
    * [Analyse your Personal Facebook Data with Python](https://medium.com/analytics-vidhya/analyse-your-personal-facebook-data-with-python-5d877e556692) - Emy Adigun (Medium)
    * [Facebook Data Analysis with Python](https://www.youtube.com/playlist?list=PLhpgLgFy42uVqkUa_5P0HZIg0dwbVm96D) - Nour Galaby (YouTube)
* Setting up Google service account via Google Cloud Console to use Python and Google Sheets
    * [Python Google Sheets API Tutorial - 2019](https://www.youtube.com/watch?v=cnPlKLEGR7E&amp;list=LL&amp;index=11) - Tech with Tim (YouTube)
    * [How to Use Google Sheets With Python (2022)](https://www.youtube.com/watch?v=bu5wXjz2KvU) - Pretty Printed (YouTube)
    * [Export Pandas DataFrame To Google Sheet in Python (Google Sheets API Tutorial)](https://www.youtube.com/watch?v=TNloGW8NzrY) - Jie Jenn (YouTube)
    * [Introduction to gspread_pandas](https://www.youtube.com/watch?v=2yIcNYzfzPw) - Diego Fernandez (YouTube)
    * [From CSV to Google Sheet Using Python](https://medium.com/craftsmenltd/from-csv-to-google-sheet-using-python-ef097cb014f9) - Md. Nahidur Rahman (YouTube)
* Specific ways to interact with Google Sheets using Python & gspread package
    * [Google Spreadsheets Python API v4](https://github.com/burnash/gspread) - burnash (GitHub)
    * [Examples of gspread Usage](https://docs.gspread.org/en/latest/user-guide.html#updating-cells) - _gspread_
    * [YouTube Video Code](https://github.com/PrettyPrinted/youtube_video_code/tree/master/2021/10/14/How%20to%20Use%20Google%20Sheets%20With%20Python%20(2021)) - PrettyPrinted (GitHub)
    * [How to read Google Sheets data in Pandas with GSpread](https://practicaldatascience.co.uk/data-science/how-to-read-google-sheets-data-in-pandas-with-gspread) - Matt Clarke (Practical Data Science)
    * [gspread-pandas Documentation - _Release 3.2.2_](https://readthedocs.org/projects/gspread-pandas/downloads/pdf/latest/) - Diego Fernandez (gspread)
