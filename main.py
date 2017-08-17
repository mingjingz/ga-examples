from chromosome import *

pop = Population(target="Hello, World!", size=1000, mutate_prob=0.05, mate_percent=0.2)
while not pop.is_solved():
    pop.next_generation()
    if pop.i_generation % 20 == 0:
        pop.display()

pop.display()