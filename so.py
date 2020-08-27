#stackoverflow job scrapping
import requests
from bs4 import BeautifulSoup

URL = "https://stackoverflow.com/jobs?q=python"

#Return maximum number of pages
def get_last_page():
    result = requests.get(URL)
    soup = BeautifulSoup(result.text,"html.parser")
    pages= soup.find("div",{"class":"s-pagination"}).find_all('a')
    last_page =pages[-2].get_text(strip =True)
    return int(last_page)

#The title, company, region, and link of each job are stored in a dictionary and returned.
def extract_job(html):
    title = html.find("h2",{"class":"mb4"}).text.strip()
    company = html.find("h3",{"class":"mb4"}).find_all('span')[0].text.strip()
    location = html.find("h3",{"class":"mb4"}).find_all('span')[1].text.strip()
    job_id = html["data-jobid"].strip()
    return {"title":title, "company":company, "location":location, "link": f"https://stackoverflow.com/jobs/{job_id}"}

#Repeat extract_job() until the end of the page
def extract_jobs(last_page):
    jobs = []
    for page in range(last_page):
        print(f"Scrapping StackOverflow: Page: {page+1}")
        result = requests.get(f"{URL}&pg={page+1}")
        soup = BeautifulSoup(result.text,'html.parser')
        results = soup.find_all('div',{'class' :"-job" })
        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs

def get_jobs():
    last_page = get_last_page()
    jobs = extract_jobs(last_page)
    return jobs
