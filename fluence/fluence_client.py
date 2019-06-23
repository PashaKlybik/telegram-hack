import requests
import base64
import json

class FluenceClient():
    # curl 'http://localhost:30000/apps/0/tx' --data $'sessionId/2\n{"data_id": "eyJkYXRhX2lkIjoxfQ==", "action": "GetData"}'
    count_request = 0
    def __init__(self,account,private_key):
        self.count_request = 0
        self.lastDataInDB = -1
        self.account = account
        self.private_key = private_key


    def send_low_level_post(self, author, title, body, parent_link):
        
        # TODO add new post. Save body 
        pass

    def get_posts(self, permlink_collection):
        result = []
        for i in range(self.lastDataInDB):
            result.append(self.get_data_from_fluence(i))
        return result

    def save_data_to_fluence(self, data):
        req_data = """sessionId/{sessionId}\n{{"data": "{data}", "action": "AddData"}}""".format(sessionId=str(self.count_request), data=data)
        # req_data = """sessionId/{0}\n{{"data_id": "{1}", "action": "AddData"}}""".format(self.count_request, data)
        response = requests.post('http://localhost:30000/apps/0/tx', data=req_data)
        self.count_request += 1
        
        jsonResponce = json.loads(response.text)
        fluenceAnswerStr = base64.b64decode(jsonResponce["result"]["data"])
        dataInfo = json.loads(fluenceAnswerStr)
        self.lastDataInDB = dataInfo["data_id"]
        return dataInfo["data_id"]
        
        # response.body

    def get_data_from_fluence(self, data_id):
        req_data = """sessionId/{sessionId}\n{{"data_id": "{data}", "action": "GetData"}}""".format(sessionId=str(self.count_request), data=data_id)
        
        response = requests.post('http://localhost:30000/apps/0/tx', data=req_data)
        self.count_request += 1
        
        jsonResponce = json.loads(response.text)
        fluenceAnswerStr = base64.b64decode(jsonResponce["result"]["data"])
        dataInfo = json.loads(fluenceAnswerStr)
        return dataInfo["data"]