import requests,json
from pawtectApp.models import UserProfile


class SalesforceService():
    def getAccessToken(self, sfInfo):
        print("SF INFO IS HERE-->>>", sfInfo)
        get_token_url = "https://test.salesforce.com/services/oauth2/token"
        querystring = {"grant_type": "password", "username": sfInfo.username, "password": sfInfo.password,
                       "client_id": sfInfo.clientId, "client_secret": sfInfo.clientSecret}
        payload = {}
        headers = {}
        response = requests.request("POST", get_token_url, data=payload, headers=headers, params=querystring)
        return response.json()

    def createnewuser(self, accessData, userId):
        make_user_url = accessData['instance_url'] + "/services/data/v42.0/actions/custom/apex/LMS_AccountSignupAction"
        userInfo = UserProfile.objects.get(user__id=userId)
        print("USER DATA IS HERE-->>", userId, userInfo.user.first_name)
        dataString = {"inputs": [
            {"lastName": userInfo.user.last_name, "firstName": userInfo.user.first_name, "mobile": str(userInfo.mobile),
             "email": userInfo.user.email, "zip": userInfo.pincode, "event": "SIGNUP",
             "customer_category": "Pet Owner"}]}
        payload = json.dumps(dataString)
        headers = {'Content-Type': "application/json",
                   'Authorization': "Bearer 00Dp00000004fsE"
                                    "!AREAQLwya1D18buGjNKjzVCSoIdBGBIpmuzdr1vKqlkHzCCL0kCNZ3KnyBUjJxIUVTSjVTQIIpZ9Vf2DORJiyCAg.lBKK1SF",
                   'Accept': "*/*", 'Host': "cs31.salesforce.com", 'Accept-Encoding': "gzip, deflate",
                   'Content-Length': "234"}
        response = requests.request("POST", make_user_url, headers=headers, data=payload)
        print("THE TYPE IS DATA IS HERE---->>>", response, payload)
        return response.json()