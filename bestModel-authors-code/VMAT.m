%vesicular monoamine transporter

% b = cDA
%c= vda

function a = VMAT(b,c,sc);

k = .2;%2;  %was 1 before Nov 3.
V = (1)*1230;  %1230 was 6300 before Nov 3  Vmax = 3500 in paper)

a = ((V.*b./(k + b))-(1).*c).*sc;  %40


% Km for uptake by vesicles = 123 or 252 nM (Slotkin77)

% Km for uptake by vesicles =  198 nM (Rau06)


