import os

print("\nZYP ART GALLERY INSTAGRAM DATA EXTRACTION\n");

# --------------------------------------------------------

# Posts

print("*** Zyp Art Gallery posts data ***");
os.system("python InstagramZyp_Posts.py");
print("Zyp Art Gallery posts data extracted!\n");

# Page Insights

print("*** Zyp Art Gallery insights 1 data ***")
os.system("python InstagramZyp_Insights1.py");
print("Zyp Art Gallery insights data 2 extracted!\n");

print("*** Zyp Art Gallery insights 2 data ***")
os.system("python InstagramZyp_Insights2.py");
print("Zyp Art Gallery insights data 2 extracted!\n");

# Audience Insights

print("*** Zyp Art Gallery Age & Gender data ***")
os.system("python InstagramZyp_Audience-AgeGender.py");
print("Zyp Art Gallery Age & Gender data extracted!\n");

print("*** Zyp Art Gallery Canadian City data ***")
os.system("python InstagramZyp_Audience-CanadianCity.py");
print("Zyp Art Gallery Canadian City data extracted!\n");

print("*** Zyp Art Gallery Country data ***")
os.system("python InstagramZyp_Audience-Country.py");
print("Zyp Art Gallery Country data extracted!\n");

print("*** Zyp Art Gallery Time of Day data ***")
os.system("python InstagramZyp_Audience-TimeOfDay.py");
print("Zyp Art Gallery Time of Day data extracted!\n");

# --------------------------------------------------------

print("ZYP ART GALLERY INSTAGRAM DATA EXTRACTION COMPLETE!\n");