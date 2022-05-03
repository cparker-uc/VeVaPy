%dosed of fluox

% function f=fluox(t);
%   n=length(t);
%   for i=1:n
%    if t(i) < .5
%        f(i) = 1 - (.75).*t(i);    
%     elseif t(i) < 1.5
%       f(i) = .425.*(t(i)-1.5).^2 + .2; 
%       elseif t(i) < 2.5
%       f(i) = .5.*.425.*(t(i)-1.5).^2 + .2; 
%       
%       
%     elseif t(i) < 3
%       f(i) = .4125 + .5*(.75).*(t(i)-2.5);
%    else
%        f(i) = 1;
%        
%    end
%    
%   end
  
  function f=fluox(t);
  n=length(t);
  for i=1:n
   
       f(i) = 1;
       
   end
   
  end
  


% function f=fluox(t);
%    n=length(t);
%   g = .85; %percent decrease in available SERTs
%   for i=1:n
%    if t(i) < 1
%        f(i) = 1;    
%     elseif t(i) < 1.6
%       f(i) = 1 - g.*(t(i)-1)./.6; 
%       elseif t(i) < 2
%       f(i) = 1 - g; 
%    elseif   t(i) < 24
%        f(i) = 1 - g + g.*(t(i)-2)./22;
%    else f(i) = 1;    
%    end
%    
%   end  
  
  
  
%   function f=fluox(t);
%    n=length(t);
%   g = .95; %percent decrease in available SERTs
%   for i=1:n
%    if t(i) < 1
%        f(i) = 1;
%        else f(i) = 1 - exp(-(t(i)-1)./37).*(g).*(t(i)-1).^2./(.04 + (t(i)-1).^2);
%    %else f(i) = 1 - exp(-(t(i)-1)./37).*(g).*(t(i)-1)./(.2 + (t(i)-1));    
%    end
%    
%   end  
%   
%   
  
  
  
  
  
  
%   function f=fluox(t);
%   n=length(t);
%   g = .85; 
%   for i=1:n
%    if t(i) < 1
%        f(i) = 1;    
%     elseif t(i) < 2.5
%       f(i) = 1 - g.*2.*(t(i)-1)./(1 + 2.*(t(i) - 1)); 
%       
%    else
%        f(i) = 1 - g.*2.*(2.5-1)./(1 + 2.*(2.5 - 1));
%        
%    end
%    
%   end