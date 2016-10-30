**[+] Google Mass Explorer**

This is a automated robot for google search engine.

Make a google search, and parse the results for a especific exploit you define.
The options can be listed with --help parameter.

For python 3!!

**How to use:**

1 - Make a normal seach with google_explorer.py bot.

Ex: python google_explorer.py --browser='chrome' --dork='site:gob.ve inurl:index.php' --location="Venezuela"


2 - Run the exploit parsers to check if results can or not be vulnerable

Ex: $ cd xpl_parsers

    $ python joomla_cve_2015_8562.py

3 - Run the exploiter.py

Ex: $ cd exploits

    $ python exploiter.py --file <vuln file>
    
    
    







