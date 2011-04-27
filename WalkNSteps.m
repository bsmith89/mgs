function out = WalkNSteps(X,S,n)


% Returns a path when given a node Nth degree from X on a graph connection
% matrix S

out = zeros(1,n);
for i = 1:n;
    X = RandomMove(X,S);
    out(i) = X;
end