import bs4 
import requests
import os
import pandas as pd
import urllib.parse
from bs4 import BeautifulSoup as bs

Geo_id={
    'Egypt':'106155005',
    'Saudi Arabia':'100459316',
    'United Arab Emirates':'104305776',
    'Qatar':'104170880',
    'Kuwait':'103239229',
    'Bahrain':'100425729',
    'Oman':'103619019',
    'Jordan':'103710677',
    'Morocco':'102787409',
    'Algeria':'106395874',
    'Germany':'101282230',
    'France':'105015875',
    'Italy':'103350119',
    'Spain':'105646813',
    'United Kingdom': '101165590',
    'Canada': '101174742',
    'United States': '103644278',
    'India': '102713980'

}

#job_name = input("Enter Job name: ")
jobs_name=["Ai Engineer","Business Intellegence Analyst","Data Analyst","Data scientist","Data Engineer","Machine Learning Engineer"]

job_country =input("Enter Job country")
job_country_URL =Geo_id.get(job_country)


for job_name in jobs_name:
    job_name_URL = urllib.parse.quote(job_name)


    URL = f'https://www.linkedin.com/jobs/search/?geoId={job_country_URL}&keywords={job_name_URL}&origin=JOB_SEARCH_PAGE_LOCATION_AUTOCOMPLETE&refresh=true'
    print(URL)

    response = requests.get(URL)
    print(response)
    soup = bs(response.content,'html.parser')

    containers = soup.find_all("div", class_="base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card")

    job_titles, link, companies, companies_links, locations, publish_time = [], [], [], [], [], []

    for container in containers:
        job_title = container.find("h3", class_="base-search-card__title")
        job_titles.append(job_title.text.strip())
    
        company = container.find("h4", class_="base-search-card__subtitle")
        companies.append(company.text.strip())

        company_links = container.find("a", class_="hidden-nested-link")
        companies_links.append(company_links.get('href'))

        location = container.find("span", class_="job-search-card__location")
        locations.append(location.text.strip())

        time = container.find("time")
        publish_time.append(time.text.strip())

        job_link = container.find("a", class_="base-card__full-link")
        link.append(job_link.get("href"))





#print(job_titles, link, companies, companies_links, locations, publish_time)

    file_name = f"linkedin_jobs.csv"
    df = pd.DataFrame({
        'country':[job_country]*len(job_titles),
        'job_titles':[job_name]*len(job_titles),
        'job_titles in Details': job_titles,
        'link': link,
        'companies': companies,
        'companies_links': companies_links,
        'location': locations,
        'publish_time': publish_time  })
    
                  

    if not os.path.exists(file_name):
        df.to_csv(file_name, index=False, encoding='utf-8-sig')
    else:
        df_old = pd.read_csv(file_name, encoding='utf-8-sig')
        df_new = df[~df['link'].isin(df_old['link'])]

        if not df_new.empty:
            df_new.to_csv(file_name, index=False, encoding='utf-8-sig', mode='a', header=False)







            #https://wuzzuf.net/search/jobs/?a=hpb%7Cspbg&filters%5Bworkplace_arrangement%5D%5B0%5D=On-site&q=Data%20analysis,