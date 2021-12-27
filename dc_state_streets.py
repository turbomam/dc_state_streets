from urllib import request
from urllib.request import Request, urlopen
import bs4.element
from bs4 import BeautifulSoup
import re

# how authoritative are these?
# use a geographical API or Wikidata?
dc_streets_url = "https://geographic.org/streetview/usa/dc/washington.html"
states_url = "https://wordcounter.net/blog/2016/04/27/101535_alphabetical-list-50-states.html"

page = request.urlopen(dc_streets_url)
soup = BeautifulSoup(page, features="html.parser")

# assuming we magically know the number of the desired lists
street_list = soup.select("ul")[0]
street_tags = street_list.select("a")
street_names = [i.string for i in street_tags]

no_sector = [re.sub(' NE$| SE$| SW$| NW$', '', i) for i in street_names]
# discovered these by inspection
# there are also some prefixes like E
no_type = [
    re.sub(
        ' Alley$| Avenue$| Circle$| Court$| Ct$| Drive$| Drive| Fwy$| Lane$| Pkwy$| Pl$| Place$| Road$| Row$| Square$| Street.*$| Ter$| Walk$ Way$',
        '', i)
    for i in no_sector]
no_type = list(set(no_type))
no_type.sort()

# 403 if no user agent asserted
req = Request(states_url, headers={'User-Agent': 'Mozilla/5.0'})
page = urlopen(req).read()
soup = BeautifulSoup(page, features="html.parser")

street_list = []

# more magic knowledge
states_p = soup.select("p")[2]
for i in states_p:
    if isinstance(i, bs4.element.NavigableString):
        j = i.lstrip().rstrip()
        street_list.append(j)

streets_set = set(no_type)
states_set = set(street_list)

no_street = list(states_set - streets_set)
no_street.sort()

print(f"{len(no_street)} STATES WITH NO STREET IN WASHINGTON DC")
print(no_street)
print("\n")

with_street = list(states_set.intersection(streets_set))
with_street.sort()

print(f"{len(with_street)} STATES WITH A STREET IN WASHINGTON DC")
print(with_street)
print("\n")

matching = [s for s in street_names if any(xs in s for xs in street_list)]
# print(matching)
matching = list(set(matching))
matching.sort()

for i in matching:
    print(i)
