function out = RandomMove(X,S)

% Returns a node when given a node 1 degree from X on a graph connection matrix S

V = S(:,X); % A slice of the graph producing only the connections to/from node X
Index = find(V); % the indeces of the non-zero entries in V

V_norm = V(Index) / sum(V); % the normalized connection values
s = cumsum(V_norm); % the matrix of cumulative sums where s(0) = v_norm(0) and s(len(s)) = 1
r = rand; % a random value between 0 and 1
ind = find(s > r); % the values of s greater than r: basically truncates it at the first s>r
out = Index(ind(1));
end