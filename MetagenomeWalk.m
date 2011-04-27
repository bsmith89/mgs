%% Metagenome Simulation
% A simulation of a novel, graph based analysis technique for metagenomic
% data
%% The Data
% Visualizing some characteristics of the data

data_files = dir('data_samplesize/*.dat');
runs = length(data_files);
path = strcat('data_samplesize/', data_files(1).name);
example_data = importdata(path);
num_genes = length(example_data);
array3 = zeros(num_genes, num_genes, runs); % 3D array of all connectivity matrices
for k = 1:runs;
    path = strcat('data_samplesize/', data_files(k).name);
    array3(:,:,k) = importdata(path);
end

max_x = max(nonzeros(array3));

counts = zeros(max_x+1, runs);
for k = 1:runs;
    all_edge_strengths = reshape(array3(:,:,k), [1, numel(array3(:,:,k))]);
    counts(:,k) = hist(all_edge_strengths, 0:1:max_x);
end
distributions = counts ./ numel(array3(:,:,k));

figure;
plot(1:1:10, distributions(2:max_x+1,:));
% legend(data_files.name);
legend([{'100-1'}, {'100-2'}, {'500-1'}, {'500-2'}, {'1000-1'}, {'1000-2'}...
    {'1500-1'}, {'1500-2'}, {'2250-1'}, {'2250-2'}, {'3000-1'}, {'3000-2'}...
    {'9999-1'}, {'9999-2'}])
figure;
bar(distributions(1,:));
set(gca,'XTickLabel', [{'100-1'}, {'100-2'}, {'500-1'}, {'500-2'}, {'1000-1'}...
    {'1000-2'}, {'1500-1'}, {'1500-2'}, {'2250-1'}, {'2250-2'}, {'3000-1'}...
    {'3000-2'}, {'9999-1'}, {'9999-2'}])

%% Metagenome Walk
% Data collection regarding the results of a random walk on an imported
% connection matrix.
% Based on http://www.mathworks.com/matlabcentral/fileexchange/22003

data_files = dir('data_standardruns/*.dat');
runs = length(data_files);
path = strcat('data_standardruns/', data_files(1).name);
example_data = importdata(path);
num_genes = length(example_data);
array3 = zeros(num_genes, num_genes, runs); % 3D array of all connectivity matrices
for k = 1:runs;
    path = strcat('data_standardruns/', data_files(k).name);
    incoming_data = importdata(path);
    array3(:,:,k) = incoming_data;
end
walkers = 1000;
max_steps = 50 ;
random_walks_result = zeros(walkers, max_steps, runs);
for k = 1:runs;
    matrix = array3(:,:,k);
    random_walks_result(:,:,k) = RandomWalks(1, matrix, max_steps, walkers);
end

counts_at_each_step = ones(max_steps, 5);
for step = 1:max_steps;
    for each_observer = 1:5;
        counts_at_each_step(step,each_observer) = sum(sum(random_walks_result(:,step,:) == each_observer));
    end
end


mean(reshape(array3(:,:,k), [1, numel(array3(:,:,k))]))
std(reshape(array3(:,:,k), [1, numel(array3(:,:,k))]))
plot(counts_at_each_step);
legend([{'Gene Itself'}, {'Common Path.'}, {'Common Org.'}, {'Control 1'}, {'Control 2'}]);









