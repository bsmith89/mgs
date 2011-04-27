function out = RandomWalks(X,S,n,N)
% Simulates N random walkers starting at node X on graph S with a maximum
% walk length of n
out = zeros(N,n);
i = 1;
while i <= N
    out(i,:) = WalkNSteps(X,S,n);
    i = i+1;
end
end

