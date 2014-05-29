# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 20:08:15 2014

@author: will
"""

from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
import re

from tutorial.items import NCAAItem

class DmozSpider(BaseSpider):
    name = "dmoz"
    baseurl = "http://home.uchicago.edu/~wmcfadden/teamsD3.html"
    allowed_domains = ["ncaa.org"]
    start_urls = [
        baseurl
    ]

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        if response.url!=baseurl:
            allconc = []
            for tr in hxs.select('//tr'):
                conc = []
                linked = False;
                for td in tr.select('td'):
                    tconc = '';                    
                    for t in td.select('.//text()').extract():  
                        tconc = tconc + re.sub('\s','',t)
                    conc.append(tconc);
                    v = td.select('a[contains(@href,"team/index")]/@href').extract()
                    if len(v)>0:
                        conc.append(v[0])
                        linked = True
                if linked and (conc[0]=="2013-14" or "/" in conc[0]):
                    allconc.append(conc)
            yield NCAAItem(value=allconc)
        else :
            for url in hxs.select('//a[contains(@href,"org_id")]/@href').extract():
                it = url.split('id=')[1]
                yield Request('http://stats.ncaa.org/player/game_by_game?game_sport_year_ctl_id=11540&org_id='+it+'&stats_player_seq=-100', callback=self.parse)
            