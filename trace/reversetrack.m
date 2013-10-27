#!/usr/bin/octave
l=2.87;         # car wheelbase(轴距)
w=1.56+0.12*2;  # car front/rear wheel distance(前/后轮距)(0.12m 道可视instruction)
#d=1.03+0.3;     # distance between rear wheel to back of car(0.3m 道可视instruction)
d=1.03;     # distance between rear wheel to back of car(0.3m 道可视instruction)
phi=10/180*pi;  # the angle between front wheelbase and horizon line

ratio=100;
l=l*ratio;
w=w*ratio;
d=d*ratio;

#   draw cricle reference:
#   http://stackoverflow.com/questions/7971467/how-to-draw-a-circle

for i=1:9
    R_middle_point=l*cot(phi);
    t=linspace(0,pi,180);        # full circle
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
    axis([-1.5*ratio,1.5*ratio,d,d+3*ratio],"equal");
    plot(X_big_round,Y_big_round,"r",'LineWidth',5);
    hold on
    axis([-1.5*ratio,1.5*ratio,d,d+3*ratio],"equal");
    plot(X_small_round,Y_small_round,"r",'LineWidth',5);
    hold off
    filename=strcat("track",num2str(i*step),".jpg");
    #print -dpdf track.pdf
    #print(filename,"-djpg","-S800,480")
    print(filename,"-djpg","-landscape")
end

axis([-1.5*ratio,1.5*ratio,d,d+3*ratio],"equal");
plot([-w/2;w/2],[d+0.3*ratio;d+0.3*ratio],"r",'LineWidth',5);
hold on
axis([-1.5*ratio,1.5*ratio,d,d+3*ratio],"equal");
plot([-w/2;w/2],[d+0.6*ratio;d+0.6*ratio],"r",'LineWidth',5);
hold on
axis([-1.5*ratio,1.5*ratio,d,d+3*ratio],"equal");
plot([-w/2;w/2],[d+1*ratio;d+1*ratio],"r",'LineWidth',5);
hold on
axis([-1.5*ratio,1.5*ratio,d,d+3*ratio],"equal");
plot([-w/2;w/2],[d+2*ratio;d+2*ratio],"r",'LineWidth',5);
hold on
axis([-1.5*ratio,1.5*ratio,d,d+3*ratio],"equal");
plot([-w/2;w/2],[d+3*ratio;d+3*ratio],"r",'LineWidth',5);
hold on
axis([-1.5*ratio,1.5*ratio,d,d+3*ratio],"equal");
plot([0*ratio;0*ratio],[d;d+3*ratio],"r",'LineWidth',5);
hold off
print("track0.jpg","-djpg","-landscape")
