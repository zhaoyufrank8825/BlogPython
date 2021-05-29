import requests
from bs4 import BeautifulSoup


request = requests.get("https://www.johnlewis.com/anyday-john-lewis-partners-hinton-office-chair/black/p4201464")
soup = BeautifulSoup(request.content, "html.parser")
element = soup.find("p", {"class":"price price--large price--large--anyday"})
string_price = element.text.strip()
price = float(string_price[1:])

print("the item price is "+str(price))


