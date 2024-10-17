import re
import os
from pathlib import Path
from edapi import EdAPI
from constants import NOTES_DIR, NEW_COURSE_ID as COURSE_ID


def find_files(path, pattern=r".*"):
    files = []
    for root, _, filenames in os.walk(path):
        for filename in filenames:
            if re.match(pattern, filename):
                files.append(os.path.join(root, filename))
    return files


def post_draft(ed, contents_file):
    '''
    return thread id
    '''
    contents = ''
    with open(contents_file, "r") as f:
        contents = f.read()

    path = Path(contents_file)
    title = path.parent.name

    thread = {
        "thread_draft": {
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
        }
    }

    try:
        t = ed.post_draft(COURSE_ID, thread)
        return t["id"]
    except Exception as e:
        raise e


def main():
    ed = EdAPI()
    ed.login()

    notes_raw = find_files(NOTES_DIR, r'.*\.html')

    for file in notes_raw:
        id = post_draft(ed, file)
        print(f"Posted Draft with thread ID: {id}")
        # schedule_draft(id, schedule_time, token)
        input("Press Enter to continue...")


if __name__ == "__main__":
    main()
