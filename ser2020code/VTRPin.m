%tryptophan transporter from blood to cytosol

% b = btyr

function a = VTRPin(b,sc);

k1 = 700.*sc;   % Vmax 
k2 = 330;  % Kilberg p. 169  (effective Km because of other AA)
            

a = k1.*b./(k2 + b); 


%Partridge75 says Km = 190 muM (with respect to total trp)
%Smith87   says Km = 15 muM  (with respect to free trp)   
%(both in BBB folder)

% kilber flux in to brain is 157 muM/hr 2.61/min  page 169


% kilber tyr flux in to brain is  muM/hr 4.14/min  page 169




