%vesicular monoamine transporter

% b = eDA

function a = VSAT(b,sc);

k = .2;
f = 1;  %f = fraction of SNC cells surviving

a = (1).*(4).*(2).*((1000).*(f).*b./(k + (f).*b)).*sc;

%a = (1).*(4000).*b.*sc;

% Jones 95 and Schmitz 03 for Km (.2 - 2 muM) and  Vmax (4-6 or 3.8)