 % in SER3 directory

function f = runser


close all;
clear all;

% y(1) = bh2
% y(2) = bh4
% y(3) = trp
% y(4) = htp
% y(5) = cht
% y(6) = vht
% y(7) = eht
% y(8) = hia
% y(9) = trppool
% y(10) = dummy
% y(11) = gstar
% y(12) = tstar
% y(13) = bound


NADP = (1)*26;  
NADPH = 330;
%K1 = .170;
%V1 = .780;
a15 = 1;
a16 = 1;
a19 = 2;
a20 = 1;
a21 = 40;
a22 = 1;
k11 = 4.32;  %bound auto produce Gha*
k12 = 1.296;  %Tha* reverses Gha* to Gha.
k13 = 14.4;   %Gha* produces THA*
k14 =  25.92;  %decay of Tha*
k15  =  432;  %eha binds to auto
k16 =  1440;  %eha dissociates from auto
gh0 = 1; %total g-protein
th0 =  60;  %total T regulary protein
bh0 =  10; %total autoreceptors
 eha = (1)*1.39; 
%eha(t,HA)
%inhibHA(y(15))


sc = 1;   %scaling factor for time: sc=1 for hours

time = 300;

% time2 = xlsread('Dtime.xls');
% %data = xlsread('EVcont01.xls');
% 
% data2 = xlsread('DHAavgcondrug5HTavgcondrug30s.xls');
% HAavgcon = data2(:,2);
% HAdrug = data2(:,4);
% X5HTavgcon = data2(:,6);
% X5HTdrug = data2(:,9);
% HA = HAspline(time2,HAavgcon);
% 


%[T,Y] = ode15s(@msc, [0 time], [0.2291 0.7709 19.6006 3.7903 2.0725 26.5214 0.0683 8.5739 141.4164 0.0000 0.9355 1.1603 1.0943 2.0892],[],sc,K1,V1); %SS for EVO3
%[T,Y] = ode15s(@msc, [0 time], [0.0995 0.9005 20.1651 1.6110 0.0376 67.4267 0.0601 1.5846 113.4289 0.0000 0.8639 1.0068 0.9757 0.0000 0.6947 12.6860 2.9428],[],sc);
[T,Y] = ode15s(@msc, [0 time], [0.09 1 20 1.50 0.01 67.0 0.05 1.40 110 0 0.75 1.10 0.9 0 0.5 13.0 2.60],[],sc);
               
%formatcompact
bh2 = Y(length(T),1);
bh4 = Y(length(T),2);
trp  = Y(length(T),3);
htp = Y(length(T),4);
cht = Y(length(T),5);
vht = Y(length(T),6);
eht = Y(length(T),7);
hia = Y(length(T),8);
pool = Y(length(T),9);
gstar = Y(length(T),11);
tstar = Y(length(T),12);
bound = Y(length(T),13);
ght = Y(length(T),14);
ghastar = Y(length(T),15);
thastar = Y(length(T),16);
habound = Y(length(T),17);
trpin = VTRPin(btrp(length(T)),sc);
vtph = inhibsyn(gstar,1).*VTPH(trp,bh4,sc);
vdrr = VDRR(bh2,NADPH,bh4,NADP,sc);
vaadc = VAADC(htp,sc);
vmatnet = VMAT(cht,vht,sc);
vsert = VSERT(eht,sc);
vgcatab = TCcatab(ght,sc);
vccatab = TCcatab(cht,sc);
fromglia = TCcatab(ght,sc) + a16.*ght.*sc;
vtrpout = a19.*(trp).*sc;
vpoolout = a20.*pool.*sc;
release = a22.*inhib(gstar,1).*inhibHA(ghastar).*fire(length(T)).*vht.*sc;
vrem = (a21).*Y(length(T),7).*sc; 
vu2 = (1)*H1(1000.*eht).*VUP2(eht,sc);
cleak = a15.*cht.*sc;
gleak = a16.*ght.*sc;


%set(figure, 'Position',[1000 500 1120 600])

figure
 subplot(3,2,1)
plot(T, 10.*Y(:,4),'b',T, 10.*Y(:,5),'m',T, Y(:,6),'c','LineWidth',3);
leg1=legend('10htp','10cht','vht');
set(leg1,'FontSize',14);

subplot(3,2,2)
plot(T,Y(:,11),'g',T,Y(:,12),'k',T,Y(:,13),'r','LineWidth',3); 
leg2 =legend('G*5HT','T*5HT','bound5HT');
set(leg2,'FontSize',14);

subplot(3,2,3)
t=0:.1:30;
plot(t,eha,'r','LineWidth',3);  %eha(t,HA)
leg1=legend('EHA');
set(leg1,'FontSize',14);

subplot(3,2,4)
plot(T, 1000.*Y(:,7),'g',T, Y(:,6),'c','LineWidth',3);
leg1=legend('eht','vht');
set(leg1,'FontSize',14);
ylim([40 100]); 

subplot(3,2,5)
plot(T,10.*Y(:,15),'g',T,Y(:,16),'k',T,Y(:,17),'r','LineWidth',3); 
leg2 =legend('10*G*HA','T*HA','boundHA');
set(leg2,'FontSize',14);

% subplot(3,2,6)
% plot(time2,46.0 + X5HTavgcon,'k',T,1000.*Y(:,7),'g','LineWidth',3); 
% leg2 =legend('ehtdata','ehtmodel');
% set(leg2,'FontSize',14);



% figure
%plot(time2,60.2 + data, 'b',T,1000.*Y(:,7),'r','Linewidth',3);
%leg3 = legend('5htdata','model');
%set(leg3,'FontSize',14);

%figure
%t = 0:.1:30;
%plot(t,eha(t,HA),'g','Linewidth',3);
 


subplot(2,2,1)
plot(T, 10*Y(:,4),'b',T, 10*Y(:,5),'m',T, Y(:,6),'c','LineWidth',3);
leg1=legend('htp','cht','vht');
set(leg1,'FontSize',14);
 
subplot(2,2,2)
plot(T,Y(:,11),'g',T,Y(:,12),'k',T,Y(:,13),'r','LineWidth',3); 
leg2 =legend('gstar','tstar','bound');
set(leg2,'FontSize',14);
 
subplot(2,2,3)
plot(T, Y(:,3),'k', T, Y(:,9),'b','LineWidth',3);
leg1=legend('tryp','tryppool');
set(leg1,'FontSize',14);
 
subplot(2,2,4)
plot(T, 1000.*Y(:,7),'g','LineWidth',3);
leg1=legend('eht');
set(leg1,'FontSize',14);


%  figure
%  plot(time2,60.2 + data, 'b',T,1000.*Y(:,7),'r','Linewidth',3);
%  leg3 = legend('5htdata','model');
%  set(leg3,'FontSize',14);





% subplot(3,1,1)
%   plot(T, btrp(T),'r', 'Linewidth',4)
%    legend('blood tryptophan')
% 
%    subplot(3,1,2)
%    plot(T,inhibsyn(y(11),1).*VTPH(Y(:,3),Y(:,2),sc) ,'k',T, Y(:,8), 'b', 'Linewidth',4)
%    legend('VTPH', '5-HIAA')
% 
%    subplot(3,1,3)
%    plot(T, 10*Y(:,5), 'y',T, Y(:,6), 'm',T,1000*10*Y(:,7), 'g','Linewidth',4) 
%     legend('10*c5HT','v5HT', '1000*e5HT')
%     

M=zeros(31,1);
M(1) = bh2;
M(2) = bh4;
M(3) = trp;
M(4) = htp; 
M(5) = cht;
M(6) = vht;
M(7) = eht;
M(8) = hia;
M(9)= pool;
M(10)= vtph ;
M(11)= vdrr;
M(12)= vaadc;
M(13)= vmatnet;
M(14)= vrem;
M(15)= vsert;
M(16)= vccatab;
M(17) = pool;
M(18) = vtrpout;
M(19) = vpoolout;
M(20) = release;
M(21) = fromglia;
M(22) = vccatab;
M(23)= gstar;
M(24)= tstar;
M(25) = bound;
M(26) = vu2;
M(27) = cleak;
M(28) = ght;
M(29) = gleak;
M(30) = trpin;
M(31) = vgcatab;

% DATA to screen
t=datestr(now); % today's date
fid=fopen('out.txt','w');  %this opens a file and then the vector components are put in  it.
fprintf(fid, '%s \n', t);
fprintf(fid,'\n');

fprintf(fid, 'concentrations \t\t\t velocities \t\t\t glia velocities \n');
fprintf(fid,'\n');
fprintf(fid,'bh2 = %4.2f \t\t\t\t trpin = %4.2f \t\t\t vup2 = %4.2f \n',M(1), M(30), M(26) );
fprintf(fid,'bh4 = %4.2f \t\t\t\t vtph = %4.4f \t\t\t vgcatab = %4.2f \n',M(2),M(10),M(31));
fprintf(fid,'trp = %4.2f \t\t\t\t vdrr = %4.4f \t\t\t gleak = %4.2f \n',M(3),M(11),M(29));
fprintf(fid,'htp = %4.2f \t\t\t\t vaadc = %4.4f \n',M(4),M(12));
fprintf(fid,'cht = %4.2f \t\t\t\t vmatnet = %4.4f \n',M(5),M(13));
fprintf(fid,'vht = %4.2f \t\t\t release = %4.4f \n',M(6),M(20));
fprintf(fid,'eht = %4.6f \t\t\t vsert = %4.4f \n',M(7),M(15));
fprintf(fid,'hia = %4.2f \t\t\t\t \t\t\t\t \t\t fromglia = %4.2f \n',M(8),M(21));
fprintf(fid,'pool = %4.2f \t\t\t vccatab = %4.4f \n',M(17),M(22));
fprintf(fid, 'gstar =%4.4f \t\t\t vrem = %4.4f \n',M(23),M(14))
fprintf(fid, 'tstar =%4.4f \t\t\t vpoolout = %4.2f \n' ,M(24),M(19));
fprintf(fid, 'bound =%4.4f \t\t\t vtrpout = %4.2f  \n' ,M(25), M(18));
fprintf(fid, 'g5ht= %4.4f \t\t\t cleak = %4.2f \n' ,M(28),M(27));
fprintf(fid,'\n');
fprintf(fid,'\n');
fprintf(fid,'endconcentrations = [%4.4f %4.4f %4.4f %4.4f %4.4f %4.4f %4.4f %4.4f %4.4f %4.4f %4.4f %4.4f %4.4f %4.4f] \n',M(1),M(2),M(3),M(4),M(5),M(6),M(7),M(8),M(9),0,M(23),M(24),M(25),M(28));
fclose(fid);

open out.txt; 

EC = [M(1),M(2),M(3),M(4),M(5),M(6),M(7),M(8),M(9),0,M(23),M(24),M(25),M(28)];


FigHandle=figure('Position',[100 100 3318/2 2683/2]); % position x y and size xx yy [x y xx yy]
%figure(2)
diagram=imread('SerotoninGlia2019d.jpg');
image(diagram)
set(gca,'xtick',[])
set(gca,'ytick',[])
hold on
IntCon=[.10 .90 20.2 1.61 .038 67.5 60.2 1.58 113 0 .87 1.01 .98 0 .69  12.7 2.94]; %male (Jan24)
fntsz=20;
text(1130,1050,sprintf('%1.2f',EC(4)),'FontSize',fntsz,'BackgroundColor',[1 1 1]) 
text(130,1050,sprintf('%2.1f',96),'FontSize',fntsz,'BackgroundColor',[1 1 1]) 
text(730,1050,sprintf('%2.1f',EC(3)),'FontSize',fntsz,'BackgroundColor',[1 1 1])
text(1310,610,sprintf('%2.1f',EC(1)),'FontSize',fntsz,'BackgroundColor',[1 1 1])
text(860,610,sprintf('%2.1f',EC(2)),'FontSize',fntsz,'BackgroundColor',[1 1 1])
text(390,1400,sprintf('%3.0f',EC(9)),'FontSize',fntsz,'BackgroundColor',[1 1 1])
text(850,1450,sprintf('%1.2f',EC(5)),'FontSize',fntsz,'BackgroundColor',[1 1 1])
text(1120,2080,sprintf('%2.1f',EC(6)),'FontSize',fntsz,'BackgroundColor',[1 1 1])
text(860,2500,sprintf('%2.1f',60.2),'FontSize',fntsz,'BackgroundColor',[1 1 1])
text(2550,2450,sprintf('%1.2f',1.39),'FontSize',fntsz,'BackgroundColor',[1 1 1])
text(2670,1200,sprintf('%1.1f',EC(14)),'FontSize',fntsz,'BackgroundColor',[1 1 1])
text(1680,1000,sprintf('%1.2f',EC(8)),'FontSize',fntsz,'BackgroundColor',[1 1 1])

%VELOCITIES
text(1000,900,sprintf('%1.1f',4.0),'FontSize',fntsz,'BackgroundColor',[1 1 1],'Color',[1 0 0])
text(600,910,sprintf('%3.0f',158),'FontSize',fntsz,'BackgroundColor',[1 1 1],'Color',[1 0 0])
text(1000,1130,sprintf('%1.1f',4.0),'FontSize',fntsz,'BackgroundColor',[1 1 1],'Color',[1 0 0])
text(1000,1340,sprintf('%1.1f',4.0),'FontSize',fntsz,'BackgroundColor',[1 1 1],'Color',[1 0 0])
text(1000,1610,sprintf('%3.1f',127.6),'FontSize',fntsz,'BackgroundColor',[1 1 1],'Color',[1 0 0])
text(1000,2330,sprintf('%3.1f',127.6),'FontSize',fntsz,'BackgroundColor',[1 1 1],'Color',[1 0 0])
text(1320,1650,sprintf('%3.0f',125),'FontSize',fntsz,'BackgroundColor',[1 1 1],'Color',[1 0 0])
text(1220,1420,sprintf('%1.1f',1.6),'FontSize',fntsz,'BackgroundColor',[1 1 1],'Color',[1 0 0])
text(1070,2620,sprintf('%1.1f',2.4),'FontSize',fntsz,'BackgroundColor',[1 1 1],'Color',[1 0 0])



% DATA to files

fid=fopen('gTime.txt','w');
fprintf(fid, '%6.6f\n',T);
 fclose(fid);

fid=fopen('gbh2.txt','w');
 fprintf(fid, '%6.6f\n',Y(:,1));
 fclose(fid);
 
 fid=fopen('gbh4.txt','w');
 fprintf(fid, '%6.6f\n',Y(:,2));
 fclose(fid);
 
 fid=fopen('gtrp.txt','w');
 fprintf(fid, '%6.6f\n',Y(:,3));
 fclose(fid);
 
 fid=fopen('ghtp.txt','w');
 fprintf(fid, '%6.6f\n',Y(:,4));
 fclose(fid);
 
 fid=fopen('gcht.txt','w');
 fprintf(fid, '%6.6f\n',Y(:,5));
 fclose(fid);
 
 fid=fopen('gvht.txt','w');
 fprintf(fid, '%6.6f\n',Y(:,6));
 fclose(fid);
 
 fid=fopen('geht.txt','w');
 fprintf(fid, '%6.6f\n',Y(:,7));
 fclose(fid);
 
 fid=fopen('ghia.txt','w');
 fprintf(fid, '%6.6f\n',Y(:,8));
 fclose(fid);
 
 fid=fopen('gvtph.txt','w');
 fprintf(fid, '%6.6f\n',inhibsyn(Y(:,11),1).*VTPH(Y(:,3),Y(:,2),sc));
 fclose(fid);




function dy=msc(t,y,sc)

dy=zeros(17,1);

NADP = (1)*26;  
NADPH = 330;

a9 = (1)*20;                         
a10 = (1)*200;                     
a11 = (1)*30;                        
a12 =(1)*200;                     
a13 = 36000;                          %432     (HA program)
a14 = 20000;                         %1440    (HA program)
g0 = 10;                             % 1      (HA program)
t0 = 10;                            % 60     (HA program)
b0 = 10; %10      (HA program)
a15 = 1; %diffusion from cytosol to extracell.
a16 = 1;  %diffusion from glia to extracellular space
a17 = 1;  %catabolism of hiaa
a18 = .001;   %UP2 multiplier
a19 = 2;  %removal of trp
a20 = 1;   %removal of pool
a21 = 40; % eht removal rate  was 10
a22 = 1;  %release per action potential
k11 = 4.32;  %bound auto produce Gha*
k12 = 1.296;  %Tha* reverses Gha* to Gha.
k13 = 14.4;   %Gha* produces THA*
k14 =  25.92;  %decay of Tha*
k15  =  432;  %eha binds to auto
k16 =  1440;  %eha dissociates from auto
gh0 = 1; %total g-protein
th0 =  60;  %total T regulary protein
bh0 =  10; %total autoreceptors
 eha = (1)*1.39;
 b = 1;
%eha(t,HA)
%inhibHA(y(15))


dy(1) = inhibsyn(y(11),1).*VTPH(y(3),y(2),sc) - VDRR(y(1),NADPH,y(2),NADP,sc); 
dy(2) = VDRR(y(1),NADPH,y(2),NADP,sc) - inhibsyn(y(11),1).*VTPH(y(3),y(2),sc);
dy(3) = VTRPin(btrp(t),sc) - inhibsyn(y(11),1).*VTPH(y(3),y(2),sc) - VPOOL(y(3),y(9),sc) - a19*y(3).*sc;
dy(4) = inhibsyn(y(11),1).*VTPH(y(3),y(2),sc) - VAADC(y(4),sc);
dy(5) = VAADC(y(4),sc) - VMAT(y(5),y(6),sc) + VSERT(y(7),sc) - TCcatab(y(5),sc) -a15.*y(5).*sc;
dy(6) = VMAT(y(5),y(6),sc) - a22.*inhib(y(11),1).*inhibHA(y(15)).*fire(t).*y(6).*sc; 
dy(7) = a22.*inhib(y(11),1).*inhibHA(y(15)).*fire(t).*y(6).*sc - VSERT(y(7),sc) - a18*H1(1000.*y(7)).*VUP2(y(7),sc) - a21.*y(7).*sc - (1).*a13.*y(7).*(b0 - y(13)).*sc + (1).*a14.*y(13).*sc + a15.*y(5).*sc + a16.*y(14).*sc; 
dy(8) = TCcatab(y(5),sc) +  TCcatab(y(14),sc) - a17.*y(8).*sc;
dy(9) = VPOOL(y(3),y(9),sc) - a20.*y(9).*sc;
dy(10) = sin(t);
dy(11)  = b*(a9.*y(13).^2.*(g0 - y(11)) - a10.*y(12).*y(11)).*sc;
dy(12) = b*(a11.*y(11).^2.*(t0 - y(12))  - a12.*y(12)).*sc;
dy(13) = b*(a13.*y(7).*(b0 - y(13)).*sc  - a14.*y(13)).*sc;
dy(14) = a18*H1(1000.*y(7)).*VUP2(y(7),sc)  - TCcatab(y(14),sc) -a16.*y(14).*sc;
dy(15) = 1.*(k11.*y(17).^2.*(gh0 - y(15)) - k12.*y(16).*y(15)).*sc;
dy(16) = 1.*(k13.*y(15).^2.*(th0 - y(16))  - k14.*y(16)).*sc;
dy(17) = 1.*(k15.*eha.*(bh0 - y(17))  - k16.*y(17)).*sc;

% y(1) = bh2
% y(2) = bh4
% y(3) = trp
% y(4) = htp
% y(5) = ht
% y(6) = vht
% y(7) = eht
% y(8) = hia
% y(9) = trppool
% y(10) = dummy
% y(11) = gstar
% y(12) = tstar
% y(13) = bound
% y(14) =  glialht
%  y(15) =  Gha*
%  y(16) = Tha*
%  y(17)  =  bha



