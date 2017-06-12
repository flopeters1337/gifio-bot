import time
import random
import twitter
import giphypop
from keys import c_key, c_secret, a_key, a_secret

MAX_GIF_SIZE = 5000000

# Initialize random engine
random.seed()

print('Initializing Twitter API interface ...')
                                # Change those with your own API keys and access tokens.
api = twitter.Api(consumer_key=c_key,
                  consumer_secret=c_secret,
                  access_token_key=a_key,
                  access_token_secret=a_secret,
                  sleep_on_rate_limit=True)
print('Done!')

print('Intializing Giphy API interface ...')
giphy = giphypop.Giphy(strict=True)
print('Done!')

# To prevent GIFIO from replying to mentions before
# he was activated.
previous_mentions = api.GetMentions()
last_processed_mention = previous_mentions[0].id

print('   ________________________     ____        __ ')
print('  / ____/  _/ ____/  _/ __ \\   / __ )____  / /_')
print(' / / __ / // /_   / // / / /  / __  / __ \\/ __/')
print('/ /_/ // // __/ _/ // /_/ /  / /_/ / /_/ / /_  ')
print('\\____/___/_/   /___/\\____/  /_____/\\____/\\__/  ')
print('')
while True:
    mentions = api.GetMentions(since_id=last_processed_mention)
    if len(mentions) > 0:
        print('Processing mention ...')
        tweet = mentions[len(mentions)-1]
        gif_search = tweet.text.replace('@GifioBot', '').strip()
        mentions_in_tweet = [x.screen_name for x in tweet.user_mentions]
        for mention in mentions_in_tweet:
            gif_search = gif_search.replace('@' + mention, '').strip()
        if gif_search == '':
            gif_search = ' '
        extraInfo = ''
        gif_url = ''
        potential_gifs = [x for x in giphypop.search(gif_search,limit=15)]
        if len(potential_gifs) == 0:
            print('Could not find GIFs, sending apology tweet ...')
            potential_gifs = [x for x in giphypop.search('sorry')]
            extraInfo = ' Sorry, I could not find any appropriate GIFs'
        random.shuffle(potential_gifs)
        index = 0
        while True:
            gif = potential_gifs[index]
            print('Found potential GIF of size ' + str(gif.filesize) + ' bytes') 
            if gif.filesize < MAX_GIF_SIZE:
                gif_url = gif.media_url
                break
            index = index + 1
        print('Sending GIF to tweet ' + str(tweet.id) + ' ...')
        api.PostUpdate('@' + tweet.user.screen_name + extraInfo, 
                       media=gif_url, in_reply_to_status_id=tweet.id)
        last_processed_mention = tweet.id
        print('Done!')
    else:
        print('No mentions yet. I\'m taking a nap then!')
        time.sleep(30)
