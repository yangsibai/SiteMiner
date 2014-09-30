# -*- coding: utf-8 -*-

__author__ = 'massimo'

import urllib2
import util
import thread
import sys
import time


class Miner:
    def __init__(self, url):
        self.start = url
        self.tasks = set()
        self.tasks.add(url)
        self.resolved = set()
        self.result = {}

    def run(self):
        thread.start_new_thread(self.status, ())
        while True:
            try:
                link = self.tasks.pop()
                self.resolve(link)
            except KeyError as e:
                print e
                break

    def status(self):
        while True:
            print '-' * 30
            for k, v in sorted(self.result.items()):
                print k, len(v)
            print '-' * 30
            time.sleep(5)

    def resolve(self, url):
        self.resolved.add(url)
        try:
            response = urllib2.urlopen(url)
            code = response.getcode()

            all_links = util.pull_out_all_links(response.read())
            [self.tasks.add(link) for link in all_links if link not in self.resolved]

            response.close()
        except urllib2.URLError as e:
            print e
            if hasattr(e, "code"):
                code = e.code
            else:
                code = -1
        except:
            print sys.exc_info()[0]
            code = -1

        self.add_result((url, code))

    def add_result(self, res):
        url = res[0]
        code = res[1]
        if code in self.result:
            self.result[code].append(url)
        else:
            self.result[code] = [url]


if __name__ == "__main__":
    miner = Miner("http://mockplus.cn")
    miner.run()
    print "all done"