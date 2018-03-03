某放送局のラジオの聞き逃しサービスに関する情報を取得するプログラムです。

実行すると簡易情報をstdoutに出力します。  
dオプションでsite_id及びcorner_idを指定すると、詳細情報をstdoutに出力します。  
値はタブ区切りのレコードとして出力されます。フィールド内容は以下の通りです。

1. site_id
1. corner_id
1. headline_id
1. file_id
1. open_time
1. close_time
1. onair_date
1. program_name
1. corner_name
1. headline
1. headline_sub
1. file_title
1. file_name

## EXAMPLE

```
# site_idが2295の番組の、corner_idが17の最新のfile_nameを取得する。
$ nhk_radio_ondemand.py -d 2295_17 | head -n 1 | cut -f 13
https://xxxxxxxxxxxxx.m3u8
```

Last update 2018/03/03
