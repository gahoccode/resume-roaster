from bs4 import BeautifulSoup
import requests
from typing import Dict
from smolagents.tools import Tool

class LinkedInScraperTool(Tool):
    name = "linkedin_scraper"
    description = "Scrapes LinkedIn profiles to extract professional information"
    inputs = {"linkedin_url": str}
    outputs = dict

    def __call__(self, linkedin_url: str) -> dict:
        try:
            # Add headers to mimic a browser request
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(linkedin_url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract profile information
            profile_data = {
                'name': self._extract_name(soup),
                'headline': self._extract_headline(soup),
                'about': self._extract_about(soup),
                'experience': self._extract_experience(soup),
                'education': self._extract_education(soup),
                'skills': self._extract_skills(soup)
            }
            
            return profile_data
            
        except Exception as e:
            return {"error": f"Failed to scrape profile: {str(e)}"}
    
    def _extract_name(self, soup):
        name_element = soup.find('h1', {'class': 'text-heading-xlarge'})
        return name_element.text.strip() if name_element else "Name not found"
    
    def _extract_headline(self, soup):
        headline_element = soup.find('div', {'class': 'text-body-medium'})
        return headline_element.text.strip() if headline_element else "Headline not found"
    
    def _extract_about(self, soup):
        about_element = soup.find('div', {'class': 'pv-about-section'})
        return about_element.text.strip() if about_element else "About section not found"
    
    def _extract_experience(self, soup):
        experience_elements = soup.find_all('li', {'class': 'experience-item'})
        experience = []
        for exp in experience_elements:
            title_element = exp.find('h3', {'class': 'experience-title'})
            company_element = exp.find('p', {'class': 'experience-company'})
            if title_element and company_element:
                experience.append({
                    'title': title_element.text.strip(),
                    'company': company_element.text.strip()
                })
        return experience if experience else ["Experience not found"]
    
    def _extract_education(self, soup):
        education_elements = soup.find_all('li', {'class': 'education-item'})
        education = []
        for edu in education_elements:
            school_element = edu.find('h3', {'class': 'education-school'})
            degree_element = edu.find('p', {'class': 'education-degree'})
            if school_element and degree_element:
                education.append({
                    'school': school_element.text.strip(),
                    'degree': degree_element.text.strip()
                })
        return education if education else ["Education not found"]
    
    def _extract_skills(self, soup):
        skills_elements = soup.find_all('span', {'class': 'skill-name'})
        return [skill.text.strip() for skill in skills_elements] if skills_elements else ["Skills not found"]