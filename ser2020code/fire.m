
function f=fire(t);

f = 1;

end

% function f = fire(t); % NEW!!
% n=length(t);
% r= 17;
% for i=1:n
% if t(i) < 5
%       f(i) = 1;
%       elseif t(i) < 7
%         f(i) = 1 + r*(1- exp(-t(i)));        
%     else f(i) = 1 + r*(exp(-(t(i)-2)) - exp(-t(i)));
%   end
%  
% end

% function f=fire(t); %This used Friday, April 26 on EV01
% n=length(t);
% r= 1.05;
% for i=1:n
% if t(i) < 5
%       f(i) = 2;
%       elseif t(i) < 7
%         f(i) = 2 + (1)*r*45*(t(i)-5); 
%     elseif t(i) < 9
%         f(i) = (2 + r*45*(2))- (r*45/(1))*(t(i)-7);
%     else f(i) = 2;
%   end
%  
% end


% function f=fire(t); 
% n=length(t);
% r= .5;
% for i=1:n
% if t(i) < 5
%       f(i) = 1;
%       elseif t(i) < 6
%         f(i) = 1 + (1)*r*45*(t(i)-5); 
%     elseif t(i) < 8
%         f(i) = (1 + r*45*(1))- (r*45/2)*(t(i)-6);
%     else f(i) = 1;
% end
% end


% function f=fire(t); %This used Sunday, April 28
% n=length(t);
% r= .5 ;
% for i=1:n
% if t(i) < 5
%       f(i) = 2;
%       elseif t(i) < 8
%         f(i) = 2 + (1)*r*45*(t(i)-5); 
%     elseif t(i) < 11
%         f(i) = (2 + r*45*(3))- (r*45/(1))*(t(i)-8);
%     else f(i) = 2;
%   end
%  
% end