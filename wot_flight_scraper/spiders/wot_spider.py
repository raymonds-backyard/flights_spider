import scrapy
import datetime


class WotSpider(scrapy.Spider):
    name = "wot_spider"
    current_date = datetime.datetime.now()
    cities = ['Gold Coast', 'Bali', 'Vancouver', 'Saigon', 'Tokyo', 'Paris', 'Bangkok', 'San Francisco', 'Bogota'
        , 'Santiago', 'Moscow']
    start_urls = []
    for dest in cities:
        crawl_date = current_date + datetime.timedelta(days=1)
        for i in range(150):  # Number of days in the future to search for
            departure_day = str(crawl_date.day)
            departure_month = str(crawl_date.month)
            departure_year = str(crawl_date.year)
            start_urls.append(
                "https://www.wotif.co.nz/Flights-Search?flight-type=on&starDate="+departure_day+"%2F"+departure_month
                + "%2F" + departure_year + "&_xpid=11905%7C1&mode"
                "=search&trip=oneway&leg1=from%3AAuckland%2C+New+Zealand+%28AKL-Auckland+Intl.%29%2Cto%3A" + dest +
                "%2C%28%29%2Cdeparture%3A14%2F08%2F2018TANYT&passengers="
                "children%3A0%2Cadults%3A1%2Cseniors%3A0%2Cinfantinlap%3AY")
            crawl_date = crawl_date + datetime.timedelta(days=1)

    def parse(self, response):
        current_crawl_date = self.crawl_date
        hxs = scrapy.Selector(response)
        origin = hxs.xpath('//span[@class = "origin"]/text()').extract_first().strip()
        destination = hxs.xpath('//span[@class = "destination"]/text()').extract_first().strip()
        airline = hxs.xpath('//ul[@id = "flightModuleList"]/li//div[@data-test-id="airline-name"]/text()').extract_first().strip()
        depart_time = hxs.xpath('//ul[@id = "flightModuleList"]/li//span[@data-test-id="departure-time"]/text()').extract_first()
        arrival_time = hxs.xpath('//ul[@id = "flightModuleList"]/li//span[@data-test-id="arrival-time"]/text()').extract_first()
        duration = hxs.xpath('//ul[@id = "flightModuleList"]/li//span[@data-test-id="duration"]/text()').extract_first().strip()
        stops = hxs.xpath('//ul[@id = "flightModuleList"]'
                          '/li//span[@data-test-id="duration"]/following-sibling::span/text()').extract_first().strip()
        price = hxs.xpath('//ul[@id = "flightModuleList"]/li//span[@data-test-id="listing-price-dollars"]/text()').extract_first()

        scraped_info = dict(extraction_date=WotSpider.current_date.strftime("%Y-%m-%d")
                            , departure_date=current_crawl_date.strftime("%Y-%m-%d")
                            , origin=origin
                            , destination=destination
                            , airline=airline
                            , depart_time_local=depart_time
                            , arrival_time_local=arrival_time
                            , stops=stops
                            , duration=duration
                            , price=price)
        yield scraped_info

        if self.crawl_date - self.current_date < datetime.timedelta(2):
            self.increment_crawl_date()

            departure_day = str(current_crawl_date.day)
            departure_month = str(current_crawl_date.month)
            departure_year = str(current_crawl_date.year)
            next_url = "https://www.wotif.co.nz/Flights-Search?flight-type=on&starDate="+departure_day+"%2F"\
                + departure_month + "%2F" + departure_year + "&_xpid=11905%7C1&mode=search&trip=oneway&leg1=from%3AAuckland%2C+New+Zealand+%28AKL-Auckland+Intl.%29%2Cto%3A"\
                + destination + "%2C%28%29%2Cdeparture%3A14%2F08%2F2018TANYT&passengers=children%3A0%2Cadults%3A1%2Cseniors%3A0%2Cinfantinlap%3AY"
            yield scrapy.Request(next_url, callback=self.parse)

    def increment_crawl_date(self):
        self.crawl_date = self.crawl_date + datetime.timedelta(days=1)




