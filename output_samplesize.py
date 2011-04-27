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
RUNS = 2

for run in [1]:
    pops = make_pops.make_testable_pops(num_genes = TOT_GENES,
                                        num_pathways = TOT_PATHS,
                                        num_orgs = TOT_ORGS,
                                        genes_per_pathway = GENES_PER_PATH,
                                        pathways_per_org = PATHS_PER_ORG,
                                        orgs_per_pop = ORGS_PER_POP,
                                        num_pops = POPS)
    for sample_size in [100, 500, 1000, 1500, 2250, 3000, 9999]:
        print sample_size
        matrix = sample_pops.construct_network_matrix(pops, sample_size)
        construct_matrix.save_connection_matrix("data_samplesize//data%s_%s.dat"\
                                                % (str(sample_size).rjust(4,'0'),
                                                   str(run).rjust(2, '0')),
                                                matrix)


##  print(make_pops.Pathway.extant_pathways.values()[0])
##    for pop in pops:
##        print(make_pops.Population.extant_populations[pop.id])
##        print(make_pops.Organism.extant_organisms[pop.id])
##        print(make_pops.Pathway.extant_pathways[pop.id])
