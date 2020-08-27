#indeed job scrapping
import requests
from bs4 import BeautifulSoup

LIMIT = 50 # Number of jobs to display per page
URL = f'https://www.indeed.com/jobs?q=python&limit={LIMIT}'

#Return maximum number of pages
def get_last_page():
    result= requests.get(URL)
    soup = BeautifulSoup(result.text, 'html.parser')
    pagination = soup.find("div",{"class":"pagination"})
    links= pagination.find_all('a')
    pages =[]
    for link in links[:-1]:
        pages.append(int(link.string))
    max_page = pages[-1]
    return max_page

#The title, company, region, and link of each job are stored in a dictionary and returned.
def extract_job(html):
    title = html.find("a",{"class": "jobtitle"}).text.strip()
    company = html.find("span",{"class":"company"}).text.strip()
    location = html.find("span",{"class":"location"}).text.strip()
    job_id = html["data-jk"].strip()
    return {'title':title, 'company':company, 'location':location, 'link':f"https://www.indeed.com/viewjob?jk={job_id}"}

#Repeat extract_job() until the end of the page
def extract_jobs(last_page):
    jobs=[]
    for page in range(last_page):
        print(f"Scrapping Indeed: Page: {page+1}")
        result = requests.get(f"{URL}&start={page*LIMIT}")
        soup = BeautifulSoup(result.text, 'html.parser')
        results = soup.find_all("div",{"class":"jobsearch-SerpJobCard"})
        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs

def get_jobs():
    last_page = get_last_page()
    jobs = extract_jobs(last_page)
    return jobs
