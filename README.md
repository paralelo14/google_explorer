**[+] Google Mass Explorer (PYTHON 3)**

This is a automated robot for google search engine.

Make a google search, and parse the results for a especific exploit you define.
The options can be listed with --help parameter.

Usage:

    google_explorer.py --dork=<arg> --browser=<arg> [--exploit_parser=<arg>]
                                                    [--language=<arg>]
                                                    [--location=<arg>]
                                                    [--last_update=<arg>]
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

    --google_domain='google domain'          google domain to use on search.
                                             Ex: google.co.uk


**How to use:**

Make a search with google bot:

    python google_explorer.py --browser='chrome' --dork='site:gob.ve inurl:index.php' --location="Venezuela"
    

Run the exploit parsers to check if results can or not be vulnerable:

    $ cd xpl_parsers

    $ python joomla_cve_2015_8562.py

Run the exploiter.py (if the original exploit is runned by command line - READ THE EXPLOIT):

    $ cd exploits

    $ python exploiter.py --file <vuln file>
    

**Exploits**

I'm using exploits from other authors, so don't take their credit on that! I put the same public exploit published, and i DON'T TAKE THE AUTHOR NAME FROM IT!! So any help with the exploit, you can look for the author =))



    
    







