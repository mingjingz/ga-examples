import random


class Item(object):
    def __init__(self, name, weight=None, value=None):
        self.name = name
        self.weight = weight
        self.value = value


class Context(object):
    # The elements
    elements = [Item("Hydrogen",389,400),Item("Helium",309,380),Item("Lithium",339,424),Item("Beryllium",405,387),Item("Boron",12,174),Item("Carbon",298,483),Item("Nitrogen",409,303),Item("Oxygen",432,497),Item("Fluorine",414,306),Item("Neon",149,127),Item("Sodium",247,341),Item("Magnesium",327,98),Item("Aluminium",195,343),Item("Silicon",356,122),Item("Phosphorus",49,157),Item("Sulfur",151,438),Item("Chlorine",56,460),Item("Argon",317,395),Item("Potassium",383,221),Item("Calcium",281,395),Item("Scandium",394,79),Item("Titanium",377,303),Item("Vanadium",381,308),Item("Chromium",299,295),Item("Manganese",114,447),Item("Iron",422,360),Item("Cobalt",288,249),Item("Nickel",458,482),Item("Copper",91,314),Item("Zinc",104,140),Item("Gallium",470,254),Item("Germanium",77,25),Item("Arsenic",213,393),Item("Selenium",419,96),Item("Bromine",114,199),Item("Krypton",490,8),Item("Rubidium",278,367),Item("Strontium",310,159),Item("Yttrium",175,109),Item("Zirconium",453,288),Item("Niobium",56,375),Item("Molybdenum",147,343),Item("Technetium",123,105),Item("Ruthenium",325,214),Item("Rhodium",418,428),Item("Palladium",353,387),Item("Silver",182,429),Item("Cadmium",411,394),Item("Indium",322,329),Item("Tin",490,436),Item("Antimony",28,479),Item("Tellurium",443,305),Item("Iodine",345,253),Item("Xenon",463,19),Item("Caesium",361,416),Item("Barium",307,417),Item("Lanthanum",291,453),Item("Cerium",259,414),Item("Praseodymium",58,83),Item("Neodymium",127,475),Item("Promethium",11,480),Item("Samarium",361,192),Item("Europium",409,271),Item("Gadolinium",86,231),Item("Terbium",100,75),Item("Dysprosium",166,128),Item("Holmium",54,109),Item("Erbium",432,399),Item("Thulium",361,395),Item("Ytterbium",417,222),Item("Lutetium",311,224),Item("Hafnium",138,101),Item("Tantalum",177,397),Item("Tungsten",14,234),Item("Rhenium",480,141),Item("Osmium",208,490),Item("Iridium",121,68),Item("Platinum",182,29),Item("Gold",339,267),Item("Mercury",259,438),Item("Thallium",342,425),Item("Lead",65,395),Item("Bismuth",33,497),Item("Polonium",293,394),Item("Astatine",392,210),Item("Radon",116,203),Item("Francium",433,253),Item("Radium",303,109),Item("Actinium",149,317),Item("Thorium",342,129),Item("Protactinium",457,50),Item("Uranium",118,77),Item("Neptunium",117,300),Item("Plutonium",106,455),Item("Americium",66,365),Item("Curium",393,407),Item("Berkelium",289,458),Item("Californium",302,322),Item("Einsteinium",455,94),Item("Fermium",216,347),Item("Mendelevium",304,331),Item("Nobelium",49,236),Item("Lawrencium",84,351),Item("Rutherfordium",345,233),Item("Dubnium",168,187),Item("Seaborgium",361,125),Item("Bohrium",236,479),Item("Hassium",201,353),Item("Meitnerium",278,307),Item("Darmstadtium",308,344),Item("Roentgenium",171,201),Item("Copernicium",251,460),Item("Ununtrium",158,52),Item("Ununquadium",282,113),Item("Ununpentium",145,497),Item("Ununhexium",459,449),Item("Ununseptium",327,7),Item("Ununoctium",184,411)]
    size = len(elements)
    weight_limit = 1000
    overweight_penalty = 50
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
