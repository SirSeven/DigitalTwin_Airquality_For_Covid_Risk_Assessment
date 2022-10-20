from sys import stdout
import time
from actions import IAction

class LogAction(IAction):
    
    TypeName: str = 'LogActionImpl'

    def execute(self, config):
        time.sleep(10/1000)
        #stdout.writelines(config['message']);