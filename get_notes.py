import os
import pandas as pd

from edapi import EdAPI
from ed_markdown_converter import EdTagsConverter
from constants import NOTES_DIR, OLD_COURSE_ID as COURSE_ID


# Create shorthand method for conversion
def md(html, **options):
    return EdTagsConverter(**options).convert(html)


def parse_date(timestamp):
    datetime = pd.to_datetime(timestamp)
    return datetime.tz_convert("America/Los_Angeles")


def main():
    ed = EdAPI()
    ed.login()

    notes = sorted(
        ed.list_all_threads(COURSE_ID),
        key=lambda a: parse_date(a["created_at"])
    )

    notes = list(filter(
        lambda a:
            a["type"] == "announcement" and a["category"] == "Lectures"
            and a["subcategory"] == "Notes",
        notes))

    for post in notes:
        title = post["title"]
        path = os.path.join(NOTES_DIR, f"{title}")
        os.makedirs(path, exist_ok=True)

        # raw HTML
        with open(os.path.join(path, "content.html"), "w") as f:
            f.write(post["content"])

        # Process Markdown
        image_path = os.path.join(path, "images")
        os.makedirs(image_path, exist_ok=True)
        with open(os.path.join(path, "content.md"), "w") as f:
            f.write(
                md(post["content"],
                   image_path=image_path,
                   download_images=True)
            )

        # Process with embedded images
        # NOTE: Use with caution. This creates quite large files, and Ed
        #       struggles with pasting them in.
        # with open(os.path.join(path, "content-embedded.md"), "w") as f:
        #     f.write(md(post["content"], embed_images=True))


if __name__ == "__main__":
    main()
    # convert_notes_to_md()
