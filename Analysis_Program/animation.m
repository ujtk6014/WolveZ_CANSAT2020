clear;close all

load('捕捉率マックス')


yoko=1500;tate=1000;
myfigure(yoko,tate)

myVideo = VideoWriter('myfile_potetial_test.mp4');
dt=0.1;
myVideo.FrameRate = 1*1/dt;
myVideo.Quality = 70;
open(myVideo);
set(gca)

subplot(221)
box1=plot(x_r1(1,1), y_r1(1,1),'r*');
hold on
box1_root=plot(x_r1(:,1), y_r1(:,1),'b-');
hold on
box2=plot(x_r2(1,1), y_r2(1,1),'b*');
hold on
box2_root=plot(x_r2(:,1), y_r2(:,1),'b-');
hold on
box3=plot(x_r3(1,1), y_r3(1,1),'g*');
hold on
box3_root=plot(x_r3(:,1), y_r3(:,1),'b-');
hold on

plot(ob_r*cosd(0:1:360)+x_ob,ob_r*sind(0:1:360)+y_ob,'r-')
hold on
plot(x_r1,y_r1,'r-')
hold on
plot(x_r2,y_r2,'r-')
hold on
plot(x_r3,y_r3,'r-')
hold on
pbaspect([1 1 1])
xlabel('x[m]')
ylabel('y[m]')
axis([max_world_x,max_world_y])
grid on

subplot(222)
potential_r1=surf(x_tmp,y_tmp,z_g+z_r2+z_r3);
hold on
uxr1=0;
uyr1=0;
vector_r1=quiver3(x_r1(1,1),y_r1(1,1),0.5,uxr1,uyr1,0);
vector_r1.Color='red';
vector_r1.LineWidth=3;
vector_r1.ShowArrowHead='on';
hold on
positon_r1=plot3(x_r1(1,1), y_r1(1,1),1,'r*');
hold on
positon_r12=plot3(x_r2(1,1), y_r2(1,1),1,'b*');
hold on

pbaspect([1 1 1])
axis([max_world_x,max_world_y,[-2,2]])
view([0 0 90])
xlabel('x[m]')
ylabel('y[m]')
%% ロボット2,3の動的ポテンシャル描画セットアップ
subplot(223)
potential_r2=surf(x_tmp,y_tmp,z_g+z_r1+z_r3);
hold on
uxr2=0;
uyr2=0;
vector_r2=quiver3(x_r2(1,1),y_r2(1,1),0.5,uxr2,uyr2,0);
vector_r2.Color='red';
vector_r2.LineWidth=3;
vector_r2.ShowArrowHead='on';
hold on
positon_r2=plot3(x_r2(1,1), y_r2(1,1),1,'b*');
hold on
positon_r21=plot3(x_r1(1,1), y_r1(1,1),1,'r*');
hold on

pbaspect([1 1 1])
axis([max_world_x,max_world_y,[-2,2]])
view([0 0 90])
xlabel('x[m]')
ylabel('y[m]')

subplot(224)
potential_r3=surf(x_tmp,y_tmp,z_g+z_r1+z_r2);
hold on
uxr3=0;
uyr3=0;
vector_r3=quiver3(x_r3(1,1),y_r3(1,1),0.5,uxr3,uyr3,0);
vector_r3.Color='red';
vector_r3.LineWidth=3;
vector_r3.ShowArrowHead='on';
hold on
positon_r3=plot3(x_r3(1,1), y_r3(1,1),1,'g*');
hold on
positon_r31=plot3(x_r1(1,1), y_r1(1,1),1,'r*');
hold on

pbaspect([1 1 1])
axis([max_world_x,max_world_y,[-2,2]])
view([0 0 90])
xlabel('x[m]')
ylabel('y[m]')
%% シミュレーション
end_time=20;

Pr1_potential=zeros(100,100);

for i=1:1:end_time/dt
    
    
%描画のためのプログラム
    for j=1:1:length(x_tmp)
        for k=1:1:length(y_tmp)
            z_g(k,j) = -1/(1+Cg*(dr-sqrt((x_tmp(j)-x_ob)^2+(y_tmp(k)-y_ob)^2))^2);
            z_r1(k,j) = 2/(1+C*sqrt((x_r1(i,1)-x_tmp(j))^2+(y_r1(i,1)-y_tmp(k))^2));
            z_r2(k,j) = 2/(1+C*sqrt((x_r2(i,1)-x_tmp(j))^2+(y_r2(i,1)-y_tmp(k))^2));
            z_r3(k,j) = 2/(1+C*sqrt((x_r3(i,1)-x_tmp(j))^2+(y_r3(i,1)-y_tmp(k))^2));
            
        end
    end
    P_r1=z_g+z_r2+z_r3;
    P_r2=z_g+z_r1+z_r3;
    P_r3=z_g+z_r1+z_r2;
    %% 更新　メインの図
    box1.XData= x_r1(i,1);
    box1.YData= y_r1(i,1);
    box1_root.XData= x_r1(:,1);
    box1_root.YData= y_r1(:,1);
    
    box2.XData= x_r2(i,1);
    box2.YData= y_r2(i,1);
    box2_root.XData= x_r2(:,1);
    box2_root.YData= y_r2(:,1);
    
    box3.XData= x_r3(i,1);
    box3.YData= y_r3(i,1);    
    box3_root.XData= x_r3(:,1);
    box3_root.YData= y_r3(:,1);
    
%更新　robot1のポテンシャル
    potential_r1.ZData=P_r1;

    vector_r1.XData= x_r1(i,1);
    vector_r1.YData=y_r1(i,1);
    vector_r1.UData=double(uxr1);
    vector_r1.VData=double(uyr1);
    positon_r1.XData= x_r1(i,1);
    positon_r1.YData= y_r1(i,1);
    positon_r12.XData= x_r2(i,1);
    positon_r12.YData= y_r2(i,1);

%更新　robot2のポテンシャル
    potential_r2.ZData=P_r2;
    
    vector_r2.XData= x_r2(i,1);
    vector_r2.YData=y_r2(i,1);
    vector_r2.UData=double(uxr2);
    vector_r2.VData=double(uyr2);
    positon_r2.XData= x_r2(i,1);
    positon_r2.YData= y_r2(i,1);
    positon_r21.XData= x_r1(i,1);
    positon_r21.YData= y_r1(i,1);
    
%更新　robot3のポテンシャル
    potential_r3.ZData=P_r3;
    
    vector_r3.XData= x_r3(i,1);
    vector_r3.YData=y_r3(i,1);
    vector_r3.UData=double(uxr3);
    vector_r3.VData=double(uyr3);
    positon_r3.XData= x_r3(i,1);
    positon_r3.YData= y_r3(i,1);
    positon_r31.XData= x_r1(i,1);
    positon_r31.YData= y_r1(i,1);
    
    myMovie(i)=getframe(gcf);
    writeVideo(myVideo, myMovie(i));
    drawnow
end

disp("writeVideo end")
close(myVideo);


yoko=350;tate=350;
myfigure(yoko,tate)
graph_time=linspace(0,end_time,length(vx_r1));
plot(graph_time,vx_r1)

myfigure(yoko,tate)
plot(graph_time,vx_r2)

myfigure(yoko,tate)
plot(graph_time,vx_r3)

myfigure(yoko,tate)
bar(rate_history_r1)
ylim([0,1])

myfigure(yoko,tate)
bar(rate_history_r2)
ylim([0,1])

myfigure(yoko,tate)
bar(rate_history_r3)
ylim([0,1])

myfigure(yoko,tate)
bar(rate_history)
ylim([0,1])