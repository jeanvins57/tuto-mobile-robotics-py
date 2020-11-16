from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py

def draw(x,w):
    clean3D(ax,-10,10,-10,10,0,20)
    draw_axis3D(ax,0,0,0,eye(3,3),10)
    draw_robot3D(ax,x[0:3],eulermat(*x[4:7,0]),'blue')
    draw_robot3D(ax,w[0:3],eulermat(*w[4:7,0],size=0.1),'red')
    ax.scatter(1,2,3,color='magenta')
           

def f(x,u):
    x,u=x.flatten(),u.flatten()
    v,φ,θ,ψ=x[3],x[4],x[5],x[6]
    cφ,sφ,cθ,sθ,cψ,sψ= cos(φ),sin(φ),cos(θ),sin(θ),cos(ψ),sin(ψ)
    return array([ [v*cθ*cψ],[v*cθ*sψ],[-v*sθ],[u[0]] ,
                    [-0.1*sφ*cθ + tan(θ)*v*(sφ*u[1]+cφ*u[2])] ,
                     [cφ*v*u[1] - sφ*v*u[2]] ,
                     [(sφ/cθ)*v*u[1] + (cφ/cθ)*v*u[2]]])

def control(x,w,dw,ddw):
    v,φ,θ,ψ=x[3],x[4],x[5],x[6]
    ct=cos(θ)
    st=sin(θ)
    cf=cos(φ)
    sf=sin(φ)
    cp=cos(ψ)
    sp=sin(ψ)
    A1=array([
        [ct*cp  , -v*st*cp  ,   -v*ct*sp,]
        [ct*sp  , v*ct*cp   ,   v*st*sp],
        [-s     ,   0       ,   -v*ct]])
    A2=array([
        [1  , 0    ,   0],
        [0  , cp   ,  -sp],
        [0  , sp/ct,  cp,ct]])
    A=A1@A2
    dp=v*array([[ct*cp],[ct*sp],[-st]])
    p=x[0:3]
    u=linalg.inv(A)*0.04*(w-p) + 0.4*(dw-dp) + ddw

def setpoint(t):
    f1=0.01
    f2=6*f1*f3=3*f1
    R=20
    w=R*array([
        [sin(f1*t)+sin(f2*t)],
        [cos(f1*t)+cos(f2*t)],
        [sin(f3*t)]])
    dw=R*array([
        [f1*cos(f1*t)+f2*cos(f2*t)],
        [-f1*sin(f1*t)-f2*sin(f2*t)],
        [f3*cos(f3*t)]])
    ddw=R*array([
        [-f1**2*sin(f1*t)-f2**2*sin(f2*t)],
        [-f1**2*cos(f1*t)-f2**2*cos(f2*t)],
        [-f3**2*sin(f3*t)]])

x = array([[0,0,10,15,0,1,0]]).T
u = array([[0,0,0.1]]).T
dt = 0.05
ax = Axes3D(figure())    
for t in arange(0,2,dt):
    xdot=f(x,u)
    x = x + dt * xdot
    draw(x)
    pause(0.001)
pause(1)    