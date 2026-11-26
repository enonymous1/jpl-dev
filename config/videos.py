"""Curated video list for the Videos tab.

Videos are hand-listed here, never scraped at build time: the list is
small, and an entry only exists when the upload is real and public.
Each section is one platform account (a YouTube channel, ...); a new
account is a new section. Thumbnails are local files under
static/images/video-thumbs/, downloaded once from the platform's
thumbnail URL — never hotlinked. The watch URL is built from the id,
so there is one source of truth per video.
"""

VIDEO_SECTIONS = [
    {
        'platform': 'YouTube',
        'channel': 'Justin Lyons',
        'channel_handle': '@JustinLyons364',
        'channel_url': 'https://www.youtube.com/@JustinLyons364',
        'videos': [
            {
                'id': 'xp-cd9AwNr8',
                'title': 'Xbox One COD Ghosts FFA Tremor 30 3',
                'date': '2013-12-13',
                'date_label': 'Dec 13, 2013',
                'description': '',
                # Duration unknown: the watch page serves a login-gated
                # variant for this one, so no length was read. Never
                # guessed — the card simply shows no duration.
                'duration': '',
                'thumbnail': 'xp-cd9AwNr8.jpg',
            },
            {
                'id': 'wO6Fp1_dhL4',
                'title': 'enonymous1 - MW3 Game Clip',
                'date': '2013-07-21',
                'date_label': 'Jul 21, 2013',
                'description': 'Game Clip',
                'duration': '0:10',
                'thumbnail': 'wO6Fp1_dhL4.jpg',
            },
            {
                'id': '6RxRTMus_dI',
                'title': '25ToCBeasts.mp4',
                'date': '2009-11-20',
                'date_label': 'Nov 20, 2009',
                'description': (
                    'Public Enemy of Thrall downing Northrend Beasts on regular '
                    'from a holy paladin view.'
                ),
                'duration': '9:48',
                'thumbnail': '6RxRTMus_dI.jpg',
            },
            {
                'id': '9qxxzUS7y6o',
                'title': '10HToCBoss2',
                'date': '2009-11-05',
                'date_label': 'Nov 5, 2009',
                'description': (
                    'Realm: Thrall Guild: Public Enemy Character: Eusebeia (Holy Paladin)'
                ),
                'duration': '5:46',
                'thumbnail': '9qxxzUS7y6o.jpg',
            },
        ],
    },
    {
        'platform': 'YouTube',
        'channel': 'Enonymous1 Gaming',
        'channel_handle': '@enonymous1gaming',
        'channel_url': 'https://www.youtube.com/@enonymous1gaming',
        'videos': [
            {
                'id': 'BGsSSGWq4kY',
                'title': 'ANVIL   Brone   no3   Symphonia',
                'date': '2024-01-14',
                'date_label': 'Jan 14, 2024',
                'description': '',
                'duration': '51:26',
                'thumbnail': 'BGsSSGWq4kY.jpg',
            },
            {
                'id': '_kNsAGBdxNI',
                'title': 'ANVIL   Bronte   no1   Czerny',
                'date': '2024-01-14',
                'date_label': 'Jan 14, 2024',
                'description': '',
                'duration': '22:03',
                'thumbnail': '_kNsAGBdxNI.jpg',
            },
            {
                'id': 'Re-BWTJpGJY',
                'title': 'ANVIL   Guillotine   no2   Czerny',
                'date': '2024-01-14',
                'date_label': 'Jan 14, 2024',
                'description': '',
                'duration': '17:47',
                'thumbnail': 'Re-BWTJpGJY.jpg',
            },
            {
                'id': 'QwZ6rULq8Sw',
                'title': 'ANVIL   Jungler   no4   Czerny',
                'date': '2024-01-14',
                'date_label': 'Jan 14, 2024',
                'description': '',
                'duration': '18:29',
                'thumbnail': 'QwZ6rULq8Sw.jpg',
            },
            {
                'id': 'dEh_8kuJYM8',
                'title': 'ANVIL   Elsa   no2   Czerny',
                'date': '2024-01-14',
                'date_label': 'Jan 14, 2024',
                'description': '',
                'duration': '25:02',
                'thumbnail': 'dEh_8kuJYM8.jpg',
            },
            {
                'id': 'NUOwvJFTNXE',
                'title': 'ANVIL   Bronte   no4   Campanella',
                'date': '2024-01-14',
                'date_label': 'Jan 14, 2024',
                'description': '',
                'duration': '5:06',
                'thumbnail': 'NUOwvJFTNXE.jpg',
            },
            {
                'id': '0pF3-K1AK7I',
                'title': (
                    "fortnite, trying to save the girl & I spot a creeper in the window! got'em"
                ),
                'date': '2023-03-29',
                'date_label': 'Mar 29, 2023',
                'description': '',
                'duration': '0:34',
                'thumbnail': '0pF3-K1AK7I.jpg',
            },
            {
                'id': 'uPt-i7tVTSo',
                'title': 'fortnite alternating shots on last 2 for the win',
                'date': '2023-03-29',
                'date_label': 'Mar 29, 2023',
                'description': '',
                'duration': '0:35',
                'thumbnail': 'uPt-i7tVTSo.jpg',
            },
            {
                'id': '0KGqi5mlqEU',
                'title': 'fortnite, mate just would let the storm get his buddy!',
                'date': '2023-03-29',
                'date_label': 'Mar 29, 2023',
                'description': '',
                'duration': '0:34',
                'thumbnail': '0KGqi5mlqEU.jpg',
            },
            {
                'id': '3S0u9fRbXGU',
                'title': 'fortnite terrible aim, still got the win though =)',
                'date': '2023-03-29',
                'date_label': 'Mar 29, 2023',
                'description': '',
                'duration': '0:35',
                'thumbnail': '3S0u9fRbXGU.jpg',
            },
            {
                'id': 'EqujTcxQ-EI',
                'title': 'Titanfall Assault',
                'date': '2017-08-31',
                'date_label': 'Aug 31, 2017',
                'description': '',
                'duration': '8:27',
                'thumbnail': 'EqujTcxQ-EI.jpg',
            },
            {
                'id': '4R7hGbsQNEg',
                'title': 'Lego Worlds 1 Billion studs method! Works with current patch',
                'date': '2017-07-08',
                'date_label': 'Jul 8, 2017',
                'description': (
                    'Search no more, 1 Billion studs is achievable on the patched version of '
                    'this game with some farming and 3rd party '
                    "utilities.\n\nRequirements\n-Cronusmax or similar product (you're going to "
                    'need to macro pressing y + a over and over and over)\n-USB Hub (poor xbox '
                    'one only having the 1 usb port) - this helps keep your profile from '
                    'disconnecting on a wireless controller and still being able to use the '
                    'cronusmax.\n-22 hours\n\nSo basically in Lego Worlds right now you can '
                    'place items you\'ve "discovered" but usually breaking items you created '
                    'results in zero loot. However if you have a 2nd controller available you '
                    'can play some split screen and when one of the characters is using the '
                    'discovery tool and placing an item the other player can destroy the item '
                    "before it's actually placed (this time the loot does drop). After that neat "
                    'discovery, I just searched from the item I could place that when destroyed '
                    'resulted in the largest amount of studs dropped. In my small experiments I '
                    'found the "Safety Deposit Boxes" dropped the most studs @ 13,680 studs '
                    'dropped every time.  So I thought if I could spam the creation of this item '
                    'while simultaneously destroying it I could easily farm the 1 billion over '
                    'time. So after recording all this I ran some numbers and came up with the '
                    'following.\n\n1 Safe Deposit Box = 13,680 Studs\nEvery minute farming these '
                    'boxes results in 759,413 Studs.\n\nThus 759,413 Studs per Minute. --- '
                    '1,000,000,000 divided by 759,413 = 1,316 Minutes or 21.95 Hours... 22 '
                    "Hours.\n\nWith the update, I don't think this needs to be done in one "
                    'sitting. But YOU DO NEED to have 1 Bil active stud count. My game kept '
                    'glitching during this process and my achievement tracker hit 1 billion long '
                    'before my in game counter and no achievement. So you definitely need to '
                    'actually have that amount.\n\nPS. For those using the cronusmax (since this '
                    "is what I used). I used the Max Rec plugin. I'm sure someone could make a "
                    'profile so you could do this without needing to be tethered to your pc... '
                    'Either way I used the plugin and it was super simple opened it up, hovered '
                    'above the record until I had a nice rhythm on the controller for pressing y '
                    'then a, y then a, y then a. Give it a go, let it run. You want a steady '
                    'stream of studs, I had to re record a few times as I kept getting pauses '
                    'from the recording looping.. if that makes since...'
                ),
                'duration': '14:42',
                'thumbnail': '4R7hGbsQNEg.jpg',
            },
            {
                'id': 'OeJjZ6oXsuA',
                'title': 'Advanced Warfare - Detroit - FFA - 30 - 17',
                'date': '2017-06-15',
                'date_label': 'Jun 15, 2017',
                'description': '',
                'duration': '8:29',
                'thumbnail': 'OeJjZ6oXsuA.jpg',
            },
            {
                'id': '_sQLaHf4KI8',
                'title': 'Asphalt 7 Heat - Windows 10',
                'date': '2017-06-12',
                'date_label': 'Jun 12, 2017',
                'description': 'Asphalt 7 Gameplay on Windows 10.',
                'duration': '9:45',
                'thumbnail': '_sQLaHf4KI8.jpg',
            },
            {
                'id': '8rYx2nIVefU',
                'title': 'The Desert - 3 Stars - Bulletstorm: Full Clip Edition',
                'date': '2017-06-06',
                'date_label': 'Jun 6, 2017',
                'description': (
                    'The Desert - 3 Stars - Bulletstorm: Full Clip Edition, ECHOES.\n\nNecessary '
                    'step for the Supernova achievement,1/20 3 Star Echo.'
                ),
                'duration': '2:48',
                'thumbnail': '8rYx2nIVefU.jpg',
            },
            {
                'id': 'puhotTGRlOE',
                'title': 'The Hideout - 3 Stars - Bulletstorm: Full Clip Edition',
                'date': '2017-06-06',
                'date_label': 'Jun 6, 2017',
                'description': (
                    'The Hideout - 3 Stars - Bulletstorm: Full Clip Edition, '
                    'ECHOES.\n\nNecessary step for the Supernova achievement, 2/20 3 Star Echo.'
                ),
                'duration': '4:56',
                'thumbnail': 'puhotTGRlOE.jpg',
            },
            {
                'id': 'uefhjfIalq4',
                'title': 'Like a Boss Achievement - Bulletstorm: Full Clip Edition',
                'date': '2017-06-05',
                'date_label': 'Jun 5, 2017',
                'description': (
                    "I was going for the Beat em' down achievement and got to a boss round. You "
                    'could go for any level and just do the waves until a boss spawns, get the '
                    'kill. Profit.'
                ),
                'duration': '2:18',
                'thumbnail': 'uefhjfIalq4.jpg',
            },
            {
                'id': 'WbVbTJHWGWI',
                'title': 'Master of Disaster Achievement - Bulletstorm: Full Clip Edition',
                'date': '2017-06-05',
                'date_label': 'Jun 5, 2017',
                'description': (
                    'Act 7 Chapter 2 after the door opens on a enemy with a turret, run past and '
                    'unleash the thumper!'
                ),
                'duration': '0:52',
                'thumbnail': 'WbVbTJHWGWI.jpg',
            },
            {
                'id': '2yzr7xUU2SY',
                'title': 'I Might Be Late Achievement - Bulletstorm: Full Clip Edition',
                'date': '2017-06-05',
                'date_label': 'Jun 5, 2017',
                'description': (
                    'Once the timer starts kill all enemies and get your achievement/trophy.'
                ),
                'duration': '2:06',
                'thumbnail': '2yzr7xUU2SY.jpg',
            },
            {
                'id': 'XI0oc48tU6A',
                'title': (
                    'Geurrilla Tactics Achievement - Monorail - Bulletstorm: Full Clip Edition'
                ),
                'date': '2017-06-05',
                'date_label': 'Jun 5, 2017',
                'description': (
                    'Just to show you it\'s "achievable" heh. Keep checking what skill shots you '
                    "havn't done, change weapons if necessary. Utilize thump, kicking, and the "
                    'leash.'
                ),
                'duration': '10:24',
                'thumbnail': 'XI0oc48tU6A.jpg',
            },
            {
                'id': 'XLxlCx1XhaY',
                'title': (
                    'Guns of Stygia - 3 Stars - Bulletstorm: Full Clip Edition - Last Blood '
                    'Achievement'
                ),
                'date': '2017-06-05',
                'date_label': 'Jun 5, 2017',
                'description': (
                    'Guns of Stygia - 3 Stars - Bulletstorm: Full Clip Edition, '
                    'ECHOES.\n\nNecessary step for the Supernova achievement, 17/20 3 Star '
                    'Echo.\n\nLast Blood achievement is pretty easy to get once you know what to '
                    "do. Just follow what I've done and you'll be good to go."
                ),
                'duration': '4:42',
                'thumbnail': 'XLxlCx1XhaY.jpg',
            },
            {
                'id': 'MsMXZj12SBo',
                'title': 'Collapsed Building - 3 Stars - Bulletstorm: Full Clip Edition - Hoarder',
                'date': '2017-06-05',
                'date_label': 'Jun 5, 2017',
                'description': (
                    'Collapsed Building - 3 Stars - Bulletstorm: Full Clip Edition, '
                    'ECHOES.\n\nNecessary step for the Supernova achievement, 10/20 3 Star '
                    'Echo.\n\nHoarder achievement popped here for me, this should unlock '
                    "somewhere along you're trek for the Supernova achievement."
                ),
                'duration': '4:33',
                'thumbnail': 'MsMXZj12SBo.jpg',
            },
            {
                'id': 'H4MReBETB1s',
                'title': 'Dreadnought - 3 Stars - Bulletstorm: Full Clip Edition',
                'date': '2017-06-04',
                'date_label': 'Jun 4, 2017',
                'description': (
                    'Dreadnought - 3 Stars - Bulletstorm: Full Clip Edition, '
                    'ECHOES.\n\nNecessary step for the Supernova achievement, 15/20 3 Star Echo.'
                ),
                'duration': '4:11',
                'thumbnail': 'H4MReBETB1s.jpg',
            },
            {
                'id': 'Tzep1zFUjfU',
                'title': 'Bell End Achievement - Villa - Bulletstorm: Full Clip Edition',
                'date': '2017-06-04',
                'date_label': 'Jun 4, 2017',
                'description': (
                    'Achievement pops for "Dung" skill shot from leashing the bell found on the '
                    'level Villa. Leash it when enemies are near and boom goes the dynamite.'
                ),
                'duration': '1:39',
                'thumbnail': 'Tzep1zFUjfU.jpg',
            },
            {
                'id': 'B1mY50lFU2U',
                'title': 'Extinguisher Achievement - Sewers - Bulletstorm: Full Clip Edition',
                'date': '2017-06-04',
                'date_label': 'Jun 4, 2017',
                'description': (
                    'Was able to get this done in wave 1 after 2 or 3 attempts, just keep '
                    'trying. They die pretty easily if they walk in so try to leash em in and '
                    'kick em out.\n\nAchievement requires Hot Flashes skill shot from catching '
                    'them on fire from leashing the valve and letting the fire out the center of '
                    'the room. as well as the Fish Food skill shot from kicking them in to the '
                    'water directly across from where the fire comes from.'
                ),
                'duration': '4:10',
                'thumbnail': 'B1mY50lFU2U.jpg',
            },
            {
                'id': 'Ki_WiFeCNM0',
                'title': (
                    'Crash Site - 3 Stars - Bulletstorm: Full Clip Edition - Hell Razor - '
                    'Shooting Star'
                ),
                'date': '2017-06-04',
                'date_label': 'Jun 4, 2017',
                'description': (
                    'Crash Site - 3 Stars - Bulletstorm: Full Clip Edition, ECHOES.\n\nNecessary '
                    'step for the Supernova achievement, 18/20 3 Star Echo.\n\nHell Razor '
                    'Achievement - Kill the Burnout with the chopper blades\n\nShooting Star '
                    'Achievement - Get at least 1 star on each echo, this just popped for me '
                    'here, I was a little out of order.'
                ),
                'duration': '5:22',
                'thumbnail': 'Ki_WiFeCNM0.jpg',
            },
            {
                'id': 'VS0iaLbuL-A',
                'title': 'Gang Territory - 3 Stars - Bulletstorm: Full Clip Edition',
                'date': '2017-06-04',
                'date_label': 'Jun 4, 2017',
                'description': (
                    'Gang Territory - 3 Stars - Bulletstorm: Full Clip Edition, '
                    'ECHOES.\n\nNecessary step for the Supernova achievement, 16/20 3 Star Echo.'
                ),
                'duration': '3:51',
                'thumbnail': 'VS0iaLbuL-A.jpg',
            },
            {
                'id': 'tlR9XTEmnxo',
                'title': (
                    'Mean Street - 3 Stars - Bulletstorm: Full Clip Edition - Fast Track '
                    'Achievement'
                ),
                'date': '2017-06-03',
                'date_label': 'Jun 3, 2017',
                'description': (
                    'Mean Street - 3 Stars - Bulletstorm: Full Clip Edition, '
                    'ECHOES.\n\nNecessary step for the Supernova achievement, 20/20 3 Star '
                    'Echo.\n\nFast Track achievement popped near end when shooting up at people '
                    'on a bridge.\n\nThe achievement is for popping off the snipers on the '
                    '"roof" looks like a bridge to me, before the bomb goes off.'
                ),
                'duration': '6:28',
                'thumbnail': 'tlR9XTEmnxo.jpg',
            },
            {
                'id': 'yX_kyp0EmvM',
                'title': (
                    'Monorail Factory - 3 Stars - Bulletstorm: Full Clip Edition - Half Way There'
                ),
                'date': '2017-06-03',
                'date_label': 'Jun 3, 2017',
                'description': (
                    'Monorail Factory - 3 Stars - Bulletstorm: Full Clip Edition, '
                    'ECHOES.\n\nNecessary step for the Supernova achievement, 19/20 3 Star '
                    'Echo.\n\nHalf way there achievement popped, I did these a little out of '
                    'order as this is the 2nd to last echo. But 45 stars gets this achievement.'
                ),
                'duration': '5:15',
                'thumbnail': 'yX_kyp0EmvM.jpg',
            },
            {
                'id': 'xDs7YgDftbo',
                'title': 'The Storm - 3 Stars - Bulletstorm: Full Clip Edition - Bounty Hunter',
                'date': '2017-06-03',
                'date_label': 'Jun 3, 2017',
                'description': (
                    'The Storm - 3 Stars - Bulletstorm: Full Clip Edition, ECHOES.\n\nNecessary '
                    'step for the Supernova achievement, 14/20 3 Star Echo.\n\nBounty Hunter '
                    'achievement for 125k total points in echo mode, you may get in from another '
                    'echo mine just popped here.'
                ),
                'duration': '5:21',
                'thumbnail': 'xDs7YgDftbo.jpg',
            },
            {
                'id': 'CToWPUfEjjU',
                'title': 'Downtown - 3 Stars - Bulletstorm: Full Clip Edition - Star struck',
                'date': '2017-06-03',
                'date_label': 'Jun 3, 2017',
                'description': (
                    'Downtown - 3 Stars - Bulletstorm: Full Clip Edition, ECHOES.\n\nNecessary '
                    'step for the Supernova achievement, 13/20 3 Star Echo.\n\nStar struck for 3 '
                    'star on 10 echoes.'
                ),
                'duration': '3:59',
                'thumbnail': 'CToWPUfEjjU.jpg',
            },
            {
                'id': 'VdQaUItSqgg',
                'title': (
                    'The Mall - 3 Stars - Bulletstorm: Full Clip Edition - Enforcer Achievement'
                ),
                'date': '2017-06-03',
                'date_label': 'Jun 3, 2017',
                'description': (
                    'The Mall - 3 Stars - Bulletstorm: Full Clip Edition, ECHOES.\n\nNecessary '
                    'step for the Supernova achievement, 12/20 3 Star Echo.\n\nEnforcer '
                    'achievement for score greater than 15k.'
                ),
                'duration': '7:13',
                'thumbnail': 'VdQaUItSqgg.jpg',
            },
            {
                'id': 'iJkLmZsBXJg',
                'title': 'The Park - 3 Stars - Bulletstorm: Full Clip Edition',
                'date': '2017-06-03',
                'date_label': 'Jun 3, 2017',
                'description': (
                    'The Park - 3 Stars - Bulletstorm: Full Clip Edition, ECHOES.\n\nNecessary '
                    'step for the Supernova achievement, 9/20 3 Star Echo.'
                ),
                'duration': '5:22',
                'thumbnail': 'iJkLmZsBXJg.jpg',
            },
            {
                'id': 'AsTni0G-hPw',
                'title': 'Forbidden Zone - 3 Stars - Bulletstorm: Full Clip Edition',
                'date': '2017-06-03',
                'date_label': 'Jun 3, 2017',
                'description': (
                    'Forbidden Zone - 3 Stars - Bulletstorm: Full Clip Edition, '
                    'ECHOES.\n\nNecessary step for the Supernova achievement, 8/20 3 Star Echo.'
                ),
                'duration': '3:22',
                'thumbnail': 'AsTni0G-hPw.jpg',
            },
            {
                'id': 'qf5hlGjhIFA',
                'title': 'The Marina - 3 Stars - Bulletstorm: Full Clip Edition',
                'date': '2017-06-02',
                'date_label': 'Jun 2, 2017',
                'description': (
                    'The Marina - 3 Stars - Bulletstorm: Full Clip Edition, ECHOES.\n\nNecessary '
                    'step for the Supernova achievement, 6/20 3 Star Echo.'
                ),
                'duration': '3:06',
                'thumbnail': 'qf5hlGjhIFA.jpg',
            },
            {
                'id': 'ucFlQD0xxnI',
                'title': 'Waterways - 3 Stars - Bulletstorm: Full Clip Edition',
                'date': '2017-06-02',
                'date_label': 'Jun 2, 2017',
                'description': (
                    'Waterways - 3 Stars - Bulletstorm: Full Clip Edition, ECHOES.\n\nNecessary '
                    'step for the Supernova achievement, 5/20 3 Star Echo.'
                ),
                'duration': '4:15',
                'thumbnail': 'ucFlQD0xxnI.jpg',
            },
            {
                'id': '2i48fjSpB5o',
                'title': 'The Club - 3 Stars - Bulletstorm: Full Clip Edition',
                'date': '2017-06-02',
                'date_label': 'Jun 2, 2017',
                'description': (
                    'The Club - 3 Stars - Bulletstorm: Full Clip Edition, ECHOES.\n\nNecessary '
                    'step for the Supernova achievement, 3/20 3 Star Echo.'
                ),
                'duration': '5:00',
                'thumbnail': '2i48fjSpB5o.jpg',
            },
            {
                'id': 'A36rC2HnpeQ',
                'title': 'Rooftops - 3 Stars - Bulletstorm: Full Clip Edition',
                'date': '2017-06-02',
                'date_label': 'Jun 2, 2017',
                'description': (
                    'Rooftops - 3 Stars - Bulletstorm: Full Clip Edition, ECHOES.\n\nNecessary '
                    'step for the Supernova achievement, 4/20 3 Star Echo.'
                ),
                'duration': '4:03',
                'thumbnail': 'A36rC2HnpeQ.jpg',
            },
            {
                'id': 'HLkXMt6p9UQ',
                'title': 'The Power Plant - 3 Stars - Bulletstorm: Full Clip Edition',
                'date': '2017-06-02',
                'date_label': 'Jun 2, 2017',
                'description': (
                    'The Power Plant - 3 Stars - Bulletstorm: Full Clip Edition, '
                    'ECHOES.\n\nNecessary step for the Supernova achievement, 7/20 3 Star Echo.'
                ),
                'duration': '5:03',
                'thumbnail': 'HLkXMt6p9UQ.jpg',
            },
            {
                'id': 'sC43XGkUoIU',
                'title': 'Heart Attack Achievement - Bulletstorm: Full Clip Edition',
                'date': '2017-06-02',
                'date_label': 'Jun 2, 2017',
                'description': (
                    'Easily acheved, but easy to miss too by an accidental kill heh.\n\nPlay the '
                    'level, get to wave 5 for the first boss. Get em to his knees once, '
                    'leash/kick his helmet off. Get him on his knees again and leash/kick hot '
                    'dog cart for kill.\n\nBest method of survival - hide in the bar area, '
                    'crouch for avoidance. kick and leash towards shocking wall for easy kills. '
                    'Upg def/health during wave changes.\n\nHeart Attack Achievement on the '
                    'level Hotel Elysium. Multiplayer, private match, choose level Hotel '
                    'Elysium. Bulletstorm: Full Clip Edition. Xbox One.'
                ),
                'duration': '18:33',
                'thumbnail': 'sC43XGkUoIU.jpg',
            },
            {
                'id': 'AyFGiyQguq8',
                'title': 'Environmentalist Achievement - Bulletstorm: Full Clip Edition',
                'date': '2017-06-01',
                'date_label': 'Jun 1, 2017',
                'description': (
                    "You can easily get this achievement on the first wave.\n\nYou're looking "
                    'out for the following skillshots.\n-Railed- kick/leash one of the rail '
                    'carts for kill\n-Man Toast- kick enemy in to fire pit\n-Blood Bath- kick in '
                    'to fan\n-Man Crush- kick towards the construction looking '
                    'equipment\n-Golden Shower- leash "hot molten lava" on to enemy for '
                    'kill\n\n\n\nEnvironmentalist Achievement on the level Rock Quarry. '
                    'Multiplayer, private match, choose level Rock Quarry. Bulletstorm: Full '
                    'Clip Edition. Xbox One.'
                ),
                'duration': '3:05',
                'thumbnail': 'AyFGiyQguq8.jpg',
            },
            {
                'id': 'Qt6iAKTpK5w',
                'title': 'PS4::Division',
                'date': '2017-01-16',
                'date_label': 'Jan 16, 2017',
                'description': (
                    'Twitch: http://www.twitch.tv/enonymous1gaming\n\nTwitter: '
                    'https://twitter.com/enonymous1\n           @enonymous1'
                ),
                'duration': '3:33:15',
                'thumbnail': 'Qt6iAKTpK5w.jpg',
            },
            {
                'id': 'QY70IzLnVvk',
                'title': 'PS4::Battlefield 1',
                'date': '2016-12-06',
                'date_label': 'Dec 6, 2016',
                'description': (
                    'Twitch: http://www.twitch.tv/enonymous1gaming\n\nTwitter: '
                    'https://twitter.com/enonymous1\n           @enonymous1'
                ),
                'duration': '50:05',
                'thumbnail': 'QY70IzLnVvk.jpg',
            },
            {
                'id': 'M19UIMYVbmU',
                'title': 'PS4::Battlefield 1',
                'date': '2016-12-02',
                'date_label': 'Dec 2, 2016',
                'description': (
                    'Twitch: http://www.twitch.tv/enonymous1gaming\n\nTwitter: '
                    'https://twitter.com/enonymous1\n           @enonymous1'
                ),
                'duration': '3:47:13',
                'thumbnail': 'M19UIMYVbmU.jpg',
            },
            {
                'id': 'GOzdeQVkPOw',
                'title': 'PS4::Apotheon',
                'date': '2016-10-26',
                'date_label': 'Oct 26, 2016',
                'description': (
                    'Twitch: http://www.twitch.tv/enonymous1gaming\n\nTwitter: '
                    'https://twitter.com/enonymous1\n           @enonymous1'
                ),
                'duration': '16:23',
                'thumbnail': 'GOzdeQVkPOw.jpg',
            },
            {
                'id': '06Xr3208xaU',
                'title': 'PS4::Furi',
                'date': '2016-10-26',
                'date_label': 'Oct 26, 2016',
                'description': (
                    'Twitch: http://www.twitch.tv/enonymous1gaming\n\nTwitter: '
                    'https://twitter.com/enonymous1\n           @enonymous1'
                ),
                'duration': '41:12',
                'thumbnail': '06Xr3208xaU.jpg',
            },
            {
                'id': 'BFo2yuhEKgw',
                'title': 'PS4::Saints Row:Gat out of Hell',
                'date': '2016-10-10',
                'date_label': 'Oct 10, 2016',
                'description': (
                    'Twitch: http://www.twitch.tv/enonymous1gaming\n\nTwitter: '
                    'https://twitter.com/enonymous1\n           @enonymous1'
                ),
                'duration': '2:13:58',
                'thumbnail': 'BFo2yuhEKgw.jpg',
            },
            {
                'id': 'GLATt0NousI',
                'title': 'PS4::Saints Row:Gat out of Hell',
                'date': '2016-10-10',
                'date_label': 'Oct 10, 2016',
                'description': (
                    'Twitch: http://www.twitch.tv/enonymous1gaming\n\nTwitter: '
                    'https://twitter.com/enonymous1\n           @enonymous1'
                ),
                'duration': '21:47',
                'thumbnail': 'GLATt0NousI.jpg',
            },
            {
                'id': '2fn_2UV6YoY',
                'title': 'PS4::Apotheon',
                'date': '2016-10-09',
                'date_label': 'Oct 9, 2016',
                'description': (
                    'Twitch: http://www.twitch.tv/enonymous1gaming\n\nTwitter: '
                    'https://twitter.com/enonymous1\n           @enonymous1'
                ),
                'duration': '28:34',
                'thumbnail': '2fn_2UV6YoY.jpg',
            },
            {
                'id': '5VqHjGy1kOw',
                'title': 'Late night',
                'date': '2016-07-18',
                'date_label': 'Jul 18, 2016',
                'description': (
                    'Twitch: http://www.twitch.tv/enonymous1gaming\n\nTwitter: '
                    'https://twitter.com/enonymous1\n           @enonymous1'
                ),
                'duration': '35:49',
                'thumbnail': '5VqHjGy1kOw.jpg',
            },
            {
                'id': 'WwOT6eknP5Y',
                'title': 'Late night',
                'date': '2016-07-12',
                'date_label': 'Jul 12, 2016',
                'description': (
                    'Twitch: http://www.twitch.tv/enonymous1gaming\n\nTwitter: '
                    'https://twitter.com/enonymous1\n           @enonymous1'
                ),
                'duration': '32:32',
                'thumbnail': 'WwOT6eknP5Y.jpg',
            },
            {
                'id': 'A1WLhjdWwkE',
                'title': 'Late night',
                'date': '2016-07-08',
                'date_label': 'Jul 8, 2016',
                'description': (
                    'Twitch: http://www.twitch.tv/enonymous1gaming\n\nTwitter: '
                    'https://twitter.com/enonymous1\n           @enonymous1'
                ),
                'duration': '4:00',
                'thumbnail': 'A1WLhjdWwkE.jpg',
            },
            {
                'id': 'JIETb0ZSp18',
                'title': 'Overwatch',
                'date': '2016-06-21',
                'date_label': 'Jun 21, 2016',
                'description': (
                    'Twitch: http://www.twitch.tv/enonymous1gaming\n\nTwitter: '
                    'https://twitter.com/enonymous1\n           @enonymous1'
                ),
                'duration': '1:12:26',
                'thumbnail': 'JIETb0ZSp18.jpg',
            },
            {
                'id': 'imDb-f7LGnk',
                'title': 'Overwatch',
                'date': '2016-06-21',
                'date_label': 'Jun 21, 2016',
                'description': (
                    'Twitch: http://www.twitch.tv/enonymous1gaming\n\nTwitter: '
                    'https://twitter.com/enonymous1\n           @enonymous1'
                ),
                'duration': '2:28:17',
                'thumbnail': 'imDb-f7LGnk.jpg',
            },
            {
                'id': 'Am_AKLhSG6c',
                'title': 'Overwatch',
                'date': '2016-06-03',
                'date_label': 'Jun 3, 2016',
                'description': (
                    'Twitch: http://www.twitch.tv/enonymous1gaming\n\nTwitter: '
                    'https://twitter.com/enonymous1\n           @enonymous1'
                ),
                'duration': '1:31:21',
                'thumbnail': 'Am_AKLhSG6c.jpg',
            },
            {
                'id': 'L8cwe3AQmCw',
                'title': 'Overwatch',
                'date': '2016-05-31',
                'date_label': 'May 31, 2016',
                'description': (
                    'Twitch: http://www.twitch.tv/enonymous1gaming\n\nTwitter: '
                    'https://twitter.com/enonymous1\n           @enonymous1'
                ),
                'duration': '1:13:10',
                'thumbnail': 'L8cwe3AQmCw.jpg',
            },
            {
                'id': 'usXGbfkBZtE',
                'title': 'Galak-Z',
                'date': '2016-05-31',
                'date_label': 'May 31, 2016',
                'description': (
                    'Twitch: http://www.twitch.tv/enonymous1gaming\n\nTwitter: '
                    'https://twitter.com/enonymous1\n           @enonymous1'
                ),
                'duration': '2:15:14',
                'thumbnail': 'usXGbfkBZtE.jpg',
            },
            {
                'id': '-RuPKeGfM7c',
                'title': 'Overwatch',
                'date': '2016-05-30',
                'date_label': 'May 30, 2016',
                'description': (
                    'Twitch: http://www.twitch.tv/enonymous1gaming\n\nTwitter: '
                    'https://twitter.com/enonymous1\n           @enonymous1'
                ),
                'duration': '4:21',
                'thumbnail': '-RuPKeGfM7c.jpg',
            },
            {
                'id': 'lNqFqnOmGYY',
                'title': 'Overwatch',
                'date': '2016-05-29',
                'date_label': 'May 29, 2016',
                'description': (
                    'Twitch: http://www.twitch.tv/enonymous1gaming\n\nTwitter: '
                    'https://twitter.com/enonymous1\n           @enonymous1'
                ),
                'duration': '1:11:03',
                'thumbnail': 'lNqFqnOmGYY.jpg',
            },
            {
                'id': 'YD3-1u-UqvY',
                'title': 'Overwatch',
                'date': '2016-05-28',
                'date_label': 'May 28, 2016',
                'description': (
                    'Twitch: http://www.twitch.tv/enonymous1gaming\n\nTwitter: '
                    'https://twitter.com/enonymous1\n           @enonymous1'
                ),
                'duration': '1:57:55',
                'thumbnail': 'YD3-1u-UqvY.jpg',
            },
            {
                'id': 'sutgDpmTAyQ',
                'title': 'Overwatch',
                'date': '2016-05-28',
                'date_label': 'May 28, 2016',
                'description': (
                    'Twitch: http://www.twitch.tv/enonymous1gaming\n\nTwitter: '
                    'https://twitter.com/enonymous1\n           @enonymous1'
                ),
                'duration': '2:09:21',
                'thumbnail': 'sutgDpmTAyQ.jpg',
            },
            {
                'id': 'YzXvQOJo4RI',
                'title': 'Overwatch',
                'date': '2016-05-28',
                'date_label': 'May 28, 2016',
                'description': (
                    'Twitch: http://www.twitch.tv/enonymous1gaming\n\nTwitter: '
                    'https://twitter.com/enonymous1\n           @enonymous1'
                ),
                'duration': '26:07',
                'thumbnail': 'YzXvQOJo4RI.jpg',
            },
            {
                'id': 'zEPozXMh10I',
                'title': 'Overwatch',
                'date': '2016-05-28',
                'date_label': 'May 28, 2016',
                'description': (
                    'Twitch: http://www.twitch.tv/enonymous1gaming\n\nTwitter: '
                    'https://twitter.com/enonymous1\n           @enonymous1'
                ),
                'duration': '2:58:37',
                'thumbnail': 'zEPozXMh10I.jpg',
            },
            {
                'id': 'ZWR25jEsiLg',
                'title': 'Warhammer: Space Hulk Deathwing Trailer',
                'date': '2015-02-17',
                'date_label': 'Feb 17, 2015',
                'description': (
                    'Next gen game set in warhammer universe. \n\ngoo.gl/5uUwL2\n\n#warhammer '
                    '#spacehulk #deathwing'
                ),
                'duration': '1:52',
                'thumbnail': 'ZWR25jEsiLg.jpg',
            },
            {
                'id': 'ZNW4SoV777E',
                'title': 'Dark Souls Stray Demon Win',
                'date': '2014-06-20',
                'date_label': 'Jun 20, 2014',
                'description': 'Stray Demon, defeated!',
                'duration': '3:50',
                'thumbnail': 'ZNW4SoV777E.jpg',
            },
            {
                'id': 'YjQus1p9Btc',
                'title': 'South Park The Stick of Truth Day Walker Achievement',
                'date': '2014-04-07',
                'date_label': 'Apr 7, 2014',
                'description': (
                    'Grab the ginger freckles, pop em on, mash buttons, win. Easy achievement to '
                    'miss, easy achievement to get.'
                ),
                'duration': '1:36',
                'thumbnail': 'YjQus1p9Btc.jpg',
            },
            {
                'id': 'ziKgyxiqSjI',
                'title': 'Stick of Truth UFO crash & First Day in South Park Achievement',
                'date': '2014-04-07',
                'date_label': 'Apr 7, 2014',
                'description': '',
                'duration': '1:19',
                'thumbnail': 'ziKgyxiqSjI.jpg',
            },
            {
                'id': 'uJ5jnFp_0lU',
                'title': 'South Park Stick of Truth Bard Battle',
                'date': '2014-04-07',
                'date_label': 'Apr 7, 2014',
                'description': (
                    'My Jew taking out the Bard to get the New Kid on the Block achievement =) I '
                    'personally like all the Jews abilities, my first run through was a Mage and '
                    'that battle was a little more embarassing heh.'
                ),
                'duration': '5:43',
                'thumbnail': 'uJ5jnFp_0lU.jpg',
            },
            {
                'id': 'pNFgQx41knw',
                'title': 'South Park New Kid on the Block Achievement',
                'date': '2014-04-07',
                'date_label': 'Apr 7, 2014',
                'description': (
                    'Just a short video to show you when and where this achievement pops.'
                ),
                'duration': '0:46',
                'thumbnail': 'pNFgQx41knw.jpg',
            },
            {
                'id': '4lJl-4pUrs0',
                'title': 'South Park Stick of Truth Intro with Subs',
                'date': '2014-04-07',
                'date_label': 'Apr 7, 2014',
                'description': (
                    'South Park Stick of Truth Intro with Subs, just finished my 1k for this '
                    'game now just throwing some videos up so others can get a look at it.'
                ),
                'duration': '1:20',
                'thumbnail': '4lJl-4pUrs0.jpg',
            },
            {
                'id': '6i_jlm4Eqx4',
                'title': 'Xbox One COD Ghosts FFA Tremor 30 3',
                'date': '2014-04-06',
                'date_label': 'Apr 6, 2014',
                'description': '',
                'duration': '6:51',
                'thumbnail': '6i_jlm4Eqx4.jpg',
            },
        ],
    },
]
