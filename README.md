SELinux Information Viewer (Ver.0.1.1)
===

本ツールはSELinux関連の調査を容易にします。
SELinux Information Extract は調査対象のマシンからSELinuxの設定情報を抽出します。
SELinux Information Viewer は、抽出したデータをもとに検索ビューを提供します。


# Description
本ツールはSELinuxの調査を効率よく行うために提供するものです。マシンのSELinuxに関する情報を、複雑なコマンドなしに調査することができます。

本ツールは２つのツールからなります。１つ目はSELinuxに関する設定情報をファイルに出力する抽出ツール。２つ目は抽出したファイルをもとにSELinux情報のデータベースを構築し、Webブラウザ上で検索できるビューワです。

データ抽出ツールにより、顧客環境など占有できないマシンについても、ビューワの利用が可能になります。
また、ビューワにより、検索機能など、CUIに比べ効率よく簡便に調査することができます。


# FEATURE
## File Contexts
SELinuxのファイルコンテキストについて検索できます。またファイルコンテキストのパターンに一致するファイルの一覧も表示できます。

まずProcess Domainを指定して下さい。これはポリシールールのソースドメインに対応します。システムは、ポリシールールのターゲットタイプに関連するファイルコンテキストを検索します。

## Files
ファイルに対してマッチするファイルコンテキストを確認できます。またドメインがファイルに対して許可された権限も確認できます。

## Others
そのほか以下についても確認できます。
* プロセス
* コネクション
* ブーリアン
* ポリシールール
* マシン情報

# Requirements
## SELinux Policy Extract
- policycoreutils-python
- python2

## SELinux Information Viewer
- python2
- Development Tools
- python-devel


# Usage
## SELinux情報の抽出
調査対象のマシン上でSELinux Information Extractを実行してください。
resultフォルダ内に抽出結果が出力されます。
```
sudo python selinux-info-extract.py
```

config.iniファイルにオプションを記載できます。
* prune : 探索時に無視するディレクトリを指定できます。
* root-path : 探索するルートディレクトリを指定できます。デフォルトは / です。
* output-dir : 探索結果を出力するディレクトリを指定できます。デフォルトは ./resultです。


例えば /opt ディレクトリのみを抽出の対象とし、そのうえで/opt/tmpディレクトリは対象から外し、さらに結果を/tmpディレクトリに出力したい場合、以下のようになります。
```
[settings]
prune = /opt/tmp
root-path =  /opt
output-dir = /tmp/result
```

注意：このプログラムは環境によっては時間がかかるかもしれません。

## ビューワの起動と停止
### 準備
1) 一般ユーザでログインしてください。
1) ビューワ用マシン上にSELinux Information Viewerを配備してください。
1) 下記コマンドを実行し必要なサードパティツールをダウンロードしてください
    * ./install.sh
    * プロキシを超える必要がある場合、~/.curlrcファイルを作成し、プロキシ情報を記載してください。
        * proxy-user = "&lt;username&gt;:&lt;passwd&gt;"
        * proxy = "&lt;proxy-url&gt;"
1) 同フォルダにSELinux Information Extractの実行結果であるresultディレクトリを配備してください。

### 起動
1) 一般ユーザでログインしてください。
1) 下記コマンドを実行してサーバを起動してください。
    * ./sh/start.sh
1) ブラウザから http://&lt;ip-adress&gt;:8080 にアクセスしてください

### 停止
1) ブラウザを閉じます。
1) コンソールに戻り、Ctrl+cで停止します。

## デーモン起動と停止
一般ユーザでログインしてください。
* 起動 : ./sh/start_daemon.sh を実行してください。
* 停止 : ./sh/stop_daemon.sh を実行してください。

## データベースの再構築
参照するデータを変更・更新する場合は、データベースの再構築が必要です。
1) 一般ユーザでログインしてください。
1) ビューワを起動している場合、「ビューワの起動と停止」または「デーモンの起動と停止」に従い、停止させてください。
1) ./sh/destroy_db.sh を実行してください。
1) resultフォルダの中身を更新してください。
1) ./sh/start.shを起動し、データベースを再構築します。

# Contributing
バグレポート、バグフィックス、および改善に貢献してくださったことに感謝します。
## Bug Report
不具合があった場合はIssueから報告してください。

## Bugfixes and Improvements
修正・機能追加はPull Requestで報告してください。


# License
Copyright (c) 2017 Hitachi, Ltd. All Rights Reserved.

Licensed under the MIT License.
You may obtain a copy of the License at

* https://opensource.org/licenses/MIT

This file is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OF ANY KIND.
