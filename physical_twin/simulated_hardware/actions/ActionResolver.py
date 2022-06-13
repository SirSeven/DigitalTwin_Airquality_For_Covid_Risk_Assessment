from actions import LogAction

class ActionResolver():
    
    @staticmethod
    def getAction(actionType: str):
        if actionType == LogAction.TypeName:
            return LogAction()
        
        return {}