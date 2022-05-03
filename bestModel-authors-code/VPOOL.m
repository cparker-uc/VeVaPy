



% b = trp
% c = pool

function a = VPOOL(b,c,sc);

k1 = 9; %to pool
k2 = .6; %from pool
 
a = (k1.*b - k2.*c).*sc;

