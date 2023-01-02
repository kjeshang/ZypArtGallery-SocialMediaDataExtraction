# ZypArtGallery-SocialMediaDataExtraction

## Description

This project repository contains a collection of scripts and related files that were used to extract unaggregated social media data of Zyp Art Gallery's Facebook & Instagram profiles from Facebook Graph API. The purpose of this project was to assist Zyp Art Gallery to extract social media data that was previously available to download directly as CSV files on Facebook and Instagram webpages. In the context of Facebook, the company decided to remove the feature for Facebook page creators & contributors to download unaggregated data, and replaced that feature with the _Facebook for Business_ page which provided concise yet limited data but was already aggregated, which in turn, hindered the organization to derive accurate social media insights. Deriving accurate social media insights is important as it helps Zyp Art Gallery to make optimal business decisions for the purpose of planning community endeavors, charity events, volunteer programs, and showcase art to give a voice to the voiceless. This can then help contribute to receiving donations and other forms of monetary support to help maintain the financial longevity of Zyp Art Gallery. Thus, the social media data extraction performed using the scripts in this repository greatly assisted Zyp Art Gallery to maintain access to unaggreated data, and create detailed & accurate PowerBI and Google Data Studio dashboards to help derive social media insights. For further context, the social media data extraction scripts were executed on a weekly basis.

The scripts were created using the **Python** programming language with the help of the **_Pandas_**, **_Time_**, **_Datetime_**, **_Requests_**, and **_Gspread_** packages, along with the incorporation of **Facebook Graph API**, **Google Drive API**, and **Google Sheets API**. The extracted, transformed, and cleaned data would be saved in both CSV files whereby the content is updated to combine the past data with the most curren week's data each time the Python scripts are run. This makes sure that the social media data is up-to-date. Then the contents of the CSV files is programmatically copied and pasted into pre-specified Google Sheets files on the organization's Google Drive. The other necessary requirements to utilize these scripts are the following:
* A **Facebook Account** that is added to the Zyp Art Gallery Facebook Page as a role type/contributor. The Facebook Account could be a personal one, or a new one preferably created using the organization email.
* A **Facebook for Developers** Account that is accessed using the Facebook Account and the email address associated with the respective Facebook Account.
* The **Facebook Graph API Access Token** which serves as an authentication key to make API requests to retrieve Facebook & Instagram data. Without the Access Token, one would not be able to make API requests to retrieve social media data.
* A **Google Services Account** that is created using the organization email account and the Google Cloud Console. With the Google Services Account, one will be able to access the Google Drive and Google Sheets API. The Google Services Account is also utilized in actual codebase, and it takes the form of a Gmail address.
* The **Google Services Account Private Key** which authenticates the user to take the contents of the social media data within the CSV files and paste it in the appropriate Google Sheets files so that other members of the organization can access it. Without the Private Key, one would not be able to programmatically save the social media data on the organization Google Drive.

Microsoft Visual Studio Code was the IDE used to construct the Python scripts. The Python version used was 3.10.1.

There are three sub-categories of Facebook & Instagram data that is retrieved from Facebook Graph API.

|Data|Explanation|
|--|--|
|Posts|Data describing the performance of the Social Media Account's posts.|
|Page|Data describing the performance of the Social Media Account's page.|
|Audience|Data describing the performance of Social Media Account in terms of Age & Gender, Country, Canadian City, and Time of Day.|

## Important Note

This GitHub repository was created for the purpose of viewing the codebase and documentation. However, the social media data files, Facebook Graph API Access Token, Google Service Account Address, and Google Services Account Private Key are not provided in this repository to protect the privacy of the Zyp Art Gallery organization and the followers of the organization's social media accounts.

## Environment Setup



## How the Data Extraction, Transformation, and Loading takes place




