# -*- coding: utf-8 -*-

__author__ = 'massimo'

import urllib2
import util
import thread
import sched
import datetime


class Miner:
    def __init__(self, url):
        self.start = url
        self.tasks = {url: 0}
        self.result = {}
        self.shed = sched.scheduler
        self.last_show_status_time = datetime.datetime.now()

    def run(self):
        thread.start_new_thread(self.status, ())
        while True:
            try:
                link = self.tasks.popitem()
                self.resolve(link[0])
            except KeyError as e:
                print e
                break

    def status(self):
        while True:
            if self.last_show_status_time < datetime.datetime.now() - datetime.timedelta(seconds=3):
                self.last_show_status_time = datetime.datetime.now()
                print self.result

    def resolve(self, url):
        try:
            response = urllib2.urlopen(url)
            self.result[url] = response.getcode()

            html = response.read()
            all_links = util.pull_out_all_links(html)
            if len(all_links) > 0:
                for link in all_links:
                    if link not in self.result and link not in self.tasks:
                        self.tasks[link] = 0

            response.close()
        except urllib2.URLError as e:
            if hasattr(e, "code"):
                self.result[url] = e.code
            print e


if __name__ == "__main__":
    miner = Miner("http://mockplus.cn")
    miner.run()
    print "all done"