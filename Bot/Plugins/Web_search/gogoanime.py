from bs4 import BeautifulSoup
from AnilistPython import Anilist
from Crypto.Cipher import AES
from requests import Request, Session
from requests.exceptions import HTTPError
from requests import Request, Session, Response
from urllib.parse import parse_qsl, urlencode, urljoin, urlparse
import requests
import functools
import base64
import m3u8
import json
import re


from Config import GOGO_ACC , GOGO_PW , anime_dict
from _Classes import TempData , AnimeLink , ResultAnime , latest , popular



def _aes_decrypt(data, key, iv):
    return (
        AES.new(key, AES.MODE_CBC, iv=iv)
        .decrypt(base64.b64decode(data))
        .strip(b"\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f\x10")
    )

def _aes_encrypt(data, key, iv):
    def pad(s):
        return s + chr(len(s) % 16) * (16 - len(s) % 16)

    return base64.b64encode(
        AES.new(key, AES.MODE_CBC, iv=iv).encrypt(pad(data).encode())
    )


def request_page(session: "Session", req: "Request") -> "Response":
    prepped = req.prepare()
    prepped.headers["User-Agent"] = (
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
    )
    res = session.send(prepped)
    res.raise_for_status()
    return res

@functools.lru_cache()
def _get_enc_keys(session: Session, embed_url: str):
    page = request_page(session, Request("GET", embed_url)).text

    keys = re.findall(r"(?:container|videocontent)-(\d+)", page)

    if not keys:
        return {}

    key, iv, second_key = keys

    return {
        "key": key.encode(),
        "second_key": second_key.encode(),
        "iv": iv.encode(),
    }


class GoGoAnime:
    session = Session()
    BASE_URL: str = "https://anitaku.bz"

    def get_search_results(self,query,page) -> list[ResultAnime]:
        anilist = Anilist()
        animelink =  self.BASE_URL + "/search.html?keyword=" + query + "&page=" + str(page)
        print(animelink)
        req = Request("GET", animelink)
        response = request_page(self.session, req)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            source_url = soup.find('ul', 'items').find_all("li")
            results = []
            for item in source_url:
                title = str(item.find('p', 'name').text).replace("\n","").lower().replace('dub','').lstrip().rstrip().replace('(','').replace(')','')
                tquery = title.lower().replace(' ','-').replace('.','')
                in_dict = tquery in [value['gogo_id'] for value in anime_dict.values()]
                if in_dict:
                    id= next((key for key, value in anime_dict.items() if value['gogo_id'] == tquery), None)
                    data = ResultAnime(title=title.title().rstrip().lstrip() ,id=id)
                    if str(title).rstrip().lstrip() not in [str(d.title).lower()for d in results]:results.append(data)
                else:
                    try:
                        id = anilist.get_anime_id(title.replace('(TV)','').lower())
                        data = ResultAnime(title=title.title().rstrip().lstrip() ,id=id)
                        if str(title).rstrip().lstrip() not in [str(d.title).lower()for d in results]:results.append(data)
                    except:pass
                if len(results) > 10:
                    break
            return results

    def get_new_release_anime(self) -> list[latest]:
        animelink = f"{self.BASE_URL}/home.html"
        anilist = Anilist()
        req = Request("GET", animelink)
        response = request_page(self.session, req)
        response_html = response.text
        soup = BeautifulSoup(response_html, 'html.parser')
        source_url = soup.find('div', 'last_episodes').find('ul', 'items').find_all('li')
        results = []
        for item in source_url:
            title = str(item.find('p','name').text).rstrip().lstrip()
            episode = int((item.find('p','episode').text).split(' ')[-1])
            try:
                id = anilist.get_anime_id(title.replace('(TV)','').lower())
                data = latest(title=title.title().rstrip().lstrip() ,id=id , episode=episode)
                if title not in [str(d.title).lower()for d in results]:results.append(data)
            except:pass
        return results
        
    def get_popular_anime(self) -> list[popular]:
            anilist = Anilist()
            animelink = f"{self.BASE_URL}/popular.html"
            req = Request("GET", animelink)
            response = request_page(self.session, req)
            response_html = response.text
            soup = BeautifulSoup(response_html, 'html.parser')
            source_url = soup.find('div', 'last_episodes').find('ul', 'items').find_all('li')
            results = []
            for item in source_url:
                title = str(item.find('p','name').text).rstrip().lstrip()
                try:
                    id = anilist.get_anime_id(title.replace('(TV)','').lower())
                    data = popular(title=title.title().rstrip().lstrip() ,id=id)
                    if title not in [str(d.title).lower()for d in results]:results.append(data)
                except:pass
            return results

    def get_stram_links(self, identifier: str, episode, is_dub: bool = False) -> list[AnimeLink]:
        ep_str = str(episode).replace(".", "-")
        if is_dub:
            urls = [
                f"{self.BASE_URL}/{identifier}-dub-episode-{ep_str}",
                f"{self.BASE_URL}/{identifier}-japanese-dub-episode-{ep_str}",
            ]
        else:
            urls = [f"{self.BASE_URL}/{identifier}-episode-{ep_str}"]

        res = None
        for u in urls:
            try:
                req = Request("GET", u)
                res = request_page(self.session, req)
                break
            except HTTPError:continue
        if res is None:return
        soup = BeautifulSoup(res.content, "html.parser")
        link = soup.find("a", {"class": "active", "rel": "1"})
        if link is None:return
        embed_url: str = link["data-video"]
        req = Request("GET", embed_url)
        res = request_page(self.session, req)
        soup = BeautifulSoup(res.content, "html.parser")
        crypto = soup.find("script", {"data-name": "episode"})
        if crypto is None:return
        crypto = crypto["data-value"]
        parsed = urlparse(embed_url)
        ajax_url = f"{parsed.scheme}://{parsed.netloc}/encrypt-ajax.php?"
        enc_keys = _get_enc_keys(self.session, embed_url)
        data = _aes_decrypt(crypto, enc_keys["key"], enc_keys["iv"]).decode()
        data = dict(parse_qsl(data))
        id_param = dict(parse_qsl(parsed.query))["id"]
        enc_id = _aes_encrypt(id_param, enc_keys["key"], enc_keys["iv"]).decode()
        data.update(id=enc_id)
        headers = {"x-requested-with": "XMLHttpRequest", "referer": embed_url}
        req = Request(
            "POST",
            ajax_url + urlencode(data) + f"&alias={id_param}",
            headers=headers,
        )
        res = request_page(self.session, req)
        json_res = json.loads(_aes_decrypt(res.json().get("data"), enc_keys["second_key"], enc_keys["iv"]))
        source_data = [x for x in json_res["source"]]
        streams = []
        for s in source_data:
            if s["type"] == "hls":
                req = Request("GET", s["file"])
                res = request_page(self.session, req)
                content = m3u8.M3U8(res.text, base_uri=urljoin(res.url, "."))
                if len(content.playlists) == 0:streams.append(AnimeLink(link=s["file"],quality=1080))
                for playlist in content.playlists:streams.append(AnimeLink(link=urljoin(content.base_uri, playlist.uri),quality=playlist.stream_info.resolution[1]))
            else:
                resolution = int(re.search(r"\d+", s["label"]).group(0))
                streams.append(AnimeLink(quality=resolution,link=s["file"]))
        return streams

    def get_download_links(self, id,episode ,is_dub: bool = False) -> list[AnimeLink]:
        auth_gogo = "PNyzv3XxTcIfmasWdA%2FIje%2FukCQ7dy4R9efTbnl0GXsF0AM5%2BkV6KmYC59zH229D3O2Bntyp2CpIJyM5Uc1D8Q%3D%3D"

        if auth_gogo:
            if is_dub: id = id + '-dub'
            ani_link = f"https://anitaku.bz/{id}-episode-{episode}"
            req = Request(method="GET", url=ani_link,cookies=dict(auth=auth_gogo))
            res = request_page(self.session, req)
            soup = BeautifulSoup(res.content, "html.parser")
            try:
                source_url = soup.find("div", {'class': 'cf-download'}).findAll('a')
                downloadLinks = []
                for links in source_url:
                    url = links['href']
                    qualitys = links.text.strip().split('x')[1]      
                    quality = "360p" if qualitys == "360" else "480p" if qualitys == "480" else "720p" if qualitys == "720" else "1080p" if qualitys == "1080" or qualitys == "1040" else None
                    downloadLinks.append(AnimeLink(quality=quality,link=url))
                return downloadLinks
            except:return

    def get_anime_new_update_id(self):
        animelink = f"{self.BASE_URL}/home.html"
        req = Request("GET", animelink)
        response = request_page(self.session, req)
        response_html = response.content
        soup = BeautifulSoup(response_html, 'html.parser')
        source_url = soup.find('div', 'last_episodes').find('ul', 'items').find_all('li')
        a = source_url[0].find('a')
        id = a['href'].replace('/category/', '')
        return id


def get_image_for_post(query): 
    anilist = Anilist()
    id = anilist.get_anime_id(query)  
    return f"https://img.anili.st/media/{id}"


def get_episodes_from_gogo(id:str) -> int:
    id = id.split('-episode-')[0].replace(' ','-')
    animelink = f"https://anitaku.bz/category/{id}"
    response = requests.get(animelink)
    plainText = response.content
    soup = BeautifulSoup(plainText, "html.parser")
    ep = soup.find(id="episode_page")
    Ep = ep.find_all("li")[-1].a
    return int(Ep.get("ep_end"))
        
def get_post_from_gogo(id:str) -> TempData:
    try:
        id = id.split('-episode-')[0].replace(' ','-')
        animelink = f"https://anitaku.bz/category/{id}"
        response = requests.get(animelink)
        plainText = response.content
        soup = BeautifulSoup(plainText, "html.parser")
        title = soup.find("div", {"class": "anime_info_body_bg"}).h1.string
        dic = soup.find_all('p', {"class": "type"})
        type = dic[0].a['title']
        genre = dic[2].find_all('a') 
        genres = []
        for x in genre:
            genres.append(x.get('title'))
        genres = ', '.join(genres)
        releaser = dic[3].get_text()
        releases = releaser.split(" ")
        release = releases[1]
        status = dic[4].a.get_text()
        ep = soup.find(id="episode_page")
        Ep = ep.find_all("li")[-1].a
        total_episodes = int(Ep.get("ep_end"))

    except:
        return 
    return TempData(title=title, genres=genres, total_episodes=total_episodes, type=type, status=status, release=release) 


def check_dub(gogo_id):
    id = gogo_id + '-dub'
    animelink = f"https://anitaku.bz/category/{id}"
    response = requests.get(animelink)
    plainText = response.content
    soup = BeautifulSoup(plainText, "html.parser")
    try:
        title = soup.find("div", {"class": "anime_info_body_bg"}).h1.string
        return True
    except:return False

def get_id(query: str, page = 0):
    def post_req(query:str):
        query = query.replace('"', '').replace('[','').replace(']','')
        animelink = f"https://anitaku.bz/search.html?keyword={query}"
        response = requests.get(animelink)
        response_html = response.text
        soup = BeautifulSoup(response_html, 'html.parser')
        source_url = soup.find('div', 'last_episodes').find('ul', 'items').find_all("li")
        if len(source_url) != 0:
            a = source_url[0].find('a')
            id = str(a['href']).replace('/category/', '')
            for item in source_url:
                title = str(item.find('p', 'name').text).replace("\n","")
                if query.lower() in title.lower():
                    a = item.find('a')
                    id = str(a['href']).replace('/category/', '')
                    break
            return id

    query = query.replace('!','').replace('  ', ' ').replace(': ','-').replace(' - ','-')
    id = post_req(query)
    if id != None:
        return id
    else:
        try:
            query = query.upper()
            id = post_req(query)
            return id
        except:pass

def anilist_id_2_gogo_id(id: int): 
    print('Anilist ID : ',id)
    id = int(id)
    in_dict = id in [anime_id for anime_id,_ in anime_dict.items()]
    if in_dict:
        gogo_id = anime_dict[id]['gogo_id']
    else:
        anilist = Anilist()
        anime = anilist.get_anime_with_id(id)
        title = anime['name_romaji']
        title = str(title).lower().replace('-',' ')
        print('Title : ',title)
        gogo_id = get_id(title)
    return gogo_id

def anilist_id_2_gogo_stream_download_id(id:int)->str:
    
    def get_gogo_digit_id(id:str) -> int:
        animelink = f"https://anitaku.bz/category/{id}"
        response = requests.get(animelink)
        response_html = response.text
        soup = BeautifulSoup(response_html, 'html.parser')
        id = int(soup.find('input', 'movie_id').get('value'))
        return id
    
    def get_gogo_id(id: int, title: str):
        title = str(title).replace(' ','%20')
        url = f"https://ajax.gogocdn.net/ajax/load-list-episode?ep_start=0&ep_end=1&id={id}&default_ep=0&alias={title}"
        response = requests.get(url)
        response_html = response.text
        soup = BeautifulSoup(response_html, 'html.parser')
        id = soup.find(name='ul', id='episode_related').find('a')['href'].lstrip(' ').split('-episode-')[0]
        return id
    
    id= int(id)
    in_dict = id in [anime_id for anime_id,_ in anime_dict.items()]
    if in_dict:
        gogo_stream_id = anime_dict[id]['gogo_stream_id']
    else:
        anilist = Anilist()
        anime = anilist.get_anime_with_id(id)
        title = str(anime['name_romaji'])
        title = str(title).lower()
        id = get_id(title)
        gogo_stream_id = str(get_gogo_id(get_gogo_digit_id(id),title)).replace('/','')
    return gogo_stream_id
