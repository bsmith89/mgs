%% Metagenome Walk
% Data collection regarding the results of a random walk on an imported
% connection matrix.
% Based on http://www.mathworks.com/matlabcentral/fileexchange/22003

connection_matrix = importdata('data.txt');
output = RandomWalk(0, connection_matrix, 10);