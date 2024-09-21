
cruc_r = 0.06;    //crucible radius
cruc_ri = 0.025;  //  radius inside
cruc_h = 0.03;    //  height
cruc_hi = 0.015;  //  height inside
cruc_z = 0.0;     //  bottom position
cruc_cl = 0.003; 

melt_h = 0.01;    //melt height
melt_cl = 0.001;

crys_r = 0.005;   //crystal radius
crys_h = 0.1;     //  height
crys_hc = 0.02;   //  cone height
crys_rs = 0.001;  //  seed radius
crys_cl = 0.002;

mag_r = 0.09;     //magnet radius
mag_ri = 0.02;    //  radius inside
mag_h = 0.005;     //  height
mag_z = -0.025;    //  bottom position
mag_cl = 0.003;

plate_r = 0.09;   //hot plate radius
plate_h = 0.01;  //  height
plate_cl = 0.003;

wall_r = 0.3;     //wall radius
wall_h = 0.5;     //wall height
wall_z = -0.12;    //wall bottom position
wall_cl = 0.02;

melt_ztop = cruc_z + cruc_h - cruc_hi + melt_h;

n = 100; //crucible
Point(n+1) = { 0, cruc_z, 0, cruc_cl };
Point(n+2) = { cruc_r, cruc_z, 0, cruc_cl };
Point(n+3) = { cruc_r, cruc_z+cruc_h, 0, cruc_cl };
Point(n+4) = { cruc_ri, cruc_z+cruc_h, 0, cruc_cl };
Point(n+5) = { cruc_ri, melt_ztop, 0, melt_cl };
Point(n+6) = { cruc_ri, cruc_z+cruc_h-cruc_hi, 0, melt_cl };
Point(n+7) = { 0, cruc_z+cruc_h-cruc_hi, 0, melt_cl };

Line(n+1) = {n+1, n+2};  Line(n+2) = {n+2, n+3};  Line(n+3) = {n+3, n+4};  Line(n+4) = {n+4, n+5};
Line(n+5) = {n+5, n+6};  Line(n+6) = {n+6, n+7};  Line(n+7) = {n+7, n+1};
Line Loop(n+10) = {(n+1):(n+7)};
Plane Surface(n+20) = {n+10};


n = 200; //melt
Point(n+1) = { crys_r, melt_ztop, 0, melt_cl };
Point(n+2) = { 0, melt_ztop, 0, melt_cl };

Line(n+1) = { 105, n+1 };
Line(n+2) = { n+1, n+2 };
Line(n+3) = { n+2, 107 };
Line Loop(n+10) = {-106, -105, n+1, n+2, n+3 };
Plane Surface(n+20) = {n+10};


n = 300; //crystal
Point(n+1) = { crys_r, melt_ztop + crys_h, 0, crys_cl };
Point(n+2) = { crys_rs, melt_ztop + crys_h + crys_hc, 0, crys_cl };
Point(n+3) = { 0, melt_ztop + crys_h + crys_hc, 0, crys_cl };

Line(n+1) = {201, n+1};  Line(n+2) = {n+1, n+2};  Line(n+3) = {n+2, n+3};  Line(n+4) = {n+3, 202};
Line Loop(n+10) = {-202, (n+1):(n+4) };
Plane Surface(n+20) = {n+10};


n = 400; //magnet
Point(n+1) = { mag_ri, mag_z, 0, mag_cl };
Point(n+2) = { mag_r,  mag_z, 0, mag_cl };
Point(n+3) = { mag_r,  mag_z+mag_h, 0, mag_cl };
Point(n+4) = { mag_ri,  mag_z+mag_h, 0, mag_cl };

Line(n+1) = {n+1, n+2};  Line(n+2) = {n+2, n+3};  Line(n+3) = {n+3, n+4};  Line(n+4) = {n+4, n+1};
Line Loop(n+10) = { (n+1):(n+4) };
Plane Surface(n+20) = {n+10};


n = 500; //hot plate
Point(n+1) = { 0, cruc_z-plate_h, 0, plate_cl };
Point(n+2) = { plate_r, cruc_z-plate_h, 0, plate_cl };
Point(n+3) = { plate_r, cruc_z, 0, plate_cl };

Line(n+1) = {n+1, n+2};  Line(n+2) = {n+2, n+3};  Line(n+3) = {n+3, 102};  Line(n+4) = {101, n+1}; 
Line Loop(n+10) = { (n+1):(n+3), -101, n+4 };
Plane Surface(n+20) = {n+10};


n = 900; //air
Point(n+1) = { 0, wall_z, 0, wall_cl };
Point(n+2) = { wall_r,  wall_z, 0, wall_cl };
Point(n+3) = { wall_r,  wall_z+wall_h, 0, wall_cl };
Point(n+4) = { 0,  wall_z+wall_h, 0, 0.3*wall_cl };

Line(n+1) = {n+1, n+2};  Line(n+2) = {n+2, n+3};  Line(n+3) = {n+3, n+4};  Line(n+4) = {n+4, 303};
Line(n+5) = {501, n+1};
Line Loop(n+10) = { (n+1):(n+4), -303, -302, -301, -201, -104, -103, -102, -503, -502, -501, n+5 };
Plane Surface(n+20) = {n+10, 410};


// export
Physical Surface("crucible", 100) = {120};  Color Grey20{ Surface{120}; }  
Physical Surface("melt", 200) = {220};      Color Yellow{ Surface{220}; }  
Physical Surface("crystal", 300) = {320};   Color Grey50{ Surface{320}; }  
Physical Surface("magnet", 400) = {420};    Color Blue{ Surface{420}; }    
Physical Surface("plate", 500) = {520};     Color Red{ Surface{520}; }     
Physical Surface("air", 900) = {920};       Color Cyan{ Surface{920}; }    

Physical Line("crucible outside", 111) = {102:104};  
Physical Line("melt free surface", 210) = {201};      
Physical Line("melt-crystal interface", 211) = {202};      
Physical Line("melt-crucible interface", 212) = {105:106}; 
Physical Line("crystal outside", 310) = {301:302};  
Physical Line("crystal end", 311) = {303};  
Physical Line("magnet outside", 410) = {401:404};  
Physical Line("hotplate outside", 510) = {501:503};  
Physical Line("outer boundary", 910) = {901:903};  
Physical Line("axis", 911) = {904, 304, 203, 107, 504, 905};  

Mesh.ElementOrder = 2;

//Recombine Surface { 220, 920 };
