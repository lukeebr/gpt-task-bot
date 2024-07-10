from cli import Logger
from gpt import GPT
from html_cleaner import HTMLCleaner

class Core:
    def __init__(self, settings, context):
        self.settings = settings
        self.context = context
        self.HTMLCleaner = HTMLCleaner()
        self.GPT = GPT(settings['API_KEY'])
        self.logger = Logger('TASK', '0')