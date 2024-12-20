"""
Script that lets you react with a lot of emojis at once to a post.
"""

from driver import Driver
import credentials
import random
import datetime
from zoneinfo import ZoneInfo

happy = [
    'smiley',
    'grin',
    'smiling_face_with_3_hearts',
    'heart_eyes',
    'star-struck',
    'yum',
    'money_mouth_face',
    'exploding_head',
    'face_with_cowboy_hat',
    'partying_face',
    'sunglasses',
    'smile_cat',
    'heart_eyes_cat',
    'heart',
    'dancers',
    'ok_hand',
    'i_love_you_hand_sign',
    'the_horns',
    'point_up_2',
    'clap',
    'raised_hands',
    'pray',
    'muscle',
    'prince',
    'princess',
    'superhero',
    'star',
    'star2',
    'fireworks',
    'sparkler',
    'sparkles',
    'tada',
    'confetti_ball',
    'medal',
    'trophy',
    'first_place_medal',
    'crown',
    'gem',
    'bangbang',
    'vacationparrot',
    'ultra_fast_parrot',
    '123inkis4',
    '123inkis2',
    'bouncingparrot',
    'tripletsparrot',
    'hilbertparrot',
    'wide_albin',
    'cutecamper',
    'flyingmoneyparrot',
    'shuffleparrot'
]
love = [
    'smiling_face_with_3_hearts',
    'heart_eyes',
    'star-struck',
    'kissing_heart',
    'money_mouth_face',
    'face_with_cowboy_hat',
    'partying_face',
    'heart_eyes_cat',
    'kiss',
    'cupid',
    'gift_heart',
    'sparkling_heart',
    'heartpulse',
    'heartbeat',
    'revolving_hearts',
    'two_hearts',
    'heart_decoration',
    'heavy_heart_exclamation_mark_ornament',
    'heart',
    'heart',
    'orange_heart',
    'yellow_heart',
    'green_heart',
    'blue_heart',
    'purple_heart',
    'brown_heart',
    '100',
    'dizzy',
    'anatomical_heart',
    'pray',
    'rose',
    'sunflower',
    'sunny',
    'fire',
    'star',
    'star2',
    'sparkles',
    'balloon',
    'crown',
    'f_spin',
    'vacationparrot',
    'chefparrot',
    'ultra_fast_parrot',
    '123inkis4',
    'thumbsup2',
    'hilbertparrot',
    'tripletsparrot',
    'shuffleparrot',
    'thumbsupparrot'
]
angry = [
    'neutral_face',
    'expressionless',
    'unamused',
    'triumph',
    'rage',
    'angry',
    'face_with_symbols_on_mouth',
    'imp',
    'japanese_ogre',
    'japanese_goblin',
    'pouting_cat',
    'anger',
    'right_anger_bubble',
    'boom',
    'speaking_head_in_silhouette',
    'middle_finger',
    '-1',
    'facepunch',
    'volcano',
    'hotsprings',
    'rotating_light',
    'octagonal_sign',
    'lightning',
    'fire',
    'firecracker',
    'boxing_glove',
    'mute',
    'axe',
    'dagger_knife',
    'gun',
    'bangbang',
    'interrobang',
    'exclamation',
    'x',
    'rat1',
    'bomb',
    'carlsocks',
    'wide_albin',
    'balenciagaskull',
    'evilparrot',
    'grabl',
    'grabr'
]
weird = [
    'upside_down_face',
    'face_with_raised_eyebrow',
    'expressionless',
    'grimacing',
    'face_with_thermometer',
    'nauseated_face',
    'face_vomiting',
    'woozy_face',
    'dizzy_face',
    'face_with_monocle',
    'flushed',
    'fearful',
    'skull',
    'skull_and_crossbones',
    'clown_face',
    'see_no_evil',
    'hear_no_evil',
    'speak_no_evil',
    'hole',
    'speech_balloon',
    'eyes',
    'no_good',
    'question',
    'grey_question',
    'dayum'
]
sexy = [
    'smirk',
    'drooling_face',
    'hot_face',
    'weary',
    'sweat_drops',
    'peach',
    'eggplant',
    'bed',
    'dayum'
]

options = [happy, love, angry, weird, sexy]
optionsnames = ['Happy', 'Love', 'Angry', 'Weirded out', 'Horny']

def timestamp_conv(unixtime):
    unixtime = int(unixtime/1000)
    time = datetime.datetime.fromtimestamp(int(unixtime), tz=ZoneInfo('Europe/Stockholm'))
    time = time.astimezone(ZoneInfo("Europe/Stockholm"))
    formatted_time = time.strftime('%H:%M %d/%m %Y')
    return formatted_time

def react_lots(driver, postId, emojis):
    random.shuffle(emojis)
    for emoji in emojis:
        driver.react(postId, emoji)

def choose_team(driver):
    teams = driver.list_teams()
    
    if len(teams) == 1:
        driver.enter_team(teams[0].get('id'))
    else:
        print('\tPlease choose team:')
        for idx, name in enumerate(teams):
            print(f'{idx}: \t\t {name}')
        print('\n')
        choice = int(input())
        driver.enter_team(teams[choice].get('id'))

def find_post(driver):
    print('Enter part of the target post:')
    search_phrase = input()
    responses = driver.search_posts(search_phrase)
    
    if len(responses) == 0:
        print('No results found. Try again.')
        return find_post(driver)
    if len(responses) == 1:
        return responses[0]
    else:
        print('\nMultiple results found. Please choose:\n')
        for idx, id in enumerate(responses):
            post = driver.get_post(id)
            author = driver.get_name(post.get('user_id'))
            timestamp = timestamp_conv(post.get('create_at'))
            
            msg = post.get('message')
            if len(msg) > 50:
                msg = msg[:50] + '...'
            
            print(f'{idx}: {author} \t {timestamp} \t {msg}')
        choice = int(input())
        return responses[choice]

def choose_mood():
    print('\tChoose mood:')
    for idx, name in enumerate(optionsnames):
        print(f'{idx}: {name}')
    return int(input())
        
mm = Driver(credentials.server_addr)
mm.login(credentials.username, credentials.password)

print('-----React shotgun-----\n')

choose_team(mm)

postId = find_post(mm)

reaction = options[choose_mood()]

react_lots(mm, postId, reaction)

print('Reactions sent.')