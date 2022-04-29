# %%
import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

# Access Token needs to be generated every 2 months
ACCESS_TOKEN = "<< access token >>";

# If facebook updates its Graph API Explorer, the version number should be changed as well.
VERSION = "v11.0";

URL = "https://graph.facebook.com/" + VERSION;

def req_facebook(req):
    r = requests.get(URL + req, {'access_token': ACCESS_TOKEN});
    return r;

def paginate(requestJSON):
    return requests.get(requestJSON['paging']['next']);

# %%
def retrieveScrapedURL(site):
    hdr = {'User-Agent': 'Mozilla/5.0'};
    req = Request(site,headers=hdr);
    page = urlopen(req);
    soup = BeautifulSoup(page);
    return soup;

site = "https://simplemaps.com/data/canada-cities";
soup = retrieveScrapedURL(site);
table = soup.find_all("table", class_="table table-hover comparison");
limitSoup = table[0].findAll("tr")[5].findAll("td")[2].find(text=True);
limitAdj = limitSoup.split(",");
limit = "";
for val in limitAdj:
    limit += val;

albertaJSON = req_facebook("search?type=adgeolocation&location_types=city&country_code=CA&q=alberta&limit="+limit).json();

britishColumbiaJSON = req_facebook("search?type=adgeolocation&location_types=city&country_code=CA&q=british+columbia&limit="+limit).json();

manitobaJSON = req_facebook("search?type=adgeolocation&location_types=city&country_code=CA&q=manitoba&limit="+limit).json();

newBrunswick = req_facebook("search?type=adgeolocation&location_types=city&country_code=CA&q=new+brunswick&limit="+limit).json();

newfoundlandAndLabradorJSON = req_facebook("search?type=adgeolocation&location_types=city&country_code=CA&q=newfoundland+labrador&limit="+limit).json();

northwestTerritoriesJSON = req_facebook("search?type=adgeolocation&location_types=city&country_code=CA&q=northwest+territories&limit="+limit).json();

novaScotiaJSON = req_facebook("search?type=adgeolocation&location_types=city&country_code=CA&q=nova+scotia&limit="+limit).json();

nunavutJSON = req_facebook("search?type=adgeolocation&location_types=city&country_code=CA&q=nunavut&limit="+limit).json();

ontarioJSON = req_facebook("search?type=adgeolocation&location_types=city&country_code=CA&q=ontario&limit="+limit).json();

princeEdwardIslandJSON = req_facebook("search?type=adgeolocation&location_types=city&country_code=CA&q=prince+edward+island&limit="+limit).json();

quebecJSON = req_facebook("search?type=adgeolocation&location_types=city&country_code=CA&q=quebec&limit="+limit).json();

saskatchewanJSON = req_facebook("search?type=adgeolocation&location_types=city&country_code=CA&q=saskatchewan&limit="+limit).json();

yukonJSON = req_facebook("search?type=adgeolocation&location_types=city&country_code=CA&q=yukon&limit="+limit).json();

# %%
provinceAbbreviations = ["AB","BC","MB","NB","NL","NT","NS","NU","ON","PE","QC","SK","YT"]

provinceJSON_List = [albertaJSON, britishColumbiaJSON, manitobaJSON, newBrunswick, newfoundlandAndLabradorJSON, northwestTerritoriesJSON, novaScotiaJSON, nunavutJSON, ontarioJSON, princeEdwardIslandJSON, quebecJSON, saskatchewanJSON, yukonJSON];

cities = [];
def getAllCitiesOfProvince(provinceJSON, provinceAbbreviation):
    i = 0;
    while True:
        try:
            for x in range(len(provinceJSON["data"])):
                city = provinceJSON["data"][x].get("name",0);
                cities.append(city + ", " + provinceAbbreviation + ", Canada");
            i += 1;
            provinceJSON = paginate(provinceJSON).json();
        except:
            print(provinceAbbreviation + " done");
            break;

for j in range(len(provinceJSON_List)):
    getAllCitiesOfProvince(provinceJSON_List[j], provinceAbbreviations[j])

# %%
df = pd.DataFrame(cities,columns=["City Names"])
df.head()


