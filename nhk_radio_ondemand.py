#! /usr/bin/env python
# -*- coding: utf-8 -*-
u"""
某放送局のラジオの聞き逃しサービスに関する情報を取得するプログラムです。

実行すると簡易情報をstdoutに出力します。
dオプションでsite_id及びcorner_idを指定すると、詳細情報をstdoutに出力します。
値はタブ区切りのレコードとして出力されます。フィールド内容は以下の通りです。

1.site_id
2.corner_id
3.headline_id
4.file_id
5.open_time
6.close_time
7.onair_date
8.program_name
9.corner_name
10.headline
11.headline_sub
12.file_title
13.file_name

ex. site_idが2295の番組の、corner_idが17の最新のfile_nameを取得する。
$ nhk_radio_ondemand.py -d 2295_17 | head -n 1 | cut -f 13
https://xxxxxxxxxxxxx.m3u8
"""
from __future__ import print_function

import argparse
import errno
import logging
import json
import os
import random
import re
import sys
import time
import urllib2

INDEX_URL='http://www.nhk.or.jp/radioondemand/json/index/index.json'


def fetch_data_list():
    """
    webからコンテンツ情報を取得する。

    Return:
    [list] 取得したdata_list

    Exception:
    [RuntimeError] 実行時に何らかのエラーが発生した場合。
    """
    try:
        readObj = urllib2.urlopen(INDEX_URL)
        if readObj.getcode() != 200:
            raise RuntimeError('Error: Server return %s.' % readObj.getcode())

        response = readObj.read()
        # print(response, file=sys.stderr)

        response = response.decode('utf-8', errors='ignore')
        data = json.loads(response.encode('utf-8'))
        #print(data, file=sys.stderr)
    
        return data['data_list']

    except Exception:
        raise RuntimeError(sys.exc_info()[1]), None, sys.exc_info()[2]


def fetch_detail_list(detail_json):
    """
    webから詳細情報を取得する。

    Args:
    [unicode] detail_json jsonファイルのurl。

    Return:
    [list] 取得したdetail_list。

    Exception:
    [RuntimeError] 実行時に何らかのエラーが発生した場合。
    """
    try:
        readObj = urllib2.urlopen(detail_json)
        if readObj.getcode() != 200:
            raise RuntimeError('Error: Server return %s.' % readObj.getcode())

        response = readObj.read()
        # print(response, file=sys.stderr)

        response = response.decode('utf-8', errors='ignore')
        data = json.loads(response.encode('utf-8'))
        #print(data, file=sys.stderr)

        """data['main'] keys
        [u'media_name', u'official_url', u'navi', u'detail_list', u'site_id',
        u'corner_detail', u'navi_name', u'share_url', u'site_detail',
        u'site_logo', u'media_type', u'week', u'corner_id', u'media_code',
        u'schedule', u'program_name', u'corner_name', u'thumbnail_c',
        u'noindex_flag', u'cast', u'thumbnail_p', u'mode']"""

        return data['main']['detail_list']

    except Exception:
        raise RuntimeError(sys.exc_info()[1]), None, sys.exc_info()[2]


def parse_argument():
    """
    コマンドライン引数をパースする。
    
    Return:
    [class ArgumentParser]
    
    Exception:
    [RuntimeError] 実行時に何らかのエラーが発生した場合。
    """
    try:
        parser = argparse.ArgumentParser(description=__doc__.encode('utf-8'),
                                 formatter_class=argparse.RawTextHelpFormatter)
        parser.add_argument('-d', dest='opt_d', metavar='SITEID_CORNERID',
            help='詳細表示。site_idとcorner_idをアンダーバーでつないだもの。')
        return parser.parse_args()

    except Exception:
        raise RuntimeError(sys.exc_info()[1]), None, sys.exc_info()[2]


def print_record(data, detail, f):
    """
    値をタブ区切りのレコードとしてstdoutに出力する。

    フィールド内容は以下の通り。
    1.  site_id
    2.  corner_id
    3.  headline_id
    4.  file_id
    5.  open_time
    6.  close_time
    7.  onair_date
    8.  program_name
    9.  corner_name
    10. headline
    11. headline_sub
    12. file_title
    13. file_name

    Args:
    [dict] data   dataレベルの情報。
    [dict] detail detailレベルの情報。
    [dict] f      fileレベルの情報。

    Exception:
    [RuntimeError] 実行時に何らかのエラーが発生した場合。
    """
    try:
        print(type(detail), type(f))

        msg = u''
        pattern = re.compile(r'[\t\r\n]+')

        # 1. site_id
        if data != None and data['site_id'] != None:
            msg += re.sub(pattern, '', data['site_id'])

        # 2. corner_id
        msg += u'\t'
        if data != None and data['corner_id'] != None:
            msg += re.sub(pattern, '', data['corner_id'])

        # 3. headline_id
        msg += u'\t'
        if detail != None and detail['headline_id'] != None:
            msg += re.sub(pattern, '', detail['headline_id'])

        # 4. file_id
        msg += u'\t'
        if f != None and f['file_id'] != None:
            msg += re.sub(pattern, '', f['file_id'])

        # 5. open_time
        msg += u'\t'
        if data != None and data['open_time'] != None:
            msg += re.sub(pattern, '', data['open_time'])
            
        # 6. close_time
        msg += u'\t'
        if data != None and data['close_time'] != None:
            msg += re.sub(pattern, '', data['close_time'])

        # 7. onair_date
        msg += u'\t'
        if data != None and data['onair_date'] != None:
            msg += re.sub(pattern, '', data['onair_date'])

        # 8. program_name
        msg += u'\t'
        if data != None and data['program_name'] != None:
            msg += re.sub(pattern, '', data['program_name'])

        # 9. corner_name
        msg += u'\t'
        if data != None and data['corner_name'] != None:
            msg += re.sub(pattern, '', data['corner_name'])
        
        # 10. headline
        msg += u'\t'
        if detail != None and detail['headline'] != None:
            msg += re.sub(pattern, '', detail['headline'])

        # 11. headline_sub
        msg += u'\t'
        if detail != None and detail['headline_sub'] != None:
            msg += re.sub(pattern, '', detail['headline_sub'])

        # 12. file_title
        msg += u'\t'
        if f != None and f['file_title'] != None:
            msg += re.sub(pattern, '', f['file_title'])

        # 13. file_name
        msg += u'\t'
        if f != None and f['file_name'] != None:
            msg += re.sub(pattern, '', f['file_name'])

        sys.stdout.write((msg + u'\n').encode('utf-8'))
        sys.stdout.flush()

    except Exception:
        raise RuntimeError(sys.exc_info()[1]), None, sys.exc_info()[2]


def setup_logger():
    """
    loggingをセットアップする。

    Return:
    [class 'logging.Logger'] loggerインスタンス。
    
    Exception:
    [RuntimeError] 実行時に何らかのエラーが発生した場合。
    """
    try:
        global args

        log_fmt = '%(filename)s: %(asctime)s %(levelname)s: %(message)s'
        #log_fmt = '%(filename)s:%(lineno)d: %(asctime)s %(levelname)s: %(message)s'
        
        #if args.verbose != '':
        if args.verbose:
            logging.basicConfig(level=logging.DEBUG, format=log_fmt)
        else:
            logging.basicConfig(format=log_fmt)

        return logging.getLogger(__name__)

    except Exception:
        raise RuntimeError(sys.exc_info()[1]), None, sys.exc_info()[2]

    
if __name__ == '__main__':

    try:
        args = parse_argument()
        if args.opt_d:
            # dオプションが指定された場合は、
            # 指定されたsite_id、corner_idが合致するdataを探し、
            # そのdataの詳細情報を取得して、出力する。

            # dオプションは、'siteid_cornerid'の書式で与えられる。
            (site_id, corner_id) = args.opt_d.split('_')
            #print(site_id, corner_id, file=sys.stderr)

            for data in fetch_data_list():
                # site_id、corner_idが合致しないものは飛ばす。
                if data['site_id']!=site_id or data['corner_id']!=corner_id:
                    continue

                for detail in fetch_detail_list(data['detail_json']):
                    for f in detail['file_list']:
                        print_record(data, detail, f)            
        else:
            # 特にオプションが指定されない場合は、
            # 簡略な情報を出力する。
            for data in fetch_data_list():
                print_record(data, None, None)

        sys.exit(0)

    except ValueError:
        # dオプションの値が不適切な場合に呼ばれる。
        (name, ext) = os.path.splitext(os.path.basename(sys.argv[0]))
        msg = u'%s: Error: Invalid option.' % name
        print(msg.encode('utf-8'), file=sys.stderr)
        sys.exit(1)

    except Exception, e:
        (name, ext) = os.path.splitext(os.path.basename(sys.argv[0]))
        msg = u'%s: Error: %s.' % (name, e)
        print(msg.encode('utf-8'), file=sys.stderr)
        sys.exit(1)
