from urllib.request import urlopen, Request
from bs4 import BeautifulSoup as bsoup

def main(status = -1, email = "", eStatus = 1):
    if status == -1:
        try: status = int(input("Enter 0 to start scraping, Enter 1 to add URLs to list.\n"))
        except ValueError: print("\nEnter a valid number!"); exit()
    if status == 1:
        inUrl = input("\nAmazon URL to scrape:\n")
        #print()
        with open("urls.txt", "a") as urls:
            urls.write(inUrl + "\n")
    elif status != 0:
        print(int(status))
        print("\nEnter a valid number!"); exit()
        
    try:
        with open("urls.txt", "r") as file:
            urls = file.readlines()
            if len(urls) == 0:
                print("\nNo links found in urls.txt! Terminating...")
            else:
                print("\nStarting scrape on", len(urls), "links from urls.txt...")
                for url in urls:
                    if urls.index(url) != 0: print("\nFetching info...")
                    checker(url)

def checker(url):
    #Disguising as normal browser for request
    try: req = Request(url, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'})
    except: print("\nInvalid URL found! Terminating..."); exit()
    page = urlopen(req).read().decode('utf-8')
    soup = bsoup(page, "html.parser")

    #Locating item name
    title = str(soup.find("span", class_ = "a-size-large product-title-word-break"))
    tInd2 = title.find("       </span")
    title = title[78:tInd2]
    #Prints first 64 chars of full item name
    print("\n" + title[:64] + "...")

    #Locating price
    price = str(soup.find("span", class_ = "a-offscreen"))
    pInd2 = price.find("</span>")
    #Converting price to float value
    try: price = float((price[27:pInd2]).replace(',', ''))
    except: print("Invalid URL found! Terminating..."); exit()
    #Re-formatting price for printing
    print("Current price: $" + f"{price:,{'.2f'}}")

if __name__ == "__main__":
    #No arguments passed
    if len(sys.argv) == 1:
        try: main()
        except KeyboardInterrupt: print("\nTerminating...")
    #One argument passed
    elif len(sys.argv) == 2:
        try:
            if int(sys.argv[1]) == 0 or int(sys.argv[1]) == 1:
                try: main(int(sys.argv[1]))
                except KeyboardInterrupt: print("\nTerminating...")
        except ValueError: print("Invalid argument!")
    else: print("Too many arguments!")
