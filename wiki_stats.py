#!/usr/bin/python3

import os
import sys
import array

import matplotlib as mt
import statistics as st

from matplotlib import rc
rc('font', family='Droid Sans', weight='normal', size=14)

import matplotlib.pyplot as plt


class WikiGraph:

    def load_from_file(self, filename):
        print('Загружаю граф из файла: ' + filename)

        with open(filename) as f:
            (n, _nlinks) = map(int, f.readline().split())
            self.pages = n


            self._titles = []
            self._sizes = array.array('I', [0]*n)
            self._links = array.array('L', [0]*_nlinks)
            self._redirect = array.array('B', [0]*n)
            self._offset = array.array('L', [0]*(n+1))
            self._num_of_links_from = array.array('L', [0]*n)
            self._num_of_links_to = array.array('L', [0]*n)
            self._num_of_redirects_to = array.array('L', [0]*n)
            curr_link = 0

            for i in range(n):
                self._titles.append(f.readline().rstrip())
                (size, redirect, num_of_links) = map(int, f.readline().split())
                self._sizes[i] = size
                self._redirect[i] = redirect
                self._num_of_links_from[i] = num_of_links
                self._offset[i+1] = self._offset[i] + num_of_links
                for j in range(curr_link, curr_link + num_of_links):
                    self._links[j] = int(f.readline())
                    self._num_of_links_to[self._links[j]] += 1
                    if self._redirect[i]:
                        self._num_of_redirects_to[self._links[j]] += 1
                curr_link += num_of_links

        print('Граф загружен')

    def get_number_of_links_from(self, _id):
        number_from = self._num_of_links_from[_id]
        return number_from

    def get_links_from(self, _id):
        links_from = list(self._links[self._offset[_id]:self._offset[_id+1]])
        return links_from

    def get_number_of_links_to(self, _id):
        number_to = self._num_of_links_to[_id]
        return number_to

    def get_number_of_redirects(self, _id):
        number_of_rd = self._num_of_redirects_to[_id]
        return number_of_rd

    def get_id(self, title):
        return self._titles.index(title)

    def get_number_of_pages(self):
        return self.pages

    def is_redirect(self, _id):
        return self._redirect[_id] == 1

    def get_title(self, _id):
        return self._titles[_id]

    def get_page_size(self, _id):
        return self._sizes[_id]

    def analysis(self):

        num_of_redirects = 0

        links_from = self._num_of_links_from
        min_links_from = min(links_from)
        max_links_from = max(links_from)
        avg_links_from = round(st.mean(links_from), 2)
        stdev_links_from = round(st.stdev(links_from), 2)

        links_to = self._num_of_links_to
        min_links_to = min(links_to)
        max_links_to = max(links_to)
        avg_links_to = round(st.mean(links_to), 2)
        stdev_links_to = round(st.stdev(links_to), 2)

        redirects = self._num_of_redirects_to
        min_redirects = min(redirects)
        max_redirects = max(redirects)
        avg_redirects = round(st.mean(redirects), 2)
        stdev_redirects = round(st.stdev(redirects), 2)

        pages_with_max_links_from = []
        pages_with_max_links_to = []
        pages_with_max_redirects = []
        num_of_pages_with_max_links_from = 0
        num_of_pages_with_min_links_from = 0
        num_of_pages_with_max_links_to = 0
        num_of_pages_with_min_links_to = 0
        num_of_pages_with_max_redirects = 0
        num_of_pages_with_min_redirects = 0


        for i in range(self.pages):

            if self.is_redirect(i):
                num_of_redirects += 1

            if self.get_number_of_links_from(i) == max_links_from:
                pages_with_max_links_from.append(self.get_title(i))
                num_of_pages_with_max_links_from += 1
            elif self.get_number_of_links_from(i) == min_links_from:
                num_of_pages_with_min_links_from += 1

            if self.get_number_of_links_to(i) == max_links_to:
                pages_with_max_links_to.append(self.get_title(i))
                num_of_pages_with_max_links_to += 1
            elif self.get_number_of_links_to(i) == min_links_to:
                num_of_pages_with_min_links_to += 1

            if self.get_number_of_redirects(i) == max_redirects:
                pages_with_max_redirects.append(self.get_title(i))
                num_of_pages_with_max_redirects += 1
            elif self.get_number_of_redirects(i) == min_redirects:
                num_of_pages_with_min_redirects += 1

        print('\nКоличество статей с перенаправлением: ', num_of_redirects)

        print('\nМинимальное количество ссылок из статьи: ', min_links_from)
        print('Максимальное количество ссылок из статьи: ', max_links_from)
        print('Среднее количество ссылок в статье: ', avg_links_from, ' ср. откл. ', stdev_links_from)
        print('Количество статей с максимальным количеством ссылок: ', num_of_pages_with_max_links_from)
        print('Статьи с наибольшим количеством ссылок:', ' '.join(pages_with_max_links_from))
        print('Количество статей с минимальным количеством ссылок: ', num_of_pages_with_min_links_from)

        print('\nМинимальное количество ссылок на статью: ', min_links_to)
        print('Максимальное количество ссылок на статью: ', max_links_to)
        print('Среднее количество ссылок на статью: ', avg_links_to, ' ср. откл. ', stdev_links_to)
        print('Количество статей с максимальным количеством внешних ссылок: ', num_of_pages_with_max_links_to)
        print('Статьи с наибольшим количеством внешних ссылок:', ' '.join(pages_with_max_links_to))
        print('Количество статей с минимальным количеством внешних ссылок: ', num_of_pages_with_min_links_to)

        print('\nМинимальное количество перенаправлений на статью: ', min_redirects)
        print('Максимальное количество перенаправлений на статью: ', max_redirects)
        print('Среднее количество перенаправлений на статью: ', avg_redirects, ' ср. откл. ', stdev_redirects)
        print('Количество статей с максимальным количеством внешних перенаправлений: ', num_of_pages_with_max_redirects)
        print('Статьи с наибольшим количеством внешних перенаправлений:', ' '.join(pages_with_max_redirects))
        print('Количество статей с минимальным количеством внешних перенаправлений: ', num_of_pages_with_min_redirects)

    def shortest_path(self, fired = set()): #поиск в ширину и так дает кратчайший путь в ребрах, просто не хватило фантазии
        print('\nВведите начальную и конечную статьи:', end = ' ')
        start_page, finish_page = input().split()
        print('Запускаем поиск в ширину')
        start_id = self.get_id(start_page)
        finish_id = self.get_id(finish_page)
        fired.add(start_id)
        queue = array.array('L', [start_id])
        shortest_from = array.array('l', [-1]*self.get_number_of_pages())
        while len(queue) != 0:
            current = queue.pop(0)
            for neighbour in self.get_links_from(current):
                if neighbour not in fired:
                    fired.add(neighbour)
                    queue.append(neighbour)
                    shortest_from[neighbour] = current
            if current == finish_id:
                break
        path = finish_page
        while shortest_from[finish_id] != -1:
            path = self.get_title(shortest_from[finish_id]) + ' --> ' + path
            finish_id = shortest_from[finish_id]
        print('Поиск закончен. Найден путь:')
        print(path)



def hist(fname, data, bins, ylabel, title, facecolor='green', alpha=0.5, transparent=True, **kwargs):
    plt.clf()
    # TODO: нарисовать гистограмму и сохранить в файл


if __name__ == '__main__':

    if len(sys.argv) != 2:
        print('Использование: wiki_stats.py <файл с графом статей>')
        sys.exit(-1)

    if os.path.isfile(sys.argv[1]):
        wg = WikiGraph()
        wg.load_from_file(sys.argv[1])
        wg.analysis()
        wg.shortest_path()


    else:
        print('Файл с графом не найден')
        sys.exit(-1)
