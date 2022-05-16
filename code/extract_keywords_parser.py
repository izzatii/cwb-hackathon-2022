# Extract data from sample resume csv file and categorize based on experience and skills. 
# Domain is already categorized.
# To get experience, calculates duration for field class = "datesWrapper"
# To get skills, extracts info from field div class section title - skills

from bs4 import BeautifulSoup as soup
import locale
import pandas as pd
import os

resume_dir = os.getcwd()
resume_html = pd.read_csv('Resume.csv')
res_html = resume_html['Resume_html'].text.strip().replace('\r\n','\n')
page_soup = soup(res_html, "html.parser")
field = page_soup.find("div_class", {"class":"datesWrapper"})
print(field.head)
#page_html_pretty = resume_html.text.strip().replace('\r\n','\n')
#page_soup = soup(page_html_pretty, "html.parser")
#field = page_soup.find("div_class")
#print(field)

