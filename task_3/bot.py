import re
import os

import pywikibot
import mwparserfromhell

site = pywikibot.Site('en', 'wikipedia')

list_page = pywikibot.Page(site, 'User:Alex 21/sandbox/No episode table')

PAGE_LIMIT = 50
DRY_RUN = False

TAG_STR = "{{Convert to Episode table}}\n"

page_count = 0

def index_or_none(a, b):
    try:
        return a.index(b)
    except:
        return None

hatnote_templates = open(os.path.join(os.path.dirname(__file__), 'hatnote_templates.txt')).read().rstrip().split('\n')

for page in list_page.linkedPages(
    namespaces=[0], follow_redirects=True, content=True, total=None
    ):

    templates = page.templates()

    if "Convert to Episode table" in (page.title(with_ns=False) for page in templates):
        print('Already tagged')
        continue

    if PAGE_LIMIT > 0 and page_count >= PAGE_LIMIT:
        print('Page limit reached')
        break

    original_text = page.text

    page: pywikibot.Page

    # MOS:SECTIONORDER
    
    parsed_text = mwparserfromhell.parse(page.text)
    if (m := next((t for t in parsed_text.ifilter_templates() if t.name.lower() == 'multiple issues'), None)):
        m.get('1').value.append(TAG_STR)
    # After hatnote, if present
    elif (m := next((t.name.lower() in hatnote_templates for t in parsed_text.ifilter_templates()), None)):
        parsed_text.insert_after(m, TAG_STR)
    # After DISPLAYTITLE, if present
    elif (m := next(
            (t 
            for t in parsed_text.ifilter_templates() if (t.name.lower() in ('displaytitle', 'italic title', 'lowercase title'))
    ), None)):
        parsed_text.insert_after(m, TAG_STR)
    # Before English variety / date format, if present
    elif (m := next(
            (t
            for t in parsed_text.ifilter_templates()
            if (re.search(r'[u]se [dmy]{3} dates|[u]se [W][w]+ English', t.name.lower()))), None)):
        parsed_text.insert_before(m, TAG_STR)
    # After short description, if present
    elif (m := next((t for t in parsed_text.ifilter_templates() if t.name.lower() == 'short description'), None)):
        parsed_text.insert_after(m, TAG_STR)
    else:
        parsed_text.insert(0, TAG_STR)

    page.text = str(parsed_text)
    if DRY_RUN:
        print("Would have saved ", page.title())
    else: 
        page.save(summary='Tagging page with {{[[Template:Convert to Episode table|Convert to Episode table]]}} (Task 4 trial)', minor=True, bot=True)

    page_count += 1
