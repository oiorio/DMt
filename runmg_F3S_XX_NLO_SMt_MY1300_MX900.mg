import model DMSimpt_NLO_v1_3_UFO-F3S_uni --modelname
define qq = u c t d s b u~ c~ t~ d~ s~ b~
define xx = xs
define yy = yf3u3 yf3u3~
define uu = u u~
define dd = d d~
define cc = c c~
define ss = s s~
define tt = t t~
define bb = b b~
define excl = yf3qu1 yf3qu2 yf3qu3 yf3qd1 yf3qd2 yf3qd3 ys3qu1 ys3qu2 ys3qu3 ys3qd1 ys3qd2 ys3qd3 ys3u1 ys3u2 ys3u3 ys3d1 ys3d2 ys3d3 xm xd xv xw a z yf3u1 yf3u2 yf3d1 yf3d2 yf3d3 xc
generate p p > xx xx  QED=0 / excl [QCD]
output DMtsimp/MG5Runs/F3S_XX_NLO_SMt_MY1300_MX900
exit
