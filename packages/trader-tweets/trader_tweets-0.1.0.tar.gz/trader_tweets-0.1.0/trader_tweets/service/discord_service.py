import logging
import os
import requests

from trader_tweets.model.classified_tweet import ClassifiedTweet
from trader_tweets.model.tweet_type import TweetType
from trader_tweets.tweet_parsing import parse_symbols_from_tweet, is_tweet_tradeable

DISCORD_WEBHOOK_URL_CHANNEL_ALPHA = os.environ['DISCORD_WEBHOOK_URL_CHANNEL_ALPHA']
DISCORD_WEBHOOK_URL_CHANNEL_ALL = os.environ['DISCORD_WEBHOOK_URL_CHANNEL_ALL']


def _make_content(tweet, should_send_push_notification):
    symbols = parse_symbols_from_tweet(tweet.text)

    # check if there are any symbols in the tweet
    trading_view_links_text = ''
    if symbols.__len__() > 0:
        trading_view_links = map(lambda symbol: f"[{symbol}](https://www.tradingview.com/chart?symbol={symbol})", symbols)
        is_tradeable_text = '✅'
        trading_view_links_text = is_tradeable_text + ' ' + ' '.join(trading_view_links)

    user_id = 903570012638416937
    user_tag = f'*<@{user_id}>*' if should_send_push_notification else ''
    return '{trading_view_links}{tag}'.format(trading_view_links=trading_view_links_text, tag=user_tag)


def make_components(tweet, should_send_push_notification):
    # adds a button to the discord message.
    # when the button is clicked, it will open a form
    return [
            {
                'type': 2,
                'label': 'Open trade',
                'style': 5,
                'custom_id': 'open-trade',
            }
        ] if should_send_push_notification else []


def post_classified_tweet_to_discord(tweet: ClassifiedTweet,
                                     discord_webhook_url: str = DISCORD_WEBHOOK_URL_CHANNEL_ALL):

    should_send_push_notification = _should_send_push_notification(tweet, discord_webhook_url)

    tweet_type_emoji = \
        '🔮' if tweet.classification == TweetType.PREDICTION \
        else '📈' if tweet.classification == TweetType.TRADE \
        else '🤔' if tweet.classification == TweetType.UNSURE \
        else '🤬😂' if tweet.classification == TweetType.SHITPOSTING \
        else '💩' if tweet.classification == TweetType.NOT_INTERESTING \
        else '🤷'

    if should_send_push_notification:
        tweet_type_emoji = tweet_type_emoji + '🌅👁'

    description = tweet.text

    content = _make_content(tweet, should_send_push_notification)
    components = make_components(tweet, should_send_push_notification)

    payload = {
        'content': content,
        # 'username': tweet.author.username,
        # 'tts': False,
        'avatar_url': tweet.author.profile_image_url,
        'embeds': [
            {
                'title': '{tweet_type_emoji} by {author}'.format(tweet_type_emoji=tweet_type_emoji,
                                                                 author=tweet.author.name),
                'description': description,
                'url': 'https://twitter.com/{}/status/{}'.format(tweet.author.username, tweet.id),
                'color': get_colour_for_tweet_type(tweet.classification),
                'thumbnail': {
                    'url': tweet.img_url
                },
            }
        ],
        # buttons
        'components': components
    }

    logging.debug(f'img url: {tweet.img_url}')
    logging.info(f'Posting tweet {tweet.id} to discord')

    requests.post(discord_webhook_url, json=payload)


def get_colour_for_tweet_type(tweet_type: TweetType) -> int:
    if tweet_type == TweetType.TRADE:
        return 14177041
    elif tweet_type == TweetType.PREDICTION:
        return 1127128
    elif tweet_type == TweetType.SHITPOSTING:
        return 16711680
    elif tweet_type == TweetType.NOT_INTERESTING:
        return 0x7289DA
    elif tweet_type == TweetType.UNSURE:
        return 16776960
    else:
        return 0


def _should_send_push_notification(tweet: ClassifiedTweet, discord_webhook_url: str) -> bool:
    if discord_webhook_url != DISCORD_WEBHOOK_URL_CHANNEL_ALPHA:
        return False

    if tweet.classification != TweetType.TRADE:
        return False

    return is_tweet_tradeable(tweet)
