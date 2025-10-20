import streamlit as st
import math
from datetime import date

st.set_page_config(page_title="Are you giving buyers free financing?", page_icon="💸", layout="centered")

st.title("Stop funding your buyers for free 💸")
st.markdown("Use Prime + Default Risk to price Net 30/60/90 fairly — or show buyers what terms *actually* cost.")

with st.sidebar:
    st.header("Assumptions")
    prime = st.number_input("Prime rate (% APR)", min_value=0.0, max_value=50.0, value=8.5, step=0.1)
    #delay_spread = st.number_input("Operational delay spread (% APR)", min_value=0.0, max_value=20.0, value=1.5, step=0.1)
    default_premium = st.number_input("Default risk premium (% APR)", min_value=0.0, max_value=40.0, value=3.0, step=0.5)
    comp = st.selectbox("Compounding", ["Simple (APR * days/365)", "Daily (APR/365 comp)"])

st.subheader("Calculator")
col1, col2 = st.columns(2)
with col1:
    invoice = st.number_input("Invoice amount ($)", min_value=0.0, value=10000.0, step=100.0, format="%.2f")
with col2:
    net_days = st.selectbox("Terms", [0, 15, 30, 45, 60, 90, 120, 150, 180], index=3)

apr = (prime + default_premium) / 100.0

if comp.startswith("Simple"):
    surcharge = invoice * apr * (net_days/365.0)
else:
    surcharge = invoice * ((1 + apr/365.0)**net_days)

total_due = invoice + surcharge
effective_apr_pct = apr * 100

st.markdown("---")
st.markdown("### Results")
c1, c2, c3 = st.columns(3)
c1.metric("Surcharge for terms", f"${surcharge:,.2f}")
c2.metric("Total due at payment", f"${total_due:,.2f}")
c3.metric("Baseline APR used", f"{effective_apr_pct:.2f}%")

st.markdown("#### Breakdown")
st.write({
    "Invoice": f"${invoice:,.2f}",
    "Net days": net_days,
    "Prime": f"{prime:.2f}%",
    #"Delay spread": f"{delay_spread:.2f}%",
    "Default premium": f"{default_premium:.2f}%",
    "Compounding": comp,
})

st.markdown("---")
st.markdown(
    "**Why this matters:** Net terms are an interest-free loan unless you price them. "
    "This baseline uses **Prime + Default risk** to reflect real financing + risk. "
    "Want buyer-specific pricing and repayment forecasts at the **point of sale**? → email hello@net30ai.com"
)

# Simple CSV download
import pandas as pd
df = pd.DataFrame([{
    "date": date.today().isoformat(),
    "invoice": invoice,
    "net_days": net_days,
    "prime_apr_pct": prime,
    #"delay_spread_pct": delay_spread,
    "default_premium_pct": default_premium,
    "compounding": comp,
    "surcharge": round(surcharge, 2),
    "total_due": round(total_due, 2),
    "baseline_apr_pct": round(effective_apr_pct, 2),
}])
st.download_button("Download result (CSV)", df.to_csv(index=False).encode("utf-8"), "net_terms_quote.csv", "text/csv")