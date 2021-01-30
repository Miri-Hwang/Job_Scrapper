import requests
from bs4 import BeautifulSoup

LIMIT = 10
URL = f"https://www.indeed.com/jobs?q=python&start={LIMIT}"


def extract_indeed_pages():
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, "html.parser")
    pagination = soup.find("ul", {"class": "pagination-list"})
    links = pagination.find_all('span')

    pages = []

    for link in links[2:-2]:
        pages.append(int(link.string))

    max_page = pages[-1]
    return max_page


def extract_indeed_jobs(last_page):
    jobs = []
    for page in range(last_page):
        result = requests.get(f"{URL}&start={page*LIMIT}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class": "jobsearch-SerpJobCard"})
        for result in results:
            title = result.find("h2", {"class": "title"}).find('a')["title"]
            company = result.find('span', {"class": "company"})
            company_anchor = company.find('a')
            if company_anchor is not None:
                company = str(company_anchor.string)
            else:
                company = str(company.string)
            company = company.strip()
            print(title, company)
    return jobs
