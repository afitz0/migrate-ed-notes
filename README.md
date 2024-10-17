# Tool to migrate posts from one Ed class to Another

## Installation

0. Recommended to use in a virtual environment. Set one up with

```
python3 -m venv .venv
source .venv/bin/activate
```

(Note: These scripts and the edapi dependency were developed using Python 3.12. No backwards compatibility guarantee is made.)

1. Then, install requirements with:

```
pip install -r requirements.txt
```

2. If you haven't already, go to https://edstem.org/us/settings/api-tokens and generate an API token.

Copy the token and save it to a .env file in the same directory as this script. It should be set as
an environment variable called `ED_API_TOKEN`.

3. Open `constants.py` and update the notes directory and course IDs as appropriate.

## Synopsis

Running `get_notes.py` with no other changes will create `NOTES_DIR` if necessary, and populate it with one subdir per post. Posts are filtered as type announcement, under category Lecture, subcategory Notes. Content is saved as both the "html" file and a conversion to markdown.

Running `upload_drafts.py` will upload all the notes in `NOTES_DIR` to Ed as drafts. It searches for all html files, and uses the parent directory names as the post title. For example, given:

```
NOTES_DIR/
    Lecture 1/
        lecture1.html
```

A draft post in your course will be created title "Lecture 1" using the content of `lecture1.html`.

### Note on Ed's Post Content

Ed, for whatever reason, saves posts as an XML document that looks a lot like HTML, but with some differences. For example, it has the following tag equivalencies:

* `link` -> `a`
* `image` -> `img`
* `paragraph` -> `p`
* `heading` -> ``h1`, `h2`, `h3`, `h4`, `h5`, `h6`
* `break` -> `br`
* `bold` -> `b`, `strong`

There are likely more, but these are the ones I've seen and added to the Ed markdown converter.

As such, the Ed markdown converter is not perfect, and will not perfectly convert Ed posts to perfect markdown. It's included just in case it's good enough.

## Changes you may want to make

... TODO