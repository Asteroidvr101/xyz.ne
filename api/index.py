from flask import Flask, request, jsonify
from datetime import datetime, timedelta
import pytz

app = Flask(__name__)

@app.route("/api/photon", methods=["POST"])
def photonauth():
        print(f"Received {request.method} request at /api/photon")
        getjson = request.get_json()
        Ticket = getjson.get("Ticket")
        Nonce = getjson.get("Nonce")
        Platform = getjson.get("Platform")
        UserId = getjson.get("UserId")
        nickName = getjson.get("username")
        if request.method.upper() == "GET":
            rjson = request.get_json()
            print(f"{request.method} : {rjson}")

            userId = Ticket.split('-')[0] if Ticket else None
            print(f"Extracted userId: {UserId}")

            if userId is None or len(userId) != 16:
                print("Invalid userId")
                return jsonify({
                    'resultCode': 2,
                    'message': 'Invalid token',
                    'userId': None,
                    'nickname': None
                })

            if Platform != 'Quest':
                return jsonify({'Error': 'Bad request', 'Message': 'Invalid platform!'}),403

            if Nonce is None:
                return jsonify({'Error': 'Bad request', 'Message': 'Not Authenticated!'}),304

            req = requests.post(
                url=f"https://{settings.TitleId}.playfabapi.com/Server/GetUserAccountInfo",
                json={"PlayFabId": userId},
                headers={
                    "content-type": "application/json",
                    "X-SecretKey": settings.SecretKey
                })

            print(f"Request to PlayFab returned status code: {req.status_code}")

            if req.status_code == 200:
                nickName = req.json().get("UserInfo",
                                          {}).get("UserAccountInfo",
                                                  {}).get("Username")
                if not nickName:
                    nickName = None

                print(
                    f"Authenticated user {userId.lower()} with nickname: {nickName}"
                )

                return jsonify({
                    'resultCode': 1,
                    'message':
                    f'Authenticated user {userId.lower()} title {settings.TitleId.lower()}',
                    'userId': f'{userId.upper()}',
                    'nickname': nickName
                })
            else:
                print("Failed to get user account info from PlayFab")
                return jsonify({
                    'resultCode': 0,
                    'message': "Something went wrong",
                    'userId': None,
                    'nickname': None
                })

        elif request.method.upper() == "POST":
            rjson = request.get_json()
            print(f"{request.method} : {rjson}")

            ticket = rjson.get("Ticket")
            userId = ticket.split('-')[0] if ticket else None
            print(f"Extracted userId: {userId}")

            if userId is None or len(userId) != 16:
                print("Invalid userId")
                return jsonify({
                    'resultCode': 2,
                    'message': 'Invalid token',
                    'userId': None,
                    'nickname': None
                })

            req = requests.post(
                 url=f"https://{settings.TitleId}.playfabapi.com/Server/GetUserAccountInfo",
                 json={"PlayFabId": userId},
                 headers={
                     "content-type": "application/json",
                     "X-SecretKey": settings.SecretKey
                 })

            print(f"Authenticated user {userId.lower()}")
            print(f"Request to PlayFab returned status code: {req.status_code}")

            if req.status_code == 200:
                 nickName = req.json().get("UserInfo",
                                           {}).get("UserAccountInfo",
                                                   {}).get("Username")
                 if not nickName:
                     nickName = None
                 return jsonify({
                     'resultCode': 1,
                     'message':
                     f'Authenticated user {userId.lower()} title {settings.TitleId.lower()}',
                     'userId': f'{userId.upper()}',
                     'nickname': nickName
                 })
            else:
                 print("Failed to get user account info from PlayFab")
                 successJson = {
                     'resultCode': 0,
                     'message': "Something went wrong",
                     'userId': None,
                     'nickname': None
                 }
                 authPostData = {}
                 for key, value in authPostData.items():
                     successJson[key] = value
                 print(f"Returning successJson: {successJson}")
                 return jsonify(successJson)
        else:
             print(f"Invalid method: {request.method.upper()}")
             return jsonify({
                 "Message":
                 "Use a POST or GET Method instead of " + request.method.upper()
             })


def ReturnFunctionJson(data, funcname, funcparam={}):
        print(f"Calling function: {funcname} with parameters: {funcparam}")
        rjson = data.get("FunctionParameter", {})
        userId = rjson.get("CallerEntityProfile",
                           {}).get("Lineage", {}).get("TitlePlayerAccountId")

        print(f"UserId: {userId}")

        req = requests.post(
            url=f"https://{settings.TitleId}.playfabapi.com/Server/ExecuteCloudScript",
            json={
                "PlayFabId": userId,
                "FunctionName": funcname,
                "FunctionParameter": funcparam
            },
            headers={
                "content-type": "application/json",
                "X-SecretKey": settings.SecretKey
            })

        if req.status_code == 200:
            result = req.json().get("data", {}).get("FunctionResult", {})
            print(f"Function result: {result}")
            return jsonify(result), req.status_code
        else:
            print(f"Function execution failed, status code: {req.status_code}")
            return jsonify({}), req.status_code
app.run(host="0.0.0.0", port=8080)
