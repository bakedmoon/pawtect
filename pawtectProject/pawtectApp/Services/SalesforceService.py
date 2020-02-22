import requests, json
from django.http import JsonResponse
from pawtectApp.models import UserProfile, SalesforceLogs, SalesforceSettings
from pawtectApp.const import SIGNUP_URL,VETCOIN_URL


class SalesforceService():
    def getAccessToken(self, sfInfo):
        querystring = {"grant_type": "password", "username": sfInfo.username, "password": sfInfo.password,
                       "client_id": sfInfo.clientId, "client_secret": sfInfo.clientSecret}
        payload = {}
        headers = {}
        response = requests.request("POST", sfInfo.tokenUrl, data=payload, headers=headers, params=querystring)
        accessData = response.json()
        if accessData:
            return accessData
        else:
            return None

    def createNewUser(self, sfInfo, userId):
        userInfo = UserProfile.objects.get(user__id=userId)
        dataString = {"inputs": [
            {"lastName": userInfo.user.last_name, "firstName": userInfo.user.first_name, "mobile": str(userInfo.mobile),
             "email": userInfo.user.email, "zip": userInfo.pincode, "event": "SIGNUP",
             "customer_category": "Pet Owner"}]}
        payload = json.dumps(dataString)

        accessData = self.getAccessToken(sfInfo)
        if not accessData:
            return None
        make_user_url = accessData['instance_url']+SIGNUP_URL
        headers = {'Content-Type': "application/json",
                   'Authorization': accessData['token_type'] + " " + accessData['access_token']}
        response = requests.request("POST", make_user_url, headers=headers, data=payload)
        addSfInfo = response.json()
        if addSfInfo[0]['isSuccess']:
            logObj = SalesforceLogs()
            for rCode in addSfInfo:
                if type(rCode) == dict:
                    logObj.status = "Success"
                    logObj.username = userInfo.user.first_name + " " + userInfo.user.last_name
                    logObj.email = userInfo.user.email
                    logObj.mobile = userInfo.user.username
                    logObj.successLog = addSfInfo
                    logObj.save()
                    userInfo.save()
                    return addSfInfo


                else:
                    logObj.status = "Error"
                    logObj.username = userInfo.user.first_name + " " + userInfo.user.last_name
                    logObj.email = userInfo.user.email
                    logObj.mobile = userInfo.user.username
                    logObj.errorLog = accessData
                    logObj.save()
                    return None
        else:
            return None

        
    def getVetcoinsDetails(self,userInfo):
        sfInfo = SalesforceSettings.objects.get()
        accessData = self.getAccessToken(sfInfo)
        userInfo = UserProfile.objects.get(user__id=userInfo.user_id)
        if not accessData:
            return None
        url = accessData['instance_url']+VETCOIN_URL

        dataString = {"inputs": [
            {"customer_mobile": str(userInfo.mobile), "event": "RETRIEVE_REWARD_POINTS"}]}

        payload = json.dumps(dataString)
        headers = {'Content-Type': "application/json",
                   'Authorization': accessData['token_type'] + " " + accessData['access_token'], }
        response = requests.request("POST", url, data=payload, headers=headers)
        vetCoinResponse = response.json()
        if vetCoinResponse[0]['isSuccess']:
            print("INSIDE IF SERVICE",vetCoinResponse[0])
            userInfo.vetcoins = vetCoinResponse[0]['outputValues']['reward_points']
            #userInfo.selfRefer = vetCoinResponse[0]['outputValues']['referral_code']
            userInfo.vetcoinObj = vetCoinResponse
            userInfo.save()
            return vetCoinResponse
        else:
            return None
    
