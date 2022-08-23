# %%
import pandas as pd

geo_df = pd.read_csv("GeoNamesData.csv", index_col=False);
city_df = pd.read_csv("CanadianCities-Adjusted.csv", index_col=False);

# %%
geo_dfNew = geo_df[["Geographical Name","Generic Term","Province - Territory"]]
geo_dfNew[0:1]

# %%
city_df[0:1]

# %%
data = [];
for i in geo_dfNew.index:
    for j in city_df.index:
        if geo_dfNew.loc[i, "Geographical Name"] == city_df.loc[j, "City"].split(", ")[0]:
            row = [city_df.loc[j, "City"], geo_dfNew.loc[i, "Province - Territory"]];
            data.append(row);
city_dfNew = pd.DataFrame(data, columns=["City","Province"]);
city_dfNew.head()

# %%
len(city_df)

# %%
len(city_dfNew)

# %%
city_dfNew.to_csv("CanadianCitiesFiltered.csv", index=False);


