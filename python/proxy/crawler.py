from pyquery import PyQuery as pq
import requests
import re
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36"}


class ProxyMetaClass(type):
    def __new__(cls, name, bases, attrs):
        count = 0
        attrs["__CrawlFunc__"] = []
        for k, v in list(attrs.items()):
            if "crawl_" in k:
                attrs["__CrawlFunc__"].append(k)
                count += 1
            attrs["__CrawlFuncCount__"] = count
        return type.__new__(cls, name, bases, attrs)


class crawler(object, metaclass=ProxyMetaClass):
    def get_proxies(self, callback):
        proxies = []
        for proxy in eval("self.{}()".format(callback)):
            print("成功获取到代理", proxy)
            proxies.append(proxy)
        return proxies

    def crawl_daili66(self, pages=4):
        for page in range(1, pages+1):
            url = f"http://www.66ip.cn/{page}.html"
            print("Crawling  ", url)
            htm = requests.get(url).text
            doc = pq(htm)
            trs = doc("table tr:gt(0)").items()
            for tr in trs:
                ip = tr.find("td:nth-child(1)").text()
                port = tr.find("td:nth-child(2)").text()
                yield ":".join([ip, port])

    def crawl_xici(self):
        urls = ["https://www.xicidaili.com/nn", "https://www.xicidaili.com/nt"]
        for url in urls:
            print("Crawling  ", url)
            htm = requests.get(url, headers=headers).text
            doc = pq(htm)
            trs = doc("table tr:gt(0)").items()
            for tr in trs:
                ip = tr.find("td:nth-child(2)").text()
                port = tr.find("td:nth-child(3)").text()
                yield ":".join([ip, port])

    def crawl_kuaidaili(self):
        BASE_URL = 'https://www.kuaidaili.com/free/inha/{page}/'
        urls = [BASE_URL.format(page=page) for page in range(1, 10)]
        for url in urls:
            print("Crawling  ", url)
            try:
                html = requests.get(url, headers=headers, timeout=1).text
                doc = pq(html)
                for item in doc('table tr').items():
                    td_ip = item.find('td[data-title="IP"]').text()
                    td_port = item.find('td[data-title="PORT"]').text()
                    if td_ip and td_port:
                        yield ":".join([td_ip, td_port])
            except:
                pass

    def crawl_66ip(self):
        BASE_URL = 'http://www.66ip.cn/{page}.html'
        MAX_PAGE = 5
        urls = [BASE_URL.format(page=page) for page in range(1, MAX_PAGE + 1)]
        for url in urls:
            try:
                html = requests.get(url, headers=headers, timeout=3).text
                doc = pq(html)
                trs = doc('.containerbox table tr:gt(0)').items()
                for tr in trs:
                    host = tr.find('td:nth-child(1)').text()
                    port = int(tr.find('td:nth-child(2)').text())
                    yield ":".join([host, port])
            except:
                pass

    def crawl_ip3366(self):
        MAX_PAGE = 5
        BASE_URL = 'http://www.ip3366.net/free/?stype=1&page={page}'
        urls = [BASE_URL.format(page=i) for i in range(1, 8)]
        for url in urls:
            html = requests.get(url, headers=headers, timeout=2).text
            ip_address = re.compile('<tr>\s*<td>(.*?)</td>\s*<td>(.*?)</td>')
            re_ip_address = ip_address.findall(html)
            for address, port in re_ip_address:
                yield ":".join([address.strip(), port.strip()])
