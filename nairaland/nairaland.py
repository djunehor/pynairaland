from bs4 import BeautifulSoup
import dateparser
import requests
import lxml


class Nairaland:
    def __init__(self, browser):
        self.BASE_URL = "https://nairaland.com"
        self.browser = browser

    def front_page_topics(self):
        soup = BeautifulSoup(requests.get(self.BASE_URL).text, "lxml")
        td = soup.find('td', attrs={'class': 'featured w'})

        links = td.find_all('a')

        output = []
        for link in links:
            datum = {'url': link['href'], 'title': link.text}
            split_list = datum['url'].split('/')
            datum['id'] = split_list[3]
            output.append(datum)

        return {'data': output}

    def categories(self, depth=0):
        first_beautiful = BeautifulSoup(requests.get(self.BASE_URL).text, 'lxml')
        table = first_beautiful.find('table', attrs={"class": "boards"})

        links = table.find_all('a')
        categories = []
        browser = self.browser
        for link in links:
            if 'class=g' in link['title']:
                datum = {
                    'url': self.BASE_URL+link['href'],
                    'name': link.text,
                    'id': browser.get_key_by_value(link.text),
                    'title': link['title'],
                    'sub_categories': [],
                }
                if depth > 0:

                    datum['title'] = datum['title'].replace('class=g', '')
                    # print('Nairaland: Visiting ', datum['url'])
                    browser.get_url(datum['url'])
                    second_table = browser.driver.find_element_by_xpath('/html/body/div/table[2]')

                    second_beautiful = BeautifulSoup(second_table.get_attribute('innerHTML'), 'lxml')
                    tds = second_beautiful.find_all('td')

                    sub_categories = []
                    total_topics = 0
                    for td in tds:
                        datum2 = {}

                        a = td.find('a')
                        datum2['url'] = self.BASE_URL+a['href']
                        datum2['name'] = a.text.strip()

                        text = td.text
                        resplit = text.split(':')[0]
                        datum2['title'] = resplit.split('(')[0]
                        datum2['topics'] = text[text.find('(') + 1: text.find(')')].replace(' topics','').strip()
                        try:
                            total_topics += int(datum2['topics'])
                        except:
                            pass

                        if depth > 1:

                            browser.get_url(datum2['url'])
                            third_table = browser.driver.find_element_by_xpath('/html/body/div/table[2]')
                            third_beautiful = BeautifulSoup(third_table.get_attribute('innerHTML'), 'lxml')
                            tds2 = third_beautiful.find_all('td')

                            child_sub_categories = []
                            child_total_topics = 0

                            for tdd in tds2:

                                ass = tdd.find_all('a')
                                for c in ass:
                                    if 'href' not in c:
                                        continue
                                    else:
                                        a = c
                                datum3 = {}
                                datum3['url'] = self.BASE_URL + a['href']
                                datum3['name'] = a.text.strip()

                                text = tdd.text
                                resplit = text.split(':')[0]
                                datum3['title'] = resplit.split('(')[0]
                                datum3['topics'] = text[text.find('(') + 1: text.find(')')].replace(' topics',
                                                                                                    '').strip()
                                try:
                                    child_total_topics += int(datum3['topics'])
                                    total_topics += child_total_topics
                                except:
                                    pass

                                child_sub_categories.append(datum3)
                            datum2['sub_categories'] = child_sub_categories
                            datum2['topics'] = child_total_topics
                        sub_categories.append(datum2)
                    datum['sub_categories'] = sub_categories
                    datum['topics'] = total_topics
                categories.append(datum)
        return {'data': categories}

    def trending_topics(self, page=0):
        url = self.BASE_URL+'/trending'
        if page > 0:
            url = url+'/'+str(page)
        browser = self.browser
        browser.get_url(url)

        trending = {}
        trending['meta'] = {}
        pagination = browser.driver.find_element_by_xpath('/html/body/div/p[1]')
        table = browser.driver.find_element_by_xpath('/html/body/div/table[2]')
        links = table.find_elements_by_tag_name('tr')
        anchors = pagination.find_elements_by_tag_name('a')
        trending['meta'] = {}
        if page < len(anchors):
            trending['meta']['next_page'] = page + 1
        else:
            trending['meta']['next_page'] = page + 1
        trending['meta']['page'] = page
        trending['meta']['per_page'] = len(links)
        if page > 0:
            trending['meta']['previous_page'] = page - 1
        else:
            trending['meta']['previous_page'] = page
        trending['meta']['total_pages'] = len(anchors)
        trending['meta']['total_entries'] = trending['meta']['per_page'] * trending['meta']['total_pages']
        trending['data'] = []
        for link in links:
            datum = {}
            beautiful = BeautifulSoup(link.get_attribute('innerHTML'), 'lxml')
            bs = beautiful.find_all('b')
            category = bs[0]
            a = category.find('a')
            datum['category'] = {}
            datum['category']['url'] = self.BASE_URL+a['href']
            datum['category']['name'] = a.text
            topic = bs[1]
            b = topic.find('a')
            datum['title'] = b.text
            datum['url'] = self.BASE_URL+b['href']
            split_list = datum['url'].split('/')
            datum['id'] = split_list[3]

            span = beautiful.find('span')
            bs = span.find_all('b')
            creator = bs[0]
            ac = creator.find('a')
            datum['creator'] = {}
            datum['creator']['name'] = ac.text
            datum['creator']['url'] = self.BASE_URL+ac['href']
            datum['posts'] = bs[1].text
            datum['views'] = bs[2].text
            datum['last_post_time'] = str(dateparser.parse(bs[3].text))
            datum['last_post_creator'] = {}
            ass = span.find_all('a')
            if len(ass) > 1:
                lc = ass[1]
                datum['last_post_creator']['name'] = lc.text
                datum['last_post_creator']['url'] = self.BASE_URL+lc['href']

            whole_text = span.text
            first_split = whole_text.split(' ')
            last_element = first_split[len(first_split)-1]
            new_text = whole_text.replace(last_element, '')
            if 'views' in new_text:
                second_split = new_text.split(' views. ')
            else:
                second_split = new_text.split(' view. ')
            datum['last_post_time'] = str(dateparser.parse(second_split[1]))

            trending['data'].append(datum)

        return trending

    def new_topics(self, page=0):
        url = self.BASE_URL+'/topics'
        if page > 0:
            url = url+'/'+str(page)
        
        browser = self.browser
        browser.get_url(url)

        trending = {}
        trending['meta'] = {}
        pagination = browser.driver.find_element_by_xpath('/html/body/div/p[1]')
        table = browser.driver.find_element_by_xpath('/html/body/div/table[2]')
        links = table.find_elements_by_tag_name('tr')
        anchors = pagination.find_elements_by_tag_name('a')
        trending['meta'] = {}
        if page < len(anchors):
            trending['meta']['next_page'] = page + 1
        else:
            trending['meta']['next_page'] = page + 1
        trending['meta']['page'] = page
        trending['meta']['per_page'] = len(links)
        if page > 0:
            trending['meta']['previous_page'] = page - 1
        else:
            trending['meta']['previous_page'] = page
        trending['meta']['total_pages'] = len(anchors)
        trending['meta']['total_entries'] = trending['meta']['per_page'] * trending['meta']['total_pages']
        trending['data'] = []
        for link in links:
            datum = {}
            beautiful = BeautifulSoup(link.get_attribute('innerHTML'), 'lxml')
            bs = beautiful.find_all('b')
            if not len(bs):
                continue
            category = bs[0]
            a = category.find('a')
            datum['category'] = {}
            datum['category']['url'] = self.BASE_URL+a['href']
            datum['category']['name'] = a.text
            topic = bs[1]
            b = topic.find('a')
            datum['title'] = b.text
            datum['url'] = self.BASE_URL+b['href']
            split_list = datum['url'].split('/')
            datum['id'] = split_list[3]

            span = beautiful.find('span')
            bs = span.find_all('b')
            creator = bs[0]
            ac = creator.find('a')
            datum['creator'] = {}
            datum['creator']['name'] = ac.text
            datum['creator']['url'] = self.BASE_URL+ac['href']
            datum['posts'] = bs[1].text
            datum['views'] = bs[2].text
            datum['last_post_time'] = str(dateparser.parse(bs[3].text))
            datum['last_post_creator'] = {}
            ass = span.find_all('a')
            if len(ass) > 1:
                lc = ass[1]
                datum['last_post_creator']['name'] = lc.text
                datum['last_post_creator']['url'] = self.BASE_URL+lc['href']

            whole_text = span.text
            first_split = whole_text.split(' ')
            last_element = first_split[len(first_split)-1]
            new_text = whole_text.replace(last_element, '')
            if 'views' in new_text:
                second_split = new_text.split(' views. ')
            else:
                second_split = new_text.split(' view. ')
            datum['last_post_time'] = str(dateparser.parse(second_split[1]))

            trending['data'].append(datum)

        return trending

    def recent_posts(self, page=0):
        url = self.BASE_URL+'/recent'
        if page > 0:
            url = url+'/'+str(page)

        browser = self.browser
        browser.get_url(url)

        trending = {}
        trending['meta'] = {}
        pagination = browser.driver.find_element_by_xpath('/html/body/div/p[1]')
        table = browser.driver.find_element_by_xpath('/html/body/div/table[2]')
        links = table.find_elements_by_tag_name('tr')
        anchors = pagination.find_elements_by_tag_name('a')
        trending['meta'] = {}
        if page < len(anchors):
            trending['meta']['next_page'] = page + 1
        else:
            trending['meta']['next_page'] = page + 1
        trending['meta']['page'] = page
        trending['meta']['per_page'] = len(links)
        if page > 0:
            trending['meta']['previous_page'] = page - 1
        else:
            trending['meta']['previous_page'] = page
        trending['meta']['total_pages'] = len(anchors)
        trending['meta']['total_entries'] = trending['meta']['per_page'] * trending['meta']['total_pages']
        trending['data'] = []

        beautiful = BeautifulSoup(browser.driver.page_source, 'lxml')
        headings = beautiful.find_all("td", class_="bold l pu")
        posts = beautiful.find_all("td", class_="l w pd")
        # print(f'[BeautifulSoup] Found {len(posts)} posts.')

        trending['data'] = []
        for l in range(len(posts)):
            # if keyword not in posts[l].text:
            #     continue
            data = {}
            data['content'] = posts[l].text
            try:
                p = posts[l].find('p')
                bs = p.find_all('b')
                data['likes'] = int(bs[0].text)
                data['shares'] = int(bs[1].text)
            except:
                data['likes'] = 0
                data['shares'] = 0

            a_s = headings[l].find_all('a')

            # get date time
            try:
                span = headings[l].find('span')
                split = span.text
                data['date_posted'] = str(dateparser.parse(split.rstrip()))
            except:
                data['date_posted'] = None

            data['user'] = {}
            data['topic'] = {}
            data['topic']['category'] = {}
            for a in a_s:

                if a.has_attr('class'):
                    data['user']['url'] = self.BASE_URL+ str(a['href'])
                    data['user']['name'] = a.text
                    continue

                if a.has_attr('href'):
                    if '#' in a['href']:
                        data['topic']['url'] = self.BASE_URL + str(a['href'])
                        splitted = a['href'].split('/')
                        data['topic']['id'] = splitted[1]
                        data['topic']['title'] = a.text.replace('Re: ', '')
                        split = data['topic']['url'].split('#')
                        data['url'] = split[0]
                        data['id'] = split[1]
                    else:
                        data['topic']['category']['url'] = self.BASE_URL+a['href']
                        data['topic']['category']['name'] = a.text
                    continue
            trending['data'].append(data)

        return trending

    def user(self, username):
        url = self.BASE_URL+'/'+username

        browser = self.browser
        browser.get_url(url)

        user = {}
        user['name'] = username
        user['url'] = url
        user['sections_most_active_in'] = []
        board = browser.driver.find_element_by_xpath('/html/body/div/table[3]')
        followers = browser.driver.find_element_by_xpath('/html/body/div/table[4]')
        ps = board.find_elements_by_tag_name('p')

        follows = followers.find_elements_by_tag_name('a')
        user['follower_count'] = len(follows)
        user['followers'] = []
        for follow in follows:
            datum = {}
            datum['name'] = follow.text
            datum['url'] = follow.get_attribute('href')
            user['followers'].append(datum)
            user['gender'] = None
            user['location'] = None
            user['twitter'] = None
            user['personal_text'] = None
            user['time_spent_online'] = None
            user['time_registered'] = None
            user['signature'] = None
            user['post_count'] = None
            user['topic_count'] = None

        for p in ps:
            if 'Gender' in p.text:
                user['gender'] = p.text.replace('Gender: ', '').strip()
            if 'Location' in p.text:
                user['location'] = p.text.replace('Location: ', '').strip()
            if 'Twitter' in p.text:
                user['twitter'] = p.text.replace('Twitter: ', '').strip()
            if 'Personal text' in p.text:
                user['personal_text'] = p.text.replace('Personal text: ', '').strip()
            if 'Time registered' in p.text:
                user['time_registered'] = str(dateparser.parse(p.text.replace('Time registered: ', '').strip()))
            if 'Last seen' in p.text:
                user['last_seen'] = str(dateparser.parse(p.text.replace('Last seen: ', '').strip()))

            if 'Time spent online' in p.text:
                user['time_spent_online'] = p.text.replace('Time spent online: ', '').strip()
            if 'Signature' in p.text:
                user['signature'] = p.text.replace('Signature: ', '').strip()
            if 'Sections Most Active In: ' in p.text:
                beautiful = BeautifulSoup(p.get_attribute('innerHTML'), 'lxml')
                anchors = beautiful.find_all('a')
                for a in anchors:
                    section = {}
                    section['url'] = self.BASE_URL+a['href']
                    section['name'] = a.text
                    user['sections_most_active_in'].append(section)
            if p.find_elements_by_tag_name('a'):
                liinks = p.find_elements_by_tag_name('a')
                for li in liinks:
                    if 'posts' in li.text:
                        user['post_count'] = li.text.split('(')[1].split(')')[0]
                    if 'topics' in li.text:
                        user['topic_count'] = li.text.split('(')[1].split(')')[0]
        return {'data': user}

    def user_posts(self, username, page=0):
        url = self.BASE_URL+'/'+username+'/posts'
        if page > 0:
            url = url+'/'+str(page)

        browser = self.browser
        browser.get_url(url)

        trending = {}
        trending['meta'] = {}
        pagination = browser.driver.find_element_by_xpath('/html/body/div/p[1]')
        table = browser.driver.find_element_by_xpath('/html/body/div/table[2]')
        links = table.find_elements_by_tag_name('tr')
        anchors = pagination.find_elements_by_tag_name('a')
        trending['meta'] = {}
        if page < len(anchors):
            trending['meta']['next_page'] = page + 1
        else:
            trending['meta']['next_page'] = page + 1
        trending['meta']['page'] = page
        trending['meta']['per_page'] = len(links)
        if page > 0:
            trending['meta']['previous_page'] = page - 1
        else:
            trending['meta']['previous_page'] = page
        trending['meta']['total_pages'] = len(anchors)
        trending['meta']['total_entries'] = trending['meta']['per_page'] * trending['meta']['total_pages']
        trending['data'] = []

        beautiful = BeautifulSoup(browser.driver.page_source, 'lxml')
        headings = beautiful.find_all("td", class_="bold l pu")
        posts = beautiful.find_all("td", class_="l w pd")
        # print(f'[BeautifulSoup] Found {len(posts)} posts.')

        trending['data'] = []
        for l in range(len(posts)):
            # if keyword not in posts[l].text:
            #     continue
            data = {}
            data['content'] = posts[l].text
            try:
                p = posts[l].find('p')
                bs = p.find_all('b')
                data['likes'] = int(bs[0].text)
                data['shares'] = int(bs[1].text)
            except:
                data['likes'] = 0
                data['shares'] = 0

            a_s = headings[l].find_all('a')

            # get date time
            try:
                span = headings[l].find('span')
                split = span.text
                data['date_posted'] = str(dateparser.parse(split.rstrip()))
            except:
                data['date_posted'] = None

            data['user'] = {}
            data['topic'] = {}
            data['topic']['category'] = {}
            for a in a_s:

                if a.has_attr('class'):
                    data['user']['url'] = self.BASE_URL + str(a['href'])
                    data['user']['name'] = a.text
                    continue

                if a.has_attr('href'):
                    if '#' in a['href']:
                        data['topic']['url'] = self.BASE_URL + str(a['href'])
                        splitted = a['href'].split('/')
                        data['topic']['id'] = splitted[1]
                        data['topic']['title'] = a.text.replace('Re: ', '')
                        split = data['topic']['url'].split('#')
                        data['url'] = split[0]
                        data['id'] = split[1]
                    else:
                        data['topic']['category']['url'] = self.BASE_URL + a['href']
                        data['topic']['category']['name'] = a.text
                    continue
            trending['data'].append(data)

        return trending

    def user_topics(self, username, page=0):
        url = self.BASE_URL+'/'+username+'/topics'
        if page > 0:
            url = url+'/'+str(page)

        browser = self.browser
        browser.get_url(url)

        trending = {}
        trending['meta'] = {}
        pagination = browser.driver.find_element_by_xpath('/html/body/div/p[1]')
        table = browser.driver.find_element_by_xpath('/html/body/div/table[2]')
        links = table.find_elements_by_tag_name('tr')
        anchors = pagination.find_elements_by_tag_name('a')
        trending['meta'] = {}
        if page < len(anchors):
            trending['meta']['next_page'] = page + 1
        else:
            trending['meta']['next_page'] = page + 1
        trending['meta']['page'] = page
        trending['meta']['per_page'] = len(links)
        if page > 0:
            trending['meta']['previous_page'] = page - 1
        else:
            trending['meta']['previous_page'] = page
        trending['meta']['total_pages'] = len(anchors)
        trending['meta']['total_entries'] = trending['meta']['per_page'] * trending['meta']['total_pages']
        trending['data'] = []
        for link in links:
            datum = {}
            beautiful = BeautifulSoup(link.get_attribute('innerHTML'), 'lxml')
            bs = beautiful.find_all('b')
            category = bs[0]
            a = category.find('a')
            datum['category'] = {}
            datum['category']['url'] = self.BASE_URL+a['href']
            datum['category']['name'] = a.text
            topic = bs[1]
            b = topic.find('a')
            datum['title'] = b.text
            datum['url'] = self.BASE_URL+b['href']

            span = beautiful.find('span')
            bs = span.find_all('b')

            ass = span.find_all('a')

            ac = ass[0]
            datum['creator'] = {}
            datum['creator']['name'] = ac.text
            datum['creator']['url'] = self.BASE_URL+ac['href']
            datum['posts'] = bs[1].text
            datum['views'] = bs[2].text
            datum['last_post_time'] = str(dateparser.parse(bs[3].text))
            datum['last_post_creator'] = {}


            if len(ass) > 1:
                lc = ass[1]
                datum['last_post_creator']['name'] = lc.text
                datum['last_post_creator']['url'] = self.BASE_URL+lc['href']

            whole_text = span.text
            first_split = whole_text.split(' ')
            last_element = first_split[len(first_split)-1]
            new_text = whole_text.replace(last_element, '')
            second_split = new_text.split(' views. ')
            datum['last_post_time'] = str(dateparser.parse(second_split[1]))
            trending['data'].append(datum)

        return trending

    def category_topics(self, category, page=0):
        url = self.BASE_URL+'/'+category
        if page > 0:
            url = url+'/'+str(page)

        browser = self.browser
        browser.get_url(url)

        trending = {}
        trending['meta'] = {}
        pagination = browser.driver.find_element_by_xpath('/html/body/div/p[4]')
        table = browser.driver.find_element_by_xpath('/html/body/div/table[3]')
        links = table.find_elements_by_tag_name('td')
        anchors = pagination.find_elements_by_tag_name('a')
        trending['meta'] = {}
        if page < len(anchors):
            trending['meta']['next_page'] = page + 1
        else:
            trending['meta']['next_page'] = page + 1
        trending['meta']['page'] = page
        trending['meta']['per_page'] = len(links)
        if page > 0:
            trending['meta']['previous_page'] = page - 1
        else:
            trending['meta']['previous_page'] = page
        trending['meta']['total_pages'] = len(anchors)
        trending['meta']['total_entries'] = trending['meta']['per_page'] * trending['meta']['total_pages']
        trending['data'] = []
        for link in links:
            datum = {}
            beautiful = BeautifulSoup(link.get_attribute('innerHTML'), 'lxml')

            b = beautiful.find('b')
            a = b.find('a')

            datum['url'] = self.BASE_URL+a['href']
            split_list = datum['url'].split('/')
            datum['id'] = split_list[3]
            datum['title'] = a.text

            span = beautiful.find('span')
            bs = span.find_all('b')
            creator = bs[0]
            ac = creator.find('a')
            datum['creator'] = {}
            datum['creator']['name'] = ac.text
            datum['creator']['url'] = self.BASE_URL+ac['href']
            datum['posts'] = bs[1].text
            datum['views'] = bs[2].text
            datum['last_post_time'] = str(dateparser.parse(bs[3].text))
            datum['last_post_creator'] = {}
            ass = span.find_all('a')
            if len(ass) > 1:
                lc = ass[1]
                datum['last_post_creator']['name'] = lc.text
                datum['last_post_creator']['url'] = self.BASE_URL+lc['href']

            whole_text = span.text
            first_split = whole_text.split(' ')
            last_element = first_split[len(first_split)-1]
            new_text = whole_text.replace(last_element, '')
            second_split = new_text.split(' views. ')
            datum['last_post_time'] = str(dateparser.parse(second_split[1]))

            trending['data'].append(datum)

        return trending

    def topic_posts(self, slug_id, page=0):
        url = self.BASE_URL+'/'+slug_id
        if page > 0:
            url = url+'/'+str(page)

        browser = self.browser
        browser.get_url(url)

        trending = {}
        trending['meta'] = {}
        pagination = browser.driver.find_element_by_xpath('/html/body/div/p[1]')
        table = browser.driver.find_element_by_xpath('/html/body/div/table[2]')
        category = browser.driver.find_element_by_xpath('/html/body/div/p[1]')
        category_links = category.find_elements_by_tag_name('a')
        links = table.find_elements_by_tag_name('tr')
        anchors = pagination.find_elements_by_tag_name('a')
        trending['meta'] = {}
        if page < len(anchors):
            trending['meta']['next_page'] = page + 1
        else:
            trending['meta']['next_page'] = page + 1
        trending['meta']['page'] = page
        trending['meta']['per_page'] = len(links)
        if page > 0:
            trending['meta']['previous_page'] = page - 1
        else:
            trending['meta']['previous_page'] = page
        trending['meta']['total_pages'] = len(anchors)
        trending['meta']['total_entries'] = trending['meta']['per_page'] * trending['meta']['total_pages']
        trending['data'] = []
        splitted = url.split('/')
        trending['topic'] = {}
        trending['topic']['id'] = splitted[3]
        trending['topic']['title'] = browser.driver.title.split('-')[0].strip()
        trending['topic']['category'] = {}
        cat_a = category_links[len(category_links) - 2]
        trending['topic']['category']['name'] = cat_a.text
        trending['topic']['category']['url'] = cat_a.get_attribute('href')

        beautiful = BeautifulSoup(browser.driver.page_source, 'lxml')
        headings = beautiful.find_all("td", class_="bold l pu")
        posts = beautiful.find_all("td", class_="l w pd")
        # print(f'[BeautifulSoup] Found {len(posts)} posts.')

        trending['data'] = []
        for l in range(len(posts)):
            # if keyword not in posts[l].text:
            #     continue
            data = {}
            div = posts[l].find('div')
            data['content'] = div.text
            try:
                p = posts[l].find('p')
                bs = p.find_all('b')
                data['likes'] = int(bs[0].text)
                data['shares'] = int(bs[1].text)
            except:
                data['likes'] = 0
                data['shares'] = 0

            a_s = headings[l].find_all('a')

            # get date time
            try:
                span = headings[l].find('span')
                split = span.text
                data['date_posted'] = str(dateparser.parse(split.rstrip()))
            except:
                data['date_posted'] = None

            data['user'] = {}
            for a in a_s:

                if a.has_attr('class'):
                    data['user']['url'] = self.BASE_URL + str(a['href'])
                    data['user']['name'] = a.text
                    continue
            trending['data'].append(data)

        return trending

    def search(self, search_term, board=0, page=0):
        if page > 0:
            url = "https://www.nairaland.com/search?q=" + search_term + "&board=" + board
        else:
            url = "https://www.nairaland.com/search/"+search_term+"/0/"+str(board) +"/0/1/"+str(page)

        browser = self.browser
        browser.get_url(url)

        trending = {}
        trending['meta'] = {}
        pagination = browser.driver.find_element_by_xpath('/html/body/div/p[1]')
        table = browser.driver.find_element_by_xpath('/html/body/div/table[2]')
        links = table.find_elements_by_tag_name('tr')
        anchors = pagination.find_elements_by_tag_name('a')
        trending['meta'] = {}
        trending['keyword'] = search_term
        if page < len(anchors):
            trending['meta']['next_page'] = page + 1
        else:
            trending['meta']['next_page'] = page + 1
        trending['meta']['page'] = page
        trending['meta']['per_page'] = len(links)
        if page > 0:
            trending['meta']['previous_page'] = page - 1
        else:
            trending['meta']['previous_page'] = page
        trending['meta']['total_pages'] = len(anchors)
        trending['meta']['total_entries'] = trending['meta']['per_page'] * trending['meta']['total_pages']
        trending['data'] = []

        beautiful = BeautifulSoup(browser.driver.page_source, 'lxml')
        headings = beautiful.find_all("td", class_="bold l pu")
        posts = beautiful.find_all("td", class_="l w pd")
        # print(f'[BeautifulSoup] Found {len(posts)} posts.')

        trending['data'] = []
        for l in range(len(posts)):
            # if keyword not in posts[l].text:
            #     continue
            data = {}
            div = posts[l].find('div')
            data['content'] = div.text
            try:
                p = posts[l].find('p')
                bs = p.find_all('b')
                data['likes'] = int(bs[0].text)
                data['shares'] = int(bs[1].text)
            except:
                data['likes'] = 0
                data['shares'] = 0

            a_s = headings[l].find_all('a')

            # get date time
            try:
                span = headings[l].find('span')
                split = span.text
                data['date_posted'] = str(dateparser.parse(split.rstrip()))
            except:
                data['date_posted'] = None

            data['user'] = {}
            data['topic'] = {}
            data['topic']['category'] = {}
            for a in a_s:

                if a.has_attr('class'):
                    data['user']['url'] = self.BASE_URL + str(a['href'])
                    data['user']['name'] = a.text
                    continue

                if a.has_attr('href'):
                    if '#' in a['href']:
                        data['url'] = self.BASE_URL + str(a['href'])
                        splitted = a['href'].split('/')
                        data['topic']['id'] = splitted[1]
                        data['topic']['title'] = a.text.replace('Re: ', '')
                        split = data['url'].split('#')
                        data['topic']['url'] = split[0]
                        data['id'] = split[1]
                    else:
                        data['topic']['category']['url'] = self.BASE_URL + a['href']
                        data['topic']['category']['name'] = a.text
                    continue
            trending['data'].append(data)

        return trending
