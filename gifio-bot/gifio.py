import time
import twitter
import giphypop

MAX_GIF_SIZE = 5000000

print('Initializing Twitter API interface ...')
                                # Change those with your own API keys and access tokens.
api = twitter.Api(consumer_key='eMUjteUH7UX3eHUjiiWbwZiR7',
                  consumer_secret='345j0R4ttwnaGAIjxU8HEKzzPjktmgSuKo089jKDTya6m0AkSh',
                  access_token_key='845267447863218176-pVoY8addT3m80Ggj3z35aexygvSkIlp',
                  access_token_secret='n3QqBzGnm5Ef0zZcdRd5iShlQ8CKinRkyKQ3sdTMNFS4u',
                  sleep_on_rate_limit=True)
print('Done!')

print('Intializing Giphy API interface ...')
giphy = giphypop.Giphy(strict=True)
print('Done!')

last_processed_mention = None

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
        gif_phrase = tweet.text.replace('@GifioBot', '').strip()
        gif_url = ''
        while True:
            gif = giphypop.translate(gif_phrase, 'phrase')
            print('Found potential GIF of size ' + str(gif.filesize) + ' bytes') 
            if gif.filesize < MAX_GIF_SIZE:
                gif_url = gif.media_url
                break
        print('Sending GIF to tweet ' + str(tweet.id) + ' ...')
        api.PostUpdate('@' + tweet.user.screen_name, media=gif_url, in_reply_to_status_id=tweet.id)
        last_processed_mention = tweet.id
        print('Done!')
    else:
        print('No mentions yet. I\'m taking a nap then!')
        time.sleep(30)
