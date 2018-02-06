import os
from queue import Queue
from urllib.parse import urlparse
from threading import Thread
import requests
import threading
from requests import get
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from lxml import html as lh

lock = threading.Lock()

class TraceAxd():

    def __init__(self, filename):
        self.filename = filename
        self.urls = self.trace_axd()

    @staticmethod
    def banner():
        os.system('clear')
        print("\n")
        print(" █████╗ ███╗   ██╗ █████╗ ██████╗  ██████╗ ██████╗ ██████╗ ███████╗██████╗ ")
        print("██╔══██╗████╗  ██║██╔══██╗██╔══██╗██╔════╝██╔═══██╗██╔══██╗██╔════╝██╔══██╗")
        print("███████║██╔██╗ ██║███████║██████╔╝██║     ██║   ██║██║  ██║█████╗  ██████╔╝")
        print("██╔══██║██║╚██╗██║██╔══██║██╔══██╗██║     ██║   ██║██║  ██║██╔══╝  ██╔══██╗")
        print("██║  ██║██║ ╚████║██║  ██║██║  ██║╚██████╗╚██████╔╝██████╔╝███████╗██║  ██║")
        print("╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝")
        print("        Trace.axd Exposed Finder - anarcoder at protonmail.com\n") 

    def remove_duplicate_targets(self):
        results = [line.rstrip('\n') for line in open(self.filename)]
        domains = []
        targets = []
        try:
            for url in results:
                urlp = urlparse(url)
                if urlp.netloc not in domains:
                    domains.append(urlp.netloc)
                    targets.append(url)
        except Exception as e:
            pass
        return list(set(targets))

    def check_vuln(self, q):
        while True:
            #with lock:
                url = q.get()
                headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; '
                           'Linux x86_64; rv:41.0) Gecko/20100101 '
                           'Firefox/41.0'}
                try:
                    ms_xpath = "//*[text()[contains(.,'Microsoft .NET Framework Version:')]]"
                    req = get(url, headers=headers, verify=False, timeout=25)
                    options = lh.fromstring(req.content)
                    if options.xpath(ms_xpath):
                        with open('axd_sites.txt', 'a+') as f:
                            print('[+] \033[31mTarget vulnerable!! {0}\033[33m exposed..\033[39m\n'.format(req.url))
                            f.write(req.url + '\n')
                except Exception as e:
                    q.task_done()
                q.task_done()

    def trace_axd(self):
        self.banner()

        # Removing duplicate targets
        url_lists = self.remove_duplicate_targets()
        print(len(url_lists))

        # My Queue
        q = Queue(maxsize=0)

        # Number of threads
        num_threads = 10

        for url in url_lists:
            q.put(url)

        # My threads
        print('[+] Trying targets.. possible vulnerable will be saved in axd_sites.txt.. ')
        print('[*] Starting evil threads =)...\n')
        for i in range(num_threads):
            worker = Thread(target=self.check_vuln, args=(q,))
            worker.setDaemon(True)
            worker.start()

        q.join()


def main():
    filename = 'results_google_search.txt'
    TraceAxd(filename)


if __name__ == '__main__':
    main()
