"""
Synthetic seed data generator for Spotify Analytics Dashboard.
Uses real artist/album/song names.
"""
import random
from datetime import datetime, timedelta

random.seed(42)

# genre_id -> genre name (10 genres)
GENRES = [
    (1, "Indie/Alternative"),
    (2, "Hip-Hop"),
    (3, "R&B/Soul"),
    (4, "Electronic/Synth-Pop"),
    (5, "Pop"),
    (6, "Rock"),
    (7, "Neo-Soul"),
    (8, "Folk/Indie-Folk"),
    (9, "Latin Trap"),
    (10, "Dream Pop"),
]

# artist_id, name, spotify_uri, genre_id
# Real artists mapped to closest genre
ARTISTS = [
    (1,  "Arctic Monkeys",    "spotify:artist:7Ln80lUS6He07XvHI8qqHH", 6),
    (2,  "Kendrick Lamar",    "spotify:artist:2YZyLoL8N0Wb9xBt1NhZWg", 2),
    (3,  "Tame Impala",       "spotify:artist:5INjqkS1o8h1imAzPqGZnR", 4),
    (4,  "Frank Ocean",       "spotify:artist:2h93pZq0e7k5yf4dywlkpM", 3),
    (5,  "Billie Eilish",     "spotify:artist:6qqNVTkY8uBg9cP3Jd7DAH", 5),
    (6,  "Travis Scott",      "spotify:artist:0Y5tJX1MQlPlqiwlOH1tJY", 2),
    (7,  "SZA",               "spotify:artist:7tYKF4w9nC0nq9CsPZTHyP", 3),
    (8,  "The Weeknd",        "spotify:artist:1Xyo4u8uXC1ZmMpatF05PJ", 3),
    (9,  "Tyler the Creator", "spotify:artist:4V8LLVI7uiuKyYONFAozRU", 2),
    (10, "Harry Styles",      "spotify:artist:6KImCVD70vtIoJWnq6nGn3", 5),
    (11, "Bad Bunny",         "spotify:artist:4q3ewBCX7sLwd24euuV69X", 9),
    (12, "Dua Lipa",          "spotify:artist:6M2wZ9GZgrQXHCFfjv46we", 5),
    (13, "Post Malone",       "spotify:artist:246dkjvS1zLTtiykXe5h60", 5),
    (14, "Lana Del Rey",      "spotify:artist:00FQb4jTyendYWaN8pK0wa", 10),
    (15, "Childish Gambino",  "spotify:artist:73sIBHcqh3Z3NyqHKZ7FOL", 3),
    (16, "Mac Miller",        "spotify:artist:4LLpKhyESBncEAOqgqSWIN", 2),
    (17, "Clairo",            "spotify:artist:5IbEL2xjRtjnJOd9BVeABN", 10),
    (18, "Steve Lacy",        "spotify:artist:5lDQHAnk5nCrNWbXFsv9rT", 7),
    (19, "Phoebe Bridgers",   "spotify:artist:1r1uxoy19fzMxunt3ONAkG", 8),
    (20, "Vampire Weekend",   "spotify:artist:5BvJzeQpmsdsFp4HGUYUEx", 1),
    (21, "Radiohead",         "spotify:artist:4Z8W4fKeB5YxbusRsdQVPb", 6),
    (22, "Bon Iver",          "spotify:artist:4LEiUm1SRbFMgfqnQTwUbQ", 8),
    (23, "Rex Orange County", "spotify:artist:74ASZWbe4lXaubB36ztrGX", 10),
    (24, "Daniel Caesar",     "spotify:artist:20wkVLutqVOYrc0kxFs7rA", 7),
    (25, "Omar Apollo",       "spotify:artist:7f8rFoOyExydnlBEcBJxoU", 7),
    (26, "Fleet Foxes",       "spotify:artist:3RGLhK1IP9jnYFH4BRFJBS", 8),
    (27, "Sufjan Stevens",    "spotify:artist:4MXUO7sVCaFgFjoTI5ox5c", 8),
    (28, "The Midnight",      "spotify:artist:2CIMQHirSU0MQqyYHq0eOx", 4),
    (29, "Jacob Collier",     "spotify:artist:0QWrMNukfcVOmgEU0FEDyD", 7),
    (30, "Jungle",            "spotify:artist:7IMhMPLDzFNYkqGbGJHtxN", 4),
]

# album_id, title, release_date, total_tracks, artist_id
ALBUMS = [
    # Arctic Monkeys (artist 1)
    (1,  "AM",                        "2013-09-09", 12, 1),
    (2,  "Whatever People Say I Am",  "2006-01-23", 13, 1),
    # Kendrick Lamar (artist 2)
    (3,  "To Pimp a Butterfly",       "2015-03-15", 16, 2),
    (4,  "DAMN.",                     "2017-04-14", 14, 2),
    # Tame Impala (artist 3)
    (5,  "Currents",                  "2015-07-17", 13, 3),
    (6,  "Lonerism",                  "2012-10-05", 13, 3),
    # Frank Ocean (artist 4)
    (7,  "Blonde",                    "2016-08-20", 17, 4),
    (8,  "Channel Orange",            "2012-07-10", 17, 4),
    # Billie Eilish (artist 5)
    (9,  "When We All Fall Asleep",   "2019-03-29", 14, 5),
    (10, "Happier Than Ever",         "2021-07-30", 16, 5),
    # Travis Scott (artist 6)
    (11, "ASTROWORLD",                "2018-08-03", 17, 6),
    (12, "Rodeo",                     "2015-09-04", 16, 6),
    # SZA (artist 7)
    (13, "SOS",                       "2022-12-09", 23, 7),
    (14, "Ctrl",                      "2017-06-09", 14, 7),
    # The Weeknd (artist 8)
    (15, "After Hours",               "2020-03-20", 14, 8),
    (16, "Starboy",                   "2016-11-25", 18, 8),
    # Tyler the Creator (artist 9)
    (17, "IGOR",                      "2019-05-17", 12, 9),
    (18, "CALL ME IF YOU GET LOST",   "2021-06-25", 16, 9),
    # Harry Styles (artist 10)
    (19, "Harry's House",             "2022-05-20", 13, 10),
    (20, "Fine Line",                 "2019-12-13", 12, 10),
    # Bad Bunny (artist 11)
    (21, "Un Verano Sin Ti",          "2022-05-06", 23, 11),
    (22, "YHLQMDLG",                  "2020-02-29", 20, 11),
    # Dua Lipa (artist 12)
    (23, "Future Nostalgia",          "2020-03-27", 11, 12),
    (24, "Dua Lipa",                  "2017-06-02", 12, 12),
    # Post Malone (artist 13)
    (25, "Hollywood's Bleeding",      "2019-09-06", 17, 13),
    (26, "beerbongs & bentleys",      "2018-04-27", 18, 13),
    # Lana Del Rey (artist 14)
    (27, "Norman Rockwell!",          "2019-08-30", 14, 14),
    (28, "Born to Die",               "2012-01-27", 15, 14),
    # Childish Gambino (artist 15)
    (29, "Awaken, My Love!",          "2016-12-02", 11, 15),
    (30, "Because the Internet",      "2013-12-10", 19, 15),
    # Mac Miller (artist 16)
    (31, "Swimming",                  "2018-08-03", 13, 16),
    (32, "Circles",                   "2020-01-17", 12, 16),
    # Clairo (artist 17)
    (33, "Sling",                     "2021-07-16", 12, 17),
    (34, "Immunity",                  "2019-08-02", 10, 17),
    # Steve Lacy (artist 18)
    (35, "Gemini Rights",             "2022-07-15", 10, 18),
    (36, "Apollo XXI",                "2019-05-24", 13, 18),
    # Phoebe Bridgers (artist 19)
    (37, "Punisher",                  "2020-06-19", 11, 19),
    (38, "Stranger in the Alps",      "2017-09-22", 10, 19),
    # Vampire Weekend (artist 20)
    (39, "Father of the Bride",       "2019-05-03", 18, 20),
    (40, "Modern Vampires of the City","2013-05-07",12, 20),
    # Radiohead (artist 21)
    (41, "OK Computer",               "1997-05-21", 12, 21),
    (42, "In Rainbows",               "2007-10-10", 10, 21),
    # Bon Iver (artist 22)
    (43, "For Emma, Forever Ago",     "2007-07-09",  9, 22),
    (44, "Bon Iver, Bon Iver",        "2011-06-17", 10, 22),
    # Rex Orange County (artist 23)
    (45, "Who Cares?",                "2022-03-11", 10, 23),
    (46, "Pony",                      "2019-10-25", 11, 23),
    # Daniel Caesar (artist 24)
    (47, "Freudian",                  "2017-08-25", 10, 24),
    (48, "Case Study 01",             "2019-06-28", 10, 24),
    # Omar Apollo (artist 25)
    (49, "Ivory",                     "2022-04-08", 13, 25),
    (50, "Apolonio",                  "2020-10-16",  9, 25),
    # Fleet Foxes (artist 26)
    (51, "Fleet Foxes",               "2008-06-03", 11, 26),
    (52, "Helplessness Blues",        "2011-05-03", 12, 26),
    # Sufjan Stevens (artist 27)
    (53, "Carrie & Lowell",           "2015-03-31", 11, 27),
    (54, "Illinois",                  "2005-07-05", 22, 27),
    # The Midnight (artist 28)
    (55, "Monsters",                  "2022-05-13", 12, 28),
    (56, "Endless Summer",            "2016-07-29", 10, 28),
    # Jacob Collier (artist 29)
    (57, "Djesse Vol. 3",             "2020-07-31", 12, 29),
    (58, "Djesse Vol. 1",             "2018-11-02", 12, 29),
    # Jungle (artist 30)
    (59, "Loving in Stereo",          "2021-08-13", 12, 30),
    (60, "Jungle",                    "2014-07-14", 11, 30),
]

# song_id, title, duration_ms, spotify_uri, track_number, album_id
SONGS = [
    # AM - Arctic Monkeys (album 1)
    (1,  "Do I Wanna Know?",          272000, "spotify:track:5FVd6KXrgO9B3JPmC8OPst", 1, 1),
    (2,  "R U Mine?",                 201000, "spotify:track:1C2QJNTmsTxCDBuIgai8QV", 2, 1),
    (3,  "Why'd You Only Call Me When You're High?", 162000, "spotify:track:1UqhkbzB1kuFwt2iy4h29Q", 3, 1),
    (4,  "Arabella",                  207000, "spotify:track:4mrXiMYMMLB8qfKEJOuFBO", 4, 1),
    (5,  "505",                       254000, "spotify:track:0BxE4FqsDD1Ot4YuBXwAPp", 5, 1),
    # Whatever People Say I Am - Arctic Monkeys (album 2)
    (6,  "I Bet You Look Good on the Dancefloor", 172000, "spotify:track:5gFMiWKoFBep5HMfBxiRpK", 1, 2),
    (7,  "Fake Tales of San Francisco", 148000, "spotify:track:14PSmFGEBbWFGhMGEiRQFJ", 3, 2),
    # To Pimp a Butterfly - Kendrick Lamar (album 3)
    (8,  "Alright",                   219000, "spotify:track:3iVcZ5G6tvkXZkZKlMpIUs", 7, 3),
    (9,  "King Kunta",                234000, "spotify:track:2HbKqm4o0w5wEeEFXm2sD1", 3, 3),
    (10, "Momma",                     309000, "spotify:track:7yJcOqFGFR8g5g35mAbJ6P", 11, 3),
    (11, "These Walls",               319000, "spotify:track:2NFWB6W2yMMClFJbFPAWk2", 12, 3),
    # DAMN. - Kendrick Lamar (album 4)
    (12, "HUMBLE.",                   177000, "spotify:track:7KXjTSCq5nL1LoYtL7XAwS", 8, 4),
    (13, "DNA.",                      185000, "spotify:track:6HZILIRieu8S0iqY8kIKhj", 1, 4),
    (14, "LOVE.",                     213000, "spotify:track:6PGoSes0D9eUDeeAafB2As", 11, 4),
    # Currents - Tame Impala (album 5)
    (15, "Let It Happen",             467000, "spotify:track:0tKcYR2II1VCQWT79i5NrW", 1, 5),
    (16, "The Less I Know the Better",218000, "spotify:track:6K4t31amVTZDgR3sKmwUJJ", 7, 5),
    (17, "Eventually",                315000, "spotify:track:3RauEVgRgj1IuWdJ9fDs58", 9, 5),
    (18, "New Person, Same Old Mistakes", 359000, "spotify:track:3cB4g5JkeAyEuBAmJHMlRU", 13, 5),
    # Lonerism - Tame Impala (album 6)
    (19, "Feels Like We Only Go Backwards", 184000, "spotify:track:0tgVpDi06FyKpA1z0VMD4v", 6, 6),
    (20, "Elephant",                  228000, "spotify:track:5S0p1LDuRKetT7V7KbH9Pl", 4, 6),
    # Blonde - Frank Ocean (album 7)
    (21, "Nikes",                     311000, "spotify:track:1DnvgT9HEX4ZBq7yVJdxrN", 1, 7),
    (22, "Self Control",              250000, "spotify:track:3nAFtrsFsION5neJcm1lbq", 9, 7),
    (23, "Pink + White",              213000, "spotify:track:3xKsf9qdS1CyvXSMEid6g8", 3, 7),
    (24, "Ivy",                       257000, "spotify:track:2vDoQ7cMpHPDiRzS2OoHBF", 6, 7),
    # Channel Orange - Frank Ocean (album 8)
    (25, "Thinkin Bout You",          200000, "spotify:track:01iyCAUm8EvOFqVWYJ3dVX", 2, 8),
    (26, "Super Rich Kids",           310000, "spotify:track:5I5bTCjJbHHi3Ll0Y7LUJB", 7, 8),
    # When We All Fall Asleep - Billie Eilish (album 9)
    (27, "bad guy",                   194000, "spotify:track:2Fxmhks0live0jlnFDfxSW", 2, 9),
    (28, "bury a friend",             193000, "spotify:track:4ZtFanR9U6ndgddUvNcjcG", 7, 9),
    (29, "when the party's over",     195000, "spotify:track:43zdsphuZLzwA9k4DJhU0I", 4, 9),
    # Happier Than Ever - Billie Eilish (album 10)
    (30, "Happier Than Ever",         298000, "spotify:track:2bjnBOPLyBpIBUQ8JFmEoV", 15, 10),
    (31, "Therefore I Am",            174000, "spotify:track:4tNbHbO1VGOB0yrFbRWHKP", 5, 10),
    # ASTROWORLD - Travis Scott (album 11)
    (32, "SICKO MODE",                312000, "spotify:track:2xLMifQCjDGFmkHkpNLD9h", 2, 11),
    (33, "Stargazing",                293000, "spotify:track:7fBv7CLKdj4V5Z9TRDjFr4", 1, 11),
    (34, "YOSEMITE",                  239000, "spotify:track:4Oun2ylbjFKMPTiaSbbCih", 11, 11),
    # Rodeo - Travis Scott (album 12)
    (35, "90210",                     407000, "spotify:track:5D7AjRHTwX9vXvZT0DLRsv", 12, 12),
    (36, "3500",                      395000, "spotify:track:2P0bVNXq2BH7NFwVhCDZSg", 7, 12),
    # SOS - SZA (album 13)
    (37, "Kill Bill",                 153000, "spotify:track:1Qrg8KqiBpW07V7PNxwwwL", 2, 13),
    (38, "Shirt",                     193000, "spotify:track:1GufbJUt1mGwWTUVqFe7xF", 5, 13),
    (39, "Nobody Gets Me",            188000, "spotify:track:0JB9JbOOJYHYPDrHLBPBwz", 4, 13),
    # Ctrl - SZA (album 14)
    (40, "Garden (Say It Like Dat)",  233000, "spotify:track:2DDEBhpqzevkmOR3JeD5TZ", 10, 14),
    (41, "The Weekend",               164000, "spotify:track:0l7CTGSmBYRcDPm7krgqgR", 11, 14),
    # After Hours - The Weeknd (album 15)
    (42, "Blinding Lights",           200000, "spotify:track:0VjIjW4GlUZAMYd2vXMi3b", 8, 15),
    (43, "Save Your Tears",           215000, "spotify:track:5QO79kh1waicV47BqGRL3g", 11, 15),
    (44, "After Hours",               361000, "spotify:track:5HCyWlXZPP0y6Gqq8TgA20", 14, 15),
    # Starboy - The Weeknd (album 16)
    (45, "Starboy",                   230000, "spotify:track:5aAx2yezTd8zXrkmtKl66Z", 1, 16),
    (46, "I Feel It Coming",          269000, "spotify:track:3MjUtNVVq3C8Fn0MP3zhXa", 18, 16),
    # IGOR - Tyler the Creator (album 17)
    (47, "EARFQUAKE",                 193000, "spotify:track:4kHtgiRnpmFIgvOHBiLXUu", 2, 17),
    (48, "A BOY IS A GUN*",           195000, "spotify:track:0X2hJLWPiEHJTxsfdFB6on", 7, 17),
    (49, "NEW MAGIC WAND",            161000, "spotify:track:3pLdWdkj83EYfDN6H2N8MR", 8, 17),
    # CALL ME IF YOU GET LOST - Tyler the Creator (album 18)
    (50, "LUMBERJACK",                177000, "spotify:track:2RlgNHKcydI9sayD2Df2xp", 2, 18),
    (51, "WUSYANAME",                 166000, "spotify:track:23EOmJivOZ88WJPUbIPjh6", 4, 18),
    # Harry's House - Harry Styles (album 19)
    (52, "As It Was",                 167000, "spotify:track:4LRPiXqCikLlN15c3yImP7", 1, 19),
    (53, "Late Night Talking",        177000, "spotify:track:4RvWPyQ5RL0ao9LPZeSouE", 3, 19),
    (54, "Music for a Sushi Restaurant", 193000, "spotify:track:3hUxzQpSfdDqR3waM5MBFE", 2, 19),
    # Fine Line - Harry Styles (album 20)
    (55, "Watermelon Sugar",          174000, "spotify:track:6UelLqGlWMcVH1E5c4H7lY", 3, 20),
    (56, "Adore You",                 207000, "spotify:track:3jjujdWJ72nww5eGnfs2E7", 4, 20),
    # Un Verano Sin Ti - Bad Bunny (album 21)
    (57, "Me Porto Bonito",           178000, "spotify:track:6wEEcZkGMtMBFNnF6J0mFH", 11, 21),
    (58, "Titi Me Pregunto",          199000, "spotify:track:1X7P1LxasWL3B0AKeHMgB4", 14, 21),
    (59, "Efecto",                    200000, "spotify:track:6x7sRKqEJBqzMSI8d9clcg", 4, 21),
    # YHLQMDLG - Bad Bunny (album 22)
    (60, "Dakiti",                    222000, "spotify:track:1IHWl5LamUGEuP4uQSpLzc", 1, 22),
    (61, "Yo Perreo Sola",            222000, "spotify:track:5yebkJkRWR9TqzijAFQ5cu", 11, 22),
    # Future Nostalgia - Dua Lipa (album 23)
    (62, "Levitating",                203000, "spotify:track:463CkQjx2Zk1yXoBuierM9", 5, 23),
    (63, "Don't Start Now",           183000, "spotify:track:3PfIrDoz19wz7qK7tYeu62", 2, 23),
    (64, "Physical",                  193000, "spotify:track:6lPb7EDO4tozbC5RFRiHrS", 3, 23),
    # Dua Lipa (album 24)
    (65, "New Rules",                 209000, "spotify:track:2ekn2ttSfGqwhhate0LSR0", 8, 24),
    (66, "IDGAF",                     232000, "spotify:track:6TwzSkLMGuSnfVPKIjlbKB", 11, 24),
    # Hollywood's Bleeding - Post Malone (album 25)
    (67, "Circles",                   215000, "spotify:track:21jGcNKet2qwijlDFuPiPb", 1, 25),
    (68, "Sunflower",                 158000, "spotify:track:3KkXRkHbMCARz0aVfEt68P", 7, 25),
    # beerbongs & bentleys - Post Malone (album 26)
    (69, "Rockstar",                  218000, "spotify:track:0e7ipj03S05BNilyu5bRzt", 5, 26),
    (70, "Better Now",                231000, "spotify:track:0sf12qNH5qcw8qpgymFOqT", 9, 26),
    # Norman Rockwell! - Lana Del Rey (album 27)
    (71, "Mariners Apartment Complex", 260000, "spotify:track:3RcFpVKVbMdwdqQfvq0yIJ", 2, 27),
    (72, "Venice Bitch",              678000, "spotify:track:3c3tGSCgmwnXYGh4VaCdIR", 5, 27),
    (73, "Hope is a Dangerous Thing", 234000, "spotify:track:0DWXqBMdxVJZCNHSvgFW5R", 14, 27),
    # Born to Die - Lana Del Rey (album 28)
    (74, "Summertime Sadness",        265000, "spotify:track:4MxHkGMPtXYvqQ5xHFBFJj", 11, 28),
    (75, "Video Games",               289000, "spotify:track:3ZCTVFBt2Brf31RLEnCkWJ", 2, 28),
    # Awaken, My Love! - Childish Gambino (album 29)
    (76, "Redbone",                   326000, "spotify:track:6K4t31amVTZDgR3sKmwUJJ", 9, 29),
    (77, "Me and Your Mama",          284000, "spotify:track:4FPanCYfHVhFMnkJqMRNaq", 1, 29),
    # Because the Internet - Childish Gambino (album 30)
    (78, "3005",                      254000, "spotify:track:0h4CEMBp7oqFWFH1B9WiIX", 11, 30),
    (79, "Sweatpants",                232000, "spotify:track:4SFkw1R1HiUlJFKaFXGIiM", 10, 30),
    # Swimming - Mac Miller (album 31)
    (80, "Self Care",                 336000, "spotify:track:2tnVG71enUj33Ic2nFN6kZ", 1, 31),
    (81, "Small Worlds",              264000, "spotify:track:7sFQ8sFVMRUb6UNnkCZJqm", 5, 31),
    (82, "Ladders",                   246000, "spotify:track:3MN4nnbBLbhK3w4K4FvLoo", 6, 31),
    # Circles - Mac Miller (album 32)
    (83, "Good News",                 230000, "spotify:track:6tNQ70jh4OwmPGpYy6R2o8", 1, 32),
    (84, "Blue World",                242000, "spotify:track:4AnnkxIbxvp8bCPAJUCzNX", 4, 32),
    # Sling - Clairo (album 33)
    (85, "Blouse",                    197000, "spotify:track:4FKjKMYb3bNjBt0M0b74fC", 1, 33),
    (86, "Amoeba",                    215000, "spotify:track:2IjRqGSECLmsFJBoN9x8M9", 3, 33),
    # Immunity - Clairo (album 34)
    (87, "Bags",                      222000, "spotify:track:3I5DLcexvNdpMRQWWe6k3Q", 2, 34),
    (88, "Sofia",                     171000, "spotify:track:3Vo4wInECJIAmBSnAaJTgI", 3, 34),
    # Gemini Rights - Steve Lacy (album 35)
    (89, "Bad Habit",                 233000, "spotify:track:3iRbhm99GCAqrKcVP3gFbq", 5, 35),
    (90, "Helmet",                    174000, "spotify:track:3nAFtrsFsION5neJcm1lbq", 3, 35),
    # Apollo XXI - Steve Lacy (album 36)
    (91, "Only If",                   168000, "spotify:track:0M1WUYjl8BpvGAFVfuRFRc", 3, 36),
    (92, "N Side",                    237000, "spotify:track:5HCyWlXZPP0y6Gqq8TgA20", 9, 36),
    # Punisher - Phoebe Bridgers (album 37)
    (93, "Garden Song",               199000, "spotify:track:3NcEOQFsXUovQST4YeSfFU", 1, 37),
    (94, "Savior Complex",            244000, "spotify:track:0I3Q5gp5lbF6YCNSjvTNha", 4, 37),
    (95, "Moon Song",                 193000, "spotify:track:0G7S1buJt8dVQOmABj9nwh", 7, 37),
    # Stranger in the Alps - Phoebe Bridgers (album 38)
    (96, "Motion Sickness",           202000, "spotify:track:2ooMCikAMSmTyUhRDqUaCl", 3, 38),
    # Father of the Bride - Vampire Weekend (album 39)
    (97,  "Harmony Hall",             243000, "spotify:track:6K4t31amVTZDgR3sKmwUJJ", 1, 39),
    (98,  "This Life",                215000, "spotify:track:3RGLhK1IP9jnYFH4BRFJBS", 3, 39),
    # Modern Vampires of the City - Vampire Weekend (album 40)
    (99,  "Diane Young",              163000, "spotify:track:4Z8W4fKeB5YxbusRsdQVPb", 3, 40),
    (100, "Hannah Hunt",              251000, "spotify:track:5BvJzeQpmsdsFp4HGUYUEx", 5, 40),
    # OK Computer - Radiohead (album 41)
    (101, "Karma Police",             261000, "spotify:track:63OQupATfueTdZMWTxW03A", 7, 41),
    (102, "Paranoid Android",         383000, "spotify:track:6LgJvl0Xdtc73RJ1mmpotq", 2, 41),
    (103, "No Surprises",             228000, "spotify:track:10nyaNGT3n0q6oVGBcSmme", 12, 41),
    # In Rainbows - Radiohead (album 42)
    (104, "Reckoner",                 290000, "spotify:track:02ppMPbg1OtEdHg9xbOBjt", 7, 42),
    (105, "All I Need",               227000, "spotify:track:5s6MKCLr0N7yGRzFFMbuuT", 5, 42),
    # For Emma, Forever Ago - Bon Iver (album 43)
    (106, "Skinny Love",              216000, "spotify:track:4XiTBnMhQRfBwQilMmuvYW", 2, 43),
    (107, "Flume",                    193000, "spotify:track:2U89cHdifobFOuOXSPc50f", 1, 43),
    # Bon Iver, Bon Iver (album 44)
    (108, "Holocene",                 346000, "spotify:track:0sUMxJqe7FmzHEALIiOZFj", 4, 44),
    (109, "Calgary",                  231000, "spotify:track:2zT38f8eBtBF0Q25vUb7k7", 9, 44),
    # Who Cares? - Rex Orange County (album 45)
    (110, "Amazing",                  174000, "spotify:track:3MlBqAzA5cKsBwZ2MSUA2n", 2, 45),
    (111, "Keep It Up",               186000, "spotify:track:1rZnJXTNbN5XYRpQYHqhp0", 5, 45),
    # Pony - Rex Orange County (album 46)
    (112, "10/10",                    203000, "spotify:track:6K4t31amVTZDgR3sKmwUJJ", 1, 46),
    (113, "Pluto Projector",          330000, "spotify:track:4LLpKhyESBncEAOqgqSWIN", 6, 46),
    # Freudian - Daniel Caesar (album 47)
    (114, "Get You",                  250000, "spotify:track:5IbEL2xjRtjnJOd9BVeABN", 1, 47),
    (115, "Best Part",                221000, "spotify:track:5lDQHAnk5nCrNWbXFsv9rT", 9, 47),
    # Case Study 01 - Daniel Caesar (album 48)
    (116, "Superposition",            230000, "spotify:track:1r1uxoy19fzMxunt3ONAkG", 1, 48),
    (117, "Cyanide",                  256000, "spotify:track:5BvJzeQpmsdsFp4HGUYUEx", 5, 48),
    # Ivory - Omar Apollo (album 49)
    (118, "Invincible",               213000, "spotify:track:74ASZWbe4lXaubB36ztrGX", 1, 49),
    (119, "Talk",                     225000, "spotify:track:20wkVLutqVOYrc0kxFs7rA", 4, 49),
    # Apolonio - Omar Apollo (album 50)
    (120, "Stayback",                 181000, "spotify:track:7f8rFoOyExydnlBEcBJxoU", 3, 50),
    (121, "Kickback",                 169000, "spotify:track:4q3ewBCX7sLwd24euuV69X", 1, 50),
    # Fleet Foxes (album 51)
    (122, "White Winter Hymnal",      138000, "spotify:track:3RGLhK1IP9jnYFH4BRFJBS", 1, 51),
    (123, "Mykonos",                  281000, "spotify:track:4Z8W4fKeB5YxbusRsdQVPb", 9, 51),
    # Helplessness Blues - Fleet Foxes (album 52)
    (124, "Helplessness Blues",       316000, "spotify:track:5BvJzeQpmsdsFp4HGUYUEx", 2, 52),
    (125, "Montezuma",                279000, "spotify:track:2YZyLoL8N0Wb9xBt1NhZWg", 1, 52),
    # Carrie & Lowell - Sufjan Stevens (album 53)
    (126, "Death With Dignity",       218000, "spotify:track:4LLpKhyESBncEAOqgqSWIN", 1, 53),
    (127, "Should Have Known Better", 261000, "spotify:track:5INjqkS1o8h1imAzPqGZnR", 2, 53),
    # Illinois - Sufjan Stevens (album 54)
    (128, "Chicago",                  375000, "spotify:track:6M2wZ9GZgrQXHCFfjv46we", 8, 54),
    (129, "Casimir Pulaski Day",       337000, "spotify:track:2h93pZq0e7k5yf4dywlkpM", 6, 54),
    # Monsters - The Midnight (album 55)
    (130, "Monsters",                 250000, "spotify:track:6qqNVTkY8uBg9cP3Jd7DAH", 1, 55),
    (131, "Fire",                     216000, "spotify:track:0Y5tJX1MQlPlqiwlOH1tJY", 4, 55),
    (132, "Avalanche",                228000, "spotify:track:7tYKF4w9nC0nq9CsPZTHyP", 6, 55),
    # Endless Summer - The Midnight (album 56)
    (133, "Endless Summer",           306000, "spotify:track:1Xyo4u8uXC1ZmMpatF05PJ", 1, 56),
    (134, "The Comeback Kid",         218000, "spotify:track:4V8LLVI7uiuKyYONFAozRU", 5, 56),
    # Djesse Vol. 3 - Jacob Collier (album 57)
    (135, "All I Need",               304000, "spotify:track:246dkjvS1zLTtiykXe5h60", 1, 57),
    (136, "He Won't Hold You",        261000, "spotify:track:00FQb4jTyendYWaN8pK0wa", 4, 57),
    # Djesse Vol. 1 - Jacob Collier (album 58)
    (137, "With the Love in My Heart",337000, "spotify:track:73sIBHcqh3Z3NyqHKZ7FOL", 1, 58),
    (138, "Hideaway",                 236000, "spotify:track:4LRPiXqCikLlN15c3yImP7", 7, 58),
    # Loving in Stereo - Jungle (album 59)
    (139, "Keep Moving",              206000, "spotify:track:0QWrMNukfcVOmgEU0FEDyD", 1, 59),
    (140, "Problemz",                 225000, "spotify:track:7IMhMPLDzFNYkqGbGJHtxN", 3, 59),
    (141, "Romeo",                    220000, "spotify:track:5lDQHAnk5nCrNWbXFsv9rT", 7, 59),
    # Jungle (album 60)
    (142, "Busy Earnin'",             212000, "spotify:track:6K4t31amVTZDgR3sKmwUJJ", 1, 60),
    (143, "Time",                     232000, "spotify:track:4LLpKhyESBncEAOqgqSWIN", 4, 60),
    # Extra songs to reach 150+
    (144, "Arabesque",                329000, "spotify:track:5INjqkS1o8h1imAzPqGZnR", 5, 59),
    (145, "Good Grief",               195000, "spotify:track:2h93pZq0e7k5yf4dywlkpM", 6, 59),
    (146, "505 (Live)",               264000, "spotify:track:6M2wZ9GZgrQXHCFfjv46we", 13, 2),
    (147, "Fluorescent Adolescent",   177000, "spotify:track:7tYKF4w9nC0nq9CsPZTHyP", 8, 2),
    (148, "Cornerstone",              188000, "spotify:track:1Xyo4u8uXC1ZmMpatF05PJ", 12, 2),
    (149, "Crying Lightning",         212000, "spotify:track:4V8LLVI7uiuKyYONFAozRU", 7, 2),
    (150, "Snap Out of It",           195000, "spotify:track:246dkjvS1zLTtiykXe5h60", 9, 2),
]

USER_NAMES = [
    "arjun_beats", "priya_melody", "rohan_vibes", "ananya_tunes",
    "vikram_rhythm", "ishaan_flow", "kavya_sounds", "pranav_tracks",
    "shreya_music", "aditya_notes"
]

lines = []
lines.append("-- Auto-generated seed data (real artist/album/song names)")
lines.append("")

# Genres
lines.append("-- GENRES")
for gid, gname in GENRES:
    lines.append(f"INSERT INTO genre (genre_id, name) VALUES ({gid}, '{gname}');")
lines.append("")

# Artists
lines.append("-- ARTISTS")
for aid, aname, auri, agid in ARTISTS:
    safe = aname.replace("'","''")
    lines.append(f"INSERT INTO artist (artist_id, name, spotify_uri, genre_id) VALUES ({aid}, '{safe}', '{auri}', {agid});")
lines.append("")

# Albums
lines.append("-- ALBUMS")
for alid, altitle, aldate, altracks, alartist in ALBUMS:
    safe = altitle.replace("'","''")
    lines.append(f"INSERT INTO album (album_id, title, release_date, total_tracks, artist_id) VALUES ({alid}, '{safe}', '{aldate}', {altracks}, {alartist});")
lines.append("")

# Songs
lines.append("-- SONGS")
for sid, stitle, sdur, suri, strk, salb in SONGS:
    safe = stitle.replace("'","''")
    lines.append(f"INSERT INTO song (song_id, title, duration_ms, spotify_uri, track_number, album_id) VALUES ({sid}, '{safe}', {sdur}, '{suri}', {strk}, {salb});")
lines.append("")

# Users
lines.append("-- USERS")
for i, uname in enumerate(USER_NAMES, 1):
    email = f"{uname}@example.com"
    spotify_id = f"spotify_user_{i:04d}"
    yr = random.randint(2020,2022)
    mo = random.randint(1,12)
    dy = random.randint(1,28)
    lines.append(f"INSERT INTO app_user (user_id, username, email, spotify_id, created_at) "
                 f"VALUES ({i}, '{uname}', '{email}', '{spotify_id}', '{yr}-{mo:02d}-{dy:02d}');")
lines.append("")

# Play history: each user has ~30 favourite songs they listen to heavily
TOTAL_SONGS = len(SONGS)
random.seed(42)

user_favourites = {}
for uid in range(1, 11):
    favs = random.sample([s[0] for s in SONGS], min(30, TOTAL_SONGS))
    user_favourites[uid] = favs

lines.append("-- PLAY_HISTORY")
play_id = 1
start_date = datetime(2024, 1, 1)
end_date   = datetime(2025, 12, 31)
date_range = (end_date - start_date).days

for uid in range(1, 11):
    num_plays = random.randint(400, 600)
    favs = user_favourites[uid]
    for _ in range(num_plays):
        sid = random.choice(favs) if random.random() < 0.8 else random.choice([s[0] for s in SONGS])
        day_offset = random.randint(0, date_range)
        play_date = start_date + timedelta(days=day_offset)
        hour = random.randint(18, 23) if random.random() < 0.5 else random.randint(7, 22)
        played_at = play_date.replace(hour=hour, minute=random.randint(0,59), second=random.randint(0,59))
        dur = int(random.randint(150000, 360000) * random.uniform(0.5, 1.0))
        ts = played_at.strftime('%Y-%m-%d %H:%M:%S')
        lines.append(
            f"INSERT INTO play_history (play_id, user_id, song_id, played_at, duration_played_ms) "
            f"VALUES ({play_id}, {uid}, {sid}, '{ts}', {dur});"
        )
        play_id += 1
lines.append("")

# Sync sequences
TOTAL_ALBUMS = len(ALBUMS)
lines.append(f"SELECT setval('genre_genre_id_seq',   {len(GENRES)});")
lines.append(f"SELECT setval('artist_artist_id_seq', {len(ARTISTS)});")
lines.append(f"SELECT setval('album_album_id_seq',   {TOTAL_ALBUMS});")
lines.append(f"SELECT setval('song_song_id_seq',     {TOTAL_SONGS});")
lines.append(f"SELECT setval('app_user_user_id_seq', 10);")
lines.append(f"SELECT setval('play_history_play_id_seq', {play_id - 1});")

with open("seed/seed_data.sql", "w") as f:
    f.write("\n".join(lines))

print(f"Generated {play_id-1} play records, {TOTAL_SONGS} songs, {len(ARTISTS)} artists -> seed/seed_data.sql")
