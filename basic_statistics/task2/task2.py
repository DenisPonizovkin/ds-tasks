import numpy as np
import matplotlib.pyplot as plt
import random

class Task2:
    def normal(self, x, mu, sigma):
        return ( 2.*np.pi*sigma**2. )**-.5 * np.exp( -.5 * (x-mu)**2. / sigma**2. )

    def mix(self, xy):
        portions = [0.2, 0.3, 0.5]
        nums = [int(len(xy['x'][i]) * portions[i]) for i in range(0, len(xy['x']))]
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

    def generate(self, option, card):
        sets = dict()
        sets['x'] = []
        sets['y'] = []

        if (option == 1):
            mu = 0. # random.random()
            sigma = 0.5 # random.random()
            for i in range(0, 3):
                xs = np.random.normal(mu, sigma, card)
                ys = self.normal(xs, mu, sigma)
                sets['x'].append(xs)
                sets['y'].append(ys)
                plt.scatter(xs, ys)
            plt.title("sigma = " + "{:.2f}".format(sigma))
            plt.show()

        if (option == 2):
            colors = ['b', 'r', 'g']
            mu = [0.1, 0.3, 0.9]
            sigma = 0.5
            for i in range(0, 3):
                xs = np.random.normal(mu[i], sigma, card)
                ys = self.normal(xs, mu[i], sigma)
                sets['x'].append(xs)
                sets['y'].append(ys)
                plt.scatter(xs, ys)
            plt.title("sigma = " + "{:.2f}".format(sigma))
            print(mu)
            print(sigma)
            plt.show()

        if (option == 3):
            colors = ['b', 'r', 'g']
            mu = [0.1, 0.3, 0.9]
            sigma = [0.3, 1.7, 0.7]
            title = "sigma = "
            for i in range(0, 3):
                xs = np.random.normal(mu[i], sigma[i], card)
                ys = self.normal(xs, mu[i], sigma[i])
                sets['x'].append(xs)
                sets['y'].append(ys)
                plt.scatter(xs, ys)
                title += "{:.2f}".format(sigma[i]) + " / "
            plt.title(title)
            plt.show()

        return sets

    def findw(self, x, all):
        for i in range(0, len(all['x'])):
            for j in range(0, len(all['x'][i])):
                if all['x'][i][j] == x:
                    return all['y'][i][j]

    def sampling(self, data, option, all):
        n = len(data)
        if (option == 1):
            return [data[i] for i in sorted(random.sample(range(n), int(0.8 * n)))]

        if (option == 2):
            xs = []
            for i in range(0, len(all['x'])):
                strat = []
                for x in all['x'][i]:
                    if x in data:
                        strat.append(x)
                xs.append(strat)

            samples = []
            for i in range(0, len(all['x'])):
                samples += self.sampling(xs[i], 1, all)
            return samples

        if (option == 3):
            i = 0
            x1 = data[random.randint(0, len(data) - 1)]
            w1 = self.findw(x1, all)
            rslt = []
            while (i < 0.8 * n):
                x = x1
                x2 = data[random.randint(0, len(data) - 1)]
                w2 = self.findw(x2, all)
                w = w2/w1
                if (w >= 1):
                    x = x2
                else:
                    if random.randrange(1) <= w:
                        x = x2
                rslt.append(x2)
                i += 1
                x1 = data[random.randint(0, len(data) - 1)]
                w1 = self.findw(x1, all)
                # if (i % 10 == 0):
                #     print("sampling " + str(i))
            return rslt

    def mean(self, data):
        return float('{:.2f}'.format(np.mean(data)))

    def distr(self, data):
        return float('{:.2f}'.format(np.var(data)))

    def run(self):
        all = self.generate(1,1000)
        general = self.mix(all)
        plt.scatter(general['x'], general['y'])
        plt.show()

        ms = []
        ds = []
        for exp_num in range(1, 4):
            m = 0
            d = 0
            n = 1000
            if (exp_num > 1):
                n = 20
            for i in range(0, n):
                if (i % 2 == 0):
                    print("==========================> sample " + str(i))
                sample = self.sampling(general['x'], exp_num, all)
                m += self.mean(sample)
                d += self.distr(sample)
            m /= n
            d /= n
            ms.append(m)
            ds.append(d)

        for i in range(0, len(ms)):
            print("{:.5f}".format(ms[i]))
            print("{:.5f}".format(ds[i]))

