#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from dimples.utils import Log, Runner
from dimples.utils import Path

path = Path.abs(path=__file__)
path = Path.dir(path=path)
path = Path.dir(path=path)
Path.add(path=path)

from tvbox.utils import http_get_text
from tvbox.lives import M3UTranslator
from tvbox import ScanParser


#
# show logs
#
Log.LEVEL = Log.DEVELOP


async def async_main():
    url = "https://live.fanmingming.com/tv/m3u/ipv6.m3u"
    text = await http_get_text(url=url)
    if text is None:
        Log.error(msg='failed to download url: %s' % url)
        return False
    else:
        count = len(text.splitlines())
        Log.info(msg='download url: %s -> %d lines' % (url, count))
    translator = M3UTranslator()
    # lives_txt = translator.translate(text=text)
    # Log.info(msg='translated: \n%s' % lives_txt)
    parser = ScanParser(translators=[translator])
    genres = parser.parse(text=text)
    Log.info(msg='parsed: \n%s' % genres)


def main():
    Runner.sync_run(main=async_main())


if __name__ == '__main__':
    main()
