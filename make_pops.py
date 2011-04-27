import random
import time

class Gene:
    extant_genes = {}
    
    def __init__(self, id):
        self.id = id
        Gene.extant_genes[id] = self

class Pathway:
    extant_pathways = {}
    
    def __init__(self, id, genes):
        self.id = id
        self.genes = genes
        Pathway.extant_pathways[id] = self
##        print("Constructed pathway %d" % self.id)


    def get_genes(self):
        return self.genes
        
    def __str__(self):
        string = "Pathway [%d] has the following genes:\n" % (self.id)
        for gene in self.get_genes():
            string += "[%d], " % (gene.id)
        string += "*\n"
        return string

class Organism():
    extant_organisms = {}
    
    def __init__(self, id, pathways):
        self.id = id
        self.pathways = pathways
        Organism.extant_organisms[id] = self
        self.genes = None
##        print("Constructed organism %d" % self.id)

    def get_pathways(self):
        return self.pathways

    def record_genes(self):
        pathways = self.get_pathways()
        genes = []
        for pathway in pathways:
            genes += pathway.get_genes()
        return list(set(genes))

    def get_genes(self):
        if self.genes == None:
##            print("Getting genes for org %d for the first time" % self.id)
            self.genes = self.record_genes()
        return self.genes
    
    def __str__(self):
        string = "Organism [%d] has the following pathways:\n" % (self.id)
        for pathway in self.get_pathways():
            string += "[%d], " % (pathway.id)
        string += "*\n"
        return string
        
def normal_dist_orgs(organism, mean = 20, std = 5, minim = 0, maxim = 100):
    """The first distribution for counts for population members.

Should look like a truncated normal distribution.
Just a proof of concept.  Instead I should look into the Pareto distribution.

"""
    rand = random.normalvariate(mean, std)
    while rand > maxim or rand < minim:
        rand = random.normalvariate(mean, std)
    return rand
    
def pareto_dist_orgs(organism, alpha = 1):
    """Implementation of the Pareto distribution for species member counts.
    
    See http://en.wikipedia.org/wiki/Pareto_distribution#Generating_bounded_Pareto_random_variables
    """
    rand = random.paretovariate(alpha)
    return rand
        
class Population():
    extant_populations = {}
    
    def __init__(self, id, organisms, frequencies = normal_dist_orgs):
        self.id = id
        self.organisms = organisms
        self.frequencies = {}
        self.counts = {}
        for org in self.organisms:
            self.counts[org] = frequencies(org)
        total_count = sum(self.counts.values())
        for org in self.organisms:
            self.frequencies[org] = self.counts[org]/total_count
        self.pathways = None
        self.genes = None
        self.gene_frequencies = None
##        print("Constructed population %d" % self.id)
        Population.extant_populations[id] = self


    def get_orgs(self):
        return self.organisms

    def record_pathways(self):
        pathways = []
        for org in self.get_orgs():
            pathways += org.get_pathways()
        return list(set(pathways))

    def get_pathways(self):
        if self.pathways == None:
##            print("Getting pathways for pop %d for the first time" % self.id)
            self.pathways = self.record_pathways()
        return self.pathways

    def record_genes(self):
        genes = []
        for pathway in self.get_pathways():
            genes += pathway.get_genes()
        return list(set(genes))

    def get_genes(self):
        if self.genes == None:
##            print("Getting genes for pop %d for the first time" % self.id)
            self.genes = self.record_genes()
        return self.genes

    def get_org_frequency(self, org):
        return self.frequencies[org]
    
    def record_gene_frequencies(self):
        genes = self.get_genes()
        orgs = self.get_orgs()
        gene_counts = dict(zip(genes, [0]*len(genes)))
        gene_frequencies = {}
        num_orgs = len(self.organisms)
        for org in orgs:
            for gene in org.get_genes():
                gene_counts[gene] += self.get_org_frequency(org)
##        print("Summing gene frequencies across all genes in pop %d" % self.id)
        for gene in gene_counts.keys():
            sum_counts = sum(gene_counts.values())
        for gene in gene_counts.keys():
            gene_frequencies[gene] = gene_counts[gene]/sum_counts
        self.gene_frequencies = gene_frequencies

    def get_gene_frequencies(self):
        if self.gene_frequencies == None:
##            print("Getting gene frequencies for pop %d for the first time" % self.id)
            self.record_gene_frequencies()
        return self.gene_frequencies
        
    def __str__(self):
        string = "Population [%d] has the following organisms:\n" % (self.id)
        for org_and_freq_tuple in self.frequencies.items():
            org_object = org_and_freq_tuple[0]
            freq = (org_and_freq_tuple[1])
            org_id = org_object.id
            perc = freq * 100.0
            string += "Organism [%d] is %d%% of the population.\n" % (org_id, perc)
        return string
                
    
def make_random_pops(num_genes, num_pathways, num_orgs, genes_per_pathway,\
                    pathways_per_org, orgs_per_pop, num_pops = 1):
    for gene_id in range(num_genes):
        Gene(gene_id)
##    print("Started constructing pathways")
    for pathway_id in range(num_pathways):
        genes = random.sample(Gene.extant_genes.values(), genes_per_pathway)
        Pathway(pathway_id, genes)
##    print("Finished constructing pathways")
##    print("Started constructing orgs")
    for org_id in range(num_orgs):
##        print("Started sampling pathways for org %d" % org_id)
        pathways = random.sample(Pathway.extant_pathways.values(), pathways_per_org)
##        print("Finished sampling pathways for org %d" % org_id)
        Organism(org_id, pathways)
##    print("Finished constructing orgs")
    populations = []
    for pop in range(num_pops):
        orgs = random.sample(Organism.extant_organisms.values(), orgs_per_pop)
        populations += [Population(pop, orgs, pareto_dist_orgs)]
    return populations

def make_testable_pops(num_genes, num_pathways, num_orgs, genes_per_pathway,\
                    pathways_per_org, orgs_per_pop, num_pops = 1):
    """Makes a population

    where genes [0] and [1] are always in pathway [0] in organism [0]
    And gene [2] is always in pathway [1], in organism [0]

    This allows us to test the nearness index (from a random walk) of
    genes [0], [1], and [2], where the nearness of [0] and [1] represents
    the pathway effect and [0] and [2] is the organism effect, and the
    nearness to [3] is the control

    """
    for gene_id in range(num_genes):
        Gene(gene_id)
##    print("Started constructing pathways")
    for pathway_id in range(num_pathways):
        genes = None
        if pathway_id == 0: # so if you're pathway [0] you definitely have genes [0] and [1]
            genes = Gene.extant_genes.values()[:2] + \
                    random.sample(Gene.extant_genes.values()[2:],
                                  genes_per_pathway - 2)
        elif pathway_id == 1: # so if you're pathway [1] you definitely have genes [2] and [3]
            gene_list = Gene.extant_genes.values()
            definite_genes = [gene_list[2]]
            other_genes = gene_list[0:2] + gene_list[3:]
            genes = definite_genes + \
                    random.sample(other_genes,
                                  genes_per_pathway - 1)
        else:
            genes = random.sample(Gene.extant_genes.values(),
                                  genes_per_pathway)
        Pathway(pathway_id, genes)
##    print("Finished constructing pathways")
##    print("Started constructing orgs")
    for org_id in range(num_orgs):
##        print("Started sampling pathways for org %d" % org_id)
        pathways = None
        if org_id == 0: # so if you're organism [0] you definitely have pathways [0] and [1]
            pathways = Pathway.extant_pathways.values()[:2] + \
                       random.sample(Pathway.extant_pathways.values()[2:],
                                     pathways_per_org - 2)
        else:
            pathways = random.sample(Pathway.extant_pathways.values(), pathways_per_org)
##        print("Finished sampling pathways for org %d" % org_id)
        Organism(org_id, pathways)
##    print("Finished constructing orgs")
    populations = []
    for pop in range(num_pops):
        if pop == 0:
            org_list = Organism.extant_organisms.values()
            orgs = [org_list[0]] + random.sample(org_list[1:], orgs_per_pop - 1)
        else:
            orgs = random.sample(Organism.extant_organisms.values(), orgs_per_pop)
        populations += [Population(pop, orgs, pareto_dist_orgs)]
    return populations
