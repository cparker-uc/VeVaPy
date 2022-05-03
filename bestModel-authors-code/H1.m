
function f=H1(a)
if a < 60.5
      f = 0;
elseif  a < 80.5
     f = (.05)*(a-60.5);   
else
    f = 1;

end