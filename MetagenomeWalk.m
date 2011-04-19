%% Metagenome Walk
% Data collection regarding the results of a random walk on an imported
% connection matrix.
% Based on http://www.mathworks.com/matlabcentral/fileexchange/22003

data_files = dir('./data/*.dat');
runs = length(data_files);
example_path = strcat('./data/', data_files(1).name);
example_data = importdata(example_path);
num_genes = length(example_data);
array3 = zeros(num_genes, num_genes, runs); % 3D array of all connectivity matrices
for k = 1:runs;
    path = strcat('./data/', data_files(k).name);
    array3(:,:,k) = importdata(path);
end

max_x = max(nonzeros(array3));

distributions = zeros(max_x+1, runs);
for k = 1:runs;
    all_edge_strengths = reshape(array3(:,:,k), [1, numel(array3(:,:,k))]);
    distributions(:,k) = hist(all_edge_strengths, 0:1:max_x) / length(all_edge_strengths);
end
plot(distributions(2:max_x,:,:));