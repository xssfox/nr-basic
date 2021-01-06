Automatically downgrade full New Relic users to basic to save money while retaining usability. If New Relic user licenses are the majority of your New Relic bill this could half your cost or more.


Why
--

New Relic One per user licensing is a joke, and it costs far too much when you have multiple developers that ocasionally use the platform (eg, on call rosters, or developers).

Luckily users on New Relic are billed per hour, rather than per month, so we have some room for improvement here. (https://docs.newrelic.com/docs/accounts/accounts-billing/new-relic-one-pricing-billing/new-relic-one-pricing-billing). Basic users are free, and basic users can upgrade themselves to full users. The problem is that basic users can't downgrade themselves to basic unless they are an admin, and users have to remember to downgrade themselves to avoid charges.

What
--
This python script logins into New Relic, checks the user list of users matching a role, and how long they've been active. If the user hasn't been active in a predetermined time it will update the user back to a basic level. (The user can upgrade their account if they need to use full again)

How
--

### Prep
1. You'll need to know your account ID. You can find this by going to https://one.newrelic.com/launcher/account-settings-launcher.account-settings-launcher and clicking on "Users and Roles". The account ID number will be in the URL bar.
2. You'll also need to create a new role, it doesn't have to have any specific permissions. Click on edit on this role and grab it's ID from the URL bar as well.
3. Create a new admin user and password. I think this can be a basic account but does need to be an admin. Log into this account at least once.

### Stand alone
0. Install Python3
1. Install requests
  ```pip3 install requests```
2. Run it
  ```TIMEOUT=3600 ACCOUNT_ID=123 ROLE_ID=123 USERNAME=nr@email PASSWORD=234 python3 index.py```
3. Use some form of task scheduler to run regularly

### AWS Lambda function
1. Deploy cloudformation.yml to us-east-1 region.
2. You might want to setup some alarms for when the Lambda fails so you don't bill shock.
