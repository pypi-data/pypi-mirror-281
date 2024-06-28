import requests
from investfly.api.RestApiClient import RestApiClient

class CliApiClient:

    def __init__(self, baseUrl: str) -> None:
        self.restApi = RestApiClient(baseUrl)

    def login(self, username: str, password: str):
        try: 
            user = self.restApi.login(username, password)
            print("Successfully logged in as: "+user.username)
        except Exception as e:
            print(e)
    
    def logout(self):
        self.restApi.logout()

    def getStatus(self):
        try:
            userInfo = self.restApi.doGet('/user/session')
            print("Currently logged in as "+userInfo['username'])
        except Exception as e:
            print(e)

    def getStrategies(self):
        try:
            strategies = self.restApi.doGet('/strategy/list')
            for strategy in strategies:
                print(str(strategy['strategyId'])+'\t'+strategy['strategyName']+'\n'+strategy['strategyDesc']+'\n')
        except Exception as e:
            print(e)

    def saveStrategy(self, strategyId: int):
        try:
            strategy = self.restApi.doGet('/strategy/'+str(strategyId))
            return strategy['pythonCode']
        except Exception as e:
            return e
        
    def updateStrategy(self, id: int, code: str):
        try:
            self.restApi.doPostCode('/strategy/'+id+'/update/code', code)
            print('Strategy successfully updated')
        except Exception as e:
            print(e)