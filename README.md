# ChangeSeqNum
Change file names to sequential numbers

* ファイル名を連番にする
* 日時を名前とする新しいサブディレクトリを作成し、元のファイルをコピー後、連番にリネームする
* 元のファイルには何もしない

    出力例　⇒　001.jpg, 002.jpg 003.jpg ...

## インストール(Windowsでの例)
```
    C:\>python -V
    Python 3.11.1

    C:\>git clone https://github.com/tomomori/ChangeSeqNum.git
    C:\>cd ChangeSeqNum
    C:\ChangeSeqNum>python -m venv venv
    C:\ChangeSeqNum>venv\Scripts\activate
    (venv) C:\ChangeSeqNum>python -m pip install --upgrade pip
    (venv) C:\ChangeSeqNum>pip install -r requirements.txt
```

## 使い方(Windowsでの例)
```
(venv) C:\ChangeSeqNum>python change_seq_num.py --help

Usage: change_seq_num.py [OPTIONS]

  * ファイル名を連番にする

  * 日時を名前とする新しいサブディレクトリを作成し、元のファイルをコピー後、連番にリネームする

  * 元のファイルには何もしない

      出力例

      001.jpg, 002.jpg 003.jpg ...

Options:
  --dir TEXT       対象ファイルが格納されているディレクトリをフルパスで入力する。
  --start INTEGER  連番の開始番号を入力する。
  --digit INTEGER  連番の桁数を入力する。
  --ext TEXT       リネームの対象とするファイルの拡張子を入力する。
  --test           実際には変更せず変更されるファイルの一覧を表示する。
  --help           Show this message and exit.

```

## 実行例(Windowsでの例)
```
(venv) C:\ChangeSeqNum>dir c:\tmp
2024/05/26  14:35                 0 002.jpg
2024/05/26  14:35                 0 1.JPG
2024/05/26  14:36                 0 3a.JPG

(venv) C:\ChangeSeqNum>python change_seq_num.py
ディレクトリを入力 [c:\ChangeSeqNum]: c:\tmp
開始番号を入力 [1]:
連番の桁数を入力 [3]:
対象となる拡張子を入力 [.jpg]:

(venv) C:\ChangeSeqNum>dir c:\tmp
2024/05/26  16:40    <DIR>          20240526_164000
2024/05/26  14:35                 0 002.jpg
2024/05/26  14:35                 0 1.JPG
2024/05/26  14:36                 0 3a.JPG

(venv) c:\ChangeSeqNum>dir c:\tmp\20240526_164000
2024/05/26  14:35                 0 001.jpg
2024/05/26  14:35                 0 002.jpg
2024/05/26  14:36                 0 003.jpg
```

## 変換リストを表示する(Windowsでの例)
```
(venv) C:\ChangeSeqNum>python change_seq_num.py --test
ディレクトリを入力 [c:\ChangeSeqNum]: c:\tmp
開始番号を入力 [1]:
連番の桁数を入力 [3]:
対象となる拡張子を入力 [.jpg]:

1.JPG -> 001.jpg
002.jpg -> 002.jpg
3a.JPG -> 003.jpg
```