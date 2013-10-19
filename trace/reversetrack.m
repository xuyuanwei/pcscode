#!/usr/bin/octave
a=85/180*pi;    # camera view angle
b=20/180*pi;    # angle between camera center line and horizon line
h=1;            # camera hight from ground
hscreen=0.1;    # screen hight
wscreen=0.2;    # screen width
l=2.87;         # car wheelbase(÷·æ‡)
w=1.56;         # car front/rear wheel distance(«∞/∫Û¬÷æ‡)
d=1.03;         # distance between rear wheel to back of car
phi=10/180*pi;  # the angle between front wheelbase and horizon line


#   draw cricle reference:
#   http://stackoverflow.com/questions/7971467/how-to-draw-a-circle


for i=1:9
    R_middle_point=l*cot(phi);
    t=linspace(0,pi,100);
    Xoffset=R_middle_point;
    Yoffset=d;
# big round
    R_big_round=R_middle_point+w/2;
    X_big_round=R_big_round*cos(t)+Xoffset;
    Y_big_round=R_big_round*sin(t)+Yoffset;

# small round
    R_small_round=R_middle_point-w/2;
    X_small_round=R_small_round*cos(t)+Xoffset;
    Y_small_round=R_small_round*sin(t)+Yoffset;

    step=5;

    phi=i*step/180*pi;
    plot(X_big_round,Y_big_round,"r",'LineWidth',5);
    hold on
    plot(X_small_round,Y_small_round,"r",'LineWidth',5);
    hold on
    filename=strcat("track",num2str(i*step),".jpg");
    #print -dpdf track.pdf
    print(filename,"-djpg")
end

