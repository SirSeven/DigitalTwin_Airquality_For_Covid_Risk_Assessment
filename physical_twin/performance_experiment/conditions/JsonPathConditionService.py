from sys import stdout
from jsonpath_ng.ext import parse
from actions import IAction, LogAction
from actions.ActionResolver import ActionResolver
from conditions.IConditionService import IConditionService
from helpers import JsonHelper

class JsonPathConditionService(IConditionService):

    def __init__(self, pathToConditionsFile):
        obj = JsonHelper.readJsonFromFile(pathToConditionsFile)
        self.sensorConditionsArray = obj['validators']

    def validate(self, component, property, propertyValue):
        validatorConfigs = []

        if component in self.sensorConditionsArray:
            validatorConfigs = self.sensorConditionsArray[component]
        
        if len(validatorConfigs) > 0:

            if self.is_float(propertyValue):
                propertyValue = float(propertyValue)

            message = [{"Property": property, "Value": propertyValue}]

            for validatorConfig in validatorConfigs:
                # performance optimizing through lazy initialization of jsme path query
                try:
                    jsonPathQuery = validatorConfig['query']
                except KeyError:
                    stringQuery = validatorConfig['jsonPathQuery'].replace("&&","&")
                    parsedQuery = parse(stringQuery)
                    validatorConfig['query'] = parsedQuery
                    jsonPathQuery = parsedQuery
                    # this is needed as the parsers AND operator is different than in the spec

                queryResult = jsonPathQuery.find(message);

                if len(queryResult) == 0:
                    continue

                for actionConfig in validatorConfig['actions']: 
                    action = ActionResolver.getAction(actionConfig['type'])
                    action.execute(actionConfig['config']);

                if validatorConfig['continue'] == False:
                    return False
        
        return True

    def is_float(self, numberStr):
        try:
            float(numberStr)
            return True
        except ValueError:
            return False