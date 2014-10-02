##SiteMiner

爬取网站内所有链接，输出 markdown 文件。

##Get start

###Install

    pip install SiteMiner

###Useage

    from SiteMiner import Miner

    miner = Miner.Miner("http://sibo.me")
    miner.run()
    print "done!"

##说明

输出文件按照 Http 状态码分组，每个链接下面用一个列表来存放所有包含该链接的页面地址。
