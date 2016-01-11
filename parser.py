# -*- coding: utf-8 -*-
import urllib
import re
from lxml.html import parse, fromstring, html_parser
import parser_settings


# TESTS
def rename_later():
    url = 'http://www.mvideo.ru'
    page = parse(url).getroot()
    hrefs = page.xpath("//a[@class = 'header-nav-item-link']")
    for row in hrefs:
        # print row.get('href')
        sub_hrefs(url, row.get('href'))


def sub_hrefs(url, link):
    page = parse(url + link).getroot()
    hrefs = page.xpath("//ul[@class = 'unstyled sidebar-categories-list']/li/a")
    for row in hrefs:
        print row.get('href')


# def get_item(url, link, items_links):
#     page = parse(url + link + items_links).getroot()
#     item_name = page.xpath("//span[@class = 'text-cutter-wrapper']")
#     price = page.xpath("//strong[@class = 'product-price-current'")
def getitem():  # parse var 1
    catalog = {}
    url = 'http://www.mvideo.ru/noutbuki-planshety-komputery/noutbuki-118'
    page = parse(url).getroot()
    total_pages = page.xpath("//li[@class = 'pagination-item']/a/text()")
    # names = page.xpath("//a[@class = 'product-tile-title-link']")
    for i in range(1, int(total_pages[-1]) + 1):
        print i
        url_pagination = 'http://www.mvideo.ru/noutbuki-planshety-komputery/noutbuki-118/f/page=%s' % str(i)
        page_pagination = parse(url_pagination).getroot()
        names = page_pagination.xpath("//a[@class = 'product-tile-title-link']")
        prices = page_pagination.xpath("//div[@class = 'product-tile-checkout-section height-ready']"
                                       "/div[@class = 'product-price ']")
        print prices
        for price in prices:
            print price
        # for item in names:
            # print item.get('data-track-label')


def get_item():
    url = 'http://www.mvideo.ru/noutbuki-planshety-komputery/noutbuki-118'
    page = parse(url).getroot()
    total_pages = page.xpath("//li[@class = 'pagination-item']/a/text()")
    for i in range(1, int(total_pages[-1]) + 1):
        print i
        url_pagination = 'http://www.mvideo.ru/noutbuki-planshety-komputery/noutbuki-118/f/page=%s' % str(i)
        page_pagination = parse(url_pagination).getroot()
        item = page_pagination.xpath("//div[@class = 'product-tiles-list grid-view']")
        print item


# WORKING
def get_pages(url):
    page = parse(url).getroot()
    total_pages = page.xpath("//li[@class = 'pagination-item']/a/text()")
    return int(total_pages[-1])


class Item(object):
    # def __init__(self, **kw):
    #     for name, value in kw:
    #         setattr(self, name, value)
    pass


def get_item_name(elem, class_name):
    elems = elem.find_class(class_name)
    if elems:
        return elems[0].get('data-track-label')
    else:
        return 'none'


def get_item_price(elem, class_name):
    elems = elem.find_class(class_name)
    if elems:
        return elems[0].text_content()
    else:
        return 'none'


# clear name from russian words
def normalize_name(var):
    pt = re.compile(r'[a-zA-z-0-9]+')
    res = re.findall(pt, var)
    s = ' '.join(res)
    return s


def main(url):
    content = urllib.urlopen(url).read()
    doc = fromstring(content)
    data = []
    for el in doc.find_class('product-tile showcompare'):
        item = Item()
        name = get_item_name(el, 'product-tile-title-link')
        item.name = normalize_name(name)
        price = get_item_price(el, 'product-price-current')
        item.price = price
        item_lst = {}
        item_lst['name'] = item.name
        item_lst['price'] = item.price
        data.append(item_lst)
        del item_lst
        # print 'name: %s | prise: %s' % (item.name, item.price)
    return data


def get_all_items(url):
    all_items = []
    total_pages = get_pages(url)
    for i in range(1, total_pages + 1):
        # print i
        url_pagination = url + '/f/page=%s' % str(i)
        all_items += main(url_pagination)
        procent = (100.0/total_pages)
        print 'done: %f procent' % (float(procent * i))
    print all_items


def save_to_file_test(file_name, data):
    f = open(file_name, 'w')
    print >>f, ''
    f.close()


def parse_site(url):
    # url = 'http://www.mvideo.ru'
    page = parse(url).getroot()
    hrefs = page.xpath("//a[@class = 'header-nav-item-link']")
    for row in hrefs:
        # print row.get('href')
        sub_hrefs(url, row.get('href'))


def get_links(url):
    link_pattern = re.compile(r'([mM]enu[a-zA-z-_]+)|([Nn]av[a-zA-z-_]+)|([Nn]avigation)|([cC]atalog)')
    content = urllib.urlopen(url).read()
    doc = fromstring(content)
    print ' '*60 + url
    divs = doc.xpath('//div')
    for div in divs:
        div_class = div.get('class')
        if isinstance(div_class, str):
            found_class = re.findall(link_pattern, div_class)
            if found_class:
                get_child(div)


# рекурсивно обходит всех потомков для нахождения в них ссылок
def get_child(element):
    content = element.getchildren()
    for child in content:
        if child.get('href'):
            print child.get('href')
        get_child(child)


if __name__ == '__main__':
    url = 'http://www.mvideo.ru/noutbuki-planshety-komputery/noutbuki-118'
    # get_all_items(url)

    for company in parser_settings.COMPANY_LIST:
        get_links(company['URL'])

    # main(url)

    # rename_later()

    # stri = 'header-nav-wrap'
    # pt = re.compile(r'([mM]enu[a-zA-z-_]+)|([Nn]av)|([Nn]avigation)|([cC]atalog)')
    # print re.findall(pt, stri)

    # get_item()