from bs4 import BeautifulSoup
import requests
import time

def find_jobs():
    job_list = []

    api_url = 'http://127.0.0.1:8000/posts'
    #print("Put some skill that you are not familiar with")
    #unfamiliar_skill = input('>').split(',')
    #print(f"Filtering out {unfamiliar_skill}")

    html_text = requests.get('https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords=python&txtLocation=').text

    soup = BeautifulSoup(html_text, "lxml")

    jobs = soup.find_all('li', class_='clearfix job-bx wht-shd-bx')

    for job in jobs:
        job_info = {}

        published_date = job.find('span', class_="sim-posted").span.text.strip()
        #if "few" not in published_date:
        #    continue

        company_name = job.find('h3', class_='joblist-comp-name').text.strip()
        more_info = job.header.h2.a["href"]
        skills = job.find('span', class_="srp-skills").text.strip()

        skills = [x.strip().lower() for x in skills.split(",")]
        skills = ", ".join(skills)

        #filtered = any(skill in skills for skill in unfamiliar_skill)
        #if filtered:
            #continue
        job_info["company_name"] = company_name
        job_info["required_skills"] = skills
        job_info["published_date"] = published_date
        job_info["more_info"] = more_info

        job_list.append(job_info)

        print(f'Company Name: {company_name}')
        print(f'Required Skills: {skills}')
        print(f'Published Date: {published_date}')
        print(f'More info: {more_info}')

        print()
    
    # Send data to database
    for data in job_list:
        try:
            response = requests.post(api_url, json=data)

            if response.status_code >= 200 and response.status_code <= 300:
                print("Data sent successfully")
            else:
                print(f"Failed to send data. Status code: {response.status_code}")
                print(response.text)

        except requests.exceptions.RequestException as e:
            print(f"Error occured: {e}")

if __name__ == "__main__":
    find_jobs()