## Welcome to Google Explorer
# Special thanks to ArchStrike and BlackArch for supporting ;)
![ArchStrike](http://i.imgur.com/i0irzZJ.png) ![BlackArch](http://i.imgur.com/3JED0EN.png)


**[+] Google Mass Explorer (PYTHON 3.6)**

This is a automated robot for google search engine and a massive exploitation tool.

Make a google search and run a specific --plugin on the results. The dork you use is the key for success ;) .

The options can be listed with --help parameter.

Usage:

    google_explorer.py --dork=<arg> --browser=<arg> [--language=<arg>]
                                                    [--location=<arg>]
                                                    [--last_update=<arg>]
                                                    [--google_domain=<arg>]
                                                    [--proxy=<arg>]
    google_explorer.py --plugin=<arg>
    google_explorer.py --help
    google_explorer.py --version

Options:

    -h --help                                Open help menu
    -v --version                             Show version

Required options for search:

    --dork='google dork'                     your favorite g00gle dork :)
    --browser='browser'                      chrome
                                             chromium
                                             firefox

Required option for massive exploitation:

    --plugin='plugins filters list'          joomla_cve_2015_8562
                                             wordpress_cve_2015_1579
                                             joomla_cve_2016_8870
                                             apache_rce_struts2_cve_2017_5638
                                             jboss_finder
                                             cors_misc
                                             verbose_sqli
                                             trace_axd
                                             drupalgeddonrce2
                                             joomla_joomanage


Optional options for the search:

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

    --google_domain='google domain'          google domain to use on search.
                                             Ex: google.co.uk
    
    --proxy='ip:port'                        proxy ip:port



**Instalation:**

Install these packages:

    libxml2-dev libxslt1-dev python-dev


This project is developed in PYTHON 3.6 Make sure u use pip3 (package: python3-pip) to install dep:

    $ sudo pip3 install -r requirements


Make sure u have installed chromedriver(chrome and chromium) or geckodriver(firefox), if you don't have this tutorial can help:

    https://developers.supportbee.com/blog/setting-up-cucumber-to-run-with-Chrome-on-Linux/
    
    !!Install this version for stability: http://chromedriver.storage.googleapis.com/index.html?path=2.24/!!

The same commands for creating symbolic links can be used for geckodriver (firefox) install.


In some distro, i had some issues with users running browser driver as root.. **TO AVOID ISSUES, RUN THE TOOL AS REGULAR USER!!**



**How to use:**

Make a search with google bot, here are some examples:

    python3 google_explorer.py --browser='chrome' --dork='site:gob.ve inurl:index.php' --location="Venezuela"
    python3 google_explorer.py --dork="index.php?option=" --browser="chrome" --google_domain="google.co.il" --location="איחוד האמירויות הערביות"
    python3 google_explorer.py --browser='chrome' --dork='inurl:index.php?option' --location="Rússia" --last_update='na última semana'
    

Run the exploit filter for the specific vulnerability u are looking for, to check if results can or not be vulnerable:

    $ python3 google_explorer.py --plugin='joomla_cve_2015_8562'
    $ python3 google_explorer.py --plugin='apache_rce_struts2_cve_2017_5638'
    $ python3 google_explorer.py --plugin='exploit filter name from list'
    

**Exploits**

I'm using exploits from other authors, so don't take their credit on that! I put the same public exploit published, and i DON'T TAKE THE AUTHOR NAME FROM IT!! So any help with the exploit, you can look for the author =))
