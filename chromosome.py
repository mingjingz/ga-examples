import random
import string


class Population(object):
    def __init__(self, target, size, mutate_prob, mate_percent):
        self.members = [Chromosome(len(target)) for _ in range(size)]
        self.target = target
        self.size = size
        self.i_generation = 0
        self.mutate_prob = mutate_prob
        self.mate_percent = mate_percent    # The percent of population that has the mating privilege
        self.calc_all_cost()
        self.sort()

    def sort(self):
        self.members.sort(key=lambda x: x.cost)

    def calc_all_cost(self):
        for m in self.members:
            m.calcCost(self.target)

    def next_generation(self):
        if self.i_generation > 0:
            self.sort()

            # First, mate the top 4% population
            n_mates = int(self.size * self.mate_percent / 2)

            # Kill the unfit ones
            self.members = self.members[:-n_mates*2]
            for i in range(n_mates):

                sp1 = self.members[i*2]
                sp2 = self.members[i*2+1]
                child1, child2 = sp1.mate(sp2, self.mutate_prob)

                self.members.append(child1)
                self.members.append(child2)

            self.calc_all_cost()
            self.sort()

        self.i_generation += 1

    def display(self):
        print("Iteration {0}".format(self.i_generation))

        for i in range(6):
            print("{0} -> {1}".format(self.members[i].genes, self.members[i].cost))

        print()

    def is_solved(self):
        return self.members[0].genes == self.target


class Chromosome(object):
    def __init__(self, length, genes=''):
        if genes:
            self.genes = genes
        else:
            self.genes = ''.join(random.choice(string.printable[0:-5]) for _ in range(length))
        self.cost = float("inf")

    def calcCost(self, target):
        total = 0
        for gene, target_gene in zip(self.genes, target):
            total += (ord(target_gene) - ord(gene)) ** 2

        total += abs(len(target) - len(self.genes)) * 255   # If the chromosomes are of different sizes
        total /= min(len(target), len(self.genes))

        self.cost = total
        return total

    def mutate(self, mutate_prob):
        self.genes = ''.join([
            g if random.random() > mutate_prob
            else random.choice(string.printable[0:-5])
            for g in self.genes
        ])

    def mate(self, spouse, mutate_prob):
        pivot = 3; #min(len(self.genes), len(spouse.genes)) // 2
        child1 = Chromosome(0, genes=self.genes[0:pivot] + spouse.genes[pivot:])
        child1.mutate(mutate_prob)
        child2 = Chromosome(0, genes=spouse.genes[0:pivot] + self.genes[pivot:])
        child2.mutate(mutate_prob)
        return child1, child2


if __name__ == '__main__':
    c = Chromosome(13)
    d = Chromosome(13)
    c1, c2 = c.mate(d, 0)
    print("c=" + c.genes, "d="+d.genes)
    print("c1=" + c1.genes, "c2="+c2.genes)
    print("c.cost={}".format(c.calcCost("Hello, World!")))


