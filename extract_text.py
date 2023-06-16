import re
import zipfile
import urllib.request
import os.path
import glob


def extract(url):
    download_text = download(url)
    text = convert(download_text)

    return text


def convert(download_text):
    binarydata = open(download_text, 'rb').read()
    text = binarydata.decode('shift_jis')

    # ルビ、注釈などの除去
    text = re.split(r'\-{5,}', text)[2]
    text = re.split(r'底本：', text)[0]
    text = re.sub(r'《.+?》', '', text)
    text = re.sub(r'［＃.+?］', '', text)
    text = text.strip()

    return text


def download(url):
    # データファイルをダウンロードする
    zip_file = re.split(r'/', url)[-1]

    if not os.path.exists(zip_file):
        urllib.request.urlretrieve(url, zip_file)
    else:
        print('Download File exists')

    # フォルダの生成
    dir, ext = os.path.splitext(zip_file)
    if not os.path.exists(dir):
        os.makedirs(dir)

    # zipファイルの展開
    zip_obj = zipfile.ZipFile(zip_file, 'r')
    zip_obj.extractall(dir)
    zip_obj.close()

    # zipファイルの削除
    os.remove(zip_file)

    # テキストファイルの抽出
    path = os.path.join(dir, '*.txt')
    list = glob.glob(path)

    return list[0]
