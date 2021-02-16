import requests
import os
import time

def handler(event,context):
    # For cookies and error handling
    session = requests.Session()
    session.hooks = {
    'response': lambda r, *args, **kwargs: r.raise_for_status()
    }


    #  Login
    login_data = {
        "login[email]": os.getenv("USERNAME"),
        "login[password]": os.getenv("PASSWORD")
    }
    login_response = session.post("https://login.newrelic.com/login", data = login_data)
    
    custom_headers = {
        "X-Requested-With": "XMLHttpRequest",
        "Accept": "application/json"
    }

    # Get users
    users_response = session.get(f"https://user-management.service.newrelic.com/accounts/{os.getenv('ACCOUNT_ID')}/users",  headers=custom_headers)
    
    # Determine which users need to be switched back to basic
    switch_to_basic = []
    for user in users_response.json():
        roles = [role['id'] for role in user['roles'] ]
        if int(os.getenv("ROLE_ID")) in roles: # check if in the auto role
            if user['user_tier_id'] == 0: #check if full role
                if user['last_access_at'] + int(os.getenv("TIMEOUT")) < time.time(): # check if the last access + timeout is less than the current timestamp
                    switch_to_basic.append(user['user_id'])

    # Update accounts
    for user_id in switch_to_basic:
        print(f"Switching {str(user_id)} back to basic")
        update_response = session.put(f"https://rpm.newrelic.com/user_management/accounts/{os.getenv('ACCOUNT_ID')}/users/{user_id}",
          headers=custom_headers,
          json={
              "account_view":{
                  "user_tier_id":1
               }
            }
        )
if __name__ == "__main__":
    handler({},{})
