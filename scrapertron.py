from urllib.request import urlopen, Request
from bs4 import BeautifulSoup as bsoup
import sys

def main(status = -1):
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

    try:
        with open("priceLog.txt", "r+", encoding = "utf-8") as log:
            full = log.read()
            if title[:64] in full:
                lines = full.splitlines()
                #Reverse iteration through log to find most recent matching entry
                for line in reversed(lines):
                    #print(line)
                    if line.find(title[:64]) != -1:
                        lPrice = float(line.split('|', 1)[1])
                        #print(lPrice)
                        if price > lPrice:
                            print("Price increased by $" + f"{(price - lPrice):,{'.2f'}}" + "!")
                            log.write(title[:64] + "|" + str(price) + "\n")
                            break
                        elif price < lPrice:
                            print("Price decreased by $" + f"{(lPrice - price):,{'.2f'}}" + "!")
                            log.write(title[:64] + "|" + str(price) + "\n")
                            break
                        else: 
                            print("No change in price.")
                            break
            else: 
                print("No price history found.")
                log.write(title[:64] + "|" + str(price) + "\n")
    except FileNotFoundError:
        print("No price history found.")
        #Creates log if it didn't previously exist
        with open("priceLog.txt", "w", encoding = "utf-8") as log, open("report.txt", "a", encoding = "utf-8") as report:
            log.write(title[:64] + "|" + str(price) + "\n")
            
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
