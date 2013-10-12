#!/usr/bin/octave
a=85/180*pi;    # camera view angle
b=20/180*pi;    # angle between camera center line and horizon line
h=1;            # camera hight from ground
hscreen=0.1;    # screen hight
wscreen=0.2;    # screen width
l=2.87;            # car wheelbase(÷·æ‡)
w=1.56;          # car front/rear wheel distance(«∞/∫Û¬÷æ‡)
d=1.03;          # distance between rear wheel to back of car
phi=10/180*pi;  # the angle between front wheelbase and horizon line

x_orig=l*cot(phi);
# big round
#x=linspace(-l*cot(phi),w/2,100);
r=l*cot(phi)+w/2;
# the x value when y=0
x=linspace(-sqrt(power(r,2)-power(d,2))-x_orig,+sqrt(power(r,2)-power(d,2))-x_orig,100);
y=sqrt(power((l*cot(phi)+w/2),2)-power((x+l*cot(phi)),2))-d;

# small round
r1=l*cot(phi)-w/2
#x1=linspace(-l*cot(phi),-w/2,100);
# the x value when y=0
x1=linspace(-sqrt(power(r1,2)-power(d,2))-x_orig,+sqrt(power(r1,2)-power(d,2))-x_orig,100)
y1=sqrt(power(r1,2)-power((x1+l*cot(phi)),2))-d

plot(x1,y1);
hold on;
plot(x,y);
#hold on;
print -dpdf track.pdf

#value1=hscreen/(2*sin(a));
#smallcircler=l*cot(phi)-w/2;
#t=linspace(asin(d/smallcircler),pi-asin(d/smallcircler),100);
#smallcirclex=smallcircler*cos(t)-l*cot(phi);
#smallcircley=smallcircler*sin(t)-d;
#plot(smallcirclex,smallcircley);
#hold on;

#t=linspace(asin(d/smallcircler)-pi/180,pi-asin(d/smallcircler)-pi/180,100);
#screenrightcirclex=((smallcircler*cos(t)-l*cot(phi))*w)./((smallcircler*sin(t)-d)*tan(a)*2)
#screenrightcircley=sin(a+b-atan(h./(smallcircler*sin(t)-d)))./cos(b-atan(h./(smallcircler*sin(t)-d))).*(smallcircler*cos(t)-l*cot(phi))*value1
#plot(screenrightcirclex,screenrightcircley);
#hold on;

#bigcircler=l*cot(phi)+w/2;
#t=linspace(asin(d/bigcircler),pi-asin(d/bigcircler),100);
#bigcirclex=bigcircler*cos(t)-l*cot(phi);
#bigcircley=bigcircler*sin(t)-d;
#plot(bigcirclex,bigcircley);
#hold on;

#t=linspace(asin(d/bigcircler)-pi/180,pi-asin(d/bigcircler)-pi/180,100);
#screenleftcirclex=((bigcircler*cos(t)-l*cot(phi))*w)./((bigcircler*sin(t)-d)*tan(a)*2)
#screenleftcircley=sin(a+b-atan(h./(bigcircler*sin(t)-d)))./cos(b-atan(h./(bigcircler*sin(t)-d))).*(bigcircler*cos(t)-l*cot(phi))*value1
#plot(screenleftcirclex,screenleftcircley);
#axis([-0.05,0.05,-0.1,0.1]);
#print -dpdf track.pdf
