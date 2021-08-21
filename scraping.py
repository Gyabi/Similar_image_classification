from os import link, truncate
import os
import requests
import random
import shutil
import bs4
import ssl
import csv
ssl._create_default_https_context = ssl._create_unverified_context

# dataで検索してimageタグの含まれるリンクを収集してnumだけはじいて出力
def get_links(data, num):
    Res = requests.get("https://www.google.com/search?hl=jp&q=" + data + "&btnG=Google+Search&tbs=0&safe=off&tbm=isch")
    Html = Res.text
    Soup = bs4.BeautifulSoup(Html,'lxml')
    links = Soup.find_all("img")
    
    out = []
    i = 0
    while num > 0:
        link_tmp = links[i].get("src")
        if str(link_tmp).split(".")[-1] != "gif":
            out.append(str(link_tmp))
            num -= 1
        i += 1
    return out

# リンクから画像を保存
def download_img(url, file_name, folder_name):
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        os.makedirs(os.path.join("./database", folder_name), exist_ok=True)
        with open(os.path.join("./database","database.csv"), mode="a", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([os.path.join("./database", folder_name,file_name+".jpg")])
             
        with open(os.path.join("./database", folder_name,file_name+".jpg"), 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
def search_google(num,data):
    # まず最上段の関数urlのlist取得
    # それをループさせてdownload_imgに入れる
    links = get_links(data, num)
    for i,link in enumerate(links):
        download_img(link, str(i), data)
    
    
if __name__ == "__main__":
    with open(os.path.join("./database","database.csv"), mode="w", encoding="utf-8", newline="") as f:
        pass
    num = 10
    words = ["森","海","空","町","犬","猫"]
    
    for word in words:
        search_google(num, word)
    