# Проверка гипотез о значимости корреляций.
# Критерий Стьюдента
# Теоретические материалы:
# https://www.coursera.org/lecture/stats-for-data-analysis/znachimost-korrieliatsii-zKGmV
# http://matstats.ru/kr.html
# http://statistica.ru/theory/znachimost-koeffitsienta-korrelyatsii-doveritelnyy-interval/
# https://einsteins.ru/subjects/statistika/teoriya-statistika/ocenka-korrelyacii
# http://eric.univ-lyon2.fr/~ricco/tanagra/fichiers/en_Tanagra_Calcul_P_Value.pdf

import numpy as np
from scipy.stats import t
import math

class Task4:
    # ---------------------------------------------------------------------------------------------------
    # Инициализационные функции: четение, init
    def __read_data(self, f):
        with open(f, 'r') as fp:
            ftrs = fp.readline()
            ftrs = fp.readline()
            while (ftrs):
                data = ftrs.split("\t")

                # Для разбиения выборки на два типа по полу
                # if (data[0] == 'Male'):
                #     ftrs = fp.readline()
                #     continue

                data = list(map(lambda s: float(s), data[1:]))
                is_undefined_value = False
                for e in data:
                    if (e < 0):
                        is_undefined_value = True
                        break
                if (is_undefined_value):
                    ftrs = fp.readline()
                    continue

                self._fsiq.append(data[1])
                self._viq.append(data[2])
                self._piq.append(data[3])
                self._w.append(data[4])

                ftrs = fp.readline()

    def __init__(self, f):
        self._fsiq = list()
        self._viq  = list()
        self._piq  = list()
        self._w    = list()

        self.__read_data(f)
    # ---------------------------------------------------------------------------------------------------
    # Коэффициент корреляции
    def corr(self, data1, data2):
        return float(np.corrcoef(data1, data2)[1, 0])

    # Значение статистикаи. n - мощность совокупности
    def stat(self, r, n):
        tv = r * math.sqrt(n) / math.sqrt(1 - r*r)
        if (tv < 0):
            tv *= -1
        return tv

    # Критическое значение, которое берется из распределения Стьюдента.
    # С ним сравниваем значение коэффициента корреляции
    def critical_t(self, tv, k):
        return t.sf(tv, k)

    def check(self, name, data, weights):
        k = len(weights) - 2 # Для вычисляемой статистики мощность равна n - 2
        r = self.corr(data, self._w)
        tv = self.stat(r, k)
        tc = self.critical_t(tv, k)
        if (tv > tc):
            print("H0 rejected for " + name + ": r = " + str(r) + "|tv = " + str(tv) + "|tc = " + str(tc))
        else:
            print("H0 not rejected for " + name + ": r = " + str(r) + "|tv = " + str(tv) + "|tc = " + str(tc))

    # Если нулевая гипотеза справедлива, то статистика имеет распределение Стьюдента
    # Основной алгоритм
    # H0 -> корреляции нет, corr(data1, data2) == 0
    # H1 -> corr != 0
    # Если нулевая гипотеза справедлива, то статистика имеет распределение Стьюдента
    def run(self):
        k = len(self._w) - 2 # Для вычисляемой статистики мощность равна n - 2
        self.check("FSIQ", self._fsiq, self._w)
        self.check("PIQ", self._piq, self._w)
        self.check("VIQ", self._viq, self._w)
