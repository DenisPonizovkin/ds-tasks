#----------------------------------------------------------------------------------------------------------------------
# Криетрий Вальда.
#
# Использемые теоретические материалы
# https://docplayer.ru/43713762-Proverka-prostyh-i-slozhnyh-gipotez-s-ispolzovaniem-posledovatelnogo-kriteriya-valda.html
# https://www.statisticshowto.datasciencecentral.com/sequential-probability-ratio-test/
# https://en.wikipedia.org/wiki/Sequential_probability_ratio_test
# http://informaticslib.ru/books/item/f00/s00/z0000031/st034.shtml
# https://www.youtube.com/watch?v=4NYbTUIkBbU
#----------------------------------------------------------------------------------------------------------------------

import numpy as np
import random

class Task3:

    # Генерация генеральной совокупности путем смешивания.
    # Смешивание - это функция mix
    def generate(self, card):
        sets = dict()
        sets['x'] = []
        sets['y'] = []

        colors = ['b', 'r', 'g']
        mu = [self._mu0, self._mu1]
        alpha = 0.8
        for i in range(0, len(mu)):
            xs = np.random.normal(mu[i], self._sigma, card)
            ys = self.normal(xs, mu[i], self._sigma)
            sets['x'].append(xs)
            sets['y'].append(ys)
        return self.mix(sets)

    # Смешивание совокупностей
    def mix(self, xy):
        nums = [int(len(xy['x'][i]) * self._portions[i]) for i in range(0, len(xy['x']))]
        xs = []
        ys = []
        for n in range(0, len(xy['x'])):
            ids = sorted(random.sample(range(len(xy['x'][n])), nums[n]))
            x = xy['x'][n]
            y = xy['y'][n]
            xs.append([x[i] for i in ids])
            ys.append([y[i] for i in ids])
        mixx = []
        for x in xs:
            mixx += x
        mixy = []
        for y in ys:
            mixy += y
        mix = dict()
        mix['x'] = mixx
        mix['y'] = mixy
        return mix


    # ------------------------------------------------------------------------------
    # По заданию известно f0, f1 выборок, которые явлются нормальным
    # распределением.
    def f(self, x, mu):
        return self.normal(x, mu, self._sigma)

    def f0(self, x):
        return self.f(x, self._a0)

    def f1(self, x) :
        return self.f(x, self._a1)
    # Значение функции нормального распределения
    def normal(self, x, mu, sigma):
        return ( 2.*np.pi*sigma**2. )**-.5 * np.exp( -.5 * (x-mu)**2. / sigma**2. )

    # свободный член, независящий от x, Который добавляется к краям c0, c1
    # следует из фморлу Log(f1/f0), где fi - это нормальное распределение
    def add_coef(self, mu0, mu1, sigma):
        return (mu0**2 - mu1**2)/sigma**2
    # ------------------------------------------------------------------------------
    def __init__(self):
        self._c0 = None
        self._c1 = None
        self._sigma = 1

    def run(self):
        # По теории говорится, что если alpha, betta заданы, то
        # то любой критерий с такими ошибками называют критерием силы,
        # как и по заданию.
        # И тогда понятно, с каких значений c0, c1 (искомого отрезка)
        # можно начинать последовательный критерий
        # По теории
        # alpha' <= (alpha) / (1 - betta)
        # betta' <= betta / (1 - alpha)
        # c0 >= betta'/(1 - alpha')
        # c1 <= (1 - betta') / alpha'
        # Как я понимаю, по заданию alpha' и betta' считаются заданными
        # тогда стартуем алгоритм
        # c0 = betta'/(1 - alpha')
        # c1 = (1 - betta')/alpha'
        # Так как штрих символа нет, то использую имена переменных без штриха в оде.
        alpha     = 0.9
        betta     = 0.1
        # мат ожидания смесей
        self._mu0 = 1
        self._mu1 = 100
        self._portions = [0.9, 0.1]

        # для гипотез
        self._a0  = 1
        self._a1  = 100

        data = self.generate(100000)
        step = 0.0001
        card = 0
        n = 10 # число тестов
        for i in range(0, n):
            lfs = list()
            self._c0 = -10000
            self._c1 = 10000
            sample = list()
            while(True):
                x = data['x'][int(random.randrange(len(data)))]
                v = x * (self._a1 - self._a0)/self._sigma**2
                lfs.append(v)
                log = np.log(np.prod(lfs))
                print(log)
                likehood = log + len(lfs) * self.add_coef(self._a0, self._a1, self._sigma)
                print(likehood)
                if (likehood >= self._c1):
                    print("Accept H1:" + str("a0,a1=") + str(self._a0) + "," + str(self._a1)
                          + " [c0,c1]=" + str(self._c0) + "," + str(self._c1) + ",sample card=" + str(len(sample)) + ", "
                          + str(likehood))
                    card += len(sample) + 1
                    break

                if (likehood <= self._c0):
                    print("Accept H0:" + str("a0,a1=") + str(self._a0) + "," + str(self._a1)
                        + " [c0,c1]=" + str(self._c0) + "," + str(self._c1) + ",sample card=" + str(len(sample)) + ", "
                          + str(likehood))
                    card += len(sample) + 1
                    break

                if ((self._c0 < likehood) and (likehood < self._c1)):
                    sample.append(x)
                    step = self.add_coef(self._a0, self._a1, self._sigma)
                    self._c0 += step
                    self._c1 -= step

        print("card = " + str(card/n))
