import random
import copy
import threading

def random_gene(l):
    return ''.join(random.choice('01') for i in range(l))

class realga:

    SELECT_RANDOM = 1
    SELECT_RANK = 2
    SELECT_PROP = 3

    def __init__(self, prototype_gene, fitness_function, nmat=10, npop=30, ngen=100, max_fitness=0.0, crossover_rate=0.5, mutation_rate=0.05, max_mutation=1.0, select_method=SELECT_RANK, multi_thread=False):
        self.nmat = nmat
        self.npop = npop
        self.ngen = ngen
        self.sm = select_method
        self.func = fitness_function
        self.mr = mutation_rate
        self.mm = max_mutation
        self.pg = prototype_gene
        self.mf = max_fitness
        self.cr = crossover_rate
        self.mt = multi_thread

        self.population = []
        for i in range(npop):
            gene = {"code": [], "fitness": 0.0, "done": False}
            for p in prototype_gene:
                gene["code"].append(random.uniform(p[0], p[1]))

            self.population.append(gene)

    def crossover(self, a, b):
        res = []
        for i in range(len(a)):
            if self.cr<=random.random():
                m = min(a[i], b[i])
                d = abs(a[i]-b[i])
                res.append(m + random.random()*d)
            else:
                res.append(a[i])

        return res

    def mutation(self, a, n):
        p = self.pg[n]
        a+=random.uniform(-self.mm, self.mm)
        return min(p[1], max(p[1], a))

    def calcfitness(self, gene, fit, best, dataset, layer):
        if dataset==None:
            gene["fitness"] = self.func(gene["code"])
        else:
            gene["fitness"] = self.func(gene["code"], dataset, layer)

        gene["done"] = True
        if gene["fitness"]>best[0]:
            best[0] = gene["fitness"]
            best[1] = gene["code"]

        fit.append(gene["fitness"])

    def run(self, dataset=None, layer=None):
        best = [0.0, None]
        for g in range(self.ngen):
            # Calc Fitness
            fit = []
            pool = []
            for gene in self.population:
                if not gene["done"]:
                    if self.mt:
                        t = threading.Thread(target=self.calcfitness, args=(gene, fit, best, dataset, layer))
                        t.start()
                        pool.append(t)
                    else:
                        self.calcfitness(gene, fit, best, dataset, layer)

            for t in pool:
                t.join()

            print "Generation ["+str(g+1)+"] best is " + str(best[0])

            if self.mf!=0 and best>=self.mf:
                print "done with " + str(best[0])
                return best

            # Select individual to mating pool
            mating_pool = []
            if self.sm==1:
                for i in range(self.nmat):
                    mating_pool.append(population[random.randint(0, len(population)-1)])
            elif self.sm==2:
                mating_pool = sorted(self.population, key=lambda k: k['fitness'], reverse=True)[:self.nmat]
            else:
                cum = []
                s = 0.0
                for gene in self.population:
                    s+=gene["fitness"]
                    cum.append(s)

                for i in range(self.nmat):
                    r = random.uniform(0, s)
                    i = 0
                    for c in cum:
                        if c>r:
                            break
                        i+=1

                    mating_pool.append(self.population[i])

            # Crossover
            self.population = copy.deepcopy(mating_pool)
            for i in range(self.npop-self.nmat):
                a = mating_pool[random.randint(0, len(mating_pool)-1)]["code"]
                b = mating_pool[random.randint(0, len(mating_pool)-1)]["code"]
                self.population.append({"code": self.crossover(a, b), "fitness":0.0, "done":False})

            # Mutation
            for gene in self.population:
                i = 0
                for g in gene["code"]:
                    if self.mr>random.random():
                        g = self.mutation(g, i)

                    i+=1

        print "done with " + str(best[0])
        return best
