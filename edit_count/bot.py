import pywikibot
site = pywikibot.Site('en', 'wikipedia')

## CONFIG ##

USERNAMES = [
    "Rusty Cat",
    "Rusty4321 Alt",
    "Rusty4321 Test",
    "Rusty Cat (mobile)"
]
WRITE_TO_WIKI_PAGE = True
WIKI_PAGE_TITLE = "User:Rusty Cat/edit count"
WIKI_EDIT_SUMMARY = "updating edit count (BOT)"

## END CONFIG ##

users = [
    pywikibot.page.User(site, user)
    for user in USERNAMES
]

total = 0

for user in users:
    total += user.editCount()

if WRITE_TO_WIKI_PAGE:
    page = pywikibot.Page(site, WIKI_PAGE_TITLE)
    page.text = str(total)
    page.save(WIKI_EDIT_SUMMARY)

