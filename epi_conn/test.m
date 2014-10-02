begS = []
temp = 1
%endS[1] = begS[1] + 4000
begS(1) = 1;
endS(1) = 4001
for i = 2: 121;
    begS(i) = (begS(i-1) + 4000 +1);
end
size(begS)
% begS
for i = 2:120;
    endS(i) = begS(i+1)-1;
end
endS(121) = endS(120) + 4000;
size(endS)
% endS

offset = zeros(1,121);
size(offset)
samples = horzcat(begS', endS', offset')