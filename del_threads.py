import requests
import os

ids = [
    666422,
    666421,
    666420,
    666419,
    666417,
    666416,
    666415,
    666414,
    666413,
    666412,
    666411,
    666410,
    666409,
    666378,
    666366
]

COURSE_ID = 67447

SECRETS_DIR = os.path.join(os.path.expanduser("~"), ".secrets")
TOKEN_FILE = os.path.join(SECRETS_DIR, "ed_token")

ED_API_ROOT = 'https://us.edstem.org/api'
DRAFT_API = f'{ED_API_ROOT}/courses/{COURSE_ID}/thread_drafts'
SCHEDULE_API = f'{ED_API_ROOT}/thread_drafts/' + '{thread_id}/schedule'
THREADS_API = f"{ED_API_ROOT}/courses/{COURSE_ID}/threads"
API_TOKEN = './.ed_api_token'


def get_api_token():
    with open(API_TOKEN, "r") as f:
        return f.read().strip(" \n\t")


def main():
    token = get_api_token()
    for id in ids:
        print(f'processing id {id}... ', end='')
        r = requests.delete(
            'https://us.edstem.org/api/thread_drafts/' + f'{id}',
            headers={"Authorization": f"Bearer {token}"},
        )

        print(r.status_code)


if __name__ == "__main__":
    main()
