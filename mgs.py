import random
import time

OLD_TIME = time.time()



def new_print(kwargs, old_time = OLD_TIME):
##    now = time.time()
##    print now - old_time
##    OLD_TIME = now
    print(kwargs)
    print "at " + str(time.clock())


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
        new_print("Constructed pathway %d" % self.id)


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
        new_print("Constructed organism %d" % self.id)

    def get_pathways(self):
        return self.pathways

    def record_genes(self):
        pathways = self.get_pathways()
        genes = []
        for pathway in pathways:
            for gene in pathway.get_genes():
                if not gene in genes:
                    genes += [gene]
        return genes

    def get_genes(self):
        if self.genes == None:
            self. genes = self.record_genes()
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
        new_print("Constructed population %d" % self.id)


    def get_orgs(self):
        return self.organisms

    def record_pathways(self):
        pathways = []
        for org in self.get_orgs():
            for pathway in org.get_pathways():
                if not pathway in pathways:
                    pathways += [pathway]
        return pathways

    def get_pathways(self):
        if self.pathways == None:
            self.pathways = self.record_pathways()
        return self.pathways

    def record_genes(self):
        genes = []
        for pathway in self.get_pathways():
            for gene in pathway.get_genes():
                if not gene in genes:
                    genes += [gene]
        return genes

    def get_genes(self):
        if self.genes == None:
            self.genes = self.record_genes()
        return self.genes

    def get_org_frequency(self, org):
        return self.frequencies[org]

    def get_gene_frequencies(self):
        genes = self.get_genes()
        orgs = self.get_orgs()
        gene_counts = dict(zip(genes, [0]*len(genes)))
        gene_frequencies = {}
        num_orgs = len(self.organisms)
        for org in orgs:
            for gene in org.get_genes():
                gene_counts[gene] += self.get_org_frequency(org)
        for gene in gene_counts.keys():
            sum_counts = sum(gene_counts.values())
        for gene in gene_counts.keys():
            gene_frequencies[gene] = gene_counts[gene]/sum_counts
        return gene_frequencies
        
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
    new_print("Started constructing pathways")
    for pathway_id in range(num_pathways):
        genes = random.sample(Gene.extant_genes.values(), genes_per_pathway)
        Pathway(pathway_id, genes)
    new_print("Finished constructing pathways")
    new_print("Started constructing orgs")
    for org_id in range(num_orgs):
##        new_print("Started sampling pathways for org %d" % org_id)
        pathways = random.sample(Pathway.extant_pathways.values(), pathways_per_org)
##        new_print("Finished sampling pathways for org %d" % org_id)
        Organism(org_id, pathways)
    new_print("Finished constructing orgs")
    populations = []
    for pop in range(num_pops):
        orgs = random.sample(Organism.extant_organisms.values(), orgs_per_pop)
        populations += [Population(pop, orgs, pareto_dist_orgs)]
    return populations
        


def sample(population, sample_size):
##    new_print("Started sampling population %d" % population.id)
    gene_freqs = population.get_gene_frequencies()
    sample = []
    for pull in range(sample_size):
        rand = random.random()
        cumu = 0
        i = 0
        while cumu < rand:
            cumu += gene_freqs.values()[i]
            i += 1
        sample += [gene_freqs.keys()[i-1].id]
##    new_print("Finished sampling population %d" % population.id)
    return sorted(sample)

def genes_in_sample(sample):
    genes = []
    for gene in sample:
        if gene not in genes:
            genes += [gene]
    return genes
    

def zeros(cols, rows):
    matrix = []
    for each_row in range(rows):
        line = [0]*cols
        matrix.append(line)
    return matrix

def construct_network_matrix(pops, sample_size):
    dims = len(Gene.extant_genes)
    matrix = zeros(dims, dims)
    for pop in pops:
        sampled_genes = genes_in_sample(sample(pop, sample_size))
        for gene1 in sampled_genes:
            for gene2 in sampled_genes:
                if gene1 != gene2:
                    matrix[gene1][gene2] += 1
    return matrix

def avg_value(matrix):
    total = 0
    cells = len(matrix)*len(matrix[0])
    for line in matrix:
        total += sum(line)
    return (total * 1.0) /cells



# now the script:
pops = make_random_pops(num_genes = 1000, num_pathways = 50, num_orgs = 10,\
                       genes_per_pathway = 35, pathways_per_org = 50,\
                       orgs_per_pop = 5, num_pops = 10)

##print sample(pops[0], 110)
##print pops[0]
##for organism in pops[0].get_orgs():
##    print organism
##for pathway in Pathway.extant_pathways.values():
##    print pathway
new_print("Done constructing populations")

matrix = construct_network_matrix(pops, 100)
print (avg_value(matrix))
##for line in matrix:
##    print line