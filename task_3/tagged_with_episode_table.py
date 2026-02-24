import re
import os

import pywikibot
import mwparserfromhell

site = pywikibot.Site('en', 'wikipedia')

list_page = pywikibot.Page(site, 'User:Alex 21/sandbox/No episode table')
template_page = pywikibot.Page(site, "Template:Convert to Episode table")

WRITE_TO_FILE = False

TAG_STR = "{{Convert to Episode table}}\n"

tagged_with_table = set()

pages = list(template_page.getReferences(only_template_inclusion=True))

for page in pages:
    page: pywikibot.Page

    templates = tuple(page.title(with_ns=False) for page in page.itertemplates())

    if "Episode table" in templates:
        print("added", page.title())
        tagged_with_table.add(page.title())

tagged_with_table = sorted(tagged_with_table)

page_contents = \
f"""The following is a list of pages transcluding both {{{{tl|Convert to Episode table}}}} and {{{{tl|Episode table}}}}.

Last updated ~~~~~.

{'\n'.join(f"#[[{page}]]" for page in tagged_with_table)}
"""

if WRITE_TO_FILE:
    open("tagged_with_table.txt", "w").write(page_contents)
else:
    output_page = pywikibot.Page(site, "User:RustyBot/Pages using Episode table tagged with Convert to Episode table")
    output_page.text = page_contents
    output_page.save("Updating page list", bot=True)
