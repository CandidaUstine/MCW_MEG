function generate_tones(f)

Fs = 11025; %Samples per second
toneFreq = f; % Tonal Frequency in Hertz
nSeconds = .1; %Duration of sound 
y = sin(linspace(0, nSeconds*toneFreq*2*pi, round(nSeconds*Fs)));
sound(y, Fs) % Play the sound at sampling rate Fs
filename = strcat('/home/custine/Desktop/Experiments/tones/','tone_', int2str(f), 'Hz_11025Smp_100ms.wav')
wavwrite(y, Fs, 8,filename) 
