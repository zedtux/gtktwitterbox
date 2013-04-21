import threading
import urllib.request
import json
from time import sleep
from gi.repository import Gtk
from gi.repository import GdkPixbuf
from gi.repository import Gdk
import douane.gui.helpers

class Operation(threading._Timer):
    def __init__(self, *args, **kwargs):
        threading._Timer.__init__(self, *args, **kwargs)
        self.setDaemon(True)

    def run(self):
        first_run = True
        while True:
            self.finished.clear()

            # Run immediatly on first run
            # Otherwise wait the definited interval
            if not first_run:
                self.finished.wait(self.interval)
            else:
                first_run = False

            if not self.finished.isSet():
                self.function(*self.args, **self.kwargs)
            else:
                return
            self.finished.set()

class Tweet(object):

    def __init__(self, id, name, screen_name, created_at, user_profile_image_url, text):
        self.id = id
        self.name = name
        self.screen_name = screen_name
        self.created_at = created_at
        self.user_profile_image_url = user_profile_image_url
        self.text = text

class TweetGrabber(object):

    def __init__(self, account, interval, spinner):
        self.__account = account
        self.__interval = interval
        self.__parent_spinner = spinner

        self.__tweets_cache = []
        self.__callback_method = None
        self.__operation = None

    def on_new_tweet(self, method):
        self.__callback_method = method

    def start(self, args=[], kwargs={}):
        self.__operation = Operation(self.__interval, self.grab, args, kwargs)
        thread = threading.Thread(target=self.__operation.run, args=())
        thread.start()

    def stop(self):
        self.__operation.cancel()

    def grab(self):
        new_tweets = []

        if self.__parent_spinner:
            Gdk.threads_enter()
            self.__parent_spinner.show()
            Gdk.threads_leave()

        # Fetch the 5 latest tweet from the given account in JSON
        try:
            url = "https://api.twitter.com/1/statuses/user_timeline.json?"
            url += "include_entities=true&include_rts=true&screen_name=%s&count=5" % self.__account
            response = urllib.request.urlopen(url)
            content = response.read()
            data = json.loads(content.decode('utf8'))

            # Iterate over each tweet and detect new
            for tweet in data:
                if not tweet['id'] in self.__tweets_cache:
                    # Initialize a new Tweet object
                    new_tweet = Tweet(tweet['id'],
                                      tweet['user']['name'],
                                      tweet['user']['screen_name'],
                                      tweet['created_at'],
                                      tweet['user']['profile_image_url'],
                                      tweet['text'])
                    # Save it to the cache
                    self.__tweets_cache.append(tweet['id'])
                    # Add it to the list that will be forwarded to the callback method
                    new_tweets.append(new_tweet)

            # If new tweets found fire the callback method
            if len(new_tweets) > 0:
                self.__callback_method(new_tweets)

            if self.__parent_spinner:
                Gdk.threads_enter()
                self.__parent_spinner.hide()
                Gdk.threads_leave()

        except (urllib.error.HTTPError, socket.gaierror, urllib.error.URLError) as error:
            print("[TweeterBox] ERROR: " + str(error))

class GtkTwitterBox(Gtk.Box):

    def __init__(self, parent_box, account, interval):
        Gtk.Box.__init__(self, spacing=6, orientation=Gtk.Orientation.VERTICAL)

        # Inject the GtkTwitterBox instance into the given Gtk.Box
        parent_box.pack_start(self, False, True, 0)

        # Add the Header
        self.__box_header = self.build_box_header()
        self.pack_start(self.__box_header, False, True, 0)

        # Add a loading widget that will be destroyed
        # as soon as tweet will be fetched
        self.__loading_widget = self.build_box_loading()
        self.pack_start(self.__loading_widget, True, True, 0)
        self.__is_loading = True

        self.show_all()

        # This spinner appear when TweetGrabber is processing
        self.__spinner_refreshing = Gtk.Spinner()
        self.__spinner_refreshing.start()
        self.__box_header.pack_start(self.__spinner_refreshing, False, True, 0)

        # Initialize a new TweetGrabber instance
        self.__tweet_grabber = TweetGrabber(account, interval, self.__spinner_refreshing)
        # When new tweet fetched fire the GtkTwitterBox#update_tweets method
        self.__tweet_grabber.on_new_tweet(self.update_tweets)
        self.__tweet_grabber.start()

    def build_box_header(self):
        hbox_header = Gtk.Box(margin_bottom=20, orientation=Gtk.Orientation.HORIZONTAL)
        image_twitter_logo = Gtk.Image(margin_left=80)
        image_twitter_logo.set_from_file("/home/zedtux/Developments/Douane/configurator/data/twitter-bird-light-bgs.png")
        image_twitter_logo.set_alignment(0.0, 0.5)
        hbox_header.pack_start(image_twitter_logo, False, True, 10)
        label_twitter_presentation = Gtk.Label()
        label_twitter_presentation.set_markup('<b>Douane</b>\n<a href="https://twitter.com/douaneapp">@douaneapp</a>')
        label_twitter_presentation.set_justify(Gtk.Justification.CENTER)
        label_twitter_presentation.set_alignment(0.0, 0.5)
        hbox_header.pack_start(label_twitter_presentation, True, True, 0)
        return hbox_header

    def build_box_loading(self):
        hbox_loading = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        spinner = Gtk.Spinner()
        spinner.start()
        hbox_loading.pack_start(spinner, True, True, 0)
        label_loading = Gtk.Label("Loading")
        label_loading.set_justify(Gtk.Justification.CENTER)
        hbox_loading.pack_start(label_loading, True, True, 0)
        return hbox_loading

    def kill(self):
        self.__tweet_grabber.stop()

    def update_tweets(self, new_tweets):
        if self.__is_loading:
            self.__is_loading = False
            self.remove(self.__loading_widget)

        for tweet in new_tweets:
            self.pack_start(self.build_tweet_box(tweet), False, True, 0)

    def build_tweet_box(self, tweet):
        # Fetch avatar from URL
        response = urllib.request.urlopen(tweet.user_profile_image_url)
        loader = GdkPixbuf.PixbufLoader()
        loader.write(response.read())
        loader.close()

        # Tweet
        hbox_tweet = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

        # Account Avatar
        image_account_avatar = Gtk.Image()
        image_account_avatar.set_from_pixbuf(loader.get_pixbuf())
        image_account_avatar.set_alignment(0.5, 0.0)
        hbox_tweet.pack_start(image_account_avatar, False, True, 8)

        # Tweet Content
        vbox_tweet_content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        # Tweet Header
        hbox_tweet_header = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        label_tweet_header = Gtk.Label()
        label_tweet_header.set_markup('<b>%s</b> ‏<a href="https://twitter.com/%s">@%s</a>' % (tweet.name, tweet.screen_name, tweet.screen_name))
        label_tweet_header.set_alignment(0.0, 0.5)
        hbox_tweet_header.pack_start(label_tweet_header, True, True, 0)
        # Tweet Since
        label_tweet_since = Gtk.Label(douane.gui.helpers.distance_of_time_in_words(tweet.created_at))
        hbox_tweet_header.pack_start(label_tweet_since, False, True, 0)
        vbox_tweet_content.pack_start(hbox_tweet_header, False, True, 0)

        # Tweet message
        label_tweet_text = Gtk.Label(tweet.text)
        label_tweet_text.set_line_wrap(True)
        label_tweet_text.set_alignment(0.0, 0.5)
        label_tweet_text.set_selectable(True)
        vbox_tweet_content.pack_start(label_tweet_text, False, True, 4)

        # Tweet Toolbox
        hbox_tweet_toolbox = Gtk.Box(spacing=12, orientation=Gtk.Orientation.HORIZONTAL)
        # Reply
        label_tweet_reply = Gtk.Label()
        label_tweet_reply.set_markup('<a href="https://twitter.com/intent/tweet?in_reply_to_status_id=%d">Reply</a>' % tweet.id)
        hbox_tweet_toolbox.pack_start(label_tweet_reply, False, True, 0)
        # Retweet
        label_tweet_retweet = Gtk.Label()
        label_tweet_retweet.set_markup('<a href="https://twitter.com/intent/retweet?tweet_id=%d">Retweet</a>' % tweet.id)
        hbox_tweet_toolbox.pack_start(label_tweet_retweet, False, True, 0)
        # Favorite
        label_tweet_favorite = Gtk.Label()
        label_tweet_favorite.set_markup('<a href="https://twitter.com/intent/favorite?tweet_id=%d">Favorite</a>' % tweet.id)
        hbox_tweet_toolbox.pack_start(label_tweet_favorite, False, True, 0)

        vbox_tweet_content.pack_start(hbox_tweet_toolbox, False, True, 8)

        hbox_tweet.pack_start(vbox_tweet_content, False, True, 0)

        hbox_tweet.show_all()
        return hbox_tweet