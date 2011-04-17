import make_pops
import random

def sample(population, sample_size):
##    print("Started sampling population %d" % population.id)
##    print("Getting gene frequencies...")
    gene_freqs = population.get_gene_frequencies()
##    print("Done getting gene frequencies...")
    sample = []
##    print("Started randomly selecting genes from the population...")
    for pull in range(sample_size):
        rand = random.random()
        cumu = 0
        i = 0
        while cumu < rand:
            cumu += gene_freqs.values()[i]
            i += 1
        sample += [gene_freqs.keys()[i-1].id]
##        print("Added gene %d to the sample" % sample[-1])
    print("Finished sampling population %d" % population.id)
##    print ("Sorting sample...")
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
    dims = len(make_pops.Gene.extant_genes)
##    print("Initializing a %d by %d matrix" % (dims, dims))
    matrix = zeros(dims, dims)
##    print("Started adding edges from %d populations" % (len(pops)))
    for pop in pops:
##        print("Started adding edges from pop %d" % pop.id)
        sampled_genes = genes_in_sample(sample(pop, sample_size))
        for gene1 in sampled_genes:
            for gene2 in sampled_genes:
                if gene1 != gene2:
                    matrix[gene1][gene2] += 1
##                    print("Strengthened and edge between nodes %d and %d" % (gene1, gene2))
##        print("Finished adding edges from pop %d" % pop.id)
    return matrix