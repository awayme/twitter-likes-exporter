class TweetParser():
    def __init__(self, raw_tweet_json):
        self.is_valid_tweet = True
        self.raw_tweet_json = raw_tweet_json
        self._media_urls = None

        if not raw_tweet_json["content"].get("itemContent", None):
            self.is_valid_tweet = False
            return

        self.key_data = raw_tweet_json["content"]["itemContent"]["tweet_results"]["result"]
        if not self.key_data.get("legacy", None):
            self.is_valid_tweet = False

    def tweet_as_json(self):
        return {
            "tweet_id": self.tweet_id,
            "user_id": self.user_id,
            "user_handle": self.user_handle,
            "user_name": self.user_name,
            "user_avatar_url": self.user_avatar_url,
            'user_extra': {
                'created_at': self.user_data["created_at"],
                'favourites_count': self.user_data["favourites_count"],
                'followers_count': self.user_data["followers_count"],
                'friends_count': self.user_data["friends_count"],
                'listed_count': self.user_data["listed_count"],
                'location': self.user_data["location"],
                'description': self.user_data["description"],
                'following': self.user_data["following"],
                'normal_followers_count': self.user_data["normal_followers_count"],
                'statuses_count': self.user_data["statuses_count"],
                'verified': self.user_data["verified"]
            },
            "tweet_content": self.tweet_content,
            "tweet_media_urls": self.media_urls,
            "tweet_created_at": self.tweet_created_at,
            "tweet_extra": {
                "favorite_count": self.key_data["legacy"]["favorite_count"],
                "is_quote_status": self.key_data["legacy"]["is_quote_status"],
                "lang": self.key_data["legacy"]["lang"],
                "quote_count": self.key_data["legacy"]["quote_count"],
                "reply_count": self.key_data["legacy"]["reply_count"],
                "retweet_count": self.key_data["legacy"]["retweet_count"],
                "retweeted": self.key_data["legacy"]["retweeted"],
                "veiw_count": self.tweet_view_count,
            }
        }

    @property
    def tweet_view_count(self):
        if 'views' in self.key_data:
            views = self.key_data["views"]
            return views.get("count", '')
        else:
            return ''

    @property
    def tweet_id(self):
        return self.key_data["legacy"]["id_str"]

    @property
    def tweet_content(self):
        return self.key_data["legacy"]["full_text"]

    @property
    def tweet_created_at(self):
        return self.key_data["legacy"]["created_at"]

    @property
    def user_id(self):
        return self.key_data["legacy"]["user_id_str"]

    @property
    def user_handle(self):
        return self.user_data["screen_name"]

    @property
    def user_name(self):
        return self.user_data["name"]

    @property
    def user_avatar_url(self):
        return self.user_data["profile_image_url_https"]

    @property
    def user_data(self):
        return self.key_data["core"]["user_results"]["result"]["legacy"]

    @property
    def media_urls(self):
        if self._media_urls is None:
            self._media_urls = []
            media_entries = self.key_data["legacy"]["entities"].get("media", [])
            for entry in media_entries:
                self._media_urls.append(entry["media_url_https"])
        return self._media_urls
