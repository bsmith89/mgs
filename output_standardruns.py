import sample_pops
import make_pops
import construct_matrix

reload(sample_pops)
reload(make_pops)
reload(construct_matrix)

TOT_GENES = 1500
TOT_PATHS = 250
TOT_ORGS = 300
GENES_PER_PATH = 15
PATHS_PER_ORG = 50
ORGS_PER_POP = 200
POPS = 10
SAMPLE_SIZE = int(1.5*TOT_GENES)
RUNS = 10

for run in [0]:
    print run
    pops = make_pops.make_testable_pops(num_genes = TOT_GENES,
                                        num_pathways = TOT_PATHS,
                                        num_orgs = TOT_ORGS,
                                        genes_per_pathway = GENES_PER_PATH,
                                        pathways_per_org = PATHS_PER_ORG,
                                        orgs_per_pop = ORGS_PER_POP,
                                        num_pops = POPS)
    matrix = sample_pops.construct_network_matrix(pops, SAMPLE_SIZE)
    construct_matrix.save_connection_matrix("data_standardruns//data%s.dat" % \
                                            str(run).rjust(2,'0'), matrix)




##    print(make_pops.Pathway.extant_pathways.values()[0])
##    for pop in pops:
##        print(make_pops.Population.extant_populations[pop.id])
##        print(make_pops.Organism.extant_organisms[pop.id])
##        print(make_pops.Pathway.extant_pathways[pop.id])
