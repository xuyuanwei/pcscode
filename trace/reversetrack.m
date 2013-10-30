#!/usr/bin/octave
l=2.87;         # car wheelbase(轴距)
w=1.56+0.12*2;  # car front/rear wheel distance(前/后轮距)(0.12m 道可视instruction)
#d=1.03+0.3;    # distance between rear wheel to back of car(0.3m 道可视instruction)
d=1.03;         # distance between rear wheel to back of car
phi=10/180*pi;  # the angle between front wheelbase and horizon line

ratio=100;
l=l*ratio;
w=w*ratio;
d=d*ratio;

#   draw cricle reference:
#   http://stackoverflow.com/questions/7971467/how-to-draw-a-circle

leftDistance=-1.5*ratio;
rightDistance=1.5*ratio;
Length=3*ratio;
linewidth=10;

axis([leftDistance,rightDistance,0,0+Length],"equal");
rectangle('Position',[-w/2,0.3*ratio,w,0.3*ratio],'FaceColor',[0.21,0.35,0.97]);
hold on
axis([leftDistance,rightDistance,0,0+Length],"equal");
rectangle('Position',[-w/2,0.6*ratio,w,0.4*ratio],'FaceColor',[0.47,0.56,0.98]);
hold on
axis([leftDistance,rightDistance,0,0+Length],"equal");
rectangle('Position',[-w/2,1*ratio,w,1*ratio],'FaceColor',[0.21,0.35,0.97]);
hold on
axis([leftDistance,rightDistance,0,0+Length],"equal");
rectangle('Position',[-w/2,2*ratio,w,1*ratio],'FaceColor',[0.47,0.56,0.98]);
hold off

print("./source/track0.jpg","-djpg","-landscape")


for i=1:13
    step=5;
    phi=i*step/180*pi;
    R_middle_point=l*cot(phi);
    #t=linspace(0,pi,180);        # half circle
    Xoffset=R_middle_point;
    Yoffset=d;
# big round
    R_big_round=R_middle_point+w/2;
    t=linspace(asin(-Yoffset/R_big_round),pi+asin(Yoffset/R_big_round),180);
    X_big_round=R_big_round*cos(t)+Xoffset;
    Y_big_round=R_big_round*sin(t)+Yoffset;

# small round
    R_small_round=R_middle_point-w/2;
    t=linspace(asin(-Yoffset/R_small_round),pi+asin(Yoffset/R_small_round),180);
    X_small_round=R_small_round*cos(t)+Xoffset;
    Y_small_round=R_small_round*sin(t)+Yoffset;


    axis([leftDistance,rightDistance,0,d+Length],"equal");
    plot(X_big_round,Y_big_round,'Color',[1,0.56,0.02],'LineWidth',linewidth);
    hold on
    axis([leftDistance,rightDistance,0,d+Length],"equal");
    plot(X_small_round,Y_small_round,'Color',[1,0.56,0.02],'LineWidth',linewidth);
    hold off
    filename=strcat("./source/track",num2str(i*step),".jpg");
    #print -dpdf track.pdf
    #print(filename,"-djpg","-S800,480")
    print(filename,"-djpg","-landscape")
end

clf     #clear plot buffer

#axis([leftDistance,rightDistance,d,d+Length],"equal");
#plot([-w/2;w/2],[d+0.3*ratio;d+0.3*ratio],"r",'LineWidth',linewidth);
#hold on
#axis([leftDistance,rightDistance,d,d+Length],"equal");
#plot([-w/2;w/2],[d+0.6*ratio;d+0.6*ratio],"r",'LineWidth',linewidth);
#hold on
#axis([leftDistance,rightDistance,d,d+Length],"equal");
#plot([-w/2;w/2],[d+1*ratio;d+1*ratio],"r",'LineWidth',linewidth);
#hold on
#axis([leftDistance,rightDistance,d,d+Length],"equal");
#plot([-w/2;w/2],[d+2*ratio;d+2*ratio],"r",'LineWidth',linewidth);
#hold on
#axis([leftDistance,rightDistance,d,d+Length],"equal");
#plot([-w/2;w/2],[d+3*ratio;d+3*ratio],"r",'LineWidth',linewidth);
#hold on
#axis([leftDistance,rightDistance,d,d+Length],"equal");
#plot([0*ratio;0*ratio],[d;d+Length],"r",'LineWidth',linewidth);
#hold off

