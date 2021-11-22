%
% Copyright (c) 2015, Yarpiz (www.yarpiz.com)
% All rights reserved. Please read the "license.txt" for license terms.
%
% Project Code: YPEA108
% Project Title: Covariance Matrix Adaptation Evolution Strategy (CMA-ES)
% Publisher: Yarpiz (www.yarpiz.com)
% 
% Developer: S. Mostapha Kalami Heris (Member of Yarpiz Team)
% 
% Contact Info: sm.kalami@gmail.com, info@yarpiz.com
%

clc;
clear;
close all;

figure;
xlabel('Iteration');
ylabel('Best Cost');
grid on;

numReps1 = 30;
numReps2 = 30;
iterations = 300

BestCosts = zeros(iterations,numReps1);
BestCosts2 = zeros(iterations,numReps2);
    
for i=1:numReps1
    BestCost = cmaes(0);
    BestCosts(:,i) = BestCost;
    semilogy(BestCost, 'LineWidth', 0.5, 'Color', [0 (0.5 + (i./numReps1)./2) 0 0.05]);
    hold on
end

semilogy(mean(BestCosts, [2 numReps1]), 'LineWidth', 2, 'Color', [0 1 0 1]);
hold on

for i=1:numReps2
    BestCost = cmaes(2);
    BestCosts2(:,i) = BestCost;
    semilogy(BestCost, 'LineWidth', 0.5, 'Color', [(0.5 + (i./numReps2)./2) 0 0 0.05]);
    hold on
end

semilogy(mean(BestCosts2, [2 numReps2]), 'LineWidth', 2, 'Color', [1 0 0 1]);

hold off;
