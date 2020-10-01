import jsonlines
import datetime
import ast
import sys

# usage: python3 fix_users.py old.json new.json

if len(sys.argv) < 3:
    print("Missing argument for old or new file")
    print("usage: python3 fix_users.py old.json new.json")
    sys.exit(1)
else:
    old_file = sys.argv[1]
    new_file = sys.argv[2]

# List of users in the export from the new server
new_users = {}

with jsonlines.open('new.json') as new_reader:
    for obj in new_reader:
        if obj['type'] == 'user':
            new_users[obj['user']['email']] = obj['user']

# dictionary containing the object of our fixed users
fixed_users = {}
# list for the user lines that are being replaced
users = []
# list with all the users that need to be changed
users_to_replace = []

with jsonlines.open('old.json') as old_reader:
    for obj in old_reader:
        if obj['type'] == 'user':
            user = obj['user']
            if new_users[user['email']]:
                if user['username'] != new_users[user['email']]['username']:
                    new_user = new_users[user['email']]
                    fixed_users[user['username']] = {"new_username": new_user['username'],
                                                     "old_username": user['username'],
                                                     "email": user['email'],
                                                     "auth_service": new_user['auth_service']}
                    replace = obj.copy()
                    replace['user']['auth_service'] = new_user['auth_service']
                    if user['auth_service'] is not None:
                        replace['user']['auth_data'] = new_user['auth_data']
                        fixed_users[user['username']].update({"auth_data": new_user['auth_data']})
                    users_to_replace.append(replace['user']['username'])
                    replace['user']['username'] = new_user['username']
                    users.append(replace)
                else:
                    users.append(obj)


# list to contain all lines for the new file
new_export = []
# flag for checking if the users have already been added to the new file
users_added = False

with jsonlines.open('old.json') as old_reader:
    for obj in old_reader:
        if obj['type'] != 'team' and obj['type'] != 'user' and obj['type'] != 'channel' and obj['type'] != 'version':
            line = str(obj)
            for user in users_to_replace:
                new_user = f"'{fixed_users[user]['new_username']}'"
                user = f"'{user}'"
                line = line.replace(user, new_user)
                obj = ast.literal_eval(line)
        if obj['type'] == 'user' and users_added is False:
            users_added = True
            new_export += users
        elif obj['type'] != 'user':
            new_export.append(obj)

filename = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + ".json"

with jsonlines.open(filename, mode='w') as writer:
    for line in new_export:
        writer.write(line)
