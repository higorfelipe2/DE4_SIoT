%%Get data (emotions, skin resistance, PPG) from matlab, put into timetable, then remove data that is not
%%common across all variables.


clc
clear all

%%Channel Access%
sensorsChannelID = [1277203];
sensorsWriteKey = 'XGCVKVKWC0BC46SX';
sensorsReadKey = "0FSTKU4LJ2ZQV9VS";

emotionsChannelID = [1279893];
emotionsWriteKey = '2KASG4QDEA07ZEBX';
emotionsReadKey = '5AYE65MS1DNUDF5V';

syncedChannelID = [1280543];
syncedWriteKey = 'ESMBMIMYDF1FQFW6';
syncedReadKey = '8UN9R91PZ812CKWC';

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


%%PSEUDO-DATA FOR TESTING
%-----------------------------------------------------------------
%Safe to assume both sensors are synced since Arduino code was set up to
%only publish when both had available data
% Time = seconds([1 2 5 7 8 9 10 11])';
% heartRate = [NaN NaN 63 64 67 1 68 64]';
% skinResistance = [NaN NaN 2 4 5 1 7 8]';
% Time2 = seconds([1 4 8 10 11])';
% emotions = [1 -2 0 3 1]';
%%-----------------------------------------------------------------

% %%REMOVE ANY SENSOR DATA THAT DOESN'T CORRESPOND TO AN EMOTION DATA
% %%----------------------------------------------------------------
% Time2inTime = [];
% for i = 1:size(Time2)
%     Time2inTime = ismember(Time2(i,:),Time{:,:});
% end
% %%Found the values that DO correspond, so inverse to delete value
% %%that DO NOT correspond
% inversedTime2inTime = 1:length(Time);
% for i = Time2inTime
%     inversedTime2inTime(i) = [];
% end
% for i = flip(inversedTime2inTime)
%     heartRate(i) = [];
%     skinResistance(i) = [];
% end
% %%----------------------------------------------------------------
% 
% %%REMOVE REMAINING EMOTION DATA THAT WASN'T CORRESPONDING TO AN EMOTION
% %%DATA
% %%---------------------------------------------------------------------
% TimeinTime2 = [];
% for i = 1:size(Time)
%     TimeinTime2 = [TimeinTime2;find(Time2==Time(i))];
% end
% inversedTimeinTime2 = 1:length(Time2);
% for i = TimeinTime2
%     inversedTimeinTime2(i) = [];
% end
% for i = flip(inversedTimeinTime2)
%     emotions(i) = [];
% end
% %%---------------------------------------------------------------------


%%Remove NaNs - Ignore, better method used above
%%-----------------------------------------------------------------
% NaNs1 = find(isnan(heartRate));
% for i = NaNs1
%     Time(i) = [];
%     heartRate(i) = [];
%     skinResistance(i) = [];
%     emotions(i) = [];
% end
% NaNs2 = find(isnan(emotions));
% for i = NaNs2
%     Time(i) = [];
%     heartRate(i) = [];
%     skinResistance(i) = [];
%     emotions(i) = [];
% end

% %%sanity check
% %%---------------------------------------------------------------------
% %%disp("Emotions: ")
% %%disp(emotions)
% %%disp("Heart Rates: ")
% %%disp(heartRate)
% %%disp("SkinResistance")
% %%disp(skinResistance)
% %%disp(timeStamp)
% %%---------------------------------------------------------------------
% 
% %%Code analysis%%
% %%analyzedData = data;
% 

