# -*- coding: utf-8 -*-

__author__ = 'massimo'

import urllib2
import util
import thread
import sys
import time
import urlparse


class Miner:
    def __init__(self, url):
        self._start = url
        self.netloc = urlparse.urlparse(url).netloc
        self._tasks = set()
        self._tasks.add(url)
        self._resolved = set()
        self._all = {}
        self.result = {}

    def run(self):
        thread.start_new_thread(self._status, ())
        while True:
            try:
                link = self._tasks.pop()
                self._resolve(link)
            except KeyError as e:
                print e
                break
        self._output()

    def _status(self):
        while True:
            print '-' * 50
            for k, v in sorted(self.result.items()):
                print k, len(v)
            print '-' * 50
            time.sleep(5)

    def _output(self):
        with open("result.md", 'w') as f:
            for k, v in sorted(self.result.items()):
                f.write("###%d(%d)\n\n" % (k, len(v)))
                for link in v:
                    f.write("+ %s \n" % (link,))
                    if self._all.has_key(link):
                        for _parent in self._all.get(link):
                            f.write("    * %s\n" % (_parent,))
                f.write("\n")

    def _resolve(self, url):
        self._resolved.add(url)
        try:
            response = urllib2.urlopen(url)
            code = response.getcode()

            all_links = util.pull_out_all_links(response.read())
            for link in all_links:
                link = urlparse.urljoin(url, link)
                self._add_link_parent(link, url)
                if self._is_current_site(link) and link not in self._resolved:
                    self._tasks.add(link)

            response.close()
        except urllib2.URLError, e:
            print e
            if hasattr(e, "code"):
                code = e.code
            else:
                code = -1
        except:
            e = sys.exc_info()[0]
            print e
            code = -1

        self._add_result((url, code))

    def _add_result(self, res):
        url = res[0]
        code = res[1]
        if code in self.result:
            self.result[code].append(url)
        else:
            self.result[code] = [url]

    def _is_current_site(self, url):
        o = urlparse.urlparse(url)
        return o.netloc == self.netloc

    def _add_link_parent(self, url, parent):
        if self._all.has_key(url):
            self._all.get(url).append(parent)
        else:
            self._all[url] = [parent]


if __name__ == "__main__":
    miner = Miner("http://mockplus.cn")
    miner.run()
    print "all done"