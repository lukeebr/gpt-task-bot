from selenium import webdriver
from selenium.webdriver.common.by import By
from core import Core
import time, json
from bs4 import BeautifulSoup

SYSTEM_PROMPT = '''
You are a browser automation AI.

You have these following actions available to interact with the website: 'set_value', 'click', 'open_url'.
You will analyze the DOM you recieve and reply with the corresponding action in JSON format.
There are three results: 'act', 'information', 'sleep'.
You will include a comment to your action.
If you are instructed to retrieve information you will respond with the corresponding text.
You will also recieve a list of the previous completed actions and contextual information from the user such as usernames, locations, etc.
The 'special-id' parameter will contain the attribute value of 'special-marking' for the element.
You can only return one result per request.

Example response 1:
{"result":"act", "comment":"Setting username field value", "instructions":{"action":"set_value","special-id":"4", "value":"username"}}

Example response 2:
{"result":"act", "comment":"Clicking sign up button", "instructions":{"action":"click","special-id":"2"}}

Example response 3:
{"result":"act", "comment":"Opening the sample site", "instructions":{"action":"open_url","url":"https://www.samplesite.com"}}

Example response 4:
{"result":"information", "comment":"Blue Mountain is a ridge that forms the eastern edge of the Appalachian mountain range in the U.S. state of Pennsylvania."}

Example response 5:
{"result":"sleep", "comment":"Task completed"}

'''

class Task(Core):
    def __init__(self, settings, context):
        Core.__init__(self, settings, context)
        self.history = []
        self.delay = float(settings['DELAY'])
        self.browser = webdriver.Chrome()
        self.complete = False
        
        self.run()

    def open_url(self, response):
        try:
            url = response['instructions']['url']
            self.browser.get(url)
        except Exception as e:
            self.logger.error(f'Exception opening URL: {e}')
            return

    def click(self, response):
        try:
            selector = response['instructions']['special-id']
            self.browser.find_element(By.CSS_SELECTOR, f"[special-id='{selector}']").click()
        except Exception as e:
            self.logger.error(f'Exception clicking button {e}')
            return
        
    def set_value(self, response):
        try:
            selector = response['instructions']['special-id']
            value = response['instructions']['value']
            element = self.browser.find_element(By.CSS_SELECTOR, f"[special-id='{selector}']").send_keys(value)
            #self.browser.execute_script("arguments[0].setAttribute('value',arguments[1])",element, value)
        except Exception as e:
            self.logger.error(f'Exception typing: {e}')
            return

    def perform_action(self, response):
        self.logger.pending('Loading response...')

        actions = {
            'open_url':self.open_url,
            'click':self.click,
            'set_value':self.set_value
        }

        try:
            print(response)
            data = json.loads(response)
            if data['result'] == 'sleep':
                self.logger.info(data['comment'])
                self.complete = True
            elif data['result'] == 'information':
                self.logger.info(data['comment'])
            elif data['result'] == 'act':
                self.logger.pending(f'Performing action: {data["comment"]}')
                actions[data['instructions']['action']](data)
            else:
                self.logger.error('Unknown response')
                return
            
        except Exception as e:
            self.logger.error(f'Exception completing action: {e}')
            return

    def setIDS(self):
        elements = self.browser.find_elements(By.XPATH, "//input | //button")
        for count, element in enumerate(elements):
            self.browser.execute_script("arguments[0].setAttribute('special-id',arguments[1])",element, count)

    def run(self):
        while True:
            self.logger.pending('Waiting for instructions: ')
            instructions = input()

            prompt = f"""
            Context:
            {self.context}

            Determine the first action based on these instructions:
            {instructions}

            """

            response = self.GPT.generate_chat_completion(prompt, SYSTEM_PROMPT)

            self.perform_action(response)

            self.history.append(response)

            while not self.complete:
                time.sleep(self.delay)

                self.setIDS()
                
                self.logger.pending('Fetching HTML...')
                HTML = self.HTMLCleaner.clean_html(self.browser.page_source)

                prompt = f"""
                Previous Actions:
                {self.history}

                Context:
                {self.context}

                Instructions:
                {instructions}

                HTML:
                {HTML}

                """

                response = self.GPT.generate_chat_completion(prompt, SYSTEM_PROMPT)

                self.perform_action(response)

                self.history.append(response)