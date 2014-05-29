bracket-madness
===============

A NCAA data crawler and a rudimentary ranking system for NCAA bracket teams

a simple ranker (loaddata.py)
===============

This works by making a random guess at each teams worth (between -1 and 1) and then it compares teams who played each other to adjust every teams rank based on playing and beating good teams.  This is probably some implementation of some entry level machine learning, but I'm just making shit up really.  

a complex ranker (loaddata_advanced.py)
================
The idea (in everything that was commented out) was to make some sort of per-possession outcome predictor based on some input defensive and offensive stats from each team.  Then it would just be a matter of adjusting the stats to reflect the individual matchups.  

This didn't work better than the simple one so I scrapped it, but the idea is there for anyone else to try.

ADDING NEW CRAWLED DATA
=======================

The files outputD1.json outputD2.json and outputD3.json contain D1, D2, and D3 team basketball stats from the 2012-2013 season.

If you want to generate your own stats files you can use the scraper provided.  You need to edit the file "dmoz_spider.py" by changing baseurl to a site of your choosing that contains a links to all of the team pages (i.e. http://stats.ncaa.org/team/index/11540?org_id=)

after that you can run

scrapy crawl dmoz -o youroutputfilename.json -t json

and edit loaddata.py to refer to whatever youroutputfilename.json was
