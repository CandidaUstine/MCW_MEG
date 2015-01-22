function [data] = megcolorplot(data,varargin)
%MEGCOLORPLOT
%
% Written by Colin Humphries
% 6/2011



scannertype = 'vectorviewmeg';
scaling = 'absmax'; % 'absmax','maxmin',[min max]
thresh = [];
threshtype = 'pn';
% samplerate = 1000;

for ii = 1:2:length(varargin)
  switch lower(varargin{ii})
   case 'scaling'
    scaling = varargin{ii+1};
   case {'th','thresh'}
    thresh = varargin{ii+1};
   case 'threshtype'
    threshtype = varargin{ii+1};
   otherwise
    error('Unknown option');
  end
end
  
pos = megsensorpositions(scannertype);


% Divide into anterior, central, and posterior sensors. This would
% probably change for different scanner types. The following works for
% the vectorview scanner.
anterior = find(pos(:,2) > .05);
central = find(pos(:,2) >= -.05 & pos(:,2) <= .05);
posterior = find(pos(:,2) < -.05);
% % 
% manterior = find(mlist(:,2) > .05);
% mcentral = find(mlist(:,2) >= -.05 & mlist(:,2) <= .05);
% mposterior = find(mlist(:,2) < -.05);
% 
% ganterior = find(glist(:,2) > .05);
% gcentral = find(glist(:,2) >= -.05 & glist(:,2) <= .05);
% gposterior = find(glist(:,2) < -.05);


% Sort from left to right
[tmp,ind] = sort(pos(anterior,1));
anterior = anterior(ind);
[tmp,ind] = sort(pos(central,1));
central = central(ind);
[tmp,ind] = sort(pos(posterior,1));
posterior = posterior(ind);

% % Sort from left to right
% [tmp,ind] = sort(mlist(manterior,1));
% manterior = manterior(ind);
% [tmp,ind] = sort(mlist(mcentral,1));
% mcentral = mcentral(ind);
% [tmp,ind] = sort(mlist(mposterior,1));
% mposterior = mposterior(ind);
% 
% % Sort from left to right
% [tmp,ind] = sort(glist(ganterior,1));
% ganterior = ganterior(ind);
% [tmp,ind] = sort(glist(gcentral,1));
% gcentral = gcentral(ind);
% [tmp,ind] = sort(glist(gposterior,1));
% gposterior = gposterior(ind);
% 

anterior;
central;
posterior;

% %%Reorder data
data = [data(anterior,:); data(central,:); data(posterior,:)];

%data = [grandavg_FT(manterior,:); grandavg_FT(mcentral,:); grandavg_FT(mposterior,:)];

% % Reorder data
% data = [grandavg_FT(manterior,:); grandavg_FT(mcentral,:); grandavg_FT(mposterior,:)] %; grandavg_FT(ganterior,:); grandavg_FT(gcentral,:); grandavg_FT(gposterior,:)];

size(data)
first = data(3:3:306, 1:601);
second = data(1:3:306, 1:601);
third = data(2:3:306, 1:601);
data = vertcat(first, second, third);
%figure
imagesc(log(abs(data(:,1:601))))

% imagesc(log(abs(data(:, 1:601))));
% 
% % if ischar(scaling)
% %   if strcmp(scaling,'absmax')
% %     ca = caxis;
% %     ca = [-max(abs(ca)) max(abs(ca))];
% %     caxis(ca);
% %   end
% % else
% %   caxis(scaling);
% % end 

% % Draw dividing lines
% xl = get(gca,'xlim');
% cc = length(anterior);
% line([xl(1) xl(2)],[cc+.5 cc+.5],...
%      'color','k');
% cc = length(anterior) + length(central);
% line([xl(1) xl(2)],[cc+.5 cc+.5],...
%      'color','k');

 
 % Draw dividing lines
xl = get(gca,'xlim');
cc = 102;
line([xl(1) xl(2)],[cc+.5 cc+.5],...
     'color','k');
cc = 204;
line([xl(1) xl(2)],[cc+.5 cc+.5],...
     'color','k');
 
 [len_first, ~] = size(first(:,1));
 [len_second, ~] = size(second(:,1));
 [len_third, ~] = size(third(:,1));
 
% % Setup yxaxis labels
% set(gca,...
%     'ytick',...
%     [1+(length(anterior)-1)/4 ...
%      1+3*(length(anterior)-1)/4 ...
%      length(anterior)+1+(length(central)-1)/4 ...
%      length(anterior)+1+3*(length(central)-1)/4 ...
%      length(anterior)+length(central)+1+(length(posterior)-1)/4 ...
%      length(anterior)+length(central)+1+3*(length(posterior)-1)/4],...
%     'yticklabel',{'L','R','L','R','L','R'});

% Setup yxaxis labels
set(gca,...
    'ytick',...
    [1+(len_first-1)/4 ...
     1+3*((len_first)-1)/4 ...
     (len_first)+1+((len_second)-1)/4 ...
     (len_first)+1+3*((len_second)-1)/4 ...
     (len_first)+(len_second)+1+((len_third)-1)/4 ...
     (len_first)+(len_second)+1+3*((len_third)-1)/4],...
    'yticklabel',{'L','R','L','R','L','R'});


end

