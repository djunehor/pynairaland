from bs4 import BeautifulSoup
import os
import dateparser
import time


class User:
    def __init__(self, browser):
        self.browser = browser
        # Browser Actions
        self.BASE_URL = "https://nairaland.com"

    def followed_topics(self, page=0):
        url = self.BASE_URL+'/followed'
        if page > 0:
            url = url+'/'+str(page)
        self.browser.get_url(url)

        trending = {}
        trending['meta'] = {}
        pagination = self.browser.driver.find_element_by_xpath('/html/body/div/p[1]')
        table = self.browser.driver.find_element_by_xpath('/html/body/div/table[2]')
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
            datum['category'] = {}
            beautiful = BeautifulSoup(link.get_attribute('innerHTML'), 'lxml')

            bss = beautiful.find_all('b')
            c = bss[0]
            a = c.find('a')

            datum['category']['url'] = self.BASE_URL + a['href']
            datum['category']['title'] = a.text

            b = bss[1]
            a = b.find('a')

            datum['url'] = self.BASE_URL+a['href']
            datum['title'] = a.text

            span = beautiful.find('span')
            bs = span.find_all('b')
            creator = bs[0]
            ac = creator.find('a')
            datum['creator'] = {}
            if ac:
                datum['creator']['name'] = ac.text
                datum['creator']['url'] = self.BASE_URL + ac['href']
            datum['posts'] = bs[1].text
            datum['views'] = bs[2].text
            datum['last_post_time'] = str(dateparser.parse(bs[3].text))
            datum['last_post_creator'] = {}
            ass = span.find_all('a')
            if len(ass) > 1:
                lc = ass[1]
                datum['last_post_creator']['name'] = lc.text
                datum['last_post_creator']['url'] = self.BASE_URL + lc['href']

            whole_text = span.text
            first_split = whole_text.split(' ')
            last_element = first_split[len(first_split) - 1]
            new_text = whole_text.replace(last_element, '')
            second_split = new_text.split(' views. ')
            datum['last_post_time'] = str(dateparser.parse(second_split[1]))

            trending['data'].append(datum)
        return trending

    def followed_boards(self, page=0):
        url = self.BASE_URL+'/followedboards'
        if page > 0:
            url = url+'/'+str(page)
        self.browser.get_url(url)

        trending = {}
        trending['meta'] = {}
        pagination = self.browser.driver.find_element_by_xpath('/html/body/div/p[1]')
        table = self.browser.driver.find_element_by_xpath('/html/body/div/table[3]')
        topics = self.browser.driver.find_element_by_xpath('/html/body/div/table[2]/tbody/tr[1]/td')
        links = table.find_elements_by_tag_name('td')
        anchors = pagination.find_elements_by_tag_name('a')
        topic_links = topics.find_elements_by_tag_name('a')

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
        trending['topics'] = []

        for to in topic_links:
            if not to.text:
                continue
            dat = {}
            dat['url'] = to.get_attribute('href')
            dat['title'] = to.text
            trending['topics'].append(dat)

        for link in links:
            datum = {}
            datum['category'] = {}
            beautiful = BeautifulSoup(link.get_attribute('innerHTML'), 'lxml')

            bss = beautiful.find_all('b')
            c = bss[0]
            a = c.find('a')

            datum['category']['url'] = self.BASE_URL + a['href']
            datum['category']['title'] = a.text

            b = bss[1]
            a = b.find('a')

            datum['url'] = self.BASE_URL+a['href']
            datum['title'] = a.text

            span = beautiful.find('span')
            bs = span.find_all('b')
            creator = bs[0]
            ac = creator.find('a')
            datum['creator'] = {}
            if ac:
                datum['creator']['name'] = ac.text
                datum['creator']['url'] = self.BASE_URL + ac['href']
            datum['posts'] = bs[1].text
            datum['views'] = bs[2].text
            datum['last_post_time'] = str(dateparser.parse(bs[3].text))
            datum['last_post_creator'] = {}
            ass = span.find_all('a')
            if len(ass) > 1:
                lc = ass[1]
                datum['last_post_creator']['name'] = lc.text
                datum['last_post_creator']['url'] = self.BASE_URL + lc['href']

            whole_text = span.text
            first_split = whole_text.split(' ')
            last_element = first_split[len(first_split) - 1]
            new_text = whole_text.replace(last_element, '')
            second_split = new_text.split(' views. ')
            datum['last_post_time'] = str(dateparser.parse(second_split[1]))

            trending['data'].append(datum)
        return trending

    def likes_and_shares(self, page=0):
        url = self.BASE_URL+'/likesandshares'
        if page > 0:
            url = url+'/'+str(page)
        self.browser.get_url(url)

        trending = {}
        trending['meta'] = {}
        pagination = self.browser.driver.find_element_by_xpath('/html/body/div/p[1]')
        table = self.browser.driver.find_element_by_xpath('/html/body/div/table[2]')
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

        beautiful = BeautifulSoup(self.browser.driver.page_source, 'lxml')
        headings = beautiful.find_all("td", class_="bold l pu")
        posts = beautiful.find_all("td", class_="l w pd")
        # print(f'[Scraper] Found {len(posts)} posts.')

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

    def mentions(self, page=0):
        url = self.BASE_URL+'/mentions'
        if page > 0:
            url = url+'/'+str(page)
        self.browser.get_url(url)

        trending = {}
        trending['meta'] = {}
        pagination = self.browser.driver.find_element_by_xpath('/html/body/div/p[1]')
        table = self.browser.driver.find_element_by_xpath('/html/body/div/table[2]')
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

        beautiful = BeautifulSoup(self.browser.driver.page_source, 'lxml')
        headings = beautiful.find_all("td", class_="bold l pu")
        posts = beautiful.find_all("td", class_="l w pd")
        # print(f'[Scraper] Found {len(posts)} posts.')

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

    def following_posts(self, page=0):
        url = self.BASE_URL+'/following'
        if page > 0:
            url = url+'/'+str(page)
        self.browser.get_url(url)

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

        beautiful = BeautifulSoup(table.get_attribute('innerHTML'), 'lxml')

        headings = beautiful.find_all("td", attrs={'class': 'bold l pu'})
        posts = beautiful.find_all("td", attrs={'class': 'l w'})
        # print(f'[BeautifulSoup] Found {len(posts)} posts.')

        trending['data'] = []
        for l in range(len(posts)):
            # if keyword not in posts[l].text:
            #     continue
            data = {}
            div = posts[l].find('div', attrs={'class': 'narrow'})
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

    def shared_with(self, page=0):
        url = self.BASE_URL+'/shared'
        if page > 0:
            url = url+'/'+str(page)
        self.browser.get_url(url)

        trending = {}
        trending['meta'] = {}
        pagination = self.browser.driver.find_element_by_xpath('/html/body/div/p[1]')
        table = self.browser.driver.find_element_by_xpath('/html/body/div/table[2]')
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

        beautiful = BeautifulSoup(self.browser.driver.page_source, 'lxml')
        headings = beautiful.find_all("td", class_="bold l pu")
        posts = beautiful.find_all("td", class_="l w")
        print(f'[Scraper] Found {len(posts)} posts.')

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
            span = headings[l].find('span')
            bees = span.find_all('b')
            our_a = span.find('a')
            data['shared_by'] = {}
            data['shared_by']['name'] = our_a.text
            data['shared_by']['url'] = self.BASE_URL+our_a['href']
            try:
                date = span.text.split(our_a.text)
                right_side = date[1].replace('at', ' ').replace('On', ' ')
                data['shared_on'] = str(dateparser.parse(right_side))
            except:
                data['shared_on'] = None

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

    def new_topic(self, board, title, content):
        url = self.BASE_URL+'/newtopic?board='+board

        self.browser.get_url(url)
        title_element = self.browser.driver.find_element_by_xpath("//input[@name='title']")
        title_element.send_keys(title)
        content_element = self.browser.driver.find_element_by_xpath("//textarea[@name='body']")
        content_element.send_keys(content)
        submit = self.browser.driver.find_element_by_xpath("//input[@value='Submit']")
        submit.click()

        time.sleep(2)
        datum = {}
        datum['url'] = self.browser.driver.current_url
        datum['title'] = self.browser.driver.title
        datum['id'] = datum['url'].split('/')[3]

        return datum

    def new_post(self, topic_id, content, post_id=False, follow_topic=False):
        if post_id:
            url = self.BASE_URL+'/newpost?topic='+topic_id+'&post='+post_id
        else:
            url = self.BASE_URL+'/newpost?topic='+topic_id

        self.browser.get_url(url)
        content_element = self.browser.driver.find_element_by_xpath("//textarea[@name='body']")
        content_element.send_keys(content)

        if follow_topic:
            follow = self.browser.driver.find_element_by_xpath("//input[@name='follow']")
            follow.click()
        submit = self.browser.driver.find_element_by_xpath("//input[@value='Submit']")
        submit.click()

        time.sleep(2)
        datum = {}
        datum['url'] = self.browser.driver.current_url
        datum['title'] = self.browser.driver.title
        datum['id'] = datum['url'].split('#')[1]

        return datum

    def like_post(self, slug_id, unlike=False):
        url = self.BASE_URL+'/'+slug_id
        self.browser.get_url(url)

        post_id = url.split('#')[1]

        td = self.browser.driver.find_element_by_id("pb"+post_id)

        if unlike:
            try:
                a = td.find_element_by_partial_link_text('Unlike')
                a.click()
            except:
                pass
        else:
            try:
                a = td.find_element_by_partial_link_text('Like')
                a.click()
            except:
                pass

        likes = self.browser.driver.find_element_by_xpath('//*[@id="lpt'+post_id+'"]').text.replace(' Likes', '').strip()

        datum = {}
        datum['url'] = url
        datum['id'] = post_id
        datum['likes'] = likes

        return datum

    def share_post(self, slug_id, unshare=False):
        url = self.BASE_URL+'/'+slug_id
        self.browser.get_url(url)

        post_id = url.split('#')[1]

        td = self.browser.driver.find_element_by_id("pb"+post_id)

        if unshare:
            try:
                a = td.find_element_by_partial_link_text('Un-Share')
                a.click()
            except:
                pass
        else:
            try:
                a = td.find_element_by_partial_link_text('Share')
                a.click()
            except:
                pass

        shares = self.browser.driver.find_element_by_xpath('//*[@id="shb'+post_id+'"]').text.replace(' Shares', '').strip()

        datum = {}
        datum['url'] = url
        datum['id'] = post_id
        datum['shares'] = shares

        return datum