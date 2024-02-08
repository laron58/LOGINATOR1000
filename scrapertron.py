from bs4 import BeautifulSoup as bsoup
from urllib.request import urlopen, Request

def checker(url):
    try: req = Request(url, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'})
    except: print("\nInvalid URL found! Terminating..."); exit()
    page = urlopen(req).read().decode('utf-8')
    soup = bsoup(page, "html.parser")

    title = str(soup.find("span", class_ = "a-size-large product-title-word-break"))
    tInd2 = title.find("       </span")
    title = title[78:tInd2]
    #print(title)
    print("\n" + title[:64] + "...")

    price = str(soup.find("span", class_ = "a-offscreen"))
    pInd2 = price.find("</span>")
    try: price = float((price[27:pInd2]).replace(',', ''))
    except: print("Invalid URL found! Terminating..."); exit()
    #print(price)
    print("Current price: $" + f"{price:,{'.2f'}}")

    #title = 
    #price = 

def main():
    status = 1
    while(status == 1):
        try: status = int(input("Enter 0 to start scraping, Enter 1 to add URLs to list.\n"))
        except ValueError: print("\nEnter a valid number!"); exit()
        if status == 1:
            inUrl = input("\nAmazon URL to scrape:\n")
            print()
            with open("urls.txt", "a") as urls:
                urls.write(inUrl + "\n")
        elif status != 0:
            print("\nEnter a valid number!"); exit()

    try:
        with open("urls.txt", "r") as file:
            urls = file.readlines()
            if len(urls) == 0:
                print("\nNo links found in urls.txt! Terminating...")
            else:
                report = open("report.txt", "w")
                report.close

                print("\nStarting scrape on", len(urls), "links from urls.txt...")
                for url in urls:
                    if urls.index(url) != 0: print("\nFetching info...")
                    checker(url)
    except FileNotFoundError:
        with open("urls.txt", "x") as file:
            print("\nNo file found! Add links to urls.txt!")

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt: print("\nTerminating...")
