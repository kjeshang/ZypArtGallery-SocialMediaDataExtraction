import os

print("\nZYP ART GALLERY FACEBOOK DATA EXTRACTION\n");

# --------------------------------------------------------

# Posts

print("*** Zyp Art Gallery posts data ***");
os.system("python FacebookZyp_Posts.py");
print("Zyp Art Gallery posts data extracted!\n");

# Page Insights

print("*** Zyp Art Gallery insights 1 data ***")
os.system("python FacebookZyp_Insights1.py");
print("Zyp Art Gallery insights data 2 extracted!\n");

print("*** Zyp Art Gallery insights 2 data ***")
os.system("python FacebookZyp_Insights2.py");
print("Zyp Art Gallery insights data 2 extracted!\n");

print("*** Zyp Art Gallery insights 3 data ***")
os.system("python FacebookZyp_Insights3.py");
print("Zyp Art Gallery insights data 3 extracted!\n");

# Audience Insights

print("*** Zyp Art Gallery Age & Gender 1 data ***")
os.system("python FacebookZyp_Audience-AgeGender1.py");
print("Zyp Art Gallery Age & Gender 1 data extracted!\n");

print("*** Zyp Art Gallery Age & Gender 2 data ***")
os.system("python FacebookZyp_Audience-AgeGender2.py");
print("Zyp Art Gallery Age & Gender 2 data extracted!\n");

print("*** Zyp Art Gallery Canadian City 1 data ***")
os.system("python FacebookZyp_Audience-CanadianCity1.py");
print("Zyp Art Gallery Canadian City 1 data extracted!\n");

print("*** Zyp Art Gallery Canadian City 1 Filtered data ***")
os.system("python FacebookZyp_Audience-CanadianCity1-Filtered.py");
print("Zyp Art Gallery Canadian City 1 Filtered data extracted!\n");

print("*** Zyp Art Gallery Canadian City 2 data ***")
os.system("python FacebookZyp_Audience-CanadianCity2.py");
print("Zyp Art Gallery Canadian City 2 data extracted!\n");

print("*** Zyp Art Gallery Canadian City 2 Filtered data ***")
os.system("python FacebookZyp_Audience-CanadianCity2-Filtered.py");
print("Zyp Art Gallery Canadian City 2 Filtered data extracted!\n");

print("*** Zyp Art Gallery Country 1 data ***")
os.system("python FacebookZyp_Audience-Country1.py");
print("Zyp Art Gallery Country 1 data extracted!\n");

print("*** Zyp Art Gallery Country 2 data ***")
os.system("python FacebookZyp_Audience-Country2.py");
print("Zyp Art Gallery Country 2 data extracted!\n");

print("*** Zyp Art Gallery Time of Day data ***")
os.system("python FacebookZyp_Audience-TimeOfDay.py");
print("Zyp Art Gallery Time of Day data extracted!\n");

# --------------------------------------------------------

print("ZYP ART GALLERY FACEBOOK DATA EXTRACTION COMPLETE!\n");