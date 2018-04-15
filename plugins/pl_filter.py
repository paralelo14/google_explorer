"""
Class used to run the exploit filters in the result file
"""
import os
import sys

PATH = os.path.join(os.sep, os.getcwd() + '/' + 'plugins')


class Plugins():

    def __init__(self, filters):
        self.filters = filters
        self.exploits = self.validate_plugins()
        self.run_filter()

    def validate_plugins(self):
        pl_list = [f.rsplit(".")[0] for f in os.listdir(PATH)]
        filters = self.filters.split(',')
        exploits = list(set(filters).intersection(set(pl_list)))
        if exploits:
            return exploits
        else:
            print("\n\033[31m### Error ###")
            print("\033[33mNone of the plugins you choose "
                  "were found!!\033[0m\n")
            print("The current options are:\n")
            for pl in pl_list:
                if '__' not in pl and 'pl_filter' not in pl:
                    print(pl)
            sys.exit(1)

    def run_filter(self):
        try:
            for pl in self.exploits:
                pl_path = os.path.join(PATH + '/' + pl + '.py')
                os.system('python3 ' + pl_path)
        except Exception as e:
            pass
