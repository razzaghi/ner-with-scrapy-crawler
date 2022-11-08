import csv
from pathlib import Path

import scrapy
from bs4 import BeautifulSoup


class DlapiperSpider(scrapy.Spider):
    name = "dlapiper"

    start_url = "https://www.dlapiper.com/en/us/"
    base_path = "https://www.dlapiper.com"
    checked_index = 0

    urls = ["https://www.dlapiper.com/en/us/"]
    crawled_urls = []
    fetched_urls = []

    work_category_header = ['category_type', 'category_name', 'category_level',
                            "category_short_description",
                            'address', 'body', "related_categories"]

    profile_category_header = ['title', 'contact_info', 'biography',
                               "related_categories", "links"]

    experience_header = ['title', 'description', 'related_categories', 'related_professionals',
                         'address']

    about_us_header = ['section_title', 'body', 'related_sections']

    contact_us_header = ["location", "contact_info", "description"]

    work_category_tags = ["service", "services", "solutions", "solution", "sector", "sectors"]
    profile_category_tags = ["people", "profile", "focus", "peoples", "profiles", "focuses"]
    experience_page_tags = ["insight", "insights"]
    about_us_page_tags = ["about", "about-us", "aboutus"]
    contact_us_page_tags = ["contact", "contacts", "contact-us", "office", "offices", "contactus", "location",
                            "locations"]

    work_category_file = open('work_category.csv', 'w', encoding="UTF-8")
    profile_category_file = open('profile_category.csv', 'w', encoding="UTF-8")
    experience_page_file = open('experience.csv', 'w', encoding="UTF-8")
    about_us_page_file = open('aboutus.csv', 'w', encoding="UTF-8")
    contact_us_page_file = open('contactus.csv', 'w', encoding="UTF-8")

    work_csv_writer = csv.writer(work_category_file)
    profile_csv_writer = csv.writer(profile_category_file)
    experience_csv_writer = csv.writer(experience_page_file)
    about_us_csv_writer = csv.writer(about_us_page_file)
    contact_us_csv_writer = csv.writer(contact_us_page_file)

    SCOPE_WORK_CATEGORY = 0
    SCOPE_PROFILE = 1
    SCOPE_EXPERIENCE = 2
    SCOPE_ABOUT_US = 3
    SCOPE_CONTACT_US = 4

    def start_requests(self):
        base_dir = Path(__file__).resolve().parent.parent.parent.parent

        xml_file_path = str(base_dir) + f"/sitemaps/{self.name}.csv"
        f = open(xml_file_path, encoding="UTF-8")
        csv_reader = csv.DictReader(f)

        self.work_csv_writer.writerow(self.work_category_header)
        self.profile_csv_writer.writerow(self.profile_category_header)
        self.experience_csv_writer.writerow(self.experience_header)
        self.about_us_csv_writer.writerow(self.about_us_header)
        self.contact_us_csv_writer.writerow(self.contact_us_header)

        for row in csv_reader:
            url = row["url"]
            yield scrapy.Request(url=url, callback=self.parse)

    def generate_email(self, text):
        return (str(text) + "@ysp.com").replace("\n", "")

    def enter_removal(self, text):
        return str(text).replace("\n", "")

    def text_normalizer(self, text):
        return str(text).replace("\n", "")

    def extract_url(self, response):
        print("---------------------- Start To Extract ----------------------")
        print(len(self.urls))
        for href in response.xpath('//a/@href').getall():
            if str(href).startswith("http") and str(href).startswith(self.base_path):
                if str(href).startswith("/") or str(href).startswith("http") and not str(href).__contains__(".pdf"):
                    if not str(href).__contains__(self.base_path):
                        url = self.base_path + href
                    else:
                        url = href
                    url = url.replace(":443", "")
                    url = url.replace("http://", "https://")

                    if not url in self.urls:
                        # print("================")
                        # print(url)
                        # print("================")
                        self.urls.append(url)

        for index, url in enumerate(self.urls):
            if index > self.checked_index:
                self.checked_index += 1
                if not url in self.crawled_urls:
                    self.crawled_urls.append(url)
                    yield scrapy.Request(url=url, callback=self.extract_url)

        if len(self.crawled_urls) == len(self.urls):
            print("=================== All URLS Fetched =================")
            print(len(self.urls))
            # for url in self.urls:
            #     yield scrapy.Request(url=url, callback=self.parse)

    def get_level(self, address: str):
        return len(address.split("/")) - 1

    def fetch_work_category(self, address, post_address, scope, category_type, body):
        work_category_header = ['category_type', 'category_name', 'category_level',
                                "category_short_description",
                                'address', 'body', "related_categories"]

        page_title_html = body.css("header h2.page-title").extract()[0]
        page_content_html = body.css(".page-content .col--main .rich-text").extract()
        page_content = None
        if page_content_html:
            page_content_html = page_content_html[0]
            page_content_soup = BeautifulSoup(page_content_html)
            page_content = page_content_soup.get_text()

        page_short_desc_html = body.css(".content h4").extract()
        category_short_description = None
        if page_short_desc_html:
            page_short_desc_html = page_short_desc_html[0]
            page_short_desc_soup = BeautifulSoup(page_short_desc_html)
            category_short_description = page_short_desc_soup.get_text()

        # related_services_html = body.css(".page-content .col--secondary .related-options").extract()[0]

        page_title_soup = BeautifulSoup(page_title_html)
        category_name = page_title_soup.get_text()

        if category_short_description is None:
            category_short_description = "-"

        level = self.get_level(post_address)

        return category_type, category_name, level, category_short_description, address, page_content, "-"

    def fetch_profile(self, address, post_address, scope, body):


        page_header_html = body.css("header.bio-header").extract()
        person_title_html = body.css("header.bio-header h3").extract()
        page_content_html = body.css(".page-content .col--main .rich-text").extract()
        page_content = None
        page_header = None
        person_title = None

        if page_header_html:
            page_header_html = page_header_html[0]
            page_header_soup = BeautifulSoup(page_header_html)
            page_header = page_header_soup.get_text()

        if person_title_html:
            person_title_html = person_title_html[0]
            person_title_soup = BeautifulSoup(person_title_html)
            person_title = person_title_soup.get_text()

        if page_content_html:
            page_content_html = page_content_html[0]
            page_content_soup = BeautifulSoup(page_content_html)
            page_content = page_content_soup.get_text()

        # related_services_html = body.css(".page-content .col--secondary .related-options").extract()[0]

        profile_category_header = ['title', 'contact_info', 'biography',
                                   "related_categories", "links"]
        return person_title, page_header, page_content, "-", "-"

    def fetch_experience(self, address, post_address, scope, body):

        page_title_html = body.css("h2.page-title").extract()[0]
        page_content_html = body.css(".page-content .col--main .rich-text").extract()
        page_content = None
        if page_content_html:
            page_content_html = page_content_html[0]
            page_content_soup = BeautifulSoup(page_content_html)
            page_content = page_content_soup.get_text()

        # related_services_html = body.css(".page-content .col--secondary .related-options").extract()[0]

        page_title_soup = BeautifulSoup(page_title_html)
        title = page_title_soup.get_text()

        experience_header = ['title', 'description', 'related_categories', 'related_professionals',
                             'address']
        return title, page_content, "-", "-", address


    def fetch_contact_us(self, address, post_address, scope, body):

        page_title_html = body.css("h2.page-title").extract()
        page_header_html = body.css("div.office-info").extract()
        page_content_html = body.css(".page-content .col--main .rich-text").extract()
        page_content = None
        page_header = None
        page_title = None

        if page_header_html:
            page_header_html = page_header_html[0]
            page_header_soup = BeautifulSoup(page_header_html)
            page_header = page_header_soup.get_text()

        if page_title_html:
            page_title_html = page_title_html[0]
            page_title_soup = BeautifulSoup(page_title_html)
            page_title = page_title_soup.get_text()

        if page_content_html:
            page_content_html = page_content_html[0]
            page_content_soup = BeautifulSoup(page_content_html)
            page_content = page_content_soup.get_text()

        contact_us_header = ["location", "contact_info", "description"]

        return page_title, page_header, page_content

    def parse(self, response, **kwargs):
        url = response.url
        post_address = str(url[len(self.start_url):len(url) + 1])
        scope = None

        category_type = None
        for tag in self.work_category_tags:
            if str(post_address).lower().__contains__(tag.lower()):
                scope = self.SCOPE_WORK_CATEGORY
                category_type = tag

        if scope is None:
            for tag in self.profile_category_tags:
                if str(post_address).lower().__contains__(tag.lower()):
                    scope = self.SCOPE_PROFILE
                    category_type = tag

        if scope is None:
            for tag in self.experience_page_tags:
                if str(post_address).lower().__contains__(tag.lower()):
                    scope = self.SCOPE_EXPERIENCE
                    category_type = tag

        if scope is None:
            for tag in self.about_us_page_tags:
                if str(post_address).lower().__contains__(tag.lower()):
                    scope = self.SCOPE_ABOUT_US
                    category_type = tag

        if scope is None:
            for tag in self.contact_us_page_tags:
                if str(post_address).lower().__contains__(tag.lower()):
                    scope = self.SCOPE_CONTACT_US
                    category_type = tag

        if scope is not None:
            body = response.css('body')
            if scope == self.SCOPE_WORK_CATEGORY:
                category_type, category_name, level, category_short_description, address, page_content, related_services = self.fetch_work_category(
                    response.url, post_address, scope, category_type, body)
                if page_content:
                    self.work_csv_writer.writerow([category_type, category_name, level, category_short_description, address, page_content,
                         related_services])
            if scope == self.SCOPE_PROFILE:
                title, contact_info, biography, related_categories, links = self.fetch_profile(
                    response.url, post_address, scope, body)
                if contact_info:
                    self.profile_csv_writer.writerow([title, contact_info, biography, related_categories, links])
            if scope == self.SCOPE_EXPERIENCE:
                title, description, related_categories, related_professionals, address = self.fetch_experience(
                    response.url, post_address, scope, body)
                if description:
                    self.experience_csv_writer.writerow([title, description, related_categories, related_professionals, address])
            if scope == self.SCOPE_CONTACT_US:
                page_title, page_header, page_content = self.fetch_contact_us(
                    response.url, post_address, scope, body)
                if page_content:
                    self.contact_us_csv_writer.writerow([page_title, page_header, page_content])
            print("==================================================")

        # for quote in response.css('div.post'):
        #     print("------------------------- yes 2 ----------------------------")
        #     username_html = quote.css('div.username').extract()
        #     title_html = quote.css('div.postTitle').extract()[0]
        #     body_html = quote.css('div.postBody').extract()[0]
        #     title_soup = BeautifulSoup(title_html)
        #     body_soup = BeautifulSoup(body_html)
        #     username = None
        #     if username_html:
        #         username_soup = BeautifulSoup(username_html[0])
        #         username = cleanmailtext(self.enter_removal(username_soup.get_text()))
        #     body = cleanmailtext(body_soup.get_text())
        #     title = cleanmailtext(self.enter_removal(title_soup.get_text()))
        #     post_date = cleanmailtext(quote.css('div.postDate::text').get())
        #     text = self.generate_email(username) + "\n" + title + "\n" + post_date + "\n" + body
        #     print(len(body))
        #     data = [username, title, post_date, body]
        #     self.csv_writer.writerow(data)
        # page = response.url.split("/")[-2]
        # filename = f'quotes-{page}.html'
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        # self.log(f'Saved file {filename}')
