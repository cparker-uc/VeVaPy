%catabolism of 5ht in the terminal

% b = cytosolic 5ht in the terminal



function a = TCcatab(b,sc)

k1 = 95;  %Gottowik93 and Fowler94
k2 = 4000;

a = (k2.*b./(k1 + b)).*sc;