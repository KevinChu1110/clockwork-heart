import numpy as np,subprocess,itertools
SR=44100
def load(f):
    x=np.frombuffer(subprocess.run(["ffmpeg","-v","quiet","-i",f,"-ac","1","-ar",str(SR),"-f","f32le","-"],capture_output=True).stdout,np.float32).astype(float)
    return x
def mmax(f,gain=0):
    o=subprocess.run(["ffmpeg","-nostats","-i",f,"-af",f"volume={gain}dB,apad=pad_dur=1,ebur128","-f","null","-"],capture_output=True,text=True).stderr
    import re; return max(float(v) for v in re.findall(r' M:\s*(-?[0-9.]+)',o))
def mel_fb(n=40,nfft=2048):
    hz=lambda m:700*(10**(m/2595)-1); mel=lambda h:2595*np.log10(1+h/700)
    pts=hz(np.linspace(mel(50),mel(16000),n+2)); bins=np.floor((nfft+1)*pts/SR).astype(int)
    fb=np.zeros((n,nfft//2+1))
    for i in range(n):
        a,b,c=bins[i:i+3]
        fb[i,a:b]=(np.arange(a,b)-a)/max(b-a,1); fb[i,b:c]=(c-np.arange(b,c))/max(c-b,1)
    return fb
FB=mel_fb()
def mfcc(x,nfft=2048,hop=512):
    x=np.pad(x,(0,max(0,nfft-len(x))))
    fr=np.array([x[i:i+nfft]*np.hanning(nfft) for i in range(0,len(x)-nfft+1,hop)])
    P=np.abs(np.fft.rfft(fr))**2; E=np.log(P@FB.T+1e-10)
    n=E.shape[1]; D=np.cos(np.pi/n*(np.arange(n)[:,None]+0.5)*np.arange(13)[None,:])
    return E@D, P
def dtw(a,b):
    n,m=len(a),len(b); C=np.full((n+1,m+1),np.inf); C[0,0]=0
    d=np.linalg.norm(a[:,None,:]-b[None,:,:],axis=2)
    for i in range(1,n+1):
        for j in range(1,m+1):
            C[i,j]=d[i-1,j-1]+min(C[i-1,j],C[i,j-1],C[i-1,j-1])
    return C[n,m]/(n+m)
files={"white(#98 舊reveal)":("reveal.wav",-5),"white(#99 新reveal)":("reveal_new99.wav",-5),"blue":("reveal_blue.wav",0),"purple":("reveal_purple.wav",0),"gold":("reveal_gold.wav",0),"rainbow":("reveal_rainbow.wav",0)}
F={}
for k,(f,g) in files.items():
    x=load(f); M,P=mfcc(x)
    spec=np.abs(np.fft.rfft(x*np.hanning(len(x)))); fr=np.fft.rfftfreq(len(x),1/SR)
    cen=(spec*fr).sum()/spec.sum()
    # pitch: strongest peak above 150Hz
    lo=fr>150; f0=fr[lo][spec[lo].argmax()]
    env=np.abs(x); pk=env.max(); onset=np.argmax(env>pk*0.1)/SR*1000; tpk=env.argmax()/SR*1000
    # number of onsets (energy flux peaks)
    e=np.convolve(env**2,np.ones(441)/441,'same')[::441]; de=np.diff(np.log(e+1e-9)); nons=int((de>1.5).sum())
    F[k]=dict(x=x,M=M[:,1:],len=len(x)/SR,lufs=mmax(f,g),cen=cen,f0=f0,onset=onset,tpk=tpk,nons=nons,mm=M[:,1:].mean(0))
    print(f"{k:20s} len={len(x)/SR:.2f}s Mmax(播出)={F[k]['lufs']:.1f} centroid={cen:5.0f}Hz 主峰={f0:5.0f}Hz onset={onset:4.0f}ms 峰值時刻={tpk:4.0f}ms 起音數={nons}")
print("\n成對距離：MFCC(c1-12) DTW 距離 ／ 平均 MFCC 歐氏距離 ／ 正規化互相關最大值")
keys=list(F)
for a,b in itertools.combinations(keys,2):
    xa,xb=F[a]["x"],F[b]["x"]
    n=1<<int(np.ceil(np.log2(len(xa)+len(xb))))
    cc=np.fft.irfft(np.fft.rfft(xa,n)*np.conj(np.fft.rfft(xb,n)),n); xc=np.abs(cc).max()/np.sqrt((xa**2).sum()*(xb**2).sum())
    print(f"{a:20s} vs {b:20s} DTW={dtw(F[a]['M'],F[b]['M']):6.1f}  meanMFCC={np.linalg.norm(F[a]['mm']-F[b]['mm']):6.1f}  xcorr={xc:.2f}")
# reference: same file vs itself with +3dB gain / pitch 1.06 (smallest audible-ish change)
x=F["blue"]["x"]; y=np.interp(np.arange(0,len(x),1.06),np.arange(len(x)),x)
My,_=mfcc(y); print(f"\n參考：blue vs blue 升半音(×1.06) DTW={dtw(F['blue']['M'],My[:,1:]):.1f} meanMFCC={np.linalg.norm(F['blue']['mm']-My[:,1:].mean(0)):.1f}")
