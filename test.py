import sample_pops
import make_pops

reload(sample_pops)
reload(make_pops)


def edge_values(matrix):
    assert(len(matrix) == len(matrix[0]))
    assert(len(matrix) == len(matrix[-1]))
    values = []
    i = 1
    for line in matrix[:-1]:
##        print("Appending edge values from line %d" % i)
        values += line[i:]
        i += 1
    return values

def existing_edge_values(matrix):
    values = edge_values(matrix)
    while 0 in values:
        print("Removing non-existent edge")
        values.remove(0)
    return values

def edge_arrays(matrix):
    assert(len(matrix) == len(matrix[0]))
    assert(len(matrix) == len(matrix[-1]))
    values = []
    i = 1
    for line in matrix[:-1]:
        values += [line[i:]]
        i += 1
    return values

def avg_edge_value(matrix):
    edge_vals = edge_values(matrix)
    total = sum(edge_vals) + 0.0
    num_possible_edges = (len(matrix)**2 - len(matrix)) / 2
    print "num_possible_edges = %d" % num_possible_edges
    print "total edge strength = %d" % total
    return (total / num_possible_edges)
##    cells = len(matrix)* (len(matrix[0]) - 1) # -1 correction to remove the zeros down the diagonal
##    for line in matrix:
##        total += sum(line)
##    return (total * 1.0) /cells

def avg_existing_edge_value(matrix):
    vals = existing_edge_values(matrix)
    return sum(vals)/len(vals)

def save_edges_to_file(file_name, matrix):
    this_file = open(file_name, 'w')
    print("Getting edge values from matrix...")
    edge_arrs = edge_arrays(matrix)
    print("Finished getting edge values from matrix, now writing to file...")
    for arr in edge_arrs:
        for item in arr:
            this_file.write(str(item) + "\t")
        this_file.write("\n")
    this_file.close()

def save_edge_values_to_file(file_name, matrix):
    this_file = open(file_name, 'w')
    print("Getting edge values from matrix...")
    edge_arrs = edge_arrays(matrix)
    print("Finished getting edge values from matrix, now writing to file...")
    for arr in edge_arrs:
        for item in arr:
            this_file.write(str(item) + "\t")
    this_file.close()

# now the script:
pops = make_pops.make_random_pops(num_genes = 1000, num_pathways = 1500, num_orgs = 1000,\
                       genes_per_pathway = 35, pathways_per_org = 50,\
                       orgs_per_pop = 150, num_pops = 10)

##print sample(pops[0], 110)
##print pops[0]
##for organism in pops[0].get_orgs():
##    print organism
##for pathway in Pathway.extant_pathways.values():
##    print pathway
print("Done constructing populations")

matrix = sample_pops.construct_network_matrix(pops, 1000)
print("Done sampling populations")
save_edge_values_to_file("data.txt", matrix)
##print (avg_existing_edge_value(matrix))
##for line in matrix:
##    print line