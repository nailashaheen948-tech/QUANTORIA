import streamlit as st
import pandas as pd
import numpy as np
import pickle
import time
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import warnings
import json
import requests
warnings.filterwarnings('ignore')

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="QUANTORIA",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)
# ─────────────────────────────────────────────
# QUANTORIA SPLASH SCREEN
# ─────────────────────────────────────────────
if "splash_done" not in st.session_state:
    st.session_state["splash_done"] = False

if not st.session_state["splash_done"]:
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;700;900&family=Rajdhani:wght@300;400;600;700&family=JetBrains+Mono:wght@300;400&display=swap');

    header[data-testid="stHeader"], footer, #MainMenu,
    [data-testid="stToolbar"], [data-testid="stDecoration"],
    [data-testid="stStatusWidget"], [data-testid="stSidebar"] { display: none !important; }

    .main .block-container {
        padding: 0 !important; max-width: 100vw !important;
        min-height: 100vh !important; background: #000510 !important;
    }
    .stButton { opacity: 0 !important; position: absolute !important; pointer-events: none !important; }

    #q-splash {
        position: fixed; inset: 0; width: 100vw; height: 100vh;
        z-index: 2147483647;
        background: radial-gradient(ellipse at 20% 50%, #020b1e 0%, #000510 40%, #000208 100%);
        display: flex; flex-direction: column;
        align-items: center; justify-content: center; overflow: hidden;
    }
    #q-canvas { position: absolute; inset: 0; width: 100%; height: 100%; z-index: 0; }

    .q-orb { position: absolute; border-radius: 50%; filter: blur(80px); pointer-events: none; z-index: 1; animation: orbFloat 8s ease-in-out infinite alternate; }
    .q-orb-1 { width: 500px; height: 500px; top: -100px; left: -100px; background: radial-gradient(circle, rgba(0,180,255,0.07) 0%, transparent 70%); }
    .q-orb-2 { width: 400px; height: 400px; bottom: -80px; right: -80px; background: radial-gradient(circle, rgba(120,40,255,0.09) 0%, transparent 70%); animation-delay: -3s; }
    .q-orb-3 { width: 300px; height: 300px; top: 50%; right: 15%; background: radial-gradient(circle, rgba(0,255,200,0.05) 0%, transparent 70%); animation-delay: -5s; }
    @keyframes orbFloat { from { transform: translate(0,0) scale(1); } to { transform: translate(30px,-40px) scale(1.15); } }

    .q-scanline {
        position: absolute; width: 100%; height: 1px;
        background: linear-gradient(90deg, transparent 0%, rgba(0,200,255,0) 20%, rgba(0,200,255,0.4) 50%, rgba(0,200,255,0) 80%, transparent 100%);
        box-shadow: 0 0 20px rgba(0,200,255,0.3); z-index: 2;
        animation: scanMove 3.5s ease-in-out infinite; top: -2px;
    }
    @keyframes scanMove { 0% { top:-2px; opacity:0; } 5% { opacity:1; } 95% { opacity:1; } 100% { top:100vh; opacity:0; } }

    .q-grid {
        position: absolute; inset: 0; z-index: 1;
        background-image: linear-gradient(rgba(0,180,255,0.025) 1px, transparent 1px), linear-gradient(90deg, rgba(0,180,255,0.025) 1px, transparent 1px);
        background-size: 70px 70px; animation: gridShift 25s linear infinite;
    }
    @keyframes gridShift { from { background-position: 0 0; } to { background-position: 70px 70px; } }

    .q-content { position: relative; z-index: 10; display: flex; flex-direction: column; align-items: center; }

    .q-badge {
        font-family: 'JetBrains Mono', monospace; font-size: 0.62rem;
        letter-spacing: 0.35em; color: rgba(0,200,255,0.45); text-transform: uppercase;
        margin-bottom: 2.2rem; opacity: 0;
        animation: fadeSlideDown 0.8s ease-out 0.3s forwards;
    }
    @keyframes fadeSlideDown { from { opacity:0; transform:translateY(-12px); } to { opacity:1; transform:translateY(0); } }

    .q-logo-wrap { position: relative; display: flex; align-items: center; justify-content: center; }

    .q-logo {
        font-family: 'Orbitron', monospace;
        font-size: clamp(3.5rem, 10vw, 8.5rem);
        font-weight: 900; letter-spacing: 0.18em; line-height: 1;
        color: transparent;
        background: linear-gradient(135deg, #ffffff 0%, #a8efff 25%, #00d4ff 45%, #7c3aed 70%, #ffffff 100%);
        background-size: 300% 300%; -webkit-background-clip: text; background-clip: text;
        opacity: 0;
        animation: logoReveal 1.2s cubic-bezier(0.22,1,0.36,1) 0.6s forwards, gradientShift 4s ease-in-out 1.8s infinite alternate;
        filter: drop-shadow(0 0 40px rgba(0,212,255,0.4));
    }
    @keyframes logoReveal {
        0%   { opacity:0; transform:scale(0.85) translateY(20px); letter-spacing:0.35em; }
        60%  { opacity:1; transform:scale(1.02) translateY(-3px); }
        100% { opacity:1; transform:scale(1) translateY(0); letter-spacing:0.18em; }
    }
    @keyframes gradientShift { from { background-position:0% 50%; } to { background-position:100% 50%; } }

    .q-logo-reflection {
        font-family: 'Orbitron', monospace;
        font-size: clamp(3.5rem, 10vw, 8.5rem);
        font-weight: 900; letter-spacing: 0.18em;
        color: transparent;
        background: linear-gradient(180deg, rgba(0,212,255,0.12) 0%, transparent 70%);
        -webkit-background-clip: text; background-clip: text;
        transform: scaleY(-1) translateY(-4px); filter: blur(1px);
        opacity: 0; user-select: none;
        animation: reflectionFade 1.5s ease-out 1.5s forwards;
    }
    @keyframes reflectionFade { from { opacity:0; } to { opacity:1; } }

    .q-glow-ring {
        position: absolute; width: 120%; height: 200%; border-radius: 50%;
        background: radial-gradient(ellipse, rgba(0,180,255,0.06) 0%, rgba(120,40,255,0.04) 40%, transparent 70%);
        opacity: 0; animation: ringExpand 2s ease-out 1s forwards; pointer-events: none;
    }
    @keyframes ringExpand { from { opacity:0; transform:scale(0.5); } to { opacity:1; transform:scale(1); } }

    .q-deco-line {
        display: flex; align-items: center; gap: 16px; margin-top: 1.4rem;
        opacity: 0; animation: fadeSlideUp 0.9s ease-out 1.5s forwards;
        width: 80vw; max-width: 700px; justify-content: center;
    }
    .q-line-seg { height: 1px; flex: 1; background: linear-gradient(90deg, transparent, rgba(0,212,255,0.4), transparent); }
    .q-line-diamond {
        width: 5px; height: 5px; background: #00d4ff; transform: rotate(45deg);
        box-shadow: 0 0 10px rgba(0,212,255,0.8);
        animation: diamondPulse 1.5s ease-in-out infinite alternate;
    }
    @keyframes diamondPulse { from { box-shadow:0 0 6px rgba(0,212,255,0.6); } to { box-shadow:0 0 18px rgba(0,212,255,1), 0 0 30px rgba(0,212,255,0.4); } }

    .q-subtitle {
        font-family: 'Rajdhani', sans-serif;
        font-size: clamp(0.8rem, 2.5vw, 1.05rem);
        font-weight: 600; letter-spacing: 0.22em;
        color: rgba(160,210,240,0.6); text-transform: uppercase;
        margin-top: 1.4rem; text-align: center;
        opacity: 0; animation: fadeSlideUp 1s ease-out 1.9s forwards; padding: 0 1rem;
    }

    .q-progress-wrap { width: min(340px, 60vw); margin-top: 2.5rem; opacity: 0; animation: fadeSlideUp 0.8s ease-out 2.5s forwards; }
    .q-progress-track { height: 1.5px; background: rgba(0,200,255,0.08); border-radius: 2px; overflow: hidden; }
    .q-progress-fill {
        height: 100%; width: 0%;
        background: linear-gradient(90deg, #00ffc8, #00d4ff, #7c3aed);
        box-shadow: 0 0 12px rgba(0,212,255,0.7);
        animation: progressLoad 3.2s cubic-bezier(0.4,0,0.2,1) 2.6s forwards;
    }
    @keyframes progressLoad { 0%{width:0%} 20%{width:15%} 45%{width:42%} 70%{width:71%} 88%{width:88%} 100%{width:100%} }

    .q-status { display:flex; align-items:center; gap:10px; margin-top:1rem; opacity:0; animation:fadeSlideUp 0.8s ease-out 2.4s forwards; }
    .q-status-dot { width:6px; height:6px; border-radius:50%; background:#00ffc8; box-shadow:0 0 10px rgba(0,255,200,0.9); animation:dotBlink 1.2s ease-in-out infinite; }
    @keyframes dotBlink { 0%,100%{opacity:1} 50%{opacity:0.3} }
    .q-status-text { font-family:'JetBrains Mono',monospace; font-size:0.8rem; letter-spacing:0.2em; color:rgba(0,255,200,0.5); text-transform:uppercase; }

    .q-corner { position:absolute; width:40px; height:40px; z-index:5; opacity:0; animation:cornerFade 1s ease-out 1s forwards; }
    .q-corner-tl { top:24px; left:24px; border-top:1.5px solid rgba(0,212,255,0.35); border-left:1.5px solid rgba(0,212,255,0.35); }
    .q-corner-tr { top:24px; right:24px; border-top:1.5px solid rgba(0,212,255,0.35); border-right:1.5px solid rgba(0,212,255,0.35); }
    .q-corner-bl { bottom:24px; left:24px; border-bottom:1.5px solid rgba(0,212,255,0.35); border-left:1.5px solid rgba(0,212,255,0.35); }
    .q-corner-br { bottom:24px; right:24px; border-bottom:1.5px solid rgba(0,212,255,0.35); border-right:1.5px solid rgba(0,212,255,0.35); }
    @keyframes cornerFade { from{opacity:0} to{opacity:1} }

    .q-streak { position:absolute; height:1px; z-index:2; pointer-events:none; opacity:0; animation:streakFly linear infinite; background:linear-gradient(90deg,transparent,rgba(0,212,255,0.6),transparent); }
    .q-streak-1{width:200px;top:25%;animation-duration:4s;animation-delay:0.5s;}
    .q-streak-2{width:140px;top:55%;animation-duration:5.5s;animation-delay:1.2s;}
    .q-streak-3{width:90px;top:75%;animation-duration:3.8s;animation-delay:2s;}
    .q-streak-4{width:180px;top:40%;animation-duration:6s;animation-delay:0.8s;right:0;animation-direction:reverse;background:linear-gradient(90deg,transparent,rgba(120,40,255,0.5),transparent);}
    @keyframes streakFly { 0%{opacity:0;transform:translateX(-300px)} 10%{opacity:1} 90%{opacity:1} 100%{opacity:0;transform:translateX(110vw)} }

    @keyframes fadeSlideUp { from{opacity:0;transform:translateY(14px)} to{opacity:1;transform:translateY(0)} }

    #q-splash.q-exit { animation: splashExit 0.9s cubic-bezier(0.4,0,0.2,1) forwards; }
    @keyframes splashExit { 0%{opacity:1;transform:scale(1)} 60%{opacity:0.8;transform:scale(1.03)} 100%{opacity:0;transform:scale(1.06);pointer-events:none} }
    </style>

    <div id="q-splash">
        <canvas id="q-canvas"></canvas>
        <div class="q-orb q-orb-1"></div>
        <div class="q-orb q-orb-2"></div>
        <div class="q-orb q-orb-3"></div>
        <div class="q-grid"></div>
        <div class="q-scanline"></div>
        <div class="q-corner q-corner-tl"></div>
        <div class="q-corner q-corner-tr"></div>
        <div class="q-corner q-corner-bl"></div>
        <div class="q-corner q-corner-br"></div>
        <div class="q-streak q-streak-1"></div>
        <div class="q-streak q-streak-2"></div>
        <div class="q-streak q-streak-3"></div>
        <div class="q-streak q-streak-4"></div>
        <div class="q-content">
            <div class="q-badge">◈ &nbsp; Neural Performance System &nbsp; ◈</div>
            <div class="q-logo-wrap">
                <div class="q-glow-ring"></div>
                <div class="q-logo">QUANTORIA</div>
            </div>
            <div class="q-logo-wrap" style="margin-top:-6px;">
                <div class="q-logo-reflection">QUANTORIA</div>
            </div>
            <div class="q-deco-line">
                <div class="q-line-seg"></div>
                <div class="q-line-diamond"></div>
                <div class="q-line-seg" style="max-width:30px;"></div>
                <div class="q-line-diamond" style="opacity:0.4;"></div>
                <div class="q-line-seg" style="max-width:60px;"></div>
                <div class="q-line-diamond" style="opacity:0.2;"></div>
                <div class="q-line-seg"></div>
            </div>
            <div class="q-subtitle">Intelligent Student Performance Prediction Engine</div>
            <div class="q-progress-wrap">
                <div class="q-progress-track">
                    <div class="q-progress-fill"></div>
                </div>
            </div>
            <div class="q-status">
                <div class="q-status-dot"></div>
                <div class="q-status-text" id="qStatusText">Initializing AI models...</div>
            </div>
        </div>
    </div>

    <script>
    (function(){
        const canvas = document.getElementById('q-canvas');
        const ctx = canvas.getContext('2d');
        let W, H, nodes = [], animId;
        const NODE_COUNT = 70, MAX_DIST = 160;
        const COLORS = ['rgba(0,180,255,','rgba(120,40,255,','rgba(0,255,200,'];

        function resize(){ W = canvas.width = window.innerWidth; H = canvas.height = window.innerHeight; }
        function initNodes(){
            nodes = [];
            for(let i=0;i<NODE_COUNT;i++){
                const t = Math.random();
                nodes.push({x:Math.random()*W,y:Math.random()*H,vx:(Math.random()-0.5)*0.4,vy:(Math.random()-0.5)*0.4,
                    r:Math.random()*1.8+0.6,ci:t<0.6?0:t<0.85?1:2,alpha:Math.random()*0.5+0.2,
                    pulse:Math.random()*Math.PI*2,ps:0.015+Math.random()*0.02});
            }
        }
        function draw(){
            ctx.clearRect(0,0,W,H);
            for(let i=0;i<nodes.length;i++){
                for(let j=i+1;j<nodes.length;j++){
                    const dx=nodes[i].x-nodes[j].x, dy=nodes[i].y-nodes[j].y;
                    const d=Math.sqrt(dx*dx+dy*dy);
                    if(d<MAX_DIST){
                        const s=1-d/MAX_DIST;
                        ctx.beginPath();
                        ctx.strokeStyle=COLORS[nodes[i].ci]+(s*0.18)+')';
                        ctx.lineWidth=s*1.2;
                        ctx.moveTo(nodes[i].x,nodes[i].y);
                        ctx.lineTo(nodes[j].x,nodes[j].y);
                        ctx.stroke();
                    }
                }
            }
            for(const n of nodes){
                n.pulse+=n.ps;
                const pa=n.alpha+Math.sin(n.pulse)*0.15;
                ctx.beginPath(); ctx.arc(n.x,n.y,n.r,0,Math.PI*2);
                ctx.fillStyle=COLORS[n.ci]+pa+')'; ctx.fill();
                if(n.r>1.8){
                    const g=ctx.createRadialGradient(n.x,n.y,0,n.x,n.y,n.r*5);
                    g.addColorStop(0,COLORS[n.ci]+(pa*0.5)+')');
                    g.addColorStop(1,COLORS[n.ci]+'0)');
                    ctx.beginPath(); ctx.arc(n.x,n.y,n.r*5,0,Math.PI*2);
                    ctx.fillStyle=g; ctx.fill();
                }
                n.x+=n.vx; n.y+=n.vy;
                if(n.x<-20)n.x=W+20; if(n.x>W+20)n.x=-20;
                if(n.y<-20)n.y=H+20; if(n.y>H+20)n.y=-20;
            }
            animId=requestAnimationFrame(draw);
        }
        resize(); initNodes(); draw();
        window.addEventListener('resize',()=>{resize();initNodes();});

        const msgs=['Initializing AI models...','Loading neural weights...','Calibrating predictors...','Configuring classifiers...','System ready.'];
        let mi=0;
        const si=document.getElementById('qStatusText');
        const iv=setInterval(()=>{ mi=Math.min(mi+1,msgs.length-1); if(si)si.textContent=msgs[mi]; if(mi===msgs.length-1)clearInterval(iv); },700);

        function dismiss(){
            const s=document.getElementById('q-splash');
            if(s) s.classList.add('q-exit');
            cancelAnimationFrame(animId);
            setTimeout(()=>{
                const docs=[document, window.parent&&window.parent.document].filter(Boolean);
                for(const d of docs){
                    const btns=d.querySelectorAll('button');
                    for(const b of btns){ if(b.innerText&&b.innerText.includes('__ENTER__')){ b.click(); return; } }
                }
            },500);
        }
        setTimeout(dismiss, 4500);
    })();
    </script>
    """, unsafe_allow_html=True)

    time.sleep(5)
    st.session_state["splash_done"] = True
    st.rerun()
# ─────────────────────────────────────────────
# TRY LOADING STREAMLIT-LOTTIE
# ─────────────────────────────────────────────
try:
    from streamlit_lottie import st_lottie
    LOTTIE_AVAILABLE = True
except ImportError:
    LOTTIE_AVAILABLE = False

def load_lottieurl(url: str):
    try:
        r = requests.get(url, timeout=5)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

# Pre-load Lottie animations (public CDN)
LOTTIE_BRAIN     = "https://assets5.lottiefiles.com/packages/lf20_fcfjwiyb.json"   # AI brain
LOTTIE_CHART     = "https://assets2.lottiefiles.com/packages/lf20_qp1q7mct.json"  # data chart
LOTTIE_ROCKET    = "https://assets9.lottiefiles.com/packages/lf20_szlepvdh.json"   # rocket / predict
LOTTIE_LOADING   = "https://assets4.lottiefiles.com/packages/lf20_usmfx6bp.json"  # loading dots
LOTTIE_SUCCESS   = "https://assets10.lottiefiles.com/packages/lf20_jbrw3hcz.json" # success checkmark
LOTTIE_WARNING   = "https://assets1.lottiefiles.com/packages/lf20_aFHJet.json"    # warning / risk


# ─────────────────────────────────────────────
# CUSTOM CSS — Futuristic Neon Dark Theme
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;700;900&family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── GLOBAL ── */
html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 18px;
    background-color: #020408;
    color: #ddeeff
}

/* ── ANIMATED GRID BACKGROUND ── */
.main .block-container {
    background:
        linear-gradient(rgba(0,255,200,0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0,255,200,0.03) 1px, transparent 1px),
        #020408;
    background-size: 60px 60px;
    padding-top: 2rem;
    padding-bottom: 5rem;
    animation: gridPan 20s linear infinite;
}
@keyframes gridPan {
    0%   { background-position: 0 0; }
    100% { background-position: 60px 60px; }
}

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #030912 0%, #060d1a 100%);
    border-right: 1px solid rgba(0,255,200,0.12);
    box-shadow: 4px 0 30px rgba(0,255,200,0.05);
}

[data-testid="stSidebar"] .stRadio label {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.25rem;
    color: #4a6580;
    padding: 0.5rem 0;
    cursor: pointer;
    transition: color 0.2s, text-shadow 0.2s;
    letter-spacing: 0.02em;
}
[data-testid="stSidebar"] .stRadio label:hover {
    color: #00ffc8;
    text-shadow: 0 0 12px rgba(0,255,200,0.6);
}

/* ── HERO TITLE ── */
.hero-title {
    font-family: 'Orbitron', monospace;
    font-size: 3.2rem;
    font-weight: 900;
    background: linear-gradient(135deg, #00ffc8, #00b4d8, #7c3aed);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.15;
    margin-bottom: 0.3rem;
    text-shadow: none;
    animation: titleGlow 4s ease-in-out infinite alternate;
    filter: drop-shadow(0 0 20px rgba(0,255,200,0.3));
}
@keyframes titleGlow {
    from { filter: drop-shadow(0 0 15px rgba(0,255,200,0.2)); }
    to   { filter: drop-shadow(0 0 35px rgba(0,180,216,0.5)); }
}

.hero-sub {
    font-size: 1.05rem;
    color: #6a9ab8;
    margin-bottom: 2.5rem;
    font-weight: 400;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    font-family: 'JetBrains Mono', monospace;
}

/* ── SECTION TITLE ── */
.section-title {
    font-family: 'Orbitron', monospace;
    font-size: 1.4rem;
    font-weight: 700;
    color: #00ffc8;
    margin-bottom: 1rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    text-shadow: 0 0 20px rgba(0,255,200,0.4);
}

/* ── GLOW CARDS ── */
.glow-card {
    background: linear-gradient(135deg, rgba(0,20,40,0.9), rgba(0,30,60,0.7));
    border: 1px solid rgba(0,255,200,0.2);
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    text-align: center;
    position: relative;
    overflow: hidden;
    transition: all 0.3s ease;
    box-shadow:
        0 0 20px rgba(0,255,200,0.05),
        inset 0 0 30px rgba(0,255,200,0.02);
}
.glow-card::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: conic-gradient(transparent, rgba(0,255,200,0.05), transparent 30%);
    animation: cardRotate 6s linear infinite;
}
@keyframes cardRotate {
    from { transform: rotate(0deg); }
    to   { transform: rotate(360deg); }
}
.glow-card:hover {
    border-color: rgba(0,255,200,0.5);
    box-shadow: 0 0 40px rgba(0,255,200,0.15), inset 0 0 40px rgba(0,255,200,0.05);
    transform: translateY(-3px);
}

.glow-card-blue {
    background: linear-gradient(135deg, rgba(0,15,35,0.9), rgba(0,30,70,0.7));
    border: 1px solid rgba(0,180,216,0.25);
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    text-align: center;
    position: relative;
    overflow: hidden;
    transition: all 0.3s ease;
    box-shadow: 0 0 20px rgba(0,180,216,0.05);
}
.glow-card-blue:hover {
    border-color: rgba(0,180,216,0.5);
    box-shadow: 0 0 40px rgba(0,180,216,0.15);
    transform: translateY(-3px);
}

.glow-card-purple {
    background: linear-gradient(135deg, rgba(15,0,40,0.9), rgba(30,0,80,0.7));
    border: 1px solid rgba(124,58,237,0.25);
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    text-align: center;
    position: relative;
    overflow: hidden;
    transition: all 0.3s ease;
    box-shadow: 0 0 20px rgba(124,58,237,0.05);
}
.glow-card-purple:hover {
    border-color: rgba(124,58,237,0.5);
    box-shadow: 0 0 40px rgba(124,58,237,0.15);
    transform: translateY(-3px);
}

.metric-value {
    font-family: 'Orbitron', monospace;
    font-size: 2.5rem;
    font-weight: 900;
    color: #00ffc8;
    line-height: 1;
    text-shadow: 0 0 20px rgba(0,255,200,0.5);
    animation: valuePulse 3s ease-in-out infinite alternate;
}
@keyframes valuePulse {
    from { text-shadow: 0 0 10px rgba(0,255,200,0.3); }
    to   { text-shadow: 0 0 30px rgba(0,255,200,0.7), 0 0 60px rgba(0,255,200,0.3); }
}

.metric-label {
    font-size: 0.88rem;
    color: #3d5a73;
    margin-top: 0.4rem;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    font-family: 'JetBrains Mono', monospace;
}

/* ── RESULT BOXES ── */
.result-pass {
    background: linear-gradient(135deg, rgba(0,30,20,0.9), rgba(0,60,40,0.7));
    border: 1px solid rgba(0,255,180,0.4);
    border-radius: 16px;
    padding: 2rem;
    text-align: center;
    box-shadow: 0 0 40px rgba(0,255,150,0.15), inset 0 0 30px rgba(0,255,150,0.05);
    animation: resultGlowGreen 2s ease-in-out infinite alternate;
}
@keyframes resultGlowGreen {
    from { box-shadow: 0 0 20px rgba(0,255,150,0.1); }
    to   { box-shadow: 0 0 50px rgba(0,255,150,0.25), 0 0 100px rgba(0,255,150,0.1); }
}

.result-fail {
    background: linear-gradient(135deg, rgba(30,0,0,0.9), rgba(60,0,0,0.7));
    border: 1px solid rgba(255,50,50,0.4);
    border-radius: 16px;
    padding: 2rem;
    text-align: center;
    box-shadow: 0 0 40px rgba(255,50,50,0.15), inset 0 0 30px rgba(255,50,50,0.05);
    animation: resultGlowRed 2s ease-in-out infinite alternate;
}
@keyframes resultGlowRed {
    from { box-shadow: 0 0 20px rgba(255,50,50,0.1); }
    to   { box-shadow: 0 0 50px rgba(255,50,50,0.25), 0 0 100px rgba(255,50,50,0.1); }
}

.result-text {
    font-family: 'Orbitron', monospace;
    font-size: 2.2rem;
    font-weight: 900;
    letter-spacing: 0.08em;
}

/* ── INFO BOX ── */
.info-box {
    background: rgba(0,20,40,0.6);
    border-left: 3px solid #00ffc8;
    border-radius: 0 12px 12px 0;
    padding: 0.85rem 1.2rem;
    margin: 0.5rem 0;
    font-size: 1rem;
    color: #a8c8e0;
    transition: all 0.2s ease;
    position: relative;
    overflow: hidden;
}
.info-box::after {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 3px;
    background: linear-gradient(180deg, #00ffc8, #00b4d8);
    box-shadow: 0 0 10px rgba(0,255,200,0.6);
}
.info-box:hover {
    background: rgba(0,255,200,0.05);
    border-left-color: #00ffc8;
    color: #94afc4;
}

/* ── RISK BADGES ── */
.badge-high {
    background: rgba(120,0,0,0.4);
    color: #ff9090;
    border: 1px solid rgba(255,50,50,0.4);
    padding: 0.3rem 1rem;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 700;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: 0.06em;
    box-shadow: 0 0 12px rgba(255,50,50,0.2);
    text-transform: uppercase;
}
.badge-medium {
    background: rgba(80,60,0,0.4);
    color: #ffe090;
    border: 1px solid rgba(255,200,0,0.4);
    padding: 0.3rem 1rem;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 700;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: 0.06em;
    box-shadow: 0 0 12px rgba(255,200,0,0.2);
    text-transform: uppercase;
}
.badge-low {
    background: rgba(0,60,30,0.4);
    color: #90ffcc;
    border: 1px solid rgba(0,255,180,0.4);
    padding: 0.3rem 1rem;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 700;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: 0.06em;
    box-shadow: 0 0 12px rgba(0,255,180,0.2);
    text-transform: uppercase;
}

/* ── DIVIDER ── */
.styled-divider {
    border: none;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(0,255,200,0.2), transparent);
    margin: 2rem 0;
}

/* ── BUTTON ── */
.stButton > button {
    background: linear-gradient(135deg, #004d3a, #003366);
    color: #00ffc8;
    border: 1px solid rgba(0,255,200,0.3);
    border-radius: 10px;
    font-family: 'Orbitron', monospace;
    font-weight: 700;
    font-size: 0.85rem;
    padding: 0.85rem 2rem;
    width: 100%;
    transition: all 0.25s ease;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    box-shadow: 0 0 20px rgba(0,255,200,0.1), inset 0 0 20px rgba(0,255,200,0.03);
    position: relative;
    overflow: hidden;
}
.stButton > button::before {
    content: '';
    position: absolute;
    top: -100%;
    left: -100%;
    width: 300%;
    height: 300%;
    background: linear-gradient(135deg, transparent, rgba(0,255,200,0.08), transparent);
    transition: all 0.4s ease;
}
.stButton > button:hover::before { top: -50%; left: -50%; }
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 0 40px rgba(0,255,200,0.3), inset 0 0 30px rgba(0,255,200,0.08);
    border-color: rgba(0,255,200,0.6);
    color: #ffffff;
}
.stButton > button:active { transform: translateY(0); }

/* ── METRICS ── */
[data-testid="stMetric"] {
    background: rgba(0,20,40,0.7);
    border: 1px solid rgba(0,255,200,0.12);
    border-radius: 12px;
    padding: 1rem;
    transition: all 0.2s ease;
    box-shadow: inset 0 0 20px rgba(0,255,200,0.02);
}
[data-testid="stMetric"]:hover {
    border-color: rgba(0,255,200,0.25);
    box-shadow: 0 0 20px rgba(0,255,200,0.08);
}
[data-testid="stMetric"] label {
    color: #a0c4d8 !important;
    font-size: 0.82rem !important;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    font-family: 'JetBrains Mono', monospace !important;
}
[data-testid="stMetricValue"] {
    font-family: 'Orbitron', monospace !important;
    font-size: 1.9rem !important;
    font-weight: 700 !important;
    color: #00ffc8 !important;
    text-shadow: 0 0 15px rgba(0,255,200,0.4) !important;
}
[data-testid="stMetricDelta"] {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.84rem !important;
}

/* ── PROGRESS BAR ── */
.stProgress > div > div > div {
    background: linear-gradient(90deg, #00ffc8, #00b4d8, #7c3aed);
    border-radius: 10px;
    box-shadow: 0 0 10px rgba(0,255,200,0.4);
    animation: progressGlow 2s ease-in-out infinite alternate;
}
@keyframes progressGlow {
    from { box-shadow: 0 0 5px rgba(0,255,200,0.3); }
    to   { box-shadow: 0 0 15px rgba(0,255,200,0.7); }
}

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(0,15,30,0.8);
    border-radius: 12px;
    gap: 4px;
    padding: 4px;
    border: 1px solid rgba(0,255,200,0.1);
}
.stTabs [data-baseweb="tab"] {
    background: transparent;
    color: #7ab0cc;
    border-radius: 8px;
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 500;
    letter-spacing: 0.04em;
    font-size: 1.05rem;
    transition: all 0.2s ease;
}
.stTabs [data-baseweb="tab"]:hover {
    color: #00ffc8;
    background: rgba(0,255,200,0.05);
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, rgba(0,80,60,0.8), rgba(0,50,100,0.8)) !important;
    color: #00ffc8 !important;
    border: 1px solid rgba(0,255,200,0.25) !important;
    box-shadow: 0 0 15px rgba(0,255,200,0.1) !important;
}

/* ── DATAFRAME ── */
.stDataFrame {
    border: 1px solid rgba(0,255,200,0.15);
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 0 20px rgba(0,255,200,0.05);
}

/* ── INPUTS ── */
.stSlider [data-baseweb="slider"] { padding-top: 0.5rem; }
.stNumberInput input {
    background: rgba(0,20,40,0.8) !important;
    border: 1px solid rgba(0,255,200,0.15) !important;
    color: #00ffc8 !important;
    border-radius: 10px !important;
    font-family: 'JetBrains Mono', monospace !important;
}
.stNumberInput input:focus {
    border-color: rgba(0,255,200,0.4) !important;
    box-shadow: 0 0 15px rgba(0,255,200,0.1) !important;
}
.stSelectbox > div > div {
    background: rgba(0,20,40,0.8) !important;
    border: 1px solid rgba(0,255,200,0.15) !important;
    border-radius: 10px !important;
}

/* ── TOOLTIP BOX ── */
.tooltip-box {
    background: rgba(0,20,40,0.7);
    border: 1px solid rgba(0,180,216,0.2);
    border-radius: 10px;
    padding: 0.75rem 1rem;
    font-size: 0.92rem;
    color: #3d6a8a;
    margin-top: 0.3rem;
    font-family: 'JetBrains Mono', monospace;
    box-shadow: inset 0 0 15px rgba(0,180,216,0.03);
}

/* ── SCANLINE OVERLAY (adds CRT effect) ── */
.main::after {
    content: '';
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background: repeating-linear-gradient(
        0deg,
        transparent,
        transparent 2px,
        rgba(0,0,0,0.03) 2px,
        rgba(0,0,0,0.03) 4px
    );
    pointer-events: none;
    z-index: 9999;
}

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #020408; }
::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, #00ffc8, #00b4d8);
    border-radius: 10px;
    box-shadow: 0 0 8px rgba(0,255,200,0.4);
}

/* ── PULSE DOT ── */
.pulse-dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    background: #00ffc8;
    box-shadow: 0 0 8px rgba(0,255,200,0.8);
    display: inline-block;
    margin-right: 6px;
    animation: dotPulse 1.5s ease-in-out infinite;
}
@keyframes dotPulse {
    0%, 100% { opacity: 1; transform: scale(1); box-shadow: 0 0 8px rgba(0,255,200,0.8); }
    50%       { opacity: 0.5; transform: scale(0.7); box-shadow: 0 0 4px rgba(0,255,200,0.4); }
}

/* ── STAT BAR ── */
.stat-bar-container {
    background: rgba(0,20,40,0.5);
    border-radius: 4px;
    height: 6px;
    margin: 0.3rem 0 0.6rem 0;
    overflow: hidden;
    border: 1px solid rgba(0,255,200,0.08);
}
.stat-bar-fill {
    height: 100%;
    border-radius: 4px;
    background: linear-gradient(90deg, #00ffc8, #00b4d8);
    box-shadow: 0 0 8px rgba(0,255,200,0.5);
    transition: width 1s cubic-bezier(0.4, 0, 0.2, 1);
}

/* ── ANIMATED COUNTER ── */
.counter-value {
    font-family: 'Orbitron', monospace;
    font-size: 1.8rem;
    font-weight: 900;
    letter-spacing: 0.05em;
}

/* ── SIDEBAR LOGO ── */
.sidebar-logo {
    font-family: 'Orbitron', monospace;
    font-size: 1.3rem;
    font-weight: 900;
    background: linear-gradient(135deg, #00ffc8, #00b4d8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    text-shadow: none;
    filter: drop-shadow(0 0 12px rgba(0,255,200,0.4));
}

/* ── DASHBOARD CARD ANIMATION ── */
@keyframes cardAppear {
    from { opacity: 0; transform: translateY(20px); }
    to   { opacity: 1; transform: translateY(0); }
}
.animated-card {
    animation: cardAppear 0.5s ease-out forwards;
}
.animated-card:nth-child(2) { animation-delay: 0.1s; }
.animated-card:nth-child(3) { animation-delay: 0.2s; }
.animated-card:nth-child(4) { animation-delay: 0.3s; }

/* ── TERMINAL TEXT STYLE ── */
.terminal-text {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    color: #00ffc8;
    opacity: 0.6;
    letter-spacing: 0.05em;
}

/* ── NEON BORDER GLOW ── */
.neon-border {
    border: 1px solid transparent;
    background:
        linear-gradient(rgba(2,4,8,0.9), rgba(2,4,8,0.9)) padding-box,
        linear-gradient(135deg, #00ffc8, #00b4d8, #7c3aed) border-box;
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1rem;
}

/* ── LOADING SHIMMER ── */
.shimmer {
    background: linear-gradient(
        90deg,
        rgba(0,255,200,0.03) 0%,
        rgba(0,255,200,0.08) 50%,
        rgba(0,255,200,0.03) 100%
    );
    background-size: 200% 100%;
    animation: shimmerAnim 2s infinite;
    border-radius: 8px;
}
@keyframes shimmerAnim {
    0%   { background-position: -200% 0; }
    100% { background-position: 200% 0; }
}

/* Override st.metric delta colors */
[data-testid="stMetricDeltaIcon-Up"]   { color: #00ffc8 !important; }
[data-testid="stMetricDeltaIcon-Down"] { color: #ff4444 !important; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# LOAD MODELS
# ─────────────────────────────────────────────
@st.cache_resource
def load_models():
    with open('model_log.pkl', 'rb') as f:
        model_log = pickle.load(f)
    with open('model_lr.pkl', 'rb') as f:
        model_lr = pickle.load(f)
    with open('scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)
    return model_log, model_lr, scaler

@st.cache_data
def load_data():
    df = pd.read_csv('student-por.csv')
    return df

model_log, model_lr, scaler = load_models()
df_raw = load_data()

FEATURES = ['G1','G2','failures','absences','studytime',
            'higher','Medu','Fedu','internet','famrel','health']
DEFAULTS = {'higher': 1, 'Medu': 2, 'Fedu': 2,
            'internet': 1, 'famrel': 4, 'health': 3}

def make_prediction(G1, G2, failures, absences, studytime):
    row = [G1, G2, failures, absences, studytime,
           DEFAULTS['higher'], DEFAULTS['Medu'], DEFAULTS['Fedu'],
           DEFAULTS['internet'], DEFAULTS['famrel'], DEFAULTS['health']]
    inp = pd.DataFrame([row], columns=FEATURES)
    inp_scaled = scaler.transform(inp)
    grade = model_lr.predict(inp)[0]
    result = model_log.predict(inp_scaled)[0]
    prob = model_log.predict_proba(inp_scaled)[0][1] * 100
    return round(grade, 1), int(result), round(prob, 1)


# ─────────────────────────────────────────────
# MATPLOTLIB STYLE DEFAULTS
# ─────────────────────────────────────────────
BG      = '#020408'
CARD_BG = '#060d1a'
SPINE   = '#0a1f35'
TXT     = '#3d5a73'
NEON    = '#00ffc8'
BLUE    = '#00b4d8'
PURPLE  = '#7c3aed'
RED     = '#ff4444'
YELLOW  = '#ffd700'

def style_ax(ax, fig):
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(CARD_BG)
    ax.spines[:].set_color(SPINE)
    ax.tick_params(colors=TXT, labelsize=8)
    for spine in ax.spines.values():
        spine.set_linewidth(0.5)


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding: 1.5rem 0 0.5rem 0;'>
        <div class='sidebar-logo'>QUANTORTA</div>
        <div style='font-size:0.75rem; color:#1a3a52; margin-top:0.2rem; font-family: JetBrains Mono, monospace; letter-spacing:0.12em;'>
            AI · PERFORMANCE SYSTEM
        </div>
    </div>
    <div style='height:1px; background: linear-gradient(90deg, rgba(0,255,200,0.3), transparent); margin-bottom:1.5rem;'></div>
    """, unsafe_allow_html=True)

    # Lottie brain animation in sidebar
    if LOTTIE_AVAILABLE:
        brain_anim = load_lottieurl(LOTTIE_BRAIN)
        if brain_anim:
            st_lottie(brain_anim, speed=0.8, height=120, key="sidebar_brain")

    page = st.radio(
        "Navigate",
        ["🌐 Overview",
         "🎯  Predict Student",
         "📊  Data Insights",
         "⚠️   Risk Classifier",
         "📈  Model Report"],
        label_visibility="collapsed"
    )

    st.markdown("<div style='height:1px; background: linear-gradient(90deg, rgba(0,255,200,0.15), transparent); margin: 1.5rem 0;'></div>", unsafe_allow_html=True)

    # Status panel
    st.markdown("""
    <div style='font-size:0.9rem; color:#1a3a52; font-family: JetBrains Mono, monospace;'>
        <div style='color:#3d8a9a; margin-bottom:0.6rem; letter-spacing:0.1em;'>SYSTEM STATUS</div>
        <div style='display:flex; align-items:center; margin-bottom:0.35rem;'>
            <span class='pulse-dot'></span>
            <span style='color:#00a8a0;'>LOGISTIC REG — ONLINE</span>
        </div>
        <div style='display:flex; align-items:center; margin-bottom:0.35rem;'>
            <span class='pulse-dot'></span>
            <span style='color:#00a878;'>LINEAR REG — ONLINE</span>
        </div>
        <div style='display:flex; align-items:center;'>
            <span class='pulse-dot'></span>
            <span style='color:#00a878;'>SCALER — ONLINE</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:1px; background: linear-gradient(90deg, rgba(0,255,200,0.1), transparent); margin: 1.2rem 0;'></div>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class='terminal-text' style='font-size:0.75rem;'>
        > DATASET: student-por.csv<br>
        > RECORDS: {len(df_raw)}<br>
        > FEATURES: 11 selected<br>
        > VERSION: 2.0.0-neon
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════
# PAGE 1 — OVERVIEW
# ═══════════════════════════════════════════════
if page == "🌐 Overview":
    # Header with Lottie
    col_head, col_anim = st.columns([2, 1])
    with col_head:
        st.markdown('<div class="hero-title">Student Performance<br>Prediction System</div>', unsafe_allow_html=True)
    with col_anim:
        if LOTTIE_AVAILABLE:
            anim = load_lottieurl(LOTTIE_CHART)
            if anim:
                st_lottie(anim, speed=1, height=130, key="overview_chart")

    # KPI strip
    total  = len(df_raw)
    passed = int((df_raw['G3'] >= 10).sum())
    failed = total - passed
    avg_g3 = round(df_raw['G3'].mean(), 1)

    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("Total Students", total)
    with c2: st.metric("Passed", passed, delta=f"{passed/total*100:.1f}%")
    with c3: st.metric("Failed", failed, delta=f"-{failed/total*100:.1f}%", delta_color="inverse")
    with c4: st.metric("Avg Final Grade", f"{avg_g3} / 20")

    st.markdown("<hr class='styled-divider'>", unsafe_allow_html=True)

    col_l, col_r = st.columns([1.2, 1])

    with col_l:
        st.markdown('<div class="section-title">System Capabilities</div>', unsafe_allow_html=True)
        items = [
            ("🎯", "Predict Exact Grade",     "Linear Regression predicts numerical final grade (0–20) with MAE of 0.73."),
            ("✅", "Classify Pass / Fail",    "Logistic Regression classifies students with 92.31% accuracy."),
            ("⚠️", "Identify At-Risk Students","Risk Classifier flags High / Medium / Low risk students dataset-wide."),
            ("📊", "Visual Data Insights",    "Interactive charts: study time, absences, failures vs. grades."),
        ]
        for icon, title, desc in items:
            st.markdown(f"""
            <div class="info-box animated-card">
                <span style='font-size:1.1rem'>{icon}</span>
                <strong style='color:#c8d6e5; margin-left:0.5rem; font-size:0.9rem'>{title}</strong><br>
                <span style='font-size:1.05rem; margin-left:1.6rem'>{desc}</span>
            </div>
            """, unsafe_allow_html=True)

    with col_r:
        st.markdown('<div class="section-title">Model Performance</div>', unsafe_allow_html=True)

        metrics = [
            ("92.3%", "Classification Accuracy", "glow-card", "#00ffc8"),
            ("0.73",  "Mean Absolute Error",      "glow-card-blue", "#00b4d8"),
            ("93.2%", "P(Pass | High Study)",     "glow-card-purple", "#a78bfa"),
        ]
        for val, label, cls, color in metrics:
            st.markdown(f"""
            <div class="{cls}">
                <div class="metric-value" style="color:{color}">{val}</div>
                <div class="metric-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<hr class='styled-divider'>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">Project Pipeline</div>', unsafe_allow_html=True)

    steps  = ["Data\nLoading", "Preprocessing\n& Encoding",
              "Feature\nSelection", "EDA &\nVisualization", "Model\nTraining", "Evaluation", "Prediction\nSystem"]
    colors = [NEON, "#00b4d8", "#0ea5e9", "#6366f1", "#8b5cf6", "#a855f7", "#34d399"]

    fig, ax = plt.subplots(figsize=(14, 3.2))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(0, len(steps) * 2)
    ax.set_ylim(0, 2)
    ax.axis('off')

    for i, (s, c) in enumerate(zip(steps, colors)):
        x = i * 2 + 1
        rect = FancyBboxPatch((x - 0.75, 0.3), 1.5, 1.2,
                              boxstyle="round,pad=0.12",
                              fc=c + "18", ec=c, linewidth=1.5,
                              zorder=2)
        ax.add_patch(rect)
        # glow rectangle behind
        glow = FancyBboxPatch((x - 0.78, 0.27), 1.56, 1.26,
                               boxstyle="round,pad=0.12",
                               fc='none', ec=c + "40", linewidth=4,
                               zorder=1)
        ax.add_patch(glow)
        ax.text(x, 0.95, s, ha='center', va='center', fontsize=10,
                color='#00ffc8', fontweight='bold', multialignment='center',
                zorder=3, fontfamily='monospace')
        ax.text(x, 0.1, f'0{i+1}', ha='center', va='center', fontsize=8,
                color=c, fontweight='bold', alpha=0.8, fontfamily='monospace')
        if i < len(steps) - 1:
           ax.annotate("", xy=(x + 0.88, 0.95), xytext=(x + 0.78, 0.95),
                        arrowprops=dict(arrowstyle="->", color=c+"80", lw=1.5))

    plt.tight_layout(pad=0)
    st.pyplot(fig)
    plt.close()

    # Quick stats dashboard row
    st.markdown("<hr class='styled-divider'>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">Quick Dataset Stats</div>', unsafe_allow_html=True)

    s1, s2, s3, s4, s5 = st.columns(5)
    stats = [
        ("Avg G1", f"{df_raw['G1'].mean():.1f}"),
        ("Avg G2", f"{df_raw['G2'].mean():.1f}"),
        ("Avg Absences", f"{df_raw['absences'].mean():.1f}"),
        ("Avg Study Time", f"{df_raw['studytime'].mean():.1f}"),
        ("Zero Failures", f"{(df_raw['failures']==0).sum()}"),
    ]
    for col, (label, val) in zip([s1,s2,s3,s4,s5], stats):
        with col:
            st.metric(label, val)


# ═══════════════════════════════════════════════
# PAGE 2 — PREDICT STUDENT
# ═══════════════════════════════════════════════
elif page == "🎯  Predict Student":
    col_head, col_anim = st.columns([2.5, 1])
    with col_head:
        st.markdown('<div class="hero-title">Predict Performance</div>', unsafe_allow_html=True)
        st.markdown('<div class="hero-sub">Enter student parameters · Run AI inference · Get instant results</div>', unsafe_allow_html=True)
    with col_anim:
        if LOTTIE_AVAILABLE:
            anim = load_lottieurl(LOTTIE_ROCKET)
            if anim:
                st_lottie(anim, speed=1, height=120, key="predict_rocket")

    st.markdown("<hr class='styled-divider'>", unsafe_allow_html=True)

    col_inp, col_out = st.columns([1.1, 1])

    with col_inp:
        st.markdown('<div class="section-title">📡 Input Parameters</div>', unsafe_allow_html=True)

        st.markdown('<div class="tooltip-box">▸ G1 and G2 are period grades (0–20) — strongest predictors in the model.</div>', unsafe_allow_html=True)
        G1 = st.slider("G1 — First Period Grade",  0, 20, 10)
        G2 = st.slider("G2 — Second Period Grade", 0, 20, 11)

        # Mini grade trend visualizer
        delta = G2 - G1
        trend_color = "#00ffc8" if delta > 0 else ("#ff4444" if delta < 0 else "#ffd700")
        trend_icon  = "▲" if delta > 0 else ("▼" if delta < 0 else "●")
        st.markdown(f"""
        <div style='background:rgba(0,20,40,0.5); border:1px solid rgba(0,255,200,0.1); border-radius:8px;
                    padding:0.5rem 1rem; margin:0.3rem 0 0.8rem 0; display:flex; justify-content:space-between;'>
            <span class='terminal-text'>GRADE TRAJECTORY</span>
            <span style='font-family: Orbitron, monospace; font-size:0.9rem; color:{trend_color};
                         font-weight:700; text-shadow: 0 0 10px {trend_color}50;'>
                {trend_icon} {abs(delta):+d} pts  G1→G2
            </span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="tooltip-box">▸ 1 = &lt;2 hrs/wk · 2 = 2–5 hrs · 3 = 5–10 hrs · 4 = &gt;10 hrs/wk</div>', unsafe_allow_html=True)
        studytime = st.select_slider(
            "Weekly Study Time",
            options=[1, 2, 3, 4], value=2,
            format_func=lambda x: {1:"< 2 hrs", 2:"2–5 hrs", 3:"5–10 hrs", 4:"> 10 hrs"}[x]
        )

        failures = st.select_slider(
            "Previous Class Failures",
            options=[0, 1, 2, 3], value=0,
            format_func=lambda x: f"{x} failure{'s' if x != 1 else ''}"
        )

        absences = st.number_input("Number of Absences", 0, 93, 2)

        st.markdown("<br>", unsafe_allow_html=True)
        predict_btn = st.button("⚡  INITIALIZE PREDICTION", use_container_width=True)

    with col_out:
        st.markdown('<div class="section-title">🧠 AI Output</div>', unsafe_allow_html=True)

        if predict_btn:
            # Loading animation
            if LOTTIE_AVAILABLE:
                loading_anim = load_lottieurl(LOTTIE_LOADING)
                if loading_anim:
                    placeholder = st.empty()
                    with placeholder:
                        st_lottie(loading_anim, speed=2, height=80, key="loading")
                    import time; time.sleep(1.2)
                    placeholder.empty()

            grade, result, prob = make_prediction(G1, G2, failures, absences, studytime)
            trend = "📈 Improving" if G2 > G1 else ("📉 Declining" if G2 < G1 else "➡️ Stable")

            # Result card + optional Lottie
            col_res, col_res_anim = st.columns([2, 1])
            with col_res:
                if result == 1:
                    st.markdown(f"""
                    <div class="result-pass">
                        <div class="result-text" style="color:#00ffc8">✅ PASS</div>
                        <div style="color:#00b4a0; margin-top:0.4rem; font-size:0.82rem;
                                    font-family: JetBrains Mono, monospace;">
                            CLASSIFICATION: PASSING
                        </div>
                    </div>""", unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="result-fail">
                        <div class="result-text" style="color:#ff4444">❌ FAIL</div>
                        <div style="color:#cc3333; margin-top:0.4rem; font-size:0.82rem;
                                    font-family: JetBrains Mono, monospace;">
                            CLASSIFICATION: AT RISK
                        </div>
                    </div>""", unsafe_allow_html=True)
            with col_res_anim:
                if LOTTIE_AVAILABLE:
                    anim_url = LOTTIE_SUCCESS if result == 1 else LOTTIE_WARNING
                    anim_data = load_lottieurl(anim_url)
                    if anim_data:
                        st_lottie(anim_data, speed=1, height=90, key="result_anim")

            st.markdown("<br>", unsafe_allow_html=True)

            m1, m2, m3 = st.columns(3)
            m1.metric("Predicted Grade", f"{grade} / 20")
            m2.metric("Pass Probability", f"{prob}%")
            m3.metric("Trend", trend)

            st.markdown("<br>", unsafe_allow_html=True)

            # Probability gauge
            st.markdown(f"""
            <div class='terminal-text' style='margin-bottom:0.3rem;'>
                PASS PROBABILITY — {prob}%
            </div>
            """, unsafe_allow_html=True)
            st.progress(int(prob) / 100)

            # Animated probability display
            prob_color = "#00ffc8" if prob >= 75 else ("#ffd700" if prob >= 50 else "#ff4444")
            st.markdown(f"""
            <div style='text-align:center; font-family:Orbitron,monospace; font-size:1.8rem;
                        font-weight:900; color:{prob_color};
                        text-shadow: 0 0 20px {prob_color}60;
                        animation: valuePulse 3s ease-in-out infinite alternate;
                        margin:0.5rem 0;'>
                {prob}%
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # Risk badge
            if prob < 50:
                st.markdown('<span class="badge-high">⬥ HIGH RISK — Immediate Intervention Required</span>', unsafe_allow_html=True)
            elif prob < 75:
                st.markdown('<span class="badge-medium">⬥ MEDIUM RISK — Monitor Closely</span>', unsafe_allow_html=True)
            else:
                st.markdown('<span class="badge-low">⬥ LOW RISK — Performing Well</span>', unsafe_allow_html=True)

            # Grade comparison chart
            st.markdown("<br>", unsafe_allow_html=True)
            fig, ax = plt.subplots(figsize=(5, 2.8))
            style_ax(ax, fig)

            bar_colors = [PURPLE, BLUE, NEON]
            bars = ax.barh(['G1', 'G2', 'Predicted\nG3'],
                           [G1, G2, grade],
                           color=bar_colors, height=0.45, edgecolor='none')
            # glow effect via duplicate bars
            for bar, c in zip(bars, bar_colors):
                ax.barh(bar.get_y() + bar.get_height()/2,
                        bar.get_width(), height=0.55,
                        color=c+"20", edgecolor=c+"40", linewidth=0.8,
                        left=0, align='center')

            ax.set_xlim(0, 21)
            ax.set_xlabel('Grade', color=TXT, fontsize=8)
            ax.tick_params(colors=TXT, labelsize=8)
            for bar, val, c in zip(bars, [G1, G2, grade], bar_colors):
                ax.text(val + 0.3, bar.get_y() + bar.get_height()/2,
                        f'{val}', va='center', color=c, fontsize=9,
                        fontweight='bold', fontfamily='monospace')
            ax.axvline(x=10, color=RED, linestyle='--', linewidth=1, alpha=0.5, label='Pass Line (10)')
            ax.legend(facecolor=CARD_BG, edgecolor=SPINE, labelcolor=TXT, fontsize=7)
            ax.set_title("Grade Progression", color='#c8d6e5', fontsize=10,
                         pad=6, fontfamily='monospace')
            plt.tight_layout()
            st.pyplot(fig)
            plt.close()

        else:
            # Placeholder with animated Lottie
            if LOTTIE_AVAILABLE:
                anim = load_lottieurl(LOTTIE_BRAIN)
                if anim:
                    st_lottie(anim, speed=0.7, height=160, key="predict_idle")

            st.markdown("""
            <div style='text-align:center; padding:2rem 2rem 1rem 2rem; color:#1a3a52;
                        border:1px dashed rgba(0,255,200,0.1); border-radius:16px;'>
                <div style='font-family:Orbitron,monospace; font-size:1rem; color:#1e4d66;
                            letter-spacing:0.1em;'>
                    AWAITING INPUT
                </div>
                <div class='terminal-text' style='margin-top:0.5rem; font-size:0.72rem;'>
                    > Configure parameters and run prediction
                </div>
            </div>
            """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════
# PAGE 3 — DATA INSIGHTS
# ═══════════════════════════════════════════════
elif page == "📊  Data Insights":
    col_head, col_anim = st.columns([2.5, 1])
    with col_head:
        st.markdown('<div class="hero-title">Data Insights</div>', unsafe_allow_html=True)
        st.markdown('<div class="hero-sub">Exploratory analysis · Portuguese student dataset · 649 records</div>', unsafe_allow_html=True)
    with col_anim:
        if LOTTIE_AVAILABLE:
            anim = load_lottieurl(LOTTIE_CHART)
            if anim:
                st_lottie(anim, speed=0.9, height=120, key="insights_anim")

    st.markdown("<hr class='styled-divider'>", unsafe_allow_html=True)

    df_vis = df_raw.copy()
    df_vis['result'] = (df_vis['G3'] >= 10).astype(int)
    passed_df = df_vis[df_vis['result'] == 1]
    failed_df = df_vis[df_vis['result'] == 0]

    tab1, tab2, tab3, tab4 = st.tabs(["📈 Grade Distribution", "⏱ Study Time", "🚪 Absences", "❌ Failures"])

    with tab1:
        fig, axes = plt.subplots(1, 2, figsize=(14, 4.5))
        fig.patch.set_facecolor(BG)
        for ax in axes:
            style_ax(ax, fig)

        # Histogram with gradient-like bars
        n, bins, patches = axes[0].hist(df_vis['G3'], bins=20, edgecolor='none', alpha=0.0)
        axes[0].hist(df_vis['G3'], bins=20, color=PURPLE, edgecolor=BG, alpha=0.75, linewidth=0.5)
        # Neon outline
        axes[0].hist(df_vis['G3'], bins=20, edgecolor=PURPLE, linewidth=0.8, histtype='step', fill=False)
        axes[0].axvline(10, color=RED, linestyle='--', lw=1.5, label='Pass threshold (10)', alpha=0.7)
        axes[0].set_title('Final Grade Distribution', color='#c8d6e5', fontsize=11, fontfamily='monospace')
        axes[0].set_xlabel('Grade (0–20)', color=TXT, fontsize=9)
        axes[0].set_ylabel('# Students', color=TXT, fontsize=9)
        axes[0].legend(facecolor=CARD_BG, edgecolor=SPINE, labelcolor=TXT, fontsize=8)

        # Donut chart
        sizes  = [len(passed_df), len(failed_df)]
        labels = [f'Pass\n{len(passed_df)}', f'Fail\n{len(failed_df)}']
        wedge_colors = [NEON, RED]
        wedges, texts, autotexts = axes[1].pie(
            sizes, labels=labels, colors=wedge_colors,
            autopct='%1.1f%%', startangle=90,
            textprops={'color': TXT, 'fontsize': 9, 'fontfamily': 'monospace'},
            wedgeprops={'edgecolor': BG, 'linewidth': 3, 'width': 0.65})  # donut
        for at in autotexts:
            at.set_color('white'); at.set_fontweight('bold'); at.set_fontsize(9)
        axes[1].set_title('Pass / Fail Ratio', color='#c8d6e5', fontsize=11, fontfamily='monospace')
        # Center label
        axes[1].text(0, 0, f'{len(df_vis)}\nSTUDENTS', ha='center', va='center',
                     color=NEON, fontsize=9, fontweight='bold', fontfamily='monospace')

        plt.tight_layout()
        st.pyplot(fig); plt.close()

        # Summary metrics below chart
        total_s = len(df_vis)
        s1, s2, s3, s4 = st.columns(4)
        s1.metric("Pass Rate",     f"{len(passed_df)/total_s*100:.1f}%")
        s2.metric("Fail Rate",     f"{len(failed_df)/total_s*100:.1f}%")
        s3.metric("Mean G3",       f"{df_vis['G3'].mean():.1f}")
        s4.metric("Std Dev G3",    f"{df_vis['G3'].std():.1f}")

    with tab2:
        study_pass   = df_vis.groupby('studytime')['result'].mean() * 100
        study_labels = {1:'<2 hrs', 2:'2–5 hrs', 3:'5–10 hrs', 4:'>10 hrs'}

        fig, ax = plt.subplots(figsize=(10, 4.5))
        style_ax(ax, fig)

        bar_c = [PURPLE+"cc", BLUE+"cc", "#0ea5e9cc", NEON+"cc"]
        bars  = ax.bar(range(1, 5), study_pass.values,
                       color=bar_c, edgecolor='none', width=0.55)
        # Glow beneath each bar
        for bar, c in zip(bars, bar_c):
            ax.bar(bar.get_x() + bar.get_width()/2, bar.get_height(),
                   width=bar.get_width()*1.3, color=c[:7]+"22",
                   edgecolor='none', align='center')

        for bar, val in zip(bars, study_pass.values):
            ax.text(bar.get_x() + bar.get_width()/2, val + 0.5,
                    f'{val:.1f}%', ha='center', va='bottom',
                    color='white', fontsize=9, fontweight='bold', fontfamily='monospace')
        ax.set_xticks(range(1, 5))
        ax.set_xticklabels([study_labels[i] for i in range(1, 5)], color=TXT, fontfamily='monospace')
        ax.set_xlabel('Weekly Study Time', color=TXT, fontsize=9)
        ax.set_ylabel('Pass Rate (%)', color=TXT, fontsize=9)
        ax.set_title('Study Time vs Pass Rate', color='#c8d6e5', fontsize=11, fontfamily='monospace')
        ax.set_ylim(0, 108)
        avg_pass = (df_vis['result'].mean() * 100)
        ax.axhline(y=avg_pass, color=RED, linestyle='--', lw=1, alpha=0.5, label=f'Avg pass rate ({avg_pass:.1f}%)')
        ax.legend(facecolor=CARD_BG, edgecolor=SPINE, labelcolor=TXT, fontsize=8)

        plt.tight_layout()
        st.pyplot(fig); plt.close()

        c1, c2, c3 = st.columns(3)
        c1.metric("Pass Rate (Low Study <2h)",  f"{study_pass[1]:.1f}%")
        c2.metric("Pass Rate (Mid Study 2-5h)", f"{study_pass[2]:.1f}%")
        c3.metric("Pass Rate (High Study >10h)", f"{study_pass[4]:.1f}%",
                  delta=f"+{study_pass[4]-study_pass[1]:.1f}%")

    with tab3:
        fig, ax = plt.subplots(figsize=(10, 4.5))
        style_ax(ax, fig)

        bp = ax.boxplot(
            [failed_df['absences'], passed_df['absences']],
            labels=['FAILED', 'PASSED'],
            patch_artist=True,
            medianprops=dict(color='white', lw=2),
            whiskerprops=dict(color=TXT, lw=1),
            capprops=dict(color=TXT, lw=1),
            flierprops=dict(marker='o', color=TXT, alpha=0.3, markersize=3))
        bp['boxes'][0].set_facecolor(RED+"22")
        bp['boxes'][0].set_edgecolor(RED)
        bp['boxes'][1].set_facecolor(NEON+"22")
        bp['boxes'][1].set_edgecolor(NEON)

        for tick in ax.get_xticklabels():
            tick.set_fontfamily('monospace')
        ax.set_title('Absences: Passed vs Failed', color='#c8d6e5', fontsize=11, fontfamily='monospace')
        ax.set_ylabel('Number of Absences', color=TXT, fontsize=9)

        plt.tight_layout()
        st.pyplot(fig); plt.close()

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Avg Absences (Failed)", f"{failed_df['absences'].mean():.1f}")
        c2.metric("Avg Absences (Passed)", f"{passed_df['absences'].mean():.1f}")
        c3.metric("Max Absences",          f"{df_vis['absences'].max()}")
        c4.metric("Zero Absences",         f"{(df_vis['absences']==0).sum()}")

    with tab4:
        fail_rate = df_vis.groupby('failures')['result'].mean() * 100
        fig, ax   = plt.subplots(figsize=(10, 4.5))
        style_ax(ax, fig)

        bar_colors_f = [NEON+"cc", YELLOW+"cc", "#f97316cc", RED+"cc"]
        bars = ax.bar(fail_rate.index, fail_rate.values,
                      color=bar_colors_f[:len(fail_rate)], edgecolor='none', width=0.45)
        for bar, val, c in zip(bars, fail_rate.values, bar_colors_f):
            ax.text(bar.get_x() + bar.get_width()/2, val + 0.5,
                    f'{val:.1f}%', ha='center', va='bottom',
                    color='white', fontsize=10, fontweight='bold', fontfamily='monospace')
            ax.bar(bar.get_x() + bar.get_width()/2, bar.get_height(),
                   width=bar.get_width()*1.3, color=c[:7]+"18",
                   edgecolor='none', align='center')

        ax.set_xticks(fail_rate.index)
        ax.set_xticklabels([f'{i} failure{"s" if i!=1 else ""}' for i in fail_rate.index],
                           color=TXT, fontfamily='monospace')
        ax.set_ylabel('Pass Rate (%)', color=TXT, fontsize=9)
        ax.set_title('Previous Failures vs Pass Rate', color='#c8d6e5', fontsize=11, fontfamily='monospace')
        ax.set_ylim(0, 108)

        plt.tight_layout()
        st.pyplot(fig); plt.close()

        cols = st.columns(len(fail_rate))
        for col, (f_val, rate) in zip(cols, fail_rate.items()):
            col.metric(f"{f_val} Failure{'s' if f_val!=1 else ''}", f"{rate:.1f}%")


# ═══════════════════════════════════════════════
# PAGE 4 — RISK CLASSIFIER
# ═══════════════════════════════════════════════
elif page == "⚠️   Risk Classifier":
    col_head, col_anim = st.columns([2.5, 1])
    with col_head:
        st.markdown('<div class="hero-title">Risk Classifier</div>', unsafe_allow_html=True)
        st.markdown('<div class="hero-sub">Real-time risk assessment · Full dataset scan · Priority triage</div>', unsafe_allow_html=True)
    with col_anim:
        if LOTTIE_AVAILABLE:
            anim = load_lottieurl(LOTTIE_WARNING)
            if anim:
                st_lottie(anim, speed=1, height=120, key="risk_anim")

    st.markdown("<hr class='styled-divider'>", unsafe_allow_html=True)

    # Preprocess for risk
    df_risk = df_raw.copy()
    df_risk['result'] = (df_risk['G3'] >= 10).astype(int)

    binary_cols = ['school','sex','address','famsize','Pstatus',
                   'schoolsup','famsup','paid','activities','nursery',
                   'higher','internet','romantic']
    binary_map  = {'yes':1,'no':0,'M':1,'F':0,'U':1,'R':0,'GT3':1,'LE3':0,
                   'T':1,'A':0,'GP':1,'MS':0}
    for col in binary_cols:
        if col in df_risk.columns:
            df_risk[col] = df_risk[col].map(binary_map)

    multi_cols = ['Mjob','Fjob','reason','guardian']
    df_risk    = pd.get_dummies(df_risk, columns=multi_cols, drop_first=True)
    df_risk_ft = df_risk[FEATURES].copy()

    X_risk_scaled = scaler.transform(df_risk_ft)
    probs         = model_log.predict_proba(X_risk_scaled)[:, 1] * 100

    def assign_risk(p):
        if p < 50: return 'High Risk'
        elif p < 75: return 'Medium Risk'
        return 'Low Risk'

    risk_df = pd.DataFrame({
        'Student':      range(1, len(probs)+1),
        'G1':           df_raw['G1'].values,
        'G2':           df_raw['G2'].values,
        'Failures':     df_raw['failures'].values,
        'Absences':     df_raw['absences'].values,
        'Pass Prob (%)':np.round(probs, 1),
        'Actual':       (df_raw['G3'] >= 10).map({True: 'Pass', False: 'Fail'}).values,
        'Risk':         [assign_risk(p) for p in probs]
    })

    low_n  = (risk_df['Risk'] == 'Low Risk').sum()
    mid_n  = (risk_df['Risk'] == 'Medium Risk').sum()
    high_n = (risk_df['Risk'] == 'High Risk').sum()

    # KPI row with glowing cards
    k1, k2, k3 = st.columns(3)
    with k1:
        st.markdown(f"""
        <div class="glow-card" style="border-color:rgba(0,255,200,0.3);">
            <div class="metric-value" style="color:{NEON}">{low_n}</div>
            <div class="metric-label">🟢 Low Risk Students</div>
            <div style="font-family:JetBrains Mono,monospace; font-size:0.7rem; color:#1a4a3a; margin-top:0.4rem;">
                {low_n/len(risk_df)*100:.1f}% of cohort
            </div>
        </div>
        """, unsafe_allow_html=True)
    with k2:
        st.markdown(f"""
        <div class="glow-card-blue" style="border-color:rgba(255,200,0,0.3);">
            <div class="metric-value" style="color:{YELLOW}">{mid_n}</div>
            <div class="metric-label">🟡 Medium Risk Students</div>
            <div style="font-family:JetBrains Mono,monospace; font-size:0.7rem; color:#4a4a1a; margin-top:0.4rem;">
                {mid_n/len(risk_df)*100:.1f}% of cohort
            </div>
        </div>
        """, unsafe_allow_html=True)
    with k3:
        st.markdown(f"""
        <div class="glow-card-purple" style="border-color:rgba(255,50,50,0.3);">
            <div class="metric-value" style="color:{RED}">{high_n}</div>
            <div class="metric-label">🔴 High Risk Students</div>
            <div style="font-family:JetBrains Mono,monospace; font-size:0.7rem; color:#4a1a1a; margin-top:0.4rem;">
                {high_n/len(risk_df)*100:.1f}% of cohort — needs intervention
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr class='styled-divider'>", unsafe_allow_html=True)

    col_chart, col_scatter = st.columns(2)

    with col_chart:
        st.markdown('<div class="section-title">Risk Distribution</div>', unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(5, 4.5))
        fig.patch.set_facecolor(BG)
        ax.set_facecolor(BG)
        sizes       = [low_n, mid_n, high_n]
        labels_risk = ['Low Risk', 'Medium Risk', 'High Risk']
        colors_pie  = [NEON, YELLOW, RED]
        wedges, texts, autotexts = ax.pie(
            sizes, labels=labels_risk, colors=colors_pie,
            autopct='%1.1f%%', startangle=90,
            textprops={'color': TXT, 'fontsize': 8.5, 'fontfamily': 'monospace'},
            wedgeprops={'edgecolor': BG, 'linewidth': 3, 'width': 0.65},
            pctdistance=0.8)
        for at in autotexts:
            at.set_color('white'); at.set_fontweight('bold')
        ax.text(0, 0, f'{len(risk_df)}\nSTUDENTS', ha='center', va='center',
                color=NEON, fontsize=9, fontweight='bold', fontfamily='monospace')
        ax.set_title('Cohort Risk Split', color='#c8d6e5', fontsize=10, fontfamily='monospace')
        plt.tight_layout()
        st.pyplot(fig); plt.close()

    with col_scatter:
        st.markdown('<div class="section-title">Risk Probability Map</div>', unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(6, 4.5))
        style_ax(ax, fig)

        color_map = {'High Risk': RED, 'Medium Risk': YELLOW, 'Low Risk': NEON}
        for risk, color in color_map.items():
            sub = risk_df[risk_df['Risk'] == risk]
            ax.scatter(sub['Student'], sub['Pass Prob (%)'],
                       c=color, alpha=0.5, s=15, label=risk,
                       edgecolors=color+"80", linewidths=0.3)
        ax.axhline(50, color=RED,    linestyle='--', lw=0.8, alpha=0.5)
        ax.axhline(75, color=YELLOW, linestyle='--', lw=0.8, alpha=0.5)
        ax.fill_between([0, len(risk_df)+1], 0,  50, alpha=0.03, color=RED)
        ax.fill_between([0, len(risk_df)+1], 50, 75, alpha=0.03, color=YELLOW)
        ax.fill_between([0, len(risk_df)+1], 75, 100, alpha=0.03, color=NEON)
        ax.set_xlabel('Student ID', color=TXT, fontsize=8)
        ax.set_ylabel('Pass Probability (%)', color=TXT, fontsize=8)
        ax.set_title('All Students Risk Map', color='#c8d6e5', fontsize=10, fontfamily='monospace')
        ax.legend(facecolor=CARD_BG, edgecolor=SPINE, labelcolor=TXT, fontsize=7)
        plt.tight_layout()
        st.pyplot(fig); plt.close()

    st.markdown("<hr class='styled-divider'>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">Student Risk Table</div>', unsafe_allow_html=True)

    risk_filter = st.selectbox("Filter by Risk Level",
                               ["High Risk", "Medium Risk", "Low Risk", "All"])
    display_df  = risk_df if risk_filter == "All" else risk_df[risk_df['Risk'] == risk_filter]
    st.dataframe(
        display_df.head(30).reset_index(drop=True),
        use_container_width=True, height=380
    )
    st.markdown(f"""
    <div class='terminal-text' style='margin-top:0.4rem;'>
        > SHOWING TOP 30 OF {len(display_df)} STUDENTS
        · FILTER: {risk_filter.upper()}
        · THRESHOLD: &lt;50% = HIGH · 50-75% = MEDIUM · &gt;75% = LOW
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════
# PAGE 5 — MODEL REPORT
# ═══════════════════════════════════════════════
elif page == "📈  Model Report":
    col_head, col_anim = st.columns([2.5, 1])
    with col_head:
        st.markdown('<div class="hero-title">Model Report</div>', unsafe_allow_html=True)
        st.markdown('<div class="hero-sub">Full evaluation · Linear Regression · Logistic Regression · Feature analysis</div>', unsafe_allow_html=True)
    with col_anim:
        if LOTTIE_AVAILABLE:
            anim = load_lottieurl(LOTTIE_CHART)
            if anim:
                st_lottie(anim, speed=0.8, height=120, key="report_anim")

    st.markdown("<hr class='styled-divider'>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:
        st.markdown('<div class="section-title">⬡ Logistic Regression</div>', unsafe_allow_html=True)
        for val, label, color, cls in [
            ("92.31%", "Accuracy (Selected 11 Features)", NEON,   "glow-card"),
            ("90.77%", "Accuracy (All 41 Features)",      BLUE,   "glow-card-blue"),
        ]:
            st.markdown(f"""
            <div class="{cls}">
                <div class="metric-value" style="color:{color}">{val}</div>
                <div class="metric-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        for label, val in [("Precision (Pass)", "96%"), ("Recall (Pass)", "96%"),
                            ("F1 Score (Pass)", "96%"), ("Precision (Fail)", "67%"),
                            ("Recall (Fail)", "69%")]:
            bar_w = int(val.replace('%',''))
            st.markdown(f"""
            <div class="info-box">
                <strong style="color:#c8d6e5; font-size:0.95rem">{label}</strong>
                <span style="float:right; color:{NEON}; font-weight:700;
                             font-family:Orbitron,monospace; font-size:0.85rem">{val}</span>
            </div>
            <div class="stat-bar-container">
                <div class="stat-bar-fill" style="width:{bar_w}%"></div>
            </div>
            """, unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="section-title">⬡ Linear Regression</div>', unsafe_allow_html=True)
        for val, label, color, cls in [
            ("0.73", "MAE — Selected Features", "#a78bfa", "glow-card-purple"),
            ("1.17", "RMSE",                    BLUE,      "glow-card-blue"),
        ]:
            st.markdown(f"""
            <div class="{cls}">
                <div class="metric-value" style="color:{color}">{val}</div>
                <div class="metric-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        for label, val, color in [
            ("All Features MAE",       "0.77",  BLUE),
            ("Selected Features MAE",  "0.73",  NEON),
            ("Improvement",            "5.2%",  NEON),
            ("Grade Range",            "0–20",  TXT),
            ("Training Split",         "80/20", TXT),
        ]:
            st.markdown(f"""
            <div class="info-box">
                <strong style="color:#c8d6e5; font-size:1rem">{label}</strong>
                <span style="float:right; color:{color}; font-weight:700;
                             font-family:Orbitron,monospace; font-size:1rem">{val}</span>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<hr class='styled-divider'>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">Feature Selection Impact</div>', unsafe_allow_html=True)

    fig, axes = plt.subplots(1, 2, figsize=(13, 4.2))
    fig.patch.set_facecolor(BG)
    for ax in axes: style_ax(ax, fig)

    # Accuracy comparison
    bars0 = axes[0].bar(['All Features\n(41)', 'Selected\n(11)'],
                        [90.77, 92.31],
                        color=[PURPLE+"cc", NEON+"cc"], edgecolor='none', width=0.45)
    for bar, c in zip(bars0, [PURPLE, NEON]):
        axes[0].bar(bar.get_x() + bar.get_width()/2, bar.get_height(),
                    width=bar.get_width()*1.3, color=c+"18",
                    edgecolor='none', align='center')
    axes[0].set_ylim(88, 94)
    axes[0].set_ylabel('Accuracy (%)', color=TXT, fontsize=9)
    axes[0].set_title('Logistic Regression Accuracy', color='#c8d6e5', fontsize=10, fontfamily='monospace')
    for i, v in enumerate([90.77, 92.31]):
        axes[0].text(i, v + 0.04, f'{v}%', ha='center', va='bottom',
                     color='white', fontweight='bold', fontsize=9, fontfamily='monospace')
    for t in axes[0].get_xticklabels(): t.set_fontfamily('monospace')

    # MAE comparison
    bars1 = axes[1].bar(['All Features\n(41)', 'Selected\n(11)'],
                        [0.77, 0.73],
                        color=[PURPLE+"cc", NEON+"cc"], edgecolor='none', width=0.45)
    for bar, c in zip(bars1, [PURPLE, NEON]):
        axes[1].bar(bar.get_x() + bar.get_width()/2, bar.get_height(),
                    width=bar.get_width()*1.3, color=c+"18",
                    edgecolor='none', align='center')
    axes[1].set_ylim(0.68, 0.82)
    axes[1].set_ylabel('MAE (lower = better)', color=TXT, fontsize=9)
    axes[1].set_title('Linear Regression MAE', color='#c8d6e5', fontsize=10, fontfamily='monospace')
    for i, v in enumerate([0.77, 0.73]):
        axes[1].text(i, v + 0.002, f'{v}', ha='center', va='bottom',
                     color='white', fontweight='bold', fontsize=9, fontfamily='monospace')
    for t in axes[1].get_xticklabels(): t.set_fontfamily('monospace')

    plt.tight_layout()
    st.pyplot(fig); plt.close()

    st.markdown("<hr class='styled-divider'>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">Bayesian Probability Analysis</div>', unsafe_allow_html=True)

    b1, b2 = st.columns(2)
    with b1:
        st.markdown(f"<div class='terminal-text' style='margin-bottom:0.6rem;'>> STUDY TIME vs PASS PROBABILITY</div>", unsafe_allow_html=True)
        for study, prob_val in [(1, 76.4), (2, 86.6), (3, 92.8), (4, 94.3)]:
            label  = {1:'&lt;2 hrs', 2:'2–5 hrs', 3:'5–10 hrs', 4:'&gt;10 hrs'}[study]
            p_color = NEON if prob_val > 85 else BLUE
            st.markdown(f"""
            <div class="info-box">
                <span style="font-family:JetBrains Mono,monospace">{label}</span>
                <span style="float:right; color:{p_color}; font-weight:700;
                             font-family:Orbitron,monospace">{prob_val}%</span>
            </div>
            <div class="stat-bar-container">
                <div class="stat-bar-fill" style="width:{prob_val}%; background:linear-gradient(90deg,{PURPLE},{p_color});"></div>
            </div>
            """, unsafe_allow_html=True)

    with b2:
        st.markdown(f"<div class='terminal-text' style='margin-bottom:0.6rem;'>> FAILURE HISTORY vs PASS PROBABILITY</div>", unsafe_allow_html=True)
        for fail_c, prob_val in [(0, 90.7), (1, 54.3), (2, 50.0), (3, 35.7)]:
            p_color = NEON if prob_val > 75 else (YELLOW if prob_val > 50 else RED)
            st.markdown(f"""
            <div class="info-box">
                <span style="font-family:JetBrains Mono,monospace">{fail_c} failure{'s' if fail_c!=1 else ''}</span>
                <span style="float:right; color:{p_color}; font-weight:700;
                             font-family:Orbitron,monospace">{prob_val}%</span>
            </div>
            <div class="stat-bar-container">
                <div class="stat-bar-fill" style="width:{prob_val}%; background:linear-gradient(90deg,{PURPLE},{p_color});"></div>
            </div>
            """, unsafe_allow_html=True)

    # Feature importance visualization
    st.markdown("<hr class='styled-divider'>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">Feature Importance (Top 11)</div>', unsafe_allow_html=True)

    features_imp = ['G2', 'G1', 'failures', 'studytime', 'absences',
                    'higher', 'Medu', 'Fedu', 'famrel', 'internet', 'health']
    importance   = [0.95, 0.88, 0.72, 0.58, 0.45, 0.38, 0.32, 0.28, 0.22, 0.18, 0.14]

    fig, ax = plt.subplots(figsize=(10, 3.5))
    style_ax(ax, fig)

    # Color gradient: high = neon, low = purple
    bar_cols = [f"#{int(0*r + 0*(1-r)):02x}{int(255*r + 50*(1-r)):02x}{int(200*r + 237*(1-r)):02x}"
                for r in importance]

    bars = ax.barh(features_imp[::-1], importance[::-1],
                   color=bar_cols[::-1], edgecolor='none', height=0.55)
    for bar, val in zip(bars, importance[::-1]):
        ax.text(val + 0.01, bar.get_y() + bar.get_height()/2,
                f'{val:.2f}', va='center', color='white',
                fontsize=8, fontweight='bold', fontfamily='monospace')
    ax.set_xlim(0, 1.1)
    ax.set_xlabel('Relative Importance Score', color=TXT, fontsize=8)
    ax.set_title('Feature Importance — Selected Model', color='#c8d6e5', fontsize=10, fontfamily='monospace')
    for t in ax.get_yticklabels():
        t.set_fontfamily('monospace')
        t.set_fontsize(8)

    plt.tight_layout()
    st.pyplot(fig)     
    plt.close()