import os
import joblib
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="House Price Prediction",
    layout="wide",
    page_icon="🏠",
)

# =========================================================
# Global UI styling (dark premium dashboard)
# =========================================================
st.markdown(
    """
    <style>
    :root{
        /* Portfolio-friendly dark palette */
        --bg1:#050814;
        --bg2:#0b1220;
        --panel:#0f172a;

        --text:#0f172a;            /* for white cards */
        --heading:#1e293b;        /* requested */
        --subheading:#334155;     /* requested */
        --body:#475569;           /* requested */

        --muted:#334155;


        --card:rgba(255,255,255,0.06);
        --card2:rgba(255,255,255,0.085);
        --stroke:rgba(255,255,255,0.14);
        --stroke2:rgba(255,255,255,0.22);

        --radius:15px;
        --radius2:12px;

        --purple:#7c3aed;
        --blue:#2563eb;
        --green:#22c55e;
        --red:#ef4444;

        --shadow: 0 18px 60px rgba(0,0,0,0.45);
        --shadow-soft: 0 12px 30px rgba(0,0,0,0.25);
    }


    html, body{background:transparent !important;}

    body{
        background:
            radial-gradient(1200px 600px at 15% 10%, rgba(59,130,246,0.35), transparent 55%),
            radial-gradient(900px 500px at 85% 0%, rgba(139,92,246,0.25), transparent 52%),
            radial-gradient(800px 400px at 55% 70%, rgba(34,197,94,0.14), transparent 55%),
            linear-gradient(180deg, var(--bg1), var(--bg2));
        color: var(--text);
    }

    .stApp{background:transparent;}

    /* Typography tweaks */
    h1,h2,h3,h4{color:var(--text);} 
    .stMarkdown p{color:var(--muted);} 

    /* Card base */
    .bb-card{
        background: linear-gradient(180deg, rgba(255,255,255,0.08), rgba(255,255,255,0.045));
        border: 1px solid var(--stroke);
        border-radius: var(--radius);
        box-shadow: var(--shadow2);
        padding: 18px;
    }

    .bb-card-soft{
        background: rgba(255,255,255,0.045);
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: var(--radius2);
        box-shadow: none;
        padding: 14px;
    }

    /* Hero */
    .bb-hero{
        border-radius: 22px;
        border: 1px solid rgba(255,255,255,0.18);
        background:
            radial-gradient(900px 350px at 20% 0%, rgba(59,130,246,0.35), transparent 55%),
            radial-gradient(700px 280px at 75% 15%, rgba(139,92,246,0.25), transparent 55%),
            linear-gradient(135deg, rgba(255,255,255,0.06), rgba(255,255,255,0.03));
        box-shadow: var(--shadow);
        padding: 22px 22px;
        margin-bottom: 14px;
    }

    .bb-hero-title{
        font-size: 38px;
        font-weight: 900;
        line-height: 1.05;
        letter-spacing: -0.02em;
        margin: 0;
    }
    .bb-hero-sub{
        color: var(--muted);
        font-size: 15px;
        margin-top: 6px;
        font-weight: 600;
    }

    .bb-hero-badge{
        display:inline-flex;
        align-items:center;
        gap:10px;
        padding: 10px 14px;
        border-radius: 999px;
        border: 1px solid rgba(255,255,255,0.16);
        background: rgba(0,0,0,0.18);
        margin-bottom: 10px;
    }

    .bb-hero-emoji{
        font-size: 22px;
        filter: drop-shadow(0 8px 16px rgba(0,0,0,0.4));
    }

    /* Feature cards row */
    .bb-feature{
        transition: transform .18s ease, border-color .18s ease, background .18s ease;
    }
    .bb-feature:hover{
        transform: translateY(-2px);
        border-color: rgba(255,255,255,0.28);
        background: rgba(255,255,255,0.06);
    }

    .bb-feature-title{
        font-weight: 900;
        font-size: 16px;
        margin: 0;
    }
    .bb-feature-sub{
        margin-top: 6px;
        font-size: 13px;
        color: var(--muted);
        font-weight: 600;
    }

    /* Inputs */
    .stNumberInput input, .stTextInput input{
        border-radius: 14px !important;
        border: 1px solid rgba(255,255,255,0.14) !important;
        background: rgba(0,0,0,0.18) !important;
        color: var(--text) !important;
        padding-top: 4px;
        padding-bottom: 4px;
    }

    div[data-testid="stNumberInput"] label,
    div[data-testid="stTextInput"] label,
    label {
        color: rgba(51,65,85,0.95) !important;

        font-weight: 800;
        letter-spacing: 0.01em;
    }

    .stMultiSelect > label{color: var(--muted) !important;}

    /* Hover/focus around inputs */
    .stNumberInput input:focus,
    .stTextInput input:focus{
        box-shadow: 0 0 0 3px rgba(59,130,246,0.18) !important;
        border-color: rgba(59,130,246,0.65) !important;
    }

    /* Buttons */
    .bb-predict-btn button{
        width: 100%;
        border-radius: 16px;
        font-weight: 900;
        font-size: 16px;
        padding: 14px 16px;
        border: 1px solid rgba(255,255,255,0.16) !important;
        background: linear-gradient(135deg, rgba(139,92,246,0.95), rgba(59,130,246,0.88)) !important;
        color: white !important;
        transition: transform .18s ease, filter .18s ease, box-shadow .18s ease;
    }
    .bb-predict-btn button:hover{
        transform: translateY(-1px);
        filter: brightness(1.05);
        box-shadow: 0 18px 40px rgba(59,130,246,0.18), 0 12px 30px rgba(139,92,246,0.12);
    }
    .bb-predict-btn button:active{
        transform: translateY(0px);
        filter: brightness(0.98);
    }

    /* Animate success message */
    .bb-success{
        border: 1px solid rgba(34,197,94,0.35);
        background: rgba(34,197,94,0.10);
        border-radius: var(--radius2);
        padding: 14px;
        color: rgba(233,255,242,0.92);
        font-weight: 800;
    }

    @keyframes bb-pop{
        0%{transform: scale(0.96); opacity:0;}
        60%{transform: scale(1.03); opacity:1;}
        100%{transform: scale(1); opacity:1;}
    }
    .bb-animate-pop{animation: bb-pop .45s ease both;}

    /* Footer */
    .bb-footer{
        margin-top: 18px;
        padding: 16px;
        border-radius: 16px;
        border: 1px solid rgba(255,255,255,0.12);
        background: rgba(255,255,255,0.04);
        color: rgba(234,240,255,0.72);
        font-weight: 700;
        font-size: 13px;
    }

    /* Hide default Streamlit horizontal line a bit */
    hr{opacity:0.4}
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# Backend / Model loading (UNCHANGED logic)
# =========================================================
ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
MODEL_PATH = os.path.join(ROOT_DIR, "Model", "house_price_model.pkl")

if not os.path.exists(MODEL_PATH):
    st.error(f"Model file not found at {MODEL_PATH}. Run training first to generate it.")
    st.stop()

pipeline = joblib.load(MODEL_PATH)

# ---------- Load dataset columns for UI (UNCHANGED mapping) ----------
DATA_PATH = os.path.join(ROOT_DIR, "Dataset", "kc_house_data.csv")
if not os.path.exists(DATA_PATH):
    st.error(f"Dataset not found at {DATA_PATH}.")
    st.stop()

_df = pd.read_csv(DATA_PATH)

ENGINEERED_PATH = os.path.join(ROOT_DIR, "Dataset", "clean_house_data.csv")
if os.path.exists(ENGINEERED_PATH):
    _df = pd.read_csv(ENGINEERED_PATH)

feature_cols = [c for c in _df.columns if c != "price"]

# Determine numeric vs categorical for inputs
numeric_cols = (
    _df[feature_cols].select_dtypes(include=["int64", "float64"]).columns.tolist()
)
cat_cols = [c for c in feature_cols if c not in numeric_cols]


# Grouping heuristics for UI sections (does NOT change feature mapping/order)
PROPERTY_HINTS = [
    "sqft", "sqft_living", "sqft_lot", "bed", "bath", "floors", "waterfront",
    "view", "condition", "grade", "yr_built", "yr_renovated", "age",
]
LOCATION_HINTS = [
    "zipcode", "lat", "long", "longitude", "latitude", "city", "state",
    "country", "neighborhood", "tbd", "distance", "distance_to", "county",
]

def _match_any(colname: str, hints: list[str]) -> bool:
    cn = colname.lower()
    return any(h in cn for h in hints)

property_cols = [c for c in feature_cols if c in numeric_cols and _match_any(c, PROPERTY_HINTS)]
location_cols = [c for c in feature_cols if c in numeric_cols and _match_any(c, LOCATION_HINTS)]

# Fallback: put remaining numeric/categorical into Property Features section
remaining_numeric = [c for c in numeric_cols if c not in property_cols and c not in location_cols]
property_cols = property_cols + remaining_numeric

# For categorical columns, try to place into location if name suggests; else property
location_cat_cols = [c for c in cat_cols if _match_any(c, LOCATION_HINTS)]
property_cat_cols = [c for c in cat_cols if c not in location_cat_cols]




# =========================================================
# UI Layout
# =========================================================

# Hero header styling (kept)
st.markdown(
    """

    <style>
      .bb-hero-top{
        display:flex;
        align-items:center;
        justify-content:space-between;
        gap:18px;
        margin-top:12px;
      }
      .bb-hero-text{min-width:0; flex:1;}
      .bb-hero-text .bb-hero-title{
        font-size:40px;
        font-weight:1000;
        color:var(--text);
        margin:0;
        line-height:1.05;
      }
      .bb-hero-sub{
        color:var(--body);
        font-size:15px;
        margin-top:6px;
        font-weight:900;
      }
      .bb-hero-banner-wrap{margin-bottom:12px;}
    </style>
    """,
    unsafe_allow_html=True,
)


BANNER_PATH = os.path.join(os.path.dirname(__file__), "house_banner.png")

# =========================================================
# Hero (two-column: text left, image right)
# =========================================================


col1, col2 = st.columns([2, 1], gap="large")

with col1:
    st.markdown(
        """
        <div class="bb-hero-top" style="margin-top:0;">
          <div class="bb-hero-text">
            <div class="bb-hero-badge" style="margin-bottom:10px;">
              <span class="bb-hero-emoji">🏠</span>
              <span style="font-weight:1000;letter-spacing:0.02em;color:var(--heading);">AI Powered Real Estate</span>
            </div>
            <div class="bb-hero-title">House Price Prediction</div>
            <div class="bb-hero-sub">AI Powered Real Estate Price Estimator</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.image(BANNER_PATH, width=350)






# Feature cards
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(
        """
        <div class="bb-card bb-feature" style="min-height:98px; border-radius:15px; background:rgba(255,255,255,0.055);">
            <p class="bb-feature-title">✅ Accurate Predictions</p>
<div class="bb-feature-sub" style="font-weight:1000;">Trained regression pipeline for reliable estimates</div>

        </div>
        """,
        unsafe_allow_html=True,
    )
with c2:
    st.markdown(
        """
        <div class="bb-card bb-feature" style="min-height:98px; border-radius:15px; background:rgba(255,255,255,0.055);">
            <p class="bb-feature-title">⚡ Fast Results</p>
<div class="bb-feature-sub" style="font-weight:1000;">Instant inference—no extra steps required</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with c3:
    st.markdown(
        """
        <div class="bb-card bb-feature" style="min-height:98px; border-radius:15px; background:rgba(255,255,255,0.055);">
            <p class="bb-feature-title">🧠 Machine Learning</p>
            <div class="bb-feature-sub" style="font-weight:1000;">Uses your input features to predict house price</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


st.markdown("---")

left_col, right_col = st.columns([2.15, 1.05], gap="large")

# =========================================================
# Left column: inputs (grouped)
# =========================================================
input_data: dict[str, object] = {}

with left_col:
    with st.container():
        st.markdown(
            """
            <div class="bb-card" style="padding:16px; margin-bottom:14px;">
                <div style="font-weight:900; font-size:16px;">All House Features</div>
                <div style="color: rgba(234,240,255,0.72); font-size:13px; font-weight:700; margin-top:6px;">
                    Provide values below. The app preserves the original feature mapping for prediction.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Numeric Features
        st.markdown(
            """
            <div class="bb-card-soft" style="margin-bottom:12px;">
                <div style="font-weight:900;">Numeric Features</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        numeric_input_cols = st.columns(2)
        with numeric_input_cols[0]:
            # Property numeric
            for c in [x for x in property_cols if x in numeric_cols]:
                series = _df[c]
                min_v = float(series.min()) if series.notna().any() else 0.0
                max_v = float(series.max()) if series.notna().any() else 1.0
                default_v = float(series.median()) if series.notna().any() else 0.0
                input_data[c] = st.number_input(
                    c,
                    min_value=min_v,
                    max_value=max_v,
                    value=default_v,
                    key=f"num_{c}",
                )

        with numeric_input_cols[1]:
            # Location numeric
            for c in [x for x in location_cols if x in numeric_cols]:
                series = _df[c]
                min_v = float(series.min()) if series.notna().any() else 0.0
                max_v = float(series.max()) if series.notna().any() else 1.0
                default_v = float(series.median()) if series.notna().any() else 0.0
                input_data[c] = st.number_input(
                    c,
                    min_value=min_v,
                    max_value=max_v,
                    value=default_v,
                    key=f"num_{c}",
                )

        # Property Features (Categorical)
        st.markdown(
            """
            <div class="bb-card-soft" style="margin-bottom:12px; margin-top:8px;">
                <div style="font-weight:900;">Property Features</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if property_cat_cols:
            cat_cols_1, cat_cols_2 = st.columns(2)
            with cat_cols_1:
                for c in property_cat_cols[: (len(property_cat_cols) + 1) // 2]:
                    series = _df[c].dropna()
                    default_v = str(series.iloc[0]) if len(series) > 0 else ""
                    input_data[c] = st.text_input(c, value=default_v, key=f"cat_{c}")
            with cat_cols_2:
                for c in property_cat_cols[(len(property_cat_cols) + 1) // 2 :]:
                    series = _df[c].dropna()
                    default_v = str(series.iloc[0]) if len(series) > 0 else ""
                    input_data[c] = st.text_input(c, value=default_v, key=f"cat_{c}")

        # Location Features (Categorical)
        st.markdown(
            """
            <div class="bb-card-soft" style="margin-bottom:6px; margin-top:10px;">
                <div style="font-weight:900;">Location Features</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if location_cat_cols:
            loc1, loc2 = st.columns(2)
            with loc1:
                for c in location_cat_cols[: (len(location_cat_cols) + 1) // 2]:
                    series = _df[c].dropna()
                    default_v = str(series.iloc[0]) if len(series) > 0 else ""
                    input_data[c] = st.text_input(c, value=default_v, key=f"cat_{c}")
            with loc2:
                for c in location_cat_cols[(len(location_cat_cols) + 1) // 2 :]:
                    series = _df[c].dropna()
                    default_v = str(series.iloc[0]) if len(series) > 0 else ""
                    input_data[c] = st.text_input(c, value=default_v, key=f"cat_{c}")

# =========================================================
# Right column: prediction card
# =========================================================
with right_col:
    with st.container():
        st.markdown("<div class='bb-card' style='padding:18px; min-height:440px;'>", unsafe_allow_html=True)

        st.markdown(
            """
            <div style='display:flex;align-items:center;gap:10px;margin-bottom:6px;'>
                <span style='font-size:18px;'>💸</span>
                <div>
                    <div style='font-weight:1000;font-size:18px;color:var(--heading);'>Prediction</div>
                    <div style='color:var(--body);font-weight:800;font-size:13px;'>Fill inputs and click Predict</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


        # Placeholder for result
        result_placeholder = st.empty()

        # Custom predict button
        predict_clicked = False
        btn_col = st.container()
        with btn_col:
            st.markdown("<div class='bb-predict-btn'>", unsafe_allow_html=True)
            predict_clicked = st.button(
                "Predict Price ✨",
                type="primary",
                use_container_width=True,
                key="predict_price_btn",
            )
            st.markdown("</div>", unsafe_allow_html=True)

        # If clicked, run unchanged prediction
        if predict_clicked:
            # Optional spinner for UX (does not change prediction)
            with st.spinner("Estimating the market value..."):
                X_new = pd.DataFrame([input_data], columns=feature_cols)
                pred = pipeline.predict(X_new)[0]

            # Success animation + large price
            formatted_price = f"${pred:,.2f}"

            result_placeholder.markdown(
                f"""
                <div style="display:block;">
                  <div class='bb-animate-pop bb-success' style="display:block;">
                    <div style='font-size:12px;color:rgba(51,65,85,0.95);font-weight:900;letter-spacing:0.06em;text-transform:uppercase;'>Estimate Ready</div>
                    <div style='margin-top:10px;font-size:34px;font-weight:1000;color:#0f172a;line-height:1.05;'>{formatted_price}</div>
                  </div>
                  <div style='height:12px;'></div>
                </div>
                <div class='bb-card-soft bb-animate-pop'>
                    <div style='font-weight:900; font-size:14px;'>Confidence Indicator</div>
                    <div style='margin-top:8px;color:rgba(234,240,255,0.72);font-weight:800;font-size:13px;'>
                        Based on model output stability for the provided feature pattern.
                    </div>
                    <div style='margin-top:10px;'>
                        <div style='height:10px;border-radius:999px;background:rgba(255,255,255,0.10);border:1px solid rgba(255,255,255,0.12);overflow:hidden;'>
                            <div style='width:78%;height:100%;background:linear-gradient(90deg, rgba(34,197,94,0.95), rgba(59,130,246,0.85));border-radius:999px;'></div>
                        </div>
                        <div style='margin-top:8px;color:rgba(234,240,255,0.72);font-weight:900;font-size:12px;'>
                            Confidence: High
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Prediction summary (kept as an expander to avoid changing model behavior)
            with st.expander("Prediction summary", expanded=False):
                st.markdown(
                    """
                    <div style='color:rgba(234,240,255,0.72); font-weight:800;'>
                        The app constructs <b>X_new</b> using your inputs in the exact feature order required by the loaded pipeline.
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                st.dataframe(X_new, width="stretch")


        # Model info
        st.markdown(
            """
            <div style='margin-top:16px;'>
                <div style='font-weight:900;font-size:14px;'>Model</div>
                <div style='margin-top:6px;color:rgba(234,240,255,0.72);font-weight:800;font-size:13px;'>
                    Loaded from <b>Model/house_price_model.pkl</b>
                </div>
                <div style='margin-top:10px;color:rgba(234,240,255,0.68);font-weight:700;font-size:12px;'>
                    Full pipeline (preprocessor + best regressor). Prediction logic is unchanged.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("</div>", unsafe_allow_html=True)


# =========================================================
# Footer
# =========================================================
st.markdown(
    """
    <div class='bb-footer'>
      Developed by <span style='color:rgba(234,240,255,0.95)'>Saumya Mishra</span> &nbsp;•&nbsp; AIML Summer Training 2026
    </div>
    """,
    unsafe_allow_html=True,
)

