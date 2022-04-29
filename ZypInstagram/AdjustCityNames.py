# %%
# https://www150.statcan.gc.ca/n1/pub/92-195-x/2011001/geo/prov/tbl/tbl8-eng.htm
import pandas as pd

# %%
df = pd.read_csv(r'CanadianCities.csv');
df.head()

# %%
# print(df.loc[4,"City Names"])
# print(df.loc[4,"City Names"][0:-12])
# print(df.loc[4,"City Names"][0:-8])
# df.loc[4,"City Names"][0:-8].split(", ")[-1]

data = [];
for i in range(len(df)):
    row = [];
    fullCityName = df.loc[i,"City Names"][0:-8].split(", ");
    city = df.loc[i,"City Names"][0:-12];
    row.append(city);
    province = fullCityName[-1];
    if province == "NL":
        row.append("Newfoundland and Labrador");
    elif province == "PE":
        row.append("Prince Edward Island");
    elif province == "NS":
        row.append("Nova Scotia");
    elif province == "NB":
        row.append("New Brunswick");
    elif province == "QC":
        row.append("Quebec");
    elif province == "ON":
        row.append("Ontario");
    elif province == "MB":
        row.append("Manitoba");
    elif province == "SK":
        row.append("Saskatchewan");
    elif province == "AB":
        row.append("Alberta");
    elif province == "BC":
        row.append("British Columbia");
    elif province == "YT":
        row.append("Yukon");
    elif province == "NT":
        row.append("Northwest Territories");
    elif province == "NU":
        row.append("Nunavut");
    data.append(row);
    

# %%
df_new = pd.DataFrame(data, columns=["City","Province"])
df_new.to_csv(r'CanadianCities-Adjusted.csv', index=False)


