import streamlit as st
import pandas as pd

# --- Page Configuration ---
st.set_page_config(page_title="E-Commerce Return Predictor", layout="wide", page_icon="📦")

# --- Mock Data Generation ---
# Simulating the backend database after AI sentiment analysis is performed
data = {
    "SKU": ["APP-TSHIRT-01", "SHOES-RUN-04", "ELEC-HEADP-09", "HOME-LAMP-02"],
    "Product Name": ["Classic Cotton T-Shirt", "AeroGlide Running Shoes", "Noise Cancelling Headphones", "Modern Desk Lamp"],
    "Recent Sales (Units)": [4500, 1200, 850, 300],
    "Predicted Return Risk (%)": [82, 14, 45, 5],
    "Risk Category": ["Critical", "Low", "Moderate", "Low"],
    "AI Extracted Pain Points": [
        "Sizing runs extremely small; stitching comes undone after one wash.",
        "Slightly narrow toe box, but overall comfortable.",
        "Bluetooth connectivity drops intermittently; confusing manual.",
        "N/A - Highly positive reviews."
    ],
    "Recommended Action": [
        "HALT BATCH. Send proactive email to unfulfilled orders offering size up.",
        "Monitor. No immediate action required.",
        "Update product listing with clearer Bluetooth pairing instructions.",
        "Promote product."
    ]
}

df = pd.DataFrame(data)

# --- Dashboard Header ---
st.title("📦 Automated Return Predictor")
st.markdown("""
*E-Commerce Operations Backend*  
This dashboard monitors live product reviews and support tickets, using NLP to predict return volume spikes before they happen.
""")
st.markdown("---")

# --- High Level Metrics ---
col1, col2, col3 = st.columns(3)
col1.metric("Total Active SKUs Monitored", "4,204")
col2.metric("Critical Risk SKUs Identified", "1", delta="-3 from yesterday", delta_color="inverse")
col3.metric("Estimated Cost Saved (Returns Prevented)", "₹1,45,000", delta="+₹25k")

st.markdown("---")

# --- Main Dashboard ---
st.subheader("⚠️ Live Product Risk Monitoring")

# Display the data interactively
for index, row in df.iterrows():
    # Set color based on risk
    risk_color = "red" if row['Predicted Return Risk (%)'] > 75 else "orange" if row['Predicted Return Risk (%)'] > 30 else "green"
    
    with st.expander(f"🔴 {row['Product Name']} (SKU: {row['SKU']})" if risk_color == "red" else f"🟢 {row['Product Name']} (SKU: {row['SKU']})"):
        c1, c2 = st.columns([1, 2])
        
        with c1:
            st.markdown(f"**Predicted Return Risk:**")
            st.progress(row['Predicted Return Risk (%)'] / 100.0)
            st.markdown(f"<h3 style='color:{risk_color};'>{row['Predicted Return Risk (%)']}% ({row['Risk Category']})</h3>", unsafe_allow_html=True)
            st.write(f"**Units Shipped/Pending:** {row['Recent Sales (Units)']}")
            
        with c2:
            st.markdown("**🧠 AI Sentinel Analysis:**")
            st.info(f"**Extracted Pain Points:** {row['AI Extracted Pain Points']}")
            st.warning(f"**Automated System Recommendation:** {row['Recommended Action']}")
            
            if risk_color == "red":
                if st.button(f"Execute Action: {row['SKU']}", key=row['SKU']):
                    st.success("Action Executed: Fulfillment halted. Automated outreach triggered via CRM.")
