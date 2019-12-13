#
# https://www.coursera.org/lecture/stats-for-data-analysis/znachimost-korrieliatsii-zKGmV
# https://habr.com/ru/company/JetBrains-education/blog/438058/
# https://www.machinelearningmastery.ru/chi-squared-test-for-machine-learning/

import scipy
from collections import Counter

class Task5:
    def __read_data(self, f):
        with open(f, 'r') as fp:
            # save features names
            ftrs = fp.readline()
            self._ftrs_names = ftrs.split("\t")[3:] # reject Age feature
            for f in self._ftrs_names:
                self._ftrs_data_f[f] = list()
                self._ftrs_data_m[f] = list()

            ftrs = fp.readline()
            while (ftrs):
                data = ftrs.split("\t")[2:]
                data = list(map(lambda s: int(s), data))
                sex = data[0]
                data = data[1:]
                if (sex == 1):
                    for i in range(0, len(self._ftrs_names)):
                        f = self._ftrs_names[i]
                        self._ftrs_data_f[f].append(data[i])
                else:
                    for i in range(0, len(self._ftrs_names)):
                        f = self._ftrs_names[i]
                        self._ftrs_data_m[f].append(data[i])
                ftrs = fp.readline()

    def __init__(self, f):
        self._ftrs_names  = list()
        self._ftrs_data_f = dict()
        self._ftrs_data_m = dict()

        self.__read_data(f)

    def table(self, f):
        fdata = dict(Counter(self._ftrs_data_f[f]))
        mdata = dict(Counter(self._ftrs_data_m[f]))

        for f in fdata.keys():
            if f not in mdata.keys():
                mdata[f] = 0
        for f in mdata.keys():
            if f not in fdata.keys():
                fdata[f] = 0

        fdata  = [fdata[k] for k in sorted(fdata.keys())]
        mdata  = [mdata[k] for k in sorted(mdata.keys())]
        return [fdata, mdata]

    def run(self):
        for f in self._ftrs_names:
            if (len(self._ftrs_data_f[f]) < 40):
                print("Data for " + f + " is too small (female)")
                continue
            if (len(self._ftrs_data_m[f]) < 40):
                print("Data for " + f + " is too small (male)")
                continue

            t = self.table(f)
            stat, p, dof, expected = scipy.stats.chi2_contingency(t)
            print(p)
            # out = "Results for " + f
            # out += "\nstat = "       + "{:.2f}".format(stat)
            # out += "\np = "        + "{:.2f}".format(p)
            # out += "\ndof = "      + "{:.2f}".format(dof)
            # out += "\nexpected = " + "\n" + str(expected)
            # out += "\n=========================================================="
            # print(out)
            # prob = 0.95
            # critical = chi2.ppf(prob, dof)
            # if abs(stat) >= critical:
	        #     print('Dependent (reject H0)')
            # else:
	        #     print('Independent (fail to reject H0)')
