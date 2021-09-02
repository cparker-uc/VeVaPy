% b = BH2
% c = NADPH
% d = BH4
% e = NADP

function a = VDRR(b,c,d,e,sc);

k1 = 100;   %Km for BH2 (BRENDA) (6-650)
k2 = 75;  %Km for NADPH (BRENDA, values 770,110,29) (schumber 70-80)
V1 = (25)*200.*sc; % Vmax forward
k3 = 10;  %Km for BH4 (BRENDA) (1.1 to 17)
k4 = 75;  %Km for NADP (BRENDA)(schumber 70-80)
V2 = 3.*sc; % Vmax backward

% forward direction from BH2 to BH4

a = V1.*b.*c./((k1 + b).*(k2 + c))  - V2.*d.*e./((k3 + d).*(k4 + e));


%regulatory function in vivo, above 0.03 mM, oxidation of Met146 and Met151
%leads to inactivation of the enzyme due to disruption of the NADH-binding
%site (BRENDA) 1.5.1.34