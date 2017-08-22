
# http://www.theprojectspot.com/tutorial-post/applying-a-genetic-algorithm-to-the-travelling-salesman-problem/5

# Expected Output
# Initial distance: 1996
# Finished
# Final distance: 940
# Solution:
# |60, 200|20, 160|40, 120|60, 80|20, 40|20, 20|60, 20|100, 40|160, 20|200, 40|180, 60|120, 80|140, 140|180, 100|200, 160|180, 200|140, 180|100, 120|100, 160|80, 180|

import random


class City(object):
    def __init__(self, name, pos):
        self.name = name
        self.pos = pos


class Context(object):
    # The elements
    elements = [City("London", (60, 200)), City("New York", (180, 200)), City("Tokyo", (80, 180)), City("Beijing", (140, 180)), City("Vancouver", (20, 160)), City("Paris", (100, 160)), City("Rome", (200, 160)), City("Seoul", (140, 140)), City("Tehran", (40, 120)), City("Bangkok", (100, 120)), City("Athens", (180, 100)), City("Moscow", (60, 80)), City("Hong Kong", (120, 80)), City("Stockholm", (180, 60)), City("Prague", (20, 40)), City("Berlin", (100, 40)), City("Taipei", (200, 40)), City("Athens", (20, 20)), City("Canberra", (60, 20)), City("Copenhagen", (160, 20))]
    size = len(elements)
    mutation_rate = 0.008
    mating_rate = 0.7       # only the top of this percentage of pairs will have a chance to mate


class Chromosome(object):
    def __init__(self, genes):
        self.genes = genes     # Genes
        self.score = None
        self.value = 0
        self.weight = 0
        self.mutate()
        self.calc_score()

    def calc_score(self):
        # 计算所有元素的value和weight之和
        self.value = sum([g*el.value for g, el in zip(self.genes, Context.elements)])
        self.weight = sum([g*el.weight for g, el in zip(self.genes, Context.elements)])

        # 如果超重的话，就对超重的部分进行惩罚
        self.score = self.value - max(self.weight - Context.weight_limit, 0) * Context.overweight_penalty

    def mate(self, spouse):
        # 随机产生pivot
        pivot = random.randint(1, Context.size-1)

        # 然后将两段切开重组
        child1 = self.genes[0:pivot] + spouse.genes[pivot:]
        child2 = spouse.genes[0:pivot] + self.genes[pivot:]

        return Chromosome(child1), Chromosome(child2)

    def mutate(self):
        for i in range(Context.size):
            if random.random() < Context.mutation_rate:
                self.genes[i] = int(not self.genes[i])
        self.calc_score()


class Population(object):
    def __init__(self, size=1000):
        self.size = size        # Number of chromosomes
        self.members = [
            Chromosome([random.choice([0, 1])
                        for _ in range(Context.size)])
            for _ in range(self.size)]  # Fill with random members

        self.i_generation = 0

    def sort(self):
        self.members.sort(key=lambda x: x.score, reverse=True)

    def mate_and_cull(self):
        quota = int(Context.mating_rate*self.size/2)
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

        for i in range(6):
            print("v={0}, w={1} score={2}:{3}".format(
                self.members[i].value,
                self.members[i].weight,
                self.members[i].score,
                self.members[i].genes,
            ))

        print()

    def is_solved(self):
        if self.i_generation >= 200:
            return True
        else:
            return False


if __name__ == "__main__":
    pop = Population()
    while True:
        pop.next_generation()
        if pop.i_generation % 100 == 0:
            pop.display()
