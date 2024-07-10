import os, json, time, sys, inquirer
from termcolor import colored
from task import Task

class Main():
    def __init__(self):
        self.cls = lambda : os.system('cls')
        
        self.loadContext()
        self.loadSettings()
        #self.menu()
        self.initialize_task()

    def initialize_task(self):
        print(colored('Starting task...', 'yellow'))
        Task(self.settings, self.context)

    def menu(self):
        self.cls()

        options = {
            'Start Task':self.initialize_task,
            'Settings':self.configureSettings
        }

        questions = [
            inquirer.List('Option',
                          message="Selection",
                          choices=list(options),
                          ),
        ]

        answers = inquirer.prompt(questions)
        options[answers['Option']]()

    def loadSettings(self):
        try:
            with open('settings.json', 'r') as f:
                self.settings = json.load(f)
                f.close()
        except:
            print(colored('Error Loading Settings!', 'red'))
            time.sleep(10)
            sys.exit()

    def loadContext(self):
        try:
            with open('context.txt', 'r') as f:
                self.context = f.read()
                f.close()
        except:
            print(colored('Error Loading Context!', 'red'))
            time.sleep(10)
            sys.exit()

    def configureSettings(self):
        settings = [
            'API_KEY',
            'DELAY'
        ]

        options = []

        for setting in settings:
            settingsOption = f'{setting} - {self.settings.setdefault(setting, "")}'
            options.append(settingsOption[:50] + (settingsOption[50:] and '...'))

        options.append('Back To Menu')

        questions = [
            inquirer.List('Option',
                          message="Please Select A Setting",
                          choices=options,
                          ),
        ]

        answer = inquirer.prompt(questions)

        if answer['Option'] == 'Back To Menu':
            self.menu()
        else:
            updateValue = settings[options.index(answer['Option'])]
            newValue = input('Please Enter New Value: ')

            try:
                with open('settings.json', 'r') as f:
                    data = json.loads(f.read())
                    data[updateValue] = newValue
                    self.settings[updateValue] = newValue
                    f.close() 

                with open('settings.json', 'w') as f:
                    json.dump(data, f, indent=2)
                    f.close()
            except:
                print(colored('Error Updating Settings!', 'red'))
                time.sleep(10)
                sys.exit()

            self.configureSettings()

if __name__ == '__main__':
    Main()


