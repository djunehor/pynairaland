# pynairaland
[![HitCount](http://hits.dwyl.io/makinde2013/pynairaland.svg)](http://hits.dwyl.io/makinde2013/pynairaland)

#### Issues and pull requests welcome.

A Python module to fetch and parse data from Nairaland.

### Table of Contents
* [Installation](#installation)
* [Usage](#usage)
* [Features](#features)
* [Contribute](#contribute)
* [Projects using `pynairaland`](#projects-using-pynairaland)
* [Acknowledgement](#acknowledegment)

## Installation
You will need [Python 3.x](https://www.python.org/download/) and [pip](http://pip.readthedocs.org/en/latest/installing.html).

Install using pip: `pip install nairaland`
Install via repo:
- Clone repor `git clone https://github.com/makinde2013/pynairaland`
- Install requirements via `pip install -r requirements.txt`
- Place pynairaland in your project root folder

## Usage

### User statistics

```python
from nairaland import Nairaland
import os
from nairaland.browser import Browser

browser = Browser(os.getenv('LINUX'))
nairaland = Nairaland(browser)

# Get front page topics
front_page_topics = nairaland.front_page_topics()

# Do stuff with the parsed activity data
print(front_page_topics)

# Get categories
categories = nairaland.categories(depth=2)

# Get category topics
category_topics = nairaland.category_topics(category='politics', page=2)

# categories are:
{
  "data": [
    {
      "id": "9",
      "name": "Nairaland / General",
      "sub_categories": [],
      "title": " class=g",
      "url": "https://nairaland.com/nairaland"
    },
    {
      "id": "12",
      "name": "Entertainment",
      "sub_categories": [],
      "title": "Entertainment threads that won't fit into any child board. class=g",
      "url": "https://nairaland.com/entertainment"
    },
    {
      "id": "8",
      "name": "Science/Technology",
      "sub_categories": [],
      "title": " class=g",
      "url": "https://nairaland.com/science"
    }
  ]
}
# Get trending topics
topics_trending = nairaland.topics_trending(page=2)

# Get latest topics
latest_topics = nairaland.new_topics(page=2)

# Get latest comments
latest_comments = nairaland.recent_posts(page=2)

# Get user profile
user_profile = nairaland.recent_posts(user='bolaji21', page=2)

# Get user posts
user_posts = nairaland.user_posts(user='bolaji21',page=2)

# Get user topics
user_topics = nairaland.user_topics(user='bolaji21',page=2)

# Get topic (thread) comments
topic_comments = nairaland.topic_posts(topic='5426482',page=2)

# comments are:
{
  "data": [
    {
      "content": "It was a battle of Zanku supremacy between Tiwa Savage and famous dancer, Poco Lee at Tiwa’s “49-99” premiere party in Obalende, Lagos.On the 17th of September would be a day to remember for some music fans as Tiwa Savage took her bubbly self and her team to entertain Lagosians for free at the very busy area of Obalende on a sunny afternoon. While the crowd that was present for the show was expecting to catch a glimpse of Tiwa Savage on stage performing her rcently released song, they got more than they had hoped for as Tiwa and Poco Lee did something that was similar to a face-off as they showed some really dope Zanku moves.Tiwa never shied away from Poco Lee’s sleek moves and she gave some really unique moves too. Watch the video below and judge who did better with the dance: https://www.youtube.com/watch?v=mkSz8mq0xfQ.https://www.thenaijafame.com.ng/2019/09/watch-tiwa-savage-battle-poco-lee-on.html?m=1",
      "date_posted": "2019-09-19 20:51:00",
      "likes": 0,
      "shares": 0,
      "user": {
        "name": "Chinekepikin",
        "url": "https://nairaland.com/chinekepikin"
      }
    },
    {
      "content": "More, Watch The Full Video HERE",
      "date_posted": "2019-09-19 20:52:00",
      "likes": 0,
      "shares": 0,
      "user": {
        "name": "Chinekepikin",
        "url": "https://nairaland.com/chinekepikin"
      }
    }
    ],
  "meta": {
    "next_page": 1,
    "page": 0,
    "per_page": 36,
    "previous_page": 0,
    "total_entries": 144,
    "total_pages": 4
  },
  "topic": {
    "category": {
      "name": "Celebrities",
      "url": "https://www.nairaland.com/celebs"
    },
    "id": "5426482",
    "title": "Tiwa Savage Battles Poco Lee On Stage For Zanku Supremacy (Video)"
  }
}

# search for posts containing keyword
search_results = nairaland.search(search_term='buhari',board=20, page=1)

```

### Authenticated user routes
```python
import os
from nairaland import User
from nairaland.browser import Browser


browser = Browser(os.getenv('LINUX'))
user = User(browser)

# Get user followed topics
followed_topics = user.followed_topics(page=2)

# Get user followed boards
followed_boards = user.followed_boards(page=2)

# Get user mentions
mentions = user.mentions(page=2)

# topics are:
{
  "data": [
    {
      "creator": {
        "name": "Seun",
        "url": "https://nairaland.com/seun"
      },
      "id": "2792995",
      "last_post_creator": {
        "name": "Youthleader22",
        "url": "https://nairaland.com/youthleader22"
      },
      "last_post_time": "2019-09-17 18:44:00",
      "posts": "3783",
      "title": "Nairaland Says No To Secessionists",
      "url": "https://nairaland.com/2792995/nairaland-says-no-secessionists",
      "views": "410717"
    },
    {
      "creator": {
        "name": "ItoroUdotim",
        "url": "https://nairaland.com/itoroudotim"
      },
      "id": "5425882",
      "last_post_creator": {
        "name": "wiseone28",
        "url": "https://nairaland.com/wiseone28"
      },
      "last_post_time": "2019-09-19 22:45:00",
      "posts": "29",
      "title": "Governor Udom Emmanuel Wins At Tribunal",
      "url": "https://nairaland.com/5425882/governor-udom-emmanuel-wins-tribunal",
      "views": "6699"
    }
  ],
  "meta": {
    "next_page": 1,
    "page": 0,
    "per_page": 64,
    "previous_page": 0,
    "total_entries": 640,
    "total_pages": 10
  }
}
```

## Features
### Currently implemented
* Front page topics
* Recent topics
* Trending topics
* Latest posts (comments)
* Categories
* Category topics
* User Profile
* User posts
* User Topics
* User followed boards
* User followed topics
* Posts by who user is following
* Posts shared to user
* Search
* Create topic
* Create post (comment) with quote
* Like/Unlike post (comment)
* Share/Unshare post (comment)

### To do
* Unit test
* Refactor code to make it DRY

## Contribute
Check out the issues on GitHub and/or make a pull request to contribute!

## Projects using `pynairaland`
* [`nairaland-api`](https://github.com/makinde2013/nairaland-api) – A REST API for Nairaland.

## Acknowledegment
* [`pyquora`](https://github.com/csu/pyquora) – The project served as boiler plate for me to get this ready.