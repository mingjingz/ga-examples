
# http://www.theprojectspot.com/tutorial-post/applying-a-genetic-algorithm-to-the-travelling-salesman-problem/5

# Expected Output
# Initial distance: 1996
# Finished
# Final distance: 940
# Solution:
# |60, 200|20, 160|40, 120|60, 80|20, 40|20, 20|60, 20|100, 40|160, 20|200, 40|180, 60|120, 80|140, 140|180, 100|200, 160|180, 200|140, 180|100, 120|100, 160|80, 180|

import random
import math
import numpy as np

import matplotlib.pyplot as plt


class City(object):
    def __init__(self, name, pos):
        self.name = name
        self.pos = pos

    def __str__(self):
        return self.name + str(self.pos)


class Context(object):
    # The elements
    def __init__(self, cities, mutation_rate = 0.05, mating_rate = 0.7):
        self.elements = cities
        self.size = len(self.elements)
        self.mutation_rate = mutation_rate
        self.mating_rate = mating_rate          # only the top of this percentage of pairs will have a chance to mate

        # precalculate all distances between cities
        self.distance = [[0 for b in range(self.size)] for a in range(self.size)]

        for a in range(self.size):
            for b in range(a+1, self.size):
                self.distance[a][b] = self.distance[b][a] = \
                    math.sqrt(
                        (self.elements[a].pos[0]-self.elements[b].pos[0]) ** 2 +
                        (self.elements[a].pos[1]-self.elements[b].pos[1]) ** 2
                    )

cxt = Context(
    cities=[City("London", (60, 200)), City("New York", (180, 200)), City("Tokyo", (80, 180)), City("Beijing", (140, 180)), City("Vancouver", (20, 160)), City("Paris", (100, 160)), City("Rome", (200, 160)), City("Seoul", (140, 140)), City("Tehran", (40, 120)), City("Bangkok", (100, 120)), City("Athens", (180, 100)), City("Moscow", (60, 80)), City("Hong Kong", (120, 80)), City("Stockholm", (180, 60)), City("Prague", (20, 40)), City("Berlin", (100, 40)), City("Taipei", (200, 40)), City("Athens", (20, 20)), City("Canberra", (60, 20)), City("Copenhagen", (160, 20))],
    mutation_rate=0.05,
    mating_rate=0.7
)

class Chromosome(object):
    def __init__(self, genes=None):
        self.genes = genes      # Genes
        if not self.genes:
            self.genes = list(range(0, cxt.size))
            random.shuffle(self.genes)

        self.cost = None       # Distance
        self.mutate()           #
        self.calc_cost()       # Distance

    def calc_cost(self):
    	# 计算距离
        # 计算所有元素的value和weight之和
        self.cost = 0
        for i in range(-1, len(self.genes)-1):
            self.cost += cxt.distance[self.genes[i]][self.genes[i+1]]

    def mate(self, spouse):
    	# 3 5 7 2 4 1 6 0
    	# 2 0 3 1 5 4 7 6 
    	# 互换一部分

    	# 3 5 7 2 0 1 4 6 -》 改变后半部分
    	# 3 2 1 0 5 4 7 6 -》 改变前半部分
        # 随机产生pivot
        # 但是至少一段要有2个城市
        pivot = 10 #random.randint(2, cxt.size-2)

        seg1 = []  #self.genes[0:pivot]
        seg2 = []

        for i in self.genes:
        	if i in spouse.genes[0:pivot]:
        		seg2.append(i)

        # print(seg2)
        for i in spouse.genes:
        	if i in self.genes[pivot:]:
        		seg1.append(i)
        # print(seg1)

        child1 = self.genes[0:pivot] + seg1
        child2 = seg2 + spouse.genes[pivot:]
        # print(child1)
        # print(child2)
        # 保留self的[0:pivot], 和spouse的[pivot:]
        return Chromosome(child1), Chromosome(child2)

    def mutate(self):
    	# 随机互换两个城市
        i = random.randint(0, len(self.genes)-1)
        j = random.randint(0, len(self.genes)-1)
        self.genes[i], self.genes[j] = self.genes[j], self.genes[i]


class Visualizer(object):
    def __init__(self, population, top_n):
        self.n_axes = top_n
        self.pop = population
        # self.len(genes)
        plt.ion()
        self.fig = plt.figure(figsize=(15,4))
        self.fig.suptitle("Generation {0}".format(self.pop.i_generation))
        self.axs = []
        self.plots = []
        self.cit = np.array(cxt.elements)

        for i, m in enumerate(self.pop.members[:self.n_axes]):  # g in enumerate(genes):
            ax = self.fig.add_subplot(1, self.n_axes, i+1, aspect='equal')
            if i > 0:
                ax.tick_params(labelleft="off")
            ax.set_title('len={:10.4f}'.format(self.pop.members[i].cost))
            ax.grid()

            self.axs.append(ax)
            x, y = self._get_path(i)
            hl, = ax.plot(x, y, marker='o', markerfacecolor='red')
            hl_start, = ax.plot(x[0], y[0], marker='^', markersize=12, markerfacecolor='green')
            hl_end, = ax.plot(x[-1], y[-1], marker='8', markersize=12, markerfacecolor='red')
            self.plots.append((hl, hl_start, hl_end))

        plt.tight_layout(rect=[0, 0.03, 1, 0.95])

        plt.pause(0.001)

    def _get_path(self, index):
        """ Build a connected path from genes
        """
        seq = self.cit[np.array(self.pop.members[index].genes)]
        x = np.array([el.pos[0] for el in seq])
        y = np.array([el.pos[1] for el in seq])
        return x, y

    def update(self):
        for i, m in enumerate(self.pop.members[:self.n_axes]):
            x, y = self._get_path(i)
            self.plots[i][0].set_xdata(x)
            self.plots[i][0].set_ydata(y)
            self.plots[i][1].set_xdata(x[0])
            self.plots[i][1].set_ydata(y[0])
            self.plots[i][2].set_xdata(x[-1])
            self.plots[i][2].set_ydata(y[-1])
            self.axs[i].set_title('len={:10.4f}'.format(self.pop.members[i].cost))

        self.fig.suptitle("Generation {0}".format(self.pop.i_generation))

        plt.pause(0.001)


class Population(object):
    def __init__(self, size=1000):
        self.size = size        # Number of chromosomes
        self.members = [Chromosome() for _ in range(self.size)]    # Fill with random members
        self.sort()
        self.i_generation = 0

    def sort(self):
        self.members.sort(key=lambda x: x.cost)

    def mate_and_cull(self):
        quota = int(cxt.mating_rate*self.size/2)
        elites = self.members[:quota]
        random.shuffle(elites)      # randomize the elites

        new_child = []
        for i in range(quota):
            new_child.extend(self.members[i*2].mate(self.members[i*2+1]))

        n_to_cull = len(new_child)

        self.members = self.members[:-n_to_cull] + new_child

    def next_generation(self):
        self.sort()
        self.mate_and_cull()
        self.sort()
        self.i_generation += 1

    def display(self):
        print("Iteration {0}".format(self.i_generation))

        # Print the top 6 members
        for i in range(6):
            print("cost={cost}:{genes}".format(
                cost = self.members[i].cost,
                genes = self.members[i].genes
            ))

        print()

    def get_top_genes(self, n):
        return [m.genes for m in self.members[0:n]]
        
    def is_solved(self):
        if self.i_generation >= 200:
            return True
        else:
            return False


if __name__ == "__main__":
    print(cxt.distance[0][1], cxt.distance[1][0])
    print(cxt.elements[0], cxt.elements[1])

    c = Chromosome()
    print(c.genes)
    c.mutate()
    print(c.genes)

    d = Chromosome()
    print(d.genes)

    c1, c2 = c.mate(d)
    print(c1.genes)
    print(c2.genes)

    # t = Chromosome([0,1,2])
    # print(t.genes)
    # print(t.cost)
    pop = Population()
#     plt.ion()

#     fig = plt.figure(figsize=(12,3))
#     ax = fig.add_subplot(151)
#    # fig, axs = plt.subplots(1, 5, )
#     x = np.array([1, 2, 3])
#     y = np.array([4, 5, 6])

#     hl, = ax.plot(x, y)
#     # plt.draw()

#     plt.pause(0.001)

    pop.next_generation()
    vis = Visualizer(pop, 5)

    while True:
        pop.next_generation()
        if pop.i_generation % 10 == 0:
            pop.display()

        vis.update()
        #  hl.set_ydata(y + pop.i_generation / 100.0)
         #plt.draw()
         # fig.canvas.draw()
         # fig.canvas.flush_events()
        plt.pause(0.001)
    plt.show()
    # generate the sequence:
    # cit = np.array(cxt.elements)
    # res = np.array([15, 12, 19, 16, 13, 10, 6, 1, 3, 7, 9, 5, 2, 0, 4, 8, 11, 14, 17, 18])
    # seq = cit[res]
    # print(seq)
    # import matplotlib.pyplot as plt
    # x = np.array([el.pos[0] for el in seq])
    # y = np.array([el.pos[1] for el in seq])
    # for xx, yy in zip(x, y):
    #     print(xx, yy)

    # plt.ion()
    # fig = plt.figure()
    # ax = plt.subplot(151)
    # plt.plot(x, y)
    # plt.show()
