# Fix Mattermost users during bulk export migration

If you want to integrate multiple mattermost servers into one it can happen that users exist on both the old and the new server.
However Mattermost only allows one email address to be assigned to a single user at any time. 
So if those same users have different usernames you're in trouble.
This script fixes the users by reading an export file from both the new and old server and then replaces all occurences of the old username with the new one.

## Notes

This script should never overwrite any existing exports. However it is strongly advised to make backups before running the script.

## Setup

This script assumes python3 and pip is installed.

`pip install -r requirements.txt`

## Usage

`python3 fix_users.py old.jsonl new.jsonl`

If the script ran successfully you should receive a file with a timestamp from the time you ran the script.