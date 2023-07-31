from bs4 import BeautifulSoup
import requests
import smtplib
import time
import datetime
import csv

URL = "https://www.amazon.fr/Quatrevingt-Treize/dp/0274158426/ref=tmm_hrd_swatch_0?_encoding=UTF8&qid=1690821576&sr=8-16"
HEADERS = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5.2 Safari/605.1.15"}
EMAIL = 'lucas42Paris@gmail.com'

def get_page(url):
	return (requests.get(url, headers=HEADERS))

def parse_price(soup):
	price_text = soup.find(id="price").get_text()
	price = float(price_text.replace("€", "").replace("\xa0", "").strip()[1:].replace(",", "."))
	return (price)

def parse_title(soup):
	title = soup.find(id="productTitle").get_text().strip()
	return (title)

def write_to_csv(data):
	with open('AmazonWebScraping.csv', 'a+', newline='', encoding='UTF') as f:
		writer = csv.writer(f)
		writer.writerow(data)

def send_mail():
	server = smtplib.SMTP_SSL('smtp.gmail.com',465)
	server.ehlo()
	server.login(EMAIL,'xxxxxxxxxxxxxx')
	subject = "Quatrevingt Treize < 10 € !"
	body = ""
	msg = f"Subject: {subject}\n\n{body}"
	server.sendmail(EMAIL, EMAIL, msg)
	server.quit()

def check_price():
	page = get_page(URL)
	soup = BeautifulSoup(page.content, "lxml")

	title = parse_title(soup)
	price = parse_price(soup)
	todaydate = datetime.date.today()

	data = [title, price, todaydate]
	write_to_csv(data)

	if (price < 10):
		send_mail()

def main():
	while True:
		check_price()
		time.sleep(5)
		time.sleep(86400)

if __name__ == "__main__":
	main()
