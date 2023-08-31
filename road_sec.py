from selenium import webdriver
from selenium.webdriver.common.by import By
import time, pprint, json

class navegator:
    def __init__(self):
        options = webdriver.ChromeOptions()
        # options.add_argument("--headless")
        # options = options
        self.chrome = webdriver.Chrome()
        self.profiles = dict()

    def roadsec_scraping(self):
        self.chrome.get("https://www.roadsec.com.br/rs23-palestrantes-confirmados")
        while self.chrome.find_elements(By.XPATH, '//div[@class="summary-title"]/a') == 0:
            time.sleep(0.001)

        all_profiles = self.chrome.find_elements(By.XPATH, '//div[@class="summary-title"]/a')
        dict_profile = {'url': ''}

        for profile in all_profiles:
            name_profile = profile.get_attribute('href').split('/')
            self.profiles.update({name_profile[-1]: {'url': profile.get_attribute('href')}})

        for profile in self.profiles:
            xpath = """//div[@class="sqs-block-content"]/div[@class="sqs-html-content"]/p[@class="preFade fadeIn"]/a"""
            self.chrome.get(self.profiles[profile]['url'])
            self.profiles[profile].pop('url')

            while self.chrome.find_elements(By.XPATH, xpath) == 0:
                time.sleep(0.001)

            social_midias = self.chrome.find_elements(By.XPATH, xpath)
            if len(social_midias) == 0:
                xpath = """//div[@class="sqs-block-content"]/div[@class="sqs-html-content"]/p[@class="preFade fadeIn"]/span[@class="sqsrte-text-highlight"]/a"""
                social_midias = self.chrome.find_elements(By.XPATH, xpath)

            for midia in social_midias:
                url = midia.get_attribute('href')

                if '//' in url:
                    url = 'https:'+url[url.rfind('//'):len(url)]
                if not 'www' in url:
                    url = url.replace('https://', 'https://www.')

                if url[-1] != '/':
                    url+='/'
                if '.nstagram.' in url:
                    url = url.replace('.nstagram.', '.instagram.')
                if 'www.br.' in url:
                    url = url.replace('www.br.', 'www.')
                if '.com.br' in url or url == "https://www.marcusnatrielli.com/":
                    self.profiles[profile]['site'] = url
                else:
                    key = url.split('.')
                    self.profiles[profile][key[1]] = url

            time.sleep(0.1)

        self.split_social_midia()

        self.write_file('profile', self.profiles)

    def split_social_midia(self):
        social_midias = dict()

        for profile in self.profiles:
            for social_midia in self.profiles[profile]:
                if not social_midia in social_midias:
                    social_midias.update({social_midia: list()})

            for social_midia in self.profiles[profile]:
                social_midias[social_midia].append(self.profiles[profile][social_midia])

        self.write_file('social_midias', social_midias)

    def write_file(self, file, dict):
        with open(f"{file}.json", "w") as arquivo:
            json.dump(dict, arquivo, indent=4)

def run():
    navegador = navegator()
    navegador.roadsec_scraping()

run()