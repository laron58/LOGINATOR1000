from urllib.request import urlopen, Request
from bs4 import BeautifulSoup as bsoup
import smtplib
from datetime import datetime
import sys

# Assigns default values if nothing is passed from command line
def main(status = -1, email = "", eStatus = 1):
    if status == -1:
        # Prompts for 0/1 if not passed through console
        try: status = int(input("Enter 0 to start scraping, Enter 1 to add URLs to list.\n"))
        except ValueError: print("\nEnter a valid number!"); exit()
    if status == 1:
        inUrl = input("\nAmazon URL to scrape:\n")
        # print()
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
                # Wipes report
                report = open("report.txt", "w")
                report.close

                print("\nStarting scrape on", len(urls), "links from urls.txt...")
                for url in urls:
                    if urls.index(url) != 0: print("\nFetching info...")
                    scrape(url)
                
                # Email report module
                if email == "0": exit()
                elif email == "":
                    # Prompts for 0/1 and email if no email is given via console 
                    try: eStatus = int(input("\nEnter 0 to generate report.txt only, Enter 1 to email report.\n"))
                    except ValueError: print("\nNot a number! Generated report only."); exit()
                if eStatus == 1:
                    if email == "": email = input("\nEnter email address: ")
                    print("\nSending email...")
                    # Starting SMTP email service
                    s = smtplib.SMTP("smtp.gmail.com", 587)
                    s.starttls()
                    s.login("scrapertron1@gmail.com", "bpuwyrbgjsdqggwn")
                    with open("report.txt", "r", encoding = "utf-8") as report:
                        body = report.read()
                        subject = "Report for " + str(len(urls)) + " items on " + str(datetime.now())[:19]
                        content = f"Subject: {subject}\n{body}"
                        try: 
                            s.sendmail("scrapertron1@gmail.com", email, content.encode("utf-8"))
                            print("\nEmail sent! Check your spam folder.")
                        except smtplib.SMTPRecipientsRefused: 
                            print("\nInvalid email! Terminating...")
                    s.quit()
                elif eStatus != 0:
                    print("\nInvalid number! Generated report only.")
    except FileNotFoundError:
        # Creates file if it didn't previously exist
        with open("urls.txt", "x") as file:
            print("\nNo file found! Add links to urls.txt!")

def scrape(url):
    # Disguising as normal browser for request
    try: req = Request(url, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'})
    except: print("\nInvalid URL found! Terminating..."); exit()
    page = urlopen(req).read().decode('utf-8')
    # Parses HTML
    soup = bsoup(page, "html.parser")

    # Locating item name
    title = str(soup.find("span", class_ = "a-size-large product-title-word-break"))
    tInd2 = title.find("       </span")
    title = title[78:tInd2]
    # Prints first 64 chars of full item name
    print("\n" + title[:64] + "...")

    # Locating price
    price = str(soup.find("span", class_ = "a-offscreen"))
    pInd2 = price.find("</span>")
    # Converting price to float value
    try: price = float((price[27:pInd2]).replace(',', ''))
    except: print("Invalid URL found! Terminating..."); exit()
    # Re-formatting price for printing
    print("Current price: $" + f"{price:,{'.2f'}}")

    # Writing to log & report
    try:
        log = open("priceLog.txt", "r+", encoding = "utf-8")
    except FileNotFoundError:
        # Creates log if it didn't previously exist
        log = open("priceLog.txt", "w", encoding = "utf-8")
    with open("priceLog.txt", "r+", encoding = "utf-8") as log, open("report.txt", "a", encoding = "utf-8") as report:
        report.write(f"\n{url}{title[:64]}...\nCurrent price: ${price:,.2f}\n")
        full = log.read()
        if title[:64] in full:
            lines = full.splitlines()
            # Reverse iteration through log to find most recent matching entry
            for line in reversed(lines):
                # print(line)
                if line.find(title[:64]) != -1:
                    lPrice = float(line.split('|', 1)[1])
                    # print(lPrice)
                    if price == lPrice:
                        print("No change in price.")
                        report.write("No change in price.\n")
                        break
                    else:
                        if price > lPrice:
                            change = "increased"
                        elif price < lPrice:
                            change = "decreased"
                        print(f"Price {change} by ${abs(price - lPrice):,.2f}!")
                        report.write(f"Price {change} by ${abs(price - lPrice):,.2f}!\n")
                        log.write(f"{title[:64]}|{price}\n")
                        break
        else: 
            print("No price history found.")
            report.write("No price history found.\n")
            log.write(f"{title[:64]}|{price}\n")

# Command line arguments
if __name__ == "__main__":
    # No arguments passed
    if len(sys.argv) == 1:
        try: main()
        except KeyboardInterrupt: print("\nTerminating...")
    # One argument passed (0 or 1)
    elif len(sys.argv) == 2:
        try:
            if int(sys.argv[1]) == 0 or int(sys.argv[1]) == 1:
                try: main(int(sys.argv[1]))
                except KeyboardInterrupt: print("\nTerminating...")
        except ValueError: print("Invalid argument!")
    # Two arguments passed (0 or 1 and email)
    elif len(sys.argv) == 3:
        try:
            if int(sys.argv[1]) == 0 or int(sys.argv[1]) == 1:
                try: main(int(sys.argv[1]), sys.argv[2])
                except KeyboardInterrupt: print("\nTerminating...")
        except ValueError: print("Invalid argument!")
    else: print("Too many arguments!")
