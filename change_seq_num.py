import click
import glob
import os
import re
import datetime
import shutil
from natsort import natsorted, natsort

def addDot(ext):
    '''拡張子の先頭に(.)ドットを付けて返却する

    Args:
        ext (str): 処理対象の拡張子

    Returns:
        str: extの先頭に(.)ドットを付けて返す

    Examples:
        ext = addDot('txt')
            上記の場合 .txt になる

    Note:
        渡されたextが(.)ドットで始まる場合はそのまま返す
    '''
    if not (ext.startswith('.')):
        ext = '.' + ext
    return ext

def isTarget(file_name: str, target_ext: str):
    '''file_nameが対象となるファイル名かどうか検査する

    ファイル名が数字のみで構成されている、且つ、拡張子がtarget_extであるかどうか検査する

    Args:
        file_name (str): 検査するファイル名（ディレクトリは含まず、拡張子を含む）
        target_ext (str): 対象とする拡張子

    Returns:
        bool: 処理対象である場合にTrueを返す

    Examples:
        b = isTarget('test.txt', '.txt')

    Note:
        特になし
    '''
    if not (target_ext.startswith('.')):
        target_ext = '.' + target_ext

    fname, ext = os.path.splitext(file_name)
    if ext.lower() == target_ext.lower():
        # 数字のファイル名だけを対象にするなら下記2行のコメントを外す
        # pattern = '(\d+)$'
        # if (re.match(pattern, fname)):
            return True

    return False

def collectFileNames(files: list, dir: str, ext: str):
    '''対象となるファイル名を検索しfilesに格納する

    対象のファイルが見つかった場合、下記形式のリストを作成しfilesに追加する \n
        [旧ファイル名, 新ファイル名]

    Args:
        files (str): 対象となるファイルを格納するリスト
        dir (str): 処理対象のディレクトリ名（フルパス）
        ext (str): 対象とする拡張子

    Returns:
        bool: 処理対象である場合にTrueを返す

    Examples:
        b = isTarget('test.txt', '.txt')

    Note:
        特になし
    '''
    for f in os.listdir(dir):
        if os.path.isfile(os.path.join(dir, f)):
            if isTarget(f, ext):
                # 元のファイル名と新ファイル名の配列として追加する
                # ただし、新ファイル名はこの時点では不明のため空値とする
                files.append([f,''])

def setNewFileNames(files: list, start: int, digit: int, ext: str):
    '''対象となるファイル名を検索しfilesに格納する

    対象のファイルが見つかった場合、下記形式のリストを作成しfilesに追加する \n
        [旧ファイル名, 新ファイル名]

    Args:
        files (str): 対象となるファイルを格納したリスト
        start (str): 連番の開始番号
        digit (str): 連番の桁数
        ext (str): ファイル名に付ける拡張子を.(ドット)込みで指定する

    Returns:
        なし

    Examples:
        setNewFileNames(files, 1, 3) \n
            上記の場合 001.jpg から始まる連番ファイル名となる（拡張子がjpgの場合）

    Note:
        filesはソート済みであること
    '''

    # filesに新ファイル名をセットする
    for ix, file in enumerate(files):
        new_name = str(start + ix).zfill(digit) + ext
        files[ix][1] = new_name

def make_out_dir(dir):
    '''出力用ディレクトリを作成する

    dirの直下に日時を名前とするサブディレクトリを作成する

    Args:
        dir (str): サブディレクトリを作成する親ディレクトリをフルパスで指定する

    Returns:
        日時を名前とするサブディレクトリを作成しそのディレクトリ名を返す \n
        日時は yyyymmdd_hhnnss の形式で作成する

    Examples:
        out_dir = make_out_dir(r'c:\tmp') \n

        出力例 ⇒ c:\tmp\20240527_092549

    Note:
        なし
    '''
    t_delta = datetime.timedelta(hours=9)
    JST = datetime.timezone(t_delta, 'JST')
    now = datetime.datetime.now(JST)
    d = now.strftime('%Y%m%d_%H%M%S')
    target_dir = os.path.join(dir, d)
    os.makedirs(target_dir, exist_ok=True)
    print(repr(target_dir))

    return target_dir

def copy_and_renames(files, dir, out_dir):
    '''リネームしながらファイルコピーを行う

    Args:
        files (list): 旧ファイル名と新ファイル名のリストを格納した2次元配列 \n
            ex. [['1.JPG', '001.jpg'], ['002.jpg', '002.jpg'], ['3a.JPG', '003.jpg']]

        dir (str): 元のファイルが格納されたディレクトリ
        out_dir (str): リネームしたファイルを出力するディレクトリ
    '''
    for ix, file in enumerate(files):
        input = os.path.join(dir, file[0])
        output = os.path.join(out_dir, file[1])
        if os.path.exists(input):
            shutil.copy2(input, output)  # パーミッション以外の属性もコピーする


def printTest(files: list):
    '''filesの中身をコンソールに出力する

    testオプションが指定された場合はファイル名変更処理は行わず、変更予定となる一覧表を表示する

    Args:
        files (list): 旧ファイル名と新ファイル名のリストを格納した2次元配列 \n
            ex. [['1.JPG', '001.jpg'], ['002.jpg', '002.jpg'], ['3a.JPG', '003.jpg']]
    '''
    for ix, file in enumerate(files):
        print (f'{file[0]} -> {file[1]}')

@click.command()
# 下記のようにpromptを指定すると実行時に入力が促される
@click.option("--dir", type=str, prompt="ディレクトリを入力",
              default=os.path.abspath(os.curdir), help="対象ファイルが格納されているディレクトリをフルパスで入力する。")
@click.option("--start", type=int, prompt="開始番号を入力",
              default=1, help="連番の開始番号を入力する。")
@click.option("--digit", type=int, prompt="連番の桁数を入力",
              default=3, help="連番の桁数を入力する。")
@click.option("--ext", type=str, prompt="対象となる拡張子を入力",
              default=".jpg", help="リネームの対象とするファイルの拡張子を入力する。")
@click.option("--test", count=True,
              help="実際には変更せず変更されるファイルの一覧を表示する。")
def main(dir, start, digit, ext, test):
    '''
    * ファイル名を連番にする \n
    * 日時を名前とする新しいサブディレクトリを作成し、元のファイルをコピー後、連番にリネームする \n
    * 元のファイルには何もしない \n

        出力例 \n
        001.jpg, 002.jpg 003.jpg ...
    '''
    print (f'dir: {os.path.abspath(dir)}')
    print (f'start: {start}')
    print (f'digit: {digit}')
    print (f'ext: {ext}')
    print (f'test: {test}')
    print ('')

    # 拡張子の先頭に(.)ドットを付ける
    ext = addDot(ext)

    # 対象ファイル名を格納する配列
    files = []

    # 対象となるファイル名を検索しfilesに格納する
    collectFileNames(files, dir, ext)

    # ファイル名で自然ソートする
    files = natsorted(files)

    # filesに新ファイル名をセットする
    setNewFileNames(files, start, digit, ext)

    if test == 0:
        # 出力用ディレクトリを作成する
        out_dir = make_out_dir(dir)
        # リネームしながらファイルコピーを行う
        copy_and_renames(files, dir, out_dir)
    else:
        # テストのみ⇒filesの中身を表示して終了
        printTest(files)

if __name__ == '__main__':
    main()