import requests
import os
from pathlib import Path
import re



COURSE_ID = 67447

SECRETS_DIR = os.path.join(os.path.expanduser("~"), ".secrets")
TOKEN_FILE = os.path.join(SECRETS_DIR, "ed_token")

ED_API_ROOT = 'https://us.edstem.org/api'
DRAFT_API = f'{ED_API_ROOT}/courses/{COURSE_ID}/thread_drafts'
SCHEDULE_API = f'{ED_API_ROOT}/thread_drafts/' + '{thread_id}/schedule'
THREADS_API = f"{ED_API_ROOT}/courses/{COURSE_ID}/threads"
API_TOKEN = './.ed_api_token'


def post_draft(contents_file, token):
    '''
    return thread id
    '''
    contents = ''
    with open(contents_file, "r") as f:
        contents = f.read()

    # request = {
    #     "thread_draft": {
    #         "course_id": COURSE_ID,
    #         "title": "testing",
    #         "type": "post",
    #         "category": "General",
    #         "contents": contents,
    #         "subcategory": "",
    #         "subsubcategory": "",
    #         "is_pinned": True,
    #         "is_private": True,
    #         "is_anonymous": False,
    #         "is_megathread": True,
    #         "anonymous_comments": True,
    #     }
    # }
    path = Path(contents_file)
    title = path.parent.name

    request = {"thread_draft": {
        "course_id": COURSE_ID,
        "type": "post",
        "title": title,
        "content": contents,
        "category": "General",
        "subcategory": "",
        "subsubcategory": "",
        "is_pinned": False,
        "is_private": False,
        "is_anonymous": False,
        "is_megathread": False,
        "anonymous_comments": False,
    }}

    r = requests.post(
        DRAFT_API,
        headers={"Authorization": f"Bearer {get_api_token()}"},
        json=request
    )

    if r.status_code == 201:
        response = r.json()
        return response["thread_draft"]["id"]

    raise Exception(f"Failed to post draft: {r.status_code} {r.text}")


def schedule_draft(thread_id, datetime, token):
    payload = {
        "send_emails": 1,
        "scheduled_time": datetime,
    }

    r = requests.patch(
        SCHEDULE_API.format(thread_id=thread_id),
        headers={"Authorization": f"Bearer {get_api_token()}"},
        params=payload
    )

    if r.status_code != 200:
        raise Exception(f"Failed to schedule draft: {r.status_code} {r.text}")


def get_token():
    if not os.path.isfile(TOKEN_FILE):
        token = input("Enter a Ed Token (ask Hunter if you don't know how): ")
        os.makedirs(SECRETS_DIR, exist_ok=True)
        with open(TOKEN_FILE, "w") as f:
            f.write(token)

    with open(TOKEN_FILE, "r") as f:
        return f.read().strip(" \n\t")


def get_api_token():
    with open(API_TOKEN, "r") as f:
        return f.read().strip(" \n\t")


def find_files(path, pattern=r".*"):
    files = []
    for root, dirs, filenames in os.walk(path):
        for filename in filenames:
            if re.match(pattern, filename):
                files.append(os.path.join(root, filename))
    return files


def main():
    # schedule_time = '2024-10-17T16:00:00.000Z'
    token = get_token()
    notes_raw = find_files("./notes/", r'.*\.html')

    for file in notes_raw:
        id = post_draft(file, token)
        print(f"Posted Draft with thread ID: {id}")
        # schedule_draft(id, schedule_time, token)
        input("Press Enter to continue...")


if __name__ == "__main__":
    main()



