
function a=  inhibsyn(b,c);
% if nargin == 2
%     gstar = .8639;
% end
%b = gstar;
%c = CCC;

% a = 1 - .34*(b - .6944)./(.03 + (b - .6944)) ;  %the multiplier was .9 in genesis  .34

%a = .7.*( 1 - 3.5.*(b - .6945));   %.4454 if 3.5 is changed to 20  befopre July 16, 2017

%a = 1.89 - (0).*(b-.8644) ;   %         1.89 - (s)*(b)
 a = 1 - (c).*(2.5)*(b - .8639);  %2.5
 
  end 