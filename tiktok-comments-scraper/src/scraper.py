thonimport requests
import json
from datetime import datetime
from .utils.proxy_handler import get_proxy

class TikTokScraper:
    def __init__(self, video_urls, comment_limit=100, proxy=None):
        self.video_urls = video_urls
        self.comment_limit = comment_limit
        self.proxy = proxy

    def scrape_comments(self):
        comments_data = []
        for url in self.video_urls:
            response = self.fetch_video_comments(url)
            comments_data.extend(response)
        return comments_data

    def fetch_video_comments(self, video_url):
        comments = []
        headers = {'User-Agent': 'Mozilla/5.0'}
        params = {'count': self.comment_limit}
        proxies = get_proxy(self.proxy)

        response = requests.get(f'https://api.tiktok.com/comments/{video_url}', params=params, headers=headers, proxies=proxies)
        if response.status_code == 200:
            data = response.json()
            for item in data['comments']:
                comment = {
                    "cid": item['cid'],
                    "create_time": datetime.fromtimestamp(item['create_time']),
                    "digg_count": item['digg_count'],
                    "text": item['text'],
                    "user/nickname": item['user']['nickname'],
                    "user/uid": item['user']['uid'],
                    "user/unique_id": item['user']['unique_id']
                }
                comments.append(comment)
        return comments

    def save_to_file(self, data, file_path):
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)