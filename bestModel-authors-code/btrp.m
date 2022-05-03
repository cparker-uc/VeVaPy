



function f=btrp(t);
n=length(t);
for i=1:n
  if t(i) < 1
      f(i) = (1)*96;    
  else 
    f(i) = (1)*96;
  end
end

% function f= btyr(t,sc);
% n=length(t);
% for i=1:n
%     f(i) = (1)*30;
% end
% 


%december 4, 2008
% function f=btrp(t);
% n=length(t);
% for i=1:n
%     f(i) = 100;
%   end
% end
%Fernstrom 72 and Fernstrom 95 say approx 100 micromolar in serum
%December 4, 2008

%   function f=btrp(t);
%  n=length(t);
%  for i=1:n
%   if t(i) < 7
%       f(i) = (.25)*97;    
%    elseif t(i) < 10
%      f(i) = (1.75)*97; 
%    elseif t(i) < 12
%      f(i) = (.25)*97;
%    elseif t(i) < 15
%       f(i) = (1.75)*97;
%     elseif t(i) < 18
%       f(i) = (.25)*97;
%     elseif t(i) < 21
%      f(i) = (3.25)*97;
%     elseif t(i) < 31
%      f(i) = (.25)*97; 
%    elseif t(i) < 34
%     f(i) = (1.75)*97;
%    elseif t(i) < 36
%      f(i) = (.25)*97;
%    elseif t(i) < 39
%      f(i) = (1.75)*97;
%    elseif t(i) < 42
%      f(i) = (.25)*97;
%    elseif t(i) < 45
%      f(i) = (3.25)*97;
%     elseif t(i) < 48
%      f(i) = (.25)*97; 
%   else f(i) = (.25)*97;
%   end
%  end
%  
%    function f=btrp(t);  %for May 19, new 5HT model, Results, Section 3.1
%  n=length(t);
%  for i=1:n
%   if t(i) < 7
%       f(i) = (.59)*97;    
%    elseif t(i) < 9
%      f(i) = (2)*97; 
%    elseif t(i) < 12
%      f(i) = (.59)*97;
%    elseif t(i) < 14
%       f(i) = (2)*97;
%     elseif t(i) < 18
%       f(i) = (.59)*97;
%     elseif t(i) < 21
%      f(i) = (2)*97;
%     elseif t(i) < 31
%      f(i) = (.59)*97; 
%    elseif t(i) < 33
%     f(i) = (2)*97;
%    elseif t(i) < 36
%      f(i) = (.59)*97;
%    elseif t(i) < 38
%      f(i) = (2)*97;
%    elseif t(i) < 42
%      f(i) = (.59)*97;
%    elseif t(i) < 45
%      f(i) = (2)*97;
%     elseif t(i) < 48
%      f(i) = (.59)*97; 
%   else f(i) = (.59)*97;
%   end
%  end


% function f=btyr(t);
% c=97;
% n=length(t);
% for i=1:n
%   if t(i) < 7*60
%       f(i) = (.25)*c;    
%   elseif t(i) < 10./sc
%     f(i) = (1.75)*c;
%   elseif t(i) < 12./sc
%     f(i) = (.25)*c;
%   elseif t(i) < 15./sc
%     f(i) = (1.75)*c;
%   elseif t(i) < 18./sc
%     f(i) = (.25)*c;
%   elseif t(i) < 21./sc
%     f(i) = (3.25)*c;
%    elseif t(i) < 31./sc
%     f(i) = (.25)*c; 
%   elseif t(i) < 34./sc
%     f(i) = (1.75)*c;
%   elseif t(i) < 36./sc
%     f(i) = (.25)*c;
%   elseif t(i) < 39./sc
%     f(i) = (1.75)*c;
%   elseif t(i) < 42./sc
%     f(i) = (.25)*c;
%   elseif t(i) < 45./sc
%     f(i) = (3.25)*c;
%    elseif t(i) < 48./sc
%     f(i) = (.25)*c; 
%     
%      elseif t(i) < 55./sc
%     f(i) = (.25)*c; 
%   elseif t(i) < 58./sc
%     f(i) = (1.75)*c;
%   elseif t(i) < 60./sc
%     f(i) = (.25)*c;
%   elseif t(i) < 63./sc
%     f(i) = (1.75)*c;
%   elseif t(i) < 66./sc
%     f(i) = (.25)*c;
%   elseif t(i) < 69./sc
%     f(i) = (3.25)*c;
%    elseif t(i) < 72./sc
%     f(i) = (.25)*c; 
%   else
%     f(i) = c;
%   end
% 
%    end
% 

