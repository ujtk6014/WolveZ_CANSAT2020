fontsize=11;
% GUI�̃t�H���g
set(0, 'defaultUicontrolFontName', 'Times New Roman');
% ���̃t�H���g
set(0, 'defaultAxesFontName','Times New Roman');
% �^�C�g���A���߂Ȃǂ̃t�H���g
set(0, 'defaultTextFontName','Times New Roman');
% GUI�̃t�H���g�T�C�Y
set(0, 'defaultUicontrolFontSize', fontsize);
% ���̃t�H���g�T�C�Y
set(0, 'defaultAxesFontSize', fontsize);% �^�C�g���A���߂Ȃǂ̃t�H���g�T�C�Y89
set(0, 'defaultTextFontSize', fontsize);

%% �܂��C���|�[�g���悤�i���l�s��Ƃ��āj
filename="20200713.xlsx"; % �����̓C���|�[�g�����ϐ���
data=x20200710; % �����̓C���|�[�g�����ϐ���
filename2=[date '�Z���T����_20200710'];
mkdir(filename2);

%% �ϐ���
Time=data{:,1}/1000;
State=data{:,2};
Ido=data{:,4};
Keido=data{:,5};
%G=data(:,8:10);
A=data{:,6:8};
Acc=sqrt(A(:,1).^2+A(:,2).^2+A(:,3).^2);
Dist=data{:,9};
Motor1=data{:,10};
Motor2=data{:,11};

%%
i=1;
figure(i)
plot(Time,State,'lineWidth',2);
grid;
xlabel('Time [s]')
ylabel('State')
yticks([0 1 2 3 4 5 6])
yticklabels({'PREPARING','FLYING','DROPPING','LANDING','WAITING','RUNNING','GOAL'})
i=i+1;

% figure(i)
% plot(Time,Light,'lineWidth',2);
% grid;
% xlabel('Time [s]')
% ylabel('Light')
% i=i+1;

% figure(i)
% plot(Time,G,'lineWidth',2);
% grid;
% xlabel('Time ([s]')
% ylabel('Acc. [m/s^2]')
% legend('x','y','z','Location','best');
% i=i+1;

figure(i)
plot(Time,A,'lineWidth',2);
grid;
xlabel('Time [s]')
ylabel('Acc. [m/s^2]')
legend('x','y','z','Location','best');
i=i+1;

figure(i)
plot(Time,Acc,'lineWidth',2);
grid;
xlabel('Time [s]')
ylabel('|Acc.| [m/s^2]')
i=i+1;

figure(i)
plot(Time,Dist,'lineWidth',2);
grid minor;
xlabel('Time [s]')
ylabel('Distance [m]')
yticks([0:50:500])
%yticklabels({'OFF','ON'})
i=i+1;

figure(i)
plot(Time,Motor1,Time,Motor2,'lineWidth',2);
legend('rightmotor','leftmotor','Location','best');
grid;
xlabel('Time [s]')
ylabel('Motor Velocity')
i=i+1;

%% �ۑ�

date=num2str(date());
% xlswrite(filename2+ "/" + filename,data);

for j = 1:i-1
   saveas(figure(j),[filename2 '/figure' int2str(j)],'fig');
   saveas(figure(j),[filename2 '/figure' int2str(j)],'jpeg');
end

%% �A�j������낤

% % for j=1:length(Time)
% %     if Module1(j)>=255
% %         Module1(j)=0;
% %     end
% % end
% 
% for j=1:length(Time)-1
%     dt2(j)=Time(j+1)-Time(j);
% end
% 
% date=num2str(date());
% 
% filename3=[date 'video'];
% 
% mkdir(filename2);
% m1x=0;
% m1y=1;
% m2x=0;
% m2y=-1;
% figure(i)
% 
% myVideo = VideoWriter([filename2 '/ARLISS_�ǉ�����']);
% dt=mean(dt2);
% div=10;
% dt=dt/div;
% Module1=intpl(Module1,div);
% Module2=intpl(Module2,div);
% myVideo.FrameRate = 1*1/dt;
% myVideo.Quality = 70;
% open(myVideo);
% set(gca)
% % RGB=[module1]
% 
% % Light1=plot(m1x,m1y,'o','MarkerSize',10,'MarkerFaceColor',[Module1(1) 0 1023-Module1(1)]/1023,'MarkerEdgeColor',[Module1(1) 0 1023-Module1(1)]/1023);
%  Light1=bar(1,Module1(1));
% hold on
% Light2=bar(2,Module2(1));
% % legend("module1","module2");
% 
% ylim([0 1023])
% xticks([1 2])
% xticklabels({'module1','module2'})
% 
% for k=1:length(Module1)
% %     Light1.MarkerFaceColor=[Module1(k) 0 1023-Module1(k)]/1023;
% %     Light1.MarkerEdgeColor=[Module1(k) 0 1023-Module1(k)]/1023;
%     Light1.YData=Module1(k);
%     Light2.YData=Module2(k);
%     myMovie(k)=getframe(gcf);
%     writeVideo(myVideo, myMovie(k));
%     drawnow
% end
% 
% disp("writeVideo end")
% close(myVideo);