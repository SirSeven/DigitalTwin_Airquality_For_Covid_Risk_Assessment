from conditions import IConditionService

class NullConditionService(IConditionService):
    
    def validate(self, component, property, propertyValue):
        return True