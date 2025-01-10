import requests
from datetime import datetime
from _Classes import AiringData , CharacterData , MangaData , AnimeData , TopAnimeData , BrowseData

class anilist:
    def __init__(self) -> None:
        self.url = 'https://graphql.anilist.co'
        self.trailer_query = "query ($id: Int, $idMal:Int, $search: String) {Media (id: $id, idMal: $idMal, search: $search, type: ANIME) {trailer {id site}}}"
        self.characters_info_query = "query ($id: Int, $page: Int) {Media (id: $id, type: ANIME) {id characters (page: $page, perPage: 25, sort: ROLE) {pageInfo {hasNextPage lastPage total} edges {node {name {full}}role}}}}"
        self.description_query = "query ($id: Int) {Media (id: $id) {id description (asHtml: false)}}"
        self.series_list_query = "query ($id: Int) {Media (id: $id, type: ANIME) {id relations {edges {node {title {romaji}type}relationType}}}}"
        self.airing_query = "query ($search: String, $page: Int) { Page (perPage: 1, page: $page) {pageInfo {total hasNextPage} media (search: $search, type: ANIME) {id title {romaji english} status countryOfOrigin nextAiringEpisode { timeUntilAiring episode} siteUrl isFavourite isAdult mediaListEntry {status id}}}}"
        self.character_query = "query ($id: Int, $search: String, $page: Int) { Page (perPage: 1, page: $page) {pageInfo {total hasNextPage} characters (id: $id, search: $search) { id name {full native}image {large} media (type: ANIME) { edges { node {title { english romaji}type} voiceActors (language: JAPANESE) {name {full}siteUrl}}} isFavourite siteUrl}}}"
        self.manga_query = "query ($search: String, $page: Int) { Page (perPage: 1, page: $page) { pageInfo { total hasNextPage} media (search: $search, type: MANGA) { id title { romaji english native} format countryOfOrigin source (version: 2) status description(asHtml: true) chapters isFavourite mediaListEntry { status score id} volumes averageScore siteUrl isAdult}}}"
        self.anime_query = "query ($id: Int, $idMal:Int, $search: String) { Media (id: $id, idMal: $idMal, search: $search, type: ANIME) {id idMal title { romaji english native} format status description(asHtml: true) episodes duration countryOfOrigin source (version: 2) trailer { id site} genres tags { name} averageScore relations { edges { node { title { romaji english}id type}relationType}}nextAiringEpisode { timeUntilAiring episode}isAdult isFavourite mediaListEntry { status score id}siteUrl}}"
        self.top_anime_query = "query ($page: Int) {Page (perPage: 15, page: $page) {pageInfo {lastPage total hasNextPage}media (sort: SCORE_DESC, type: ANIME){title{romaji english}}}}"
        self.browse_query = "query ($s: MediaSeason, $y: Int, $sort: [MediaSort]){Page{media (season: $s, seasonYear: $y, sort: $sort){title{romaji english}format}}}"

    def post_request(self, query: str,variables: dict) -> dict:
        headers = None
        return requests.post(self.url, json={'query': query, 'variables': variables},headers=headers).json()
    
    def hat_notation(self,episode):
        ep_ = list(str(episode))
        x = ep_.pop()
        if ep_ != [] and ep_.pop()=='1':return 'th'
        return "st" if x == "1" else "nd" if x == "2" else "rd" if x == "3" else "th"
    
    def get_season(self,future: bool = False):
        k = datetime.now()
        m =k.month +3 if future else k.month
        year = k.year
        if m > 12:y = y+1
        season = "WINTER" if (m in [1, 2, 3] or m > 12) else "SPRING" if m in [4, 5, 6] else "SUMMER" if m in [7, 8, 9] else "FALL" if m in [10, 11, 12] else None
        return season , year
    
    def format_time_elapsed(self,time_stamp):
        seconds, milliseconds = divmod(int(time_stamp), 1000)
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)
        tmp = (((str(days) + " Days, ") if days else "") + ((str(hours) + " Hours, ") if hours else "") + ((str(minutes) + " Minutes, ") if minutes else "") + ((str(seconds) + " Seconds, ") if seconds else "") + ((str(milliseconds) + " ms, ") if milliseconds else ""))
        return tmp[:-2]

    def get_trailer(self, query: int) -> str:
        result = self.post_request(self.trailer_query, {"id": query})
        if result.get("errors"):return None
        data = result["data"]["Media"]
        trailer_link = f"https://www.youtube.com/watch?v={data['trailer']['id']}feature=youtu.be" if data["trailer"] and data["trailer"]["site"] == "youtube" else None
        return trailer_link

    def get_characters(self, query: int ,page: int) -> tuple:
        result = self.post_request(self.characters_info_query,{"id": query, "page" : page})
        data = (result["data"]["Media"])
        charlist = [f"<blockquote>• {char['node']['name']['full']} ({char['role']})</blockquote>" for char in data["characters"]['edges']]
        chrctrs = ("\n").join(charlist)
        charls = f"{chrctrs}" if len(charlist) != 0 else ""
        return charls, data["characters"]['pageInfo']

    def get_description(self, query: int) -> str:
        result = self.post_request(self.description_query,{"id": query})
        data = (result["data"]["Media"])
        description = str(data.get("description")).replace('<i>','').replace('</i>','').replace('<br>','')
        return description

    def get_series_list(self, query: int) -> str:
        result = self.post_request(self.series_list_query,{"id": query})
        data = (result["data"]["Media"])
        series_list = data.get("relations").get("edges")
        series_list_str = ''.join([f'<blockquote>• {i["node"]["title"]["romaji"]} ({i["node"]["type"]}) {i["relationType"]}</blockquote>\n' for i in series_list])
        return series_list_str

    def get_airing(self, query: str, page: int) -> AiringData:
        result = self.post_request(self.airing_query, {"search": query, "page": int(page)})
        try:data = dict(result["data"]["Page"]["media"][0])
        except IndexError:return 

        return  AiringData(
            title=data["title"]["english"] or data["title"]["romaji"],
            image=f"https://img.anili.st/media/{data.get('id')}",
            anilist_id=data.get("id"),
            url=data["siteUrl"],
            status=data.get("status"),
            episode=data["nextAiringEpisode"]["episode"] if data["nextAiringEpisode"] else None,
            hat_notation=self.hat_notation(data["nextAiringEpisode"]["episode"]) if data["nextAiringEpisode"] else None,
            airing=self.format_time_elapsed(data["nextAiringEpisode"]["timeUntilAiring"]*1000) if data["nextAiringEpisode"] else None
        )
    
    def get_character(self,query: str, page: int) -> CharacterData:
        result = self.post_request(self.character_query, {"search": query, "page": int(page)})
        if len(result['data']['Page']['characters'])==0:return None
        data = result["data"]["Page"]["characters"][0]
        return CharacterData(
            image=data["image"]["large"],
            name=data["name"]["full"],
            native=data["name"]["native"],
            id=data["id"],
            voice_actors=list({f"<a href='{ii['siteUrl']}'>{ii['name']['full']}</a>" for i in data['media']['edges'] for ii in i['voiceActors']}),
            url=data["siteUrl"]
        )

    def get_anime(self,query: int) -> AnimeData:
        result = self.post_request(self.anime_query,{"id": int(query)})
        data = dict(result["data"]["Media"])
        if not data: return None
        return AnimeData(
            title=data["title"]["english"] or data["title"]["romaji"],
            id= data.get("id"),
            image=f"https://img.anili.st/media/{data.get('id')}",
            mail_id=data.get('idMal'),
            type=data.get("format"),
            score=data['averageScore'],
            episodes=data.get("episodes"),
            duration=data.get("duration"),
            status=data.get("status"),
            genres=", ".join(data['genres']),
            tags=", ".join(tag['name'] for tag in (data['tags'][0:5] if len(data['tags'])>5 else data['tags'])),
            description=str(data['description']).replace('<br>','').replace('<p>','').replace('</p>','').replace('<i>','').replace('</i>','').replace('<br />','').replace('<ul>','').replace('</ul>','').replace('<li>','').replace('</li>','')
        )
    
    def get_manga(self,query: str, page: int = 0) -> MangaData:
        if query.isdigit():
            search = {"id": int(query)}
        else:
            search = {"search": query, "asHtml": True, "page": page}
        result = self.post_request(self.manga_query, search)
        if len(result['data']['Page']['media'])==0:return None
        data = dict(result["data"]["Page"]["media"][0])
        return MangaData(
            image=f"https://img.anili.st/media/{data.get('id')}",
            id=data.get("id"),
            name=data["title"]["english"] or data["title"]["romaji"],
            native=data["title"]["native"],
            status=data.get("status"),
            source=data.get("source"),
            format=data.get("format"),
            score=data.get("averageScore"),
            chapters=data.get("chapters"),
            volumes=data.get("volumes"),
            description=str(data.get("description")[:500]).replace('<br>','').replace('<p>','').replace('</p>','').replace('<i>','').replace('</i>','').replace('<br />',''),
            url=data.get("siteUrl")
        )

    def get_top_anime(self,page: int) -> TopAnimeData:
        result = self.post_request(self.top_anime_query , {"page": int(page)})
        if len(result['data']['Page']['media'])==0:return None
        data = result["data"]["Page"]["media"]
        page = result["data"]["Page"]['pageInfo']
        return TopAnimeData(
            anime= [item["title"]["english"] or item["title"]["romaji"] for item in data],
            last_page=page['lastPage'],
            has_next_page=page['hasNextPage'],
            total=page['total']
        )

    def browse(self,query: str) -> BrowseData:
        seson, year = self.get_season(True) if query == 'upcoming' else self.get_season()
        sort = "TRENDING_DESC" if query == 'trending' else "POPULARITY_DESC"
        result =  self.post_request(self.browse_query, {"s": seson, "y": year, "sort": sort})
        data = result["data"]["Page"]["media"]

        return BrowseData(
            title=f'{query.capitalize()} animes in {seson} {year}',
            anime=list(set([i['title']['english'] for i in data if i['format'] in ['TV', 'MOVIE', 'ONA']]))[0:20]
        )
