%SERTS

% b = e5ht

function a = VSERT(b,sc);

k = (1).*.060;  %feldman says (page 355) that k = .05-.1 for synptosomes
          % and .1 - .5 muM for slices.

%a = (1)*(1).*(4.7).*((70).*b./(k + b)).*sc;  % (in paper Vmax = 8000)

a = (1)*(250).*b./(k + b).*sc;  % (250)

% Km is from Bunin98, see also Daws05