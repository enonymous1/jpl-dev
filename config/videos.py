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
]
