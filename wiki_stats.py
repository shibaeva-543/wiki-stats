#!/usr/bin/python3

import os
import sys
import math

import array

import statistics

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
            self._sizes = array.array('L', [0]*n)
            self._links = array.array('L', [0]*_nlinks)
            self._redirect = array.array('B', [0]*n)
            self._offset = array.array('L', [0]*(n+1))
            curr_link = 0

            for i in range(n):
                self._titles.append(f.readline().rstrip())
                (size, redirect, num_of_links) = map(int, f.readline().split())
                self._sizes[i] = size
                self._redirect[i] = redirect
                self._offset[i+1] = self._offset[i] + num_of_links
                for j in range(curr_link, curr_link + num_of_links):
                    self._links[j] = int(f.readline())
                curr_link += num_of_links

        print(self._titles[0], list(self._links[self._offset[0]:self._offset[1]]))
        print('Граф загружен')

    def get_number_of_links_from(self, _id):
        number = len(list(self._links[self._offset[_id]:self._offset[_id+1]]))
        print('Number of links from ', _id, ' is ', number)

    def get_links_from(self, _id):
        links = list(self._links[self._offset[_id]:self._offset[_id+1]])
        print('Links from', _id, ':')
        print('\n'.join(map(str, links)))

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
        for i in range(self.pages):

            if self.is_redirect(i):
                num_of_redirects += 1
        print(num_of_redirects)


def hist(fname, data, bins, xlabel, ylabel, title, facecolor='green', alpha=0.5, transparent=True, **kwargs):
    plt.clf()
    # TODO: нарисовать гистограмму и сохранить в файл


if __name__ == '__main__':

    if len(sys.argv) != 2:
        print('Использование: wiki_stats.py <файл с графом статей>')
        sys.exit(-1)

    if os.path.isfile(sys.argv[1]):
        wg = WikiGraph()
        wg.load_from_file(sys.argv[1])
        wg.get_number_of_links_from(0)
        wg.get_links_from(0)
        print(wg.get_id('Windows_98'))
        print(wg.get_number_of_pages())
        print(wg.is_redirect(0))
        wg.analysis()

    else:
        print('Файл с графом не найден')
        sys.exit(-1)

    # TODO: статистика и гистограммы