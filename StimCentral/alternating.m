function alternating(code1, code2, soa, numofstim, file1, file2, seqfile, program)

% ALTERNATING Produces an alternating sequence (1, 2, 1, 2, 1, 2 etc)
%
%
% ALTERNATING(code1, code2, soa, numofstim, file1, file2, seqfile, program)
%    
%    code1       trigger code for stimulus 1
%    code2       trigger code for stimulus 2
%    soa         stimulus onset asynchrony (in seconds)
%    numofstim   total number of stimuli wanted
%    file1       file name of stimulus 1
%    file2       file name of stimulus 2
%    seqfile     file name for sequence file
%    program     an integer: 1 for Stim, 2 for BrainStim, 3 for Presentation
%
%    CBRU / University of Helsinki, Finland

rand('state',sum(100*clock)) % The seed for the random number generator from the system clock.

% The sequence is created using the STIM notation:

for i = 1:numofstim
  seq{i,1} = i;
  seq{i,2} = 3;
  seq{i,3} = 0;
  seq{i,4} = 0;
  seq{i,5} = soa;
  seq{i,6} = 90;
  seq{i,7} = 90;
  seq{i,8} = -1;
  
  if (mod(i,2)==1)
    seq{i,9} = code1;
    seq{i,10} = file1;
  else
    seq{i,9} = code2;
    seq{i,10} = file2;
  end
end

wbar = waitbar(0.5,'Creating the sequence...');
%%%
% The sequence is written into a file.
filename = sequencefile(seq, program, seqfile, wbar);
