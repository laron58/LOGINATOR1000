from bs4 import BeautifulSoup as bsoup
from urllib.request import urlopen, Request

#url = "https://www.amazon.com/dp/B0B6BYYNQS"
#url = "https://www.amazon.com/LG-Lightweight-Laptop-Platform-Windows/dp/B0BY3WCL4P/ref=sr_1_34?crid=1HLXB671VYABA&keywords=intel%2Blaptop&qid=1692988722&refinements=p_36%3A50000-100000&rnid=2421885011&s=pc&sprefix=intel%2Bl%2Caps%2C120&sr=1-34&th=1"
url = input("Amazon URL to scrape:\n")
req = Request(url, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'})

page = urlopen(req).read().decode('utf-8')
soup = bsoup(page, "html.parser")

title = str(soup.find("title"))
tInd2 = title.find('  </title>')
title = title[19:tInd2]
#print(title[:32])
print("\n" + title[:64] + "...")

price = str(soup.find("span", class_ = "a-offscreen"))
pInd2 = price.find("</span>")
try: price = float((price[27:pInd2]).replace(',', ''))
except: 
    print("Something went wrong!")
    exit()
#print(price)
print("Current price: $" + f"{price:,{'.2f'}}")

#title = 
#price = 
