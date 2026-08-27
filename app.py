"""
REELMATCH — a Streamlit projection room for the TF-IDF movie recommender.

Run with:
    streamlit run app.py
"""

import html
import time

import streamlit as st

from logic import all_titles, engine_stats, get_recommendations, load_data

st.set_page_config(
    page_title="REELMATCH — Projection Room",
    page_icon="🎞️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────
# Boot — pickles load ONCE per server process, then everything is RAM-speed
# ─────────────────────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def boot_engine():
    load_data()                 # warms logic.py's internal cache
    return engine_stats()


@st.cache_data(show_spinner=False)
def boot_titles():
    return all_titles()


def hue(s: str) -> int:
    h = 0
    for ch in s:
        h = (h * 31 + ord(ch)) % 360
    return h


# ─────────────────────────────────────────────────────────────
# The house style — marquee bulbs, film grain, ticket-stub cards
# ─────────────────────────────────────────────────────────────
CSS = """
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Instrument+Sans:wght@400;500;600;700&family=Space+Mono:ital,wght@0,400;0,700;1,400&display=swap');

/* ── hide Streamlit chrome ── */
#MainMenu, footer {visibility: hidden;}
[data-testid="stToolbar"] {display: none;}
header[data-testid="stHeader"] {background: transparent;}
.block-container {padding-top: 1rem; padding-bottom: 3rem; max-width: 1220px;}

.stApp {
  background-color: #0d0a07;
  background-image: radial-gradient(1100px 560px at 50% -8%, rgba(233,180,76,.10), transparent 62%);
  color: #f5ecd9;
}
/* film grain over everything */
body::before {
  content: ""; position: fixed; inset: 0; z-index: 999; pointer-events: none; opacity: .06;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='300' height='300'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='2'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
}

/* ── Streamlit widget restyle ── */
.stSelectbox label, .stSlider label, .stSelectSlider label {
  font-family: 'Space Mono', monospace !important;
  font-size: .62rem !important; letter-spacing: .26em; color: #e9b44c !important;
}
div[data-baseweb="select"] {border-radius: 0;}
div[data-baseweb="select"] > div {
  background-color: #151009 !important; border: 2px solid #3a2f1d !important;
  border-radius: 0 !important; min-height: 58px;
}
div[data-baseweb="select"] > div:hover,
div[data-baseweb="select"] > div:focus-within {border-color: #e9b44c !important; box-shadow: none !important;}
div[data-baseweb="select"] input, div[data-baseweb="select"] input::placeholder {
  font-family: 'Bebas Neue', sans-serif; font-size: 1.45rem; letter-spacing: .05em;
  color: #f5ecd9; opacity: 1;
}
div[data-baseweb="select"] input::placeholder {color: #6d5f4a;}
div[data-baseweb="popover"] {background: #14100a; border: 1px solid rgba(233,180,76,.25); border-radius: 0;}
ul[data-baseweb="menu"] {background: #14100a; border-radius: 0; font-family: 'Instrument Sans', sans-serif;}
ul[data-baseweb="menu"] li {color: #f5ecd9; font-size: .9rem;}
ul[data-baseweb="menu"] li:hover, ul[data-baseweb="menu"] li[aria-selected="true"] {background: rgba(233,180,76,.16);}

/* PROJECT button */
.stFormSubmitButton > button {
  width: 100%; font-family: 'Bebas Neue', sans-serif; font-size: 1.4rem; letter-spacing: .12em;
  background: #c73e2e; color: #f5ecd9; border: none; border-radius: 0;
  padding: .95rem 1.4rem; box-shadow: 6px 6px 0 #3d1512;
  transition: transform .15s ease, box-shadow .15s ease, background .2s;
}
.stFormSubmitButton > button:hover {background: #d84a38; color: #f5ecd9; transform: translate(-2px,-2px); box-shadow: 8px 8px 0 #3d1512;}
.stFormSubmitButton > button:active {transform: translate(2px,2px); box-shadow: 2px 2px 0 #3d1512;}
.stFormSubmitButton > button p {font: inherit; color: inherit;}

/* sidebar */
section[data-testid="stSidebar"] {background: #120d07; border-right: 1px solid rgba(233,180,76,.22);}
section[data-testid="stSidebar"] .stButton > button {
  font-family: 'Space Mono', monospace; font-size: .6rem; letter-spacing: .05em;
  background: transparent; color: #e9b44c; border: 1px dashed rgba(233,180,76,.4);
  border-radius: 0; box-shadow: none; padding: .55rem .5rem;
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}
section[data-testid="stSidebar"] .stButton > button:hover {
  background: rgba(233,180,76,.12); color: #ffcf6e; border-color: #e9b44c; transform: translateY(-2px);
}
section[data-testid="stSidebar"] .stButton > button p {font: inherit; color: inherit;}

div[data-testid="stMetric"] {background: #171209; border: 1px solid rgba(233,180,76,.22); border-radius: 0; padding: .9rem 1.1rem;}
div[data-testid="stMetricLabel"] p {font-family: 'Space Mono', monospace !important; font-size: .58rem !important; letter-spacing: .22em; color: #c9bda4 !important;}
div[data-testid="stMetricValue"] {font-family: 'Bebas Neue', sans-serif !important; font-size: 2rem !important; color: #f5ecd9 !important;}

div[data-testid="stExpander"] {background: #141009; border: 1px solid rgba(233,180,76,.22); border-radius: 0;}
div[data-testid="stExpander"] summary {font-family: 'Bebas Neue', sans-serif; font-size: 1.25rem; letter-spacing: .08em; color: #e9b44c;}
div[data-testid="stExpander"] summary:hover {color: #ffcf6e;}
.stSpinner {color: #e9b44c; font-family: 'Space Mono', monospace; letter-spacing: .3em;}

/* ── REELMATCH components ── */
.rm-marquee {border: 1px solid rgba(233,180,76,.22); background: linear-gradient(180deg,#1a120a,#120d07); margin-top: .5rem;}
.rm-bulbs {height: 16px; background-color: #1a130a;
  background-image: radial-gradient(circle 4px at 9px 8px, #ffcf6e 0 3px, #3a2c12 3.5px 4.5px, transparent 5px);
  background-size: 28px 16px; animation: rmBlink 1.4s steps(2) infinite;}
.rm-bulbs.flip {background-position: 14px 0; animation-delay: .7s;}
@keyframes rmBlink {50% {filter: brightness(.55);}}
.rm-sign {display: flex; justify-content: space-between; align-items: flex-end; gap: 1.5rem; flex-wrap: wrap; padding: 1.6rem 1.8rem 1.2rem;}
.rm-brand {font-family: 'Bebas Neue', sans-serif; font-size: clamp(2.8rem, 6vw, 4.6rem); line-height: .9;
  letter-spacing: .04em; color: #e9b44c; text-shadow: 0 0 26px rgba(233,180,76,.4), 3px 3px 0 rgba(0,0,0,.5);}
.rm-tagline {font-family: 'Space Mono', monospace; font-size: .62rem; letter-spacing: .28em; color: #c9bda4; margin-top: .4rem;}
.rm-chip {display: inline-flex; align-items: center; gap: .5rem; border: 1px solid rgba(233,180,76,.22);
  padding: .5rem .9rem; font-family: 'Space Mono', monospace; font-size: .62rem; letter-spacing: .12em; background: rgba(0,0,0,.25);}
.rm-dot {width: 8px; height: 8px; border-radius: 50%; background: #ffcf6e; box-shadow: 0 0 8px #ffcf6e; animation: rmPulse 1.6s ease infinite;}
@keyframes rmPulse {50% {opacity: .35;}}

.rm-ticker {overflow: hidden; border-top: 1px solid rgba(233,180,76,.22); background: #0a0705; margin-bottom: 2.6rem;}
.rm-ticker-rail {display: flex; gap: 3rem; width: max-content; padding: .55rem 0;
  font-family: 'Space Mono', monospace; font-size: .66rem; letter-spacing: .2em; color: #e9b44c;
  animation: rmTicker 46s linear infinite;}
.rm-ticker-rail b {color: #f5ecd9; font-weight: 400;}
.rm-ticker:hover .rm-ticker-rail {animation-play-state: paused;}
@keyframes rmTicker {to {transform: translateX(-33.3333%);}}

.rm-kicker {font-family: 'Space Mono', monospace; font-size: .64rem; letter-spacing: .3em; color: #e9b44c; margin-bottom: .8rem;}
.rm-display {font-family: 'Bebas Neue', sans-serif; font-size: clamp(2.8rem, 7vw, 6rem); line-height: .95;
  letter-spacing: .02em; color: #f5ecd9; margin-bottom: 2rem;}
.rm-outline {color: transparent; -webkit-text-stroke: 2px #e9b44c;}

/* the screen */
.rm-screen-head {display: flex; justify-content: space-between; align-items: center; margin: 2.6rem 0 .9rem;}
.rm-stamped {font-family: 'Space Mono', monospace; font-size: .68rem; letter-spacing: .3em; color: #e9b44c;}
.rm-reel {width: 28px; height: 28px; border-radius: 50%; border: 3px solid #e9b44c;
  background: conic-gradient(#e9b44c 0 12%, transparent 12% 25%, #e9b44c 25% 37%, transparent 37% 50%,
             #e9b44c 50% 62%, transparent 62% 75%, #e9b44c 75% 87%, transparent 87%);
  animation: rmSpin 6s linear infinite;}
.rm-reel.fast {animation-duration: 1s;}
@keyframes rmSpin {to {transform: rotate(360deg);}}
.rm-screen {position: relative; background: #080604; border: 1px solid rgba(233,180,76,.22);}
.rm-screen::before, .rm-screen::after {content: ""; position: absolute; top: 0; bottom: 0; width: 52px; z-index: 2; pointer-events: none;
  background: repeating-linear-gradient(90deg, #7c2620 0 11px, #5d1f1c 11px 21px, #40140f 21px 29px);
  box-shadow: inset 0 -60px 60px rgba(0,0,0,.7);}
.rm-screen::before {left: 0;} .rm-screen::after {right: 0;}
.rm-frame {padding: 2.2rem 4.6rem; min-height: 330px; display: flex; align-items: center; justify-content: center;}

/* results rail */
.rm-rail {display: flex; gap: 1.2rem; overflow-x: auto; padding: 1.1rem .3rem 1.5rem; width: 100%; scroll-snap-type: x mandatory;}
.rm-rail::-webkit-scrollbar {height: 8px;}
.rm-rail::-webkit-scrollbar-thumb {background: #e9b44c;}
.rm-rail::-webkit-scrollbar-track {background: #171209;}
.rm-card {position: relative; flex: 0 0 232px; scroll-snap-align: start; min-height: 252px;
  padding: 1.6rem 1.1rem 1.2rem 2rem; animation: rmCardIn .55s cubic-bezier(.2,.75,.2,1) both;
  transition: transform .25s ease, box-shadow .25s ease;}
.rm-card:hover {transform: translateY(-8px) rotate(-.6deg); box-shadow: 0 22px 40px rgba(0,0,0,.55); z-index: 3;}
@keyframes rmCardIn {from {opacity: 0; transform: translateY(26px) scale(.97);} to {opacity: 1; transform: none;}}
.rm-tkt {background: #f2e7d3; color: #1d1710;}
.rm-tkt::before {content: ""; position: absolute; left: 13px; top: 0; bottom: 0; width: 1px;
  background: repeating-linear-gradient(180deg, transparent 0 7px, rgba(29,23,16,.4) 7px 13px);}
.rm-pstr {background: linear-gradient(160deg, hsl(var(--h) 42% 17%), #0c0a08 75%);
  border: 1px solid hsl(var(--h) 60% 42% / .55); color: #f5ecd9;}
.rm-rank {position: absolute; top: -13px; right: -9px; transform: rotate(9deg);
  font-family: 'Bebas Neue', sans-serif; font-size: 1rem; letter-spacing: .06em;
  color: #c73e2e; border: 2px solid #c73e2e; border-radius: 999px; padding: .45rem .6rem; background: rgba(242,231,211,.92);}
.rm-pstr .rm-rank {color: #ffcf6e; border-color: #ffcf6e; background: rgba(12,10,8,.9);}
.rm-card-title {font-family: 'Bebas Neue', sans-serif; font-size: 1.45rem; line-height: 1.05; letter-spacing: .03em;
  margin-bottom: .7rem; min-height: 3.1em; text-transform: uppercase;}
.rm-card-meta {font-family: 'Space Mono', monospace; font-size: .6rem; letter-spacing: .1em; opacity: .75; min-height: 2.4em;}
.rm-cells {display: flex; gap: 3px; margin: .9rem 0 .45rem;}
.rm-cells span {width: 11px; height: 14px; border: 1px solid rgba(120,100,60,.5);}
.rm-cells span.on {background: #e9b44c; border-color: #e9b44c; box-shadow: 0 0 6px rgba(233,180,76,.5);}
.rm-pstr .rm-cells span {border-color: rgba(233,180,76,.35);}
.rm-pct {font-family: 'Space Mono', monospace; font-size: .58rem; letter-spacing: .1em; opacity: .85;}

/* idle leader + not found */
.rm-leader {text-align: center;}
.rm-leader-ring {width: 180px; height: 180px; margin: 0 auto 1.3rem; border-radius: 50%; border: 3px solid #e9b44c;
  display: flex; align-items: center; justify-content: center; position: relative;
  box-shadow: inset 0 0 0 12px #080604, inset 0 0 0 14px rgba(233,180,76,.35);}
.rm-leader-ring::before, .rm-leader-ring::after {content: ""; position: absolute; background: rgba(233,180,76,.3);}
.rm-leader-ring::before {left: 50%; top: -24px; bottom: -24px; width: 1px;}
.rm-leader-ring::after {top: 50%; left: -24px; right: -24px; height: 1px;}
.rm-leader-ring b {font-family: 'Bebas Neue', sans-serif; font-size: 5.4rem; color: #e9b44c;}
.rm-leader p, .rm-notfound p {font-family: 'Space Mono', monospace; font-size: .62rem; letter-spacing: .3em; color: #c9bda4;}
.rm-notfound {text-align: center;}
.rm-stamp-x {display: inline-block; font-family: 'Space Mono', monospace; font-size: 1.4rem; letter-spacing: .2em;
  color: #c73e2e; border: 3px solid #c73e2e; padding: .6rem 1.6rem; transform: rotate(-5deg);
  box-shadow: 0 0 0 5px rgba(199,62,46,.15); margin-bottom: 1.4rem;}
.rm-notfound p {letter-spacing: .14em; max-width: 430px; margin: 0 auto;}

/* expander content */
.rm-formula {display: inline-block; font-family: 'Space Mono', monospace; color: #ffcf6e;
  border: 1px solid rgba(233,180,76,.22); background: #141009; padding: .8rem 1.3rem; letter-spacing: .06em; margin: .4rem 0 1rem;}
.rm-code {font-family: 'Space Mono', monospace; font-size: .78rem; line-height: 1.7; background: #0a0806;
  border: 1px solid rgba(233,180,76,.22); padding: 1.1rem 1.2rem; overflow-x: auto; color: #c9bda4;}
.rm-code .c {color: #7a6f5c; font-style: italic;} .rm-code .g {color: #e9b44c;}

/* sidebar bits */
.rm-side-brand {font-family: 'Bebas Neue', sans-serif; font-size: 2.2rem; letter-spacing: .04em; color: #e9b44c; line-height: 1;}
.rm-side-brand span {color: transparent; -webkit-text-stroke: 1.5px #f5ecd9;}
.rm-side-label {font-family: 'Space Mono', monospace; font-size: .58rem; letter-spacing: .28em; color: #e9b44c;
  margin: 1.7rem 0 .9rem; padding-top: 1.2rem; border-top: 1px dashed rgba(233,180,76,.25);}

/* credits */
.rm-credits {margin-top: 4rem; border-top: 1px solid rgba(233,180,76,.22); background: #0a0705; text-align: center;}
.rm-credits p {font-family: 'Space Mono', monospace; font-size: .62rem; letter-spacing: .28em; color: #c9bda4;
  line-height: 2.4; padding: 2.4rem 0 2.8rem;}
.rm-credits b {color: #e9b44c; font-weight: 400;}

@media (max-width: 700px) {
  .rm-frame {padding: 1.6rem 2.4rem;}
  .rm-screen::before, .rm-screen::after {width: 20px;}
}
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {animation-duration: .01ms !important; animation-iteration-count: 1 !important; transition-duration: .01ms !important;}
}
"""

st.markdown(f"<style>{CSS}</style>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# Boot or fail gracefully
# ─────────────────────────────────────────────────────────────
try:
    stats = boot_engine()
    movie_titles = boot_titles()
except FileNotFoundError as err:
    st.markdown(
        f"""
        <div class="rm-marquee"><div class="rm-bulbs"></div>
        <div class="rm-sign"><div><div class="rm-brand">REELMATCH</div>
        <div class="rm-tagline">PROJECTOR FAULT</div></div></div>
        <div class="rm-bulbs flip"></div></div>
        <div class="rm-screen" style="margin-top:2rem"><div class="rm-frame">
        <div class="rm-notfound"><div class="rm-stamp-x">NO FILM LOADED</div>
        <p>{html.escape(str(err))}</p></div></div></div>
        """,
        unsafe_allow_html=True,
    )
    st.stop()


# ─────────────────────────────────────────────────────────────
# Sidebar — projection controls
# ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="rm-side-brand">REEL<span>MATCH</span></div>', unsafe_allow_html=True)

    st.markdown('<p class="rm-side-label">PROJECTION CONTROLS</p>', unsafe_allow_html=True)
    count = st.select_slider("PICKS PER REEL", options=[5, 7, 10], value=7,
                             help="How many kindred spirits to project.")

    st.markdown('<p class="rm-side-label">TRY A REEL</p>', unsafe_allow_html=True)
    side_cols = st.columns(2)
    for i, frac in enumerate((0.1, 0.35, 0.6, 0.85)):
        sample = movie_titles[int(len(movie_titles) * frac)]
        with side_cols[i % 2]:
            if st.button(sample, key=f"sample{i}", use_container_width=True):
                st.session_state["title_pick"] = sample
                st.rerun()

    st.markdown('<p class="rm-side-label">ENGINE</p>', unsafe_allow_html=True)
    e1, e2 = st.columns(2)
    e1.metric("FILMS", f"{stats['movies']:,}")
    e2.metric("DIMS", f"{stats['features']:,}")
    st.caption("One TF-IDF row per film — cosine similarity ranks the whole archive in a single pass.")


# ─────────────────────────────────────────────────────────────
# HTML builders
# ─────────────────────────────────────────────────────────────
def ticker_html(titles_: list) -> str:
    phrases = ["NOW SERVING COSINE SIMILARITY", "TF-IDF VECTORS LOADED",
               "CONTENT-BASED · NO RATINGS REQUIRED", "TOP-N PICKS ON DEMAND"]
    samples = [titles_[int(len(titles_) * f)] for f in (0, .2, .4, .6, .8)] if titles_ else []
    seq = "".join(f"<span>✦ <b>{html.escape(t)}</b></span>" for t in phrases + samples)
    return f'<div class="rm-ticker"><div class="rm-ticker-rail">{seq * 3}</div></div>'


def card_html(i: int, r: dict, top: float) -> str:
    dark = i % 2 == 1
    meta = " · ".join(filter(None, [
        " · ".join(r["genres"][:2]) if r.get("genres") else "",
        f"★ {r['rating']}" if r.get("rating") else "",
        str(r["year"]) if r.get("year") else "",
    ])) or "—"
    filled = 3 + round(9 * r["score"] / top)
    cells = "".join(f'<span class="{"on" if j < filled else ""}"></span>' for j in range(12))
    sim = max(15, round(r["score"] / top * 100))
    style = f'style="--h:{hue(r["title"])}"' if dark else ""
    cls = "rm-card rm-pstr" if dark else "rm-card rm-tkt"
    return f"""
    <article class="{cls}" {style}>
      <div class="rm-rank">No. {i + 1:02d}</div>
      <h3 class="rm-card-title">{html.escape(r["title"])}</h3>
      <p class="rm-card-meta">{html.escape(meta)}</p>
      <div class="rm-cells">{cells}</div>
      <span class="rm-pct">SIMILARITY {sim}% · COS {r["score"]:.3f}</span>
    </article>"""


def screen_shell(head_text: str, inner_html: str, fast: bool = False) -> str:
    return f"""
    <div class="rm-screen-head">
      <span class="rm-stamped">{head_text}</span>
      <span class="rm-reel{' fast' if fast else ''}"></span>
    </div>
    <div class="rm-screen"><div class="rm-frame">{inner_html}</div></div>
    """


LEADER = """
<div class="rm-leader">
  <div class="rm-leader-ring"><b>7</b></div>
  <p>PICTURE START — SEARCH A TITLE, THEN HIT PROJECT</p>
</div>"""


# ─────────────────────────────────────────────────────────────
# Main stage
# ─────────────────────────────────────────────────────────────
st.markdown(
    f"""
    <div class="rm-marquee">
      <div class="rm-bulbs"></div>
      <div class="rm-sign">
        <div>
          <div class="rm-brand">REELMATCH</div>
          <div class="rm-tagline">TF–IDF × COSINE SIMILARITY · CONTENT-BASED PROJECTION ROOM</div>
        </div>
        <div class="rm-chip"><span class="rm-dot"></span>PROJECTOR ONLINE · {stats['movies']:,} FILMS</div>
      </div>
      <div class="rm-bulbs flip"></div>
    </div>
    {ticker_html(movie_titles)}
    <p class="rm-kicker">ADMIT ONE — PICK A FILM, GET KINDRED SPIRITS</p>
    <h1 class="rm-display">WHAT SHOULD <span class="rm-outline">YOU WATCH</span> NEXT?</h1>
    """,
    unsafe_allow_html=True,
)

# the booth
with st.form("booth", clear_on_submit=False):
    fc1, fc2 = st.columns([3.2, 1])
    with fc1:
        pick = st.selectbox(
            "REEL TITLE",
            movie_titles,
            index=None,
            placeholder="TYPE A MOVIE — E.G. INCEPTION",
            key="title_pick",
        )
    with fc2:
        submitted = st.form_submit_button("PROJECT ▸", use_container_width=True)

# handle a projection request
if submitted:
    st.session_state.pop("last_result", None)
    st.session_state.pop("last_error", None)
    if not pick:
        st.session_state["last_error"] = "GIVE THE PROJECTIONIST A TITLE FIRST."
    else:
        with st.spinner("THREADING FILM…"):
            t0 = time.perf_counter()
            recs = get_recommendations(pick, n=count)
            ms = round((time.perf_counter() - t0) * 1000)
        if recs and "error" in recs[0]:
            st.session_state["last_error"] = (
                f"“{pick.upper()}” IS NOT IN THE ARCHIVE. "
                "CHECK THE SPELLING OR TRY ANOTHER REEL."
            )
        else:
            st.session_state["last_result"] = {"movie": pick, "recs": recs, "ms": ms}

# the screen
last = st.session_state.get("last_result")
err = st.session_state.get("last_error")

if last:
    top = max((r["score"] for r in last["recs"]), default=0.0001) or 0.0001
    cards = "".join(
        f'<div style="animation-delay:{i * 0.07}s; display:contents">'
        + card_html(i, r, top) + "</div>"
        for i, r in enumerate(last["recs"])
    )
    st.markdown(
        screen_shell(
            f'NOW SHOWING — “{html.escape(last["movie"].upper())}” + {len(last["recs"])} PICKS · {last["ms"]}MS',
            f'<div class="rm-rail">{cards}</div>',
        ),
        unsafe_allow_html=True,
    )
elif err:
    st.markdown(
        screen_shell(
            "NOW SHOWING — REEL NOT FOUND",
            f'<div class="rm-notfound"><div class="rm-stamp-x">REEL NOT FOUND</div><p>{html.escape(err)}</p></div>',
        ),
        unsafe_allow_html=True,
    )
else:
    st.markdown(screen_shell("NOW SHOWING — AWAITING FIRST REEL", LEADER), unsafe_allow_html=True)

# engine stats
q_ms = last["ms"] if last else 0
m1, m2, m3, m4 = st.columns(4)
m1.metric("FILMS INDEXED", f"{stats['movies']:,}")
m2.metric("VECTOR DIMENSIONS", f"{stats['features']:,}")
m3.metric("PAIRS SCORED / QUERY", f"{max(stats['movies'] - 1, 0):,}")
m4.metric("MS · LAST QUERY", f"{q_ms}")

# how it works
with st.expander("SCENE 02 — HOW THE PROJECTIONIST THINKS", expanded=False):
    st.markdown(
        """
        <div class="rm-formula">cos θ = ( A · B ) / ( ‖A‖ ‖B‖ )</div>

        No ratings, no watch history — just text. Every film owns one sparse TF-IDF row:
        a fingerprint of its most distinctive words. Your pick is compared against the whole
        matrix in a single pass, the query film is spliced out, and the nearest neighbours roll.

        <pre class="rm-code">scores = <span class="g">cosine_similarity</span>(matrix[idx], matrix).flatten()
picked = [i for i in scores.argsort()[::-1] if i != idx][:n]
<span class="c"># → the top-n kindred spirits, stamped and metered</span></pre>
        """,
        unsafe_allow_html=True,
    )

# credits
st.markdown(
    """
    <div class="rm-credits">
      <div class="rm-bulbs"></div>
      <p>A CONTENT-BASED PICTURE · DIRECTED BY <b>YOUR MODEL</b><br>
      CINEMATOGRAPHY — <b>scikit-learn</b> · SCORE — <b>cosine similarity</b> · SET DESIGN — <b>Streamlit</b><br>
      REELMATCH · EST. 2026 · NO RATINGS WERE HARMED</p>
    </div>
    """,
    unsafe_allow_html=True,
)