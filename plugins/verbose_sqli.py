import os
import re
from queue import Queue
from urllib.parse import urlparse
from threading import Thread
import requests
import threading
from requests import get
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

lock = threading.Lock()

ERRORS = [r'\[(ODBC SQL Server Driver|SQL Server)\]', r'mysql_fetch_assoc',
          r'You have an error in your SQL syntax;',
          r'A syntax error has occurred', r'ADODB.Field error', r'ASP.NET is configured to show verbose error messages',
          r'ASP.NET_SessionId', r'Active Server Pages error', r'An illegal character has been found in the statement',
          r'An unexpected token "END-OF-STATEMENT" was found', r'CLI Driver', r'Can\'t connect to local', r'Custom Error Message',
          r'DB2 Driver', r'DB2 Error', r'DB2 ODBC', r'Died at', r'Disallowed Parent Path', r'Error Diagnostic Information',
          r'Error Message : Error loading required libraries.', r'Error Report', r'Error converting data type varchar to numeric',
          r'Incorrect syntax near',r'Invalid procedure call or argument', r'Invision Power Board Database Error', r'JDBC Driver', r'JDBC Error', r'JDBC MySQL',
          r'JDBC Oracle', r'JDBC SQL', r'Microsoft OLE DB Provider for ODBC Drivers', r'Microsoft VBScript compilation error',
          r'Microsoft VBScript error', r'MySQL Driver', r'MySQL Error', r'MySQL ODBC', r'ODBC DB2', r'ODBC Driver', r'ODBC Error',
          r'ODBC Microsoft Access', r'ODBC Oracle', r'ODBC SQL', r'ODBC SQL Server', r'OLE/DB provider returned message',
          r'ORA-0', r'ORA-1', r'Oracle DB2', r'Oracle Driver', r'Oracle Error', r'Oracle ODBC', r'PHP Error',
          r'PHP Parse error', r'PHP Warning', r'Parent Directory', r'Permission denied: \'GetObject\'',
          r'PostgreSQL query failed: ERROR: parser: parse error', r'SQL Server Driver\]\[SQL Server', r'SQL command not properly ended',
          r'SQLException', r'Supplied argument is not a valid PostgreSQL result', r'Syntax error in query expression', r'The error occurred in',
          r'The script whose uid is', r'Type mismatch', r'Unable to jump to row', r'Unclosed quotation mark before the character string',
          r'Unterminated string constant', r'Warning: Cannot modify header information - headers already sent',
          r'Warning: Supplied argument is not a valid File-Handle resource in', r'Warning: mysql_query()',
          r'Warning: pg_connect(): Unable to connect to PostgreSQL server: FATAL', r'You have an error in your SQL syntax near',
          r'data source=', r'detected an internal error \[IBM\]\[CLI Driver\]\[DB2/6000\]', r'include_path', r'invalid query',
          r'is not allowed to access', r'missing expression', r'mySQL error with query', r'mysql error', r'on MySQL result index',
          r'supplied argument is not a valid MySQL result resource', r'unexpected end of SQL command']

ERROR_RGX = [re.compile(error, re.IGNORECASE) for error in ERRORS]

class Sqli_Finder():

    def __init__(self, filename):
        self.filename = filename
        self.urls = self.sqli_f()

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
        print("           Verbose SQLi Plugin  - anarcoder at protonmail.com\n") 

    def remove_duplicate_targets(self):
        results = [line.rstrip('\n') for line in open(self.filename)]
        url_lists = []
        for url in results:
            try:
                urlp = urlparse(url)
                urlp = urlp.scheme + '://' + urlp.netloc + urlp.path + '?' + urlp.query
                url_lists.append(urlp)
            except Exception as e:
                pass
        url_lists = set(url_lists)
        url_lists = list(url_lists)
        return url_lists

    def insert_payloads(self, url_list):
        ret_list = []
        payloads = ["'","\"", "\\",";"]
        try:
            for url in url_list:
                urlq = urlparse(url)
                for par in urlq.query.split("&"):
                    for pay in payloads:
                        ret_list.append(url.replace(par,par+pay))
        except:
            pass
        return ret_list

    def check_vuln(self, q):
        while True:
            #with lock:
                url = q.get()
                headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; '
                           'Linux x86_64; rv:41.0) Gecko/20100101 '
                           'Firefox/41.0'}
                try:
                    req = get(url, headers=headers, verify=False, timeout=25)
                    with open('sqli_sites.txt','a+') as f:
                        for error in ERROR_RGX:
                            match = error.search(req.content.decode('utf-8'))
                            if match:
                                f.write(url+'\n')
                                match_res = match.group(0)
                                print('[+] {0} \033[31mPossible Vulnerable!!\033[33m error exposed..\033[39m'.format(url))
                except Exception as e:
                    q.task_done()
                q.task_done()

    def sqli_f(self):
        self.banner()

        # Removing duplicate targets
        url_lists = self.remove_duplicate_targets()
        print(len(url_lists))
        pay_list = self.insert_payloads(url_lists)

        # My Queue
        q = Queue(maxsize=0)

        # Number of threads
        num_threads = 10

        for url in pay_list:
            q.put(url)

        # My threads
        print('[+] Trying targets.. possible vulnerable will be saved in sqli_sites.txt.. ')
        print('[*] Starting evil threads =)...\n')
        for i in range(num_threads):
            worker = Thread(target=self.check_vuln, args=(q,))
            worker.setDaemon(True)
            worker.start()

        q.join()


def main():
    filename = 'results_google_search.txt'
    Sqli_Finder(filename)


if __name__ == '__main__':
    main()
