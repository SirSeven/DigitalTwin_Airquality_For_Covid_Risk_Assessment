from sys import stdout
from actions import IAction

class LogAction(IAction):
    
    TypeName: str = 'LogActionImpl'

    def execute(self, config):
        stdout.writelines(config['message']);