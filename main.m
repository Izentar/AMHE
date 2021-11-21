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

figure;
xlabel('Iteration');
ylabel('Best Cost');
grid on;
    
for i=1:20
    BestCost = cmaes(0);
    semilogy(BestCost, 'LineWidth', 1, 'Color', [0 (0.5 + rand./2) 0 0.5]);
    hold on
end
for i=1:20
    BestCost = cmaes(20);
    semilogy(BestCost, 'LineWidth', 1, 'Color', [(0.5 + rand./2) 0 0 0.5]);
    hold on
end
hold off;
