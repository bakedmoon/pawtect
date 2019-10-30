import requests, json
from django.http import JsonResponse
from pawtectApp.models import UserProfile, SalesforceLogs


class SalesforceService():
    def getAccessToken(self, sfInfo, userId):
        querystring = {"grant_type": "password", "username": sfInfo.username, "password": sfInfo.password,
                       "client_id": sfInfo.clientId, "client_secret": sfInfo.clientSecret}
        payload = {}
        headers = {}
        response = requests.request("POST", sfInfo.tokenUrl, data=payload, headers=headers, params=querystring)
        accessData = response.json()
        if accessData['access_token']:
            print("AFTER GET TOKEN DATA IS HERE-->>",accessData)
            getNewUser = self.createNewUser(accessData, sfInfo, userId)
            return getNewUser
        else:
            return JsonResponse({"Error": "Something Went Wrong."})

    def createNewUser(self, accessData, sfInfo, userId):
        print("INSIDE HERE IS --->>",accessData['instance_url'])
        make_user_url = accessData['instance_url'] + "/" + sfInfo.serviceUrl
        userInfo = UserProfile.objects.get(user__id=userId)

        dataString = {"inputs": [
            {"lastName": userInfo.user.last_name, "firstName": userInfo.user.first_name, "mobile": str(userInfo.mobile),
             "email": userInfo.user.email, "zip": userInfo.pincode, "event": "SIGNUP",
             "customer_category": "Pet Owner"}]}
        payload = json.dumps(dataString)
        headers = {'Content-Type': "application/json",
                   'Authorization': accessData['token_type'] + " " + accessData['access_token'], }
        response = requests.request("POST", make_user_url, headers=headers, data=payload)
        addSfInfo = response.json()

        if addSfInfo[0]['isSuccess']:
            logObj = SalesforceLogs()
            for rCode in addSfInfo:
                if type(rCode) == dict:
                    userInfo.selfRefer = rCode['outputValues']['output']['REFERRAL_CODE__c']
                    logObj.status = "Success"
                    logObj.username = userInfo.user.first_name + " " + userInfo.user.last_name
                    logObj.email = userInfo.user.email
                    logObj.mobile = userInfo.user.username
                    logObj.successLog = addSfInfo
                    logObj.save()
                    userInfo.save()
                    return JsonResponse({"Success": "Successfully add user."})


                else:
                    logObj.status = "Error"
                    logObj.username = userInfo.user.first_name + " " + userInfo.user.last_name
                    logObj.email = userInfo.user.email
                    logObj.mobile = userInfo.user.username
                    logObj.errorLog = accessData
                    logObj.save()
                    return JsonResponse({"Error": "Something went wrong."})
        else:
            return JsonResponse({"Error": "Something went wrong."})
