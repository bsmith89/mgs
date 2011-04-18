import sample_pops
import make_pops
import construct_matrix

reload(sample_pops)
reload(make_pops)
reload(construct_matrix)

TOT_GENES = 500
TOT_PATHS = 50
TOT_ORGS = 300
GENES_PER_PATH = 10
PATHS_PER_ORG = 25
ORGS_PER_POP = 200
POPS = 10
SAMPLE_SIZE = 500
RUNS = 1

pops = make_pops.make_testable_pops(num_genes = TOT_GENES,
                                    num_pathways = TOT_PATHS,
                                    num_orgs = TOT_ORGS,
                                    genes_per_pathway = GENES_PER_PATH,
                                    pathways_per_org = PATHS_PER_ORG,
                                    orgs_per_pop = ORGS_PER_POP,
                                    num_pops = POPS)

for run in range(RUNS):
##    print("Done constructing populations")
    matrix = sample_pops.construct_network_matrix(pops, SAMPLE_SIZE)
##    print("Done sampling populations")
    construct_matrix.save_connection_matrix("data//data%d.txt" % run, matrix)
##    for pop in pops:
##        print(make_pops.Population.extant_populations[pop.id])
##        print(make_pops.Organism.extant_organisms[pop.id])
##        print(make_pops.Pathway.extant_pathways[pop.id])