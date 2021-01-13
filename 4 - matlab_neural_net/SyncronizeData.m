%%Get data (emotions, skin resistance, PPG) from matlab, put into timetable, then remove data that is not
%%common across all variables.


clc
clear all

%%Channel Access%
sensorsChannelID = [1277203];
sensorsWriteKey = '';
sensorsReadKey = '';

emotionsChannelID = [1279893];
emotionsWriteKey = '';
emotionsReadKey = '';

syncedChannelID = [1280543];
syncedWriteKey = '';
syncedReadKey = '';

%%Read Data%%
[sensorsData,channelInfo] = thingSpeakRead(sensorsChannelID,'OutputFormat','table', 'NumPoints',8000);
%[sensorsData,channelInfo] = thingSpeakRead(sensorsChannelID,'OutputFormat','table','DateRange',[datetime(2020,1,9,12,00,00),datetime(2020,1,9,23,59,59)]);
[emotionsData, channelInfo] = thingSpeakRead(emotionsChannelID,'OutputFormat','table', 'NumPoints',8000);
%[emotionsData,channelInfo] = thingSpeakRead(emotionsChannelID,'OutputFormat','table','DateRange',[datetime(2020,1,9,12,00,00),datetime(2020,1,9,23,59,59)]);
Data = outerjoin(sensorsData, emotionsData, 'Keys', 'Timestamps', 'MergeKeys', 1);

%%Replace columns 3, 5 and 7's NaNs with zeroes
vars = {'PPGSynced' 'SkinResistanceSynced' 'EmotionsSynced'};
DataFormatted = Data{:,vars};
DataFormatted(isnan(DataFormatted)) = 0;
Data{:,vars} = DataFormatted;
%%remove missing data (removes rows with with NaN)
DataFormatted = rmmissing(Data);
%%remove empty strings from emotions, which correspond with when the user
%%looked away (specified in pytho script)
a = table2cell(DataFormatted); % covert to cell
double = str2double(a(:,6)); % convert emotions column to double (numbers)
a(:,6) = num2cell(double); %convert double to cells then place with rest of data 
DataFormatted = cell2table(a);
DataFormatted = rmmissing(DataFormatted); %Empty space now shows as NaN, so remove

%data = data(~any(strcmp(data{:,:},''),2),:)
%data = data(~any(strcmp(data{:,:},'Null'),2),:)
Time = DataFormatted(:,1);
PPG = DataFormatted(:,2);
skinResistance = DataFormatted(:,4);
emotions = DataFormatted(:,6);

test = Time{1,:};
test2 = Time{2,:};
test3 = datetime('now');

%Write Data with correct timestamps
%---------------------------------------------------------------------
for i = 1:height(emotions)-1
%     disp("PPG "+ i+ ":");
%     PPG{i,:};
%     disp("GSR "+ i+ ":");
%     skinResistance{i,:};
%     disp("Emotion "+ i+ ":");
%     emotions{i,:};
    timeStamp = Time{i,:};
    thingSpeakWrite(syncedChannelID, "Fields",[1,2,3],"Values", {PPG{i,:},skinResistance{i,:},emotions{i,:}}, 'WriteKey', syncedWriteKey,'TimeStamp',Time{i,:});
    %thingSpeakWrite(writeChannelID emotions(i),'WriteKey','23ZLGOBBU9TWHG2H')
    disp("Successfully uploaded "+ (i/height(emotions))*100 + "% to Channel.")
    disp("Time left "+ (height(emotions)-i)/60 + " minutes")
    pause(1);
end



