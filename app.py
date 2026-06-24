import streamlit as st
import pandas as pd
import plotly.express as px

# --- Page Configuration ---
st.set_page_config(page_title="E-Commerce Return Predictor", layout="wide", page_icon="📦")

# --- Mock Data Generation ---
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

# --- Sidebar Filters ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3176/3176369.png", width=50) # Optional generic icon
st.sidebar.header("Filter Options")
selected_risk = st.sidebar.multiselect(
    "Select Risk Category to View:",
    options=df["Risk Category"].unique(),
    default=df["Risk Category"].unique()
)

# Apply filter
filtered_df = df[df["Risk Category"].isin(selected_risk)]

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
col3.metric("Estimated Cost Saved", "₹1,45,000", delta="+₹25k (This Week)")

st.markdown("---")

# --- Main Dashboard Tabs ---
tab1, tab2 = st.tabs(["🚨 Action Center", "📊 Analytics Hub"])

with tab1:
    st.subheader("Live Product Risk Monitoring")
    
    if filtered_df.empty:
        st.info("No SKUs match the selected filters.")
    
    # Display the data interactively based on filters
    for index, row in filtered_df.iterrows():
        # Set color based on risk
        if row['Predicted Return Risk (%)'] > 75:
            risk_color = "red"
            icon = "🔴"
        elif row['Predicted Return Risk (%)'] > 30:
            risk_color = "orange"
            icon = "🟡"
        else:
            risk_color = "green"
            icon = "🟢"
        
        with st.expander(f"{icon} {row['Product Name']} (SKU: {row['SKU']})"):
            c1, c2 = st.columns([1, 2])
            
            with c1:
                st.markdown("**Predicted Return Risk:**")
                st.progress(row['Predicted Return Risk (%)'] / 100.0)
                st.markdown(f"<h3 style='color:{risk_color}; margin-top: 0;'>{row['Predicted Return Risk (%)']}% ({row['Risk Category']})</h3>", unsafe_allow_html=True)
                st.write(f"**Units Shipped/Pending:** {row['Recent Sales (Units)']}")
                
            with c2:
                st.markdown("**🧠 AI Sentinel Analysis:**")
                st.info(f"**Extracted Pain Points:** {row['AI Extracted Pain Points']}")
                st.warning(f"**Automated Recommendation:** {row['Recommended Action']}")
                
                if risk_color == "red":
                    if st.button(f"Execute Action: {row['SKU']}", key=row['SKU']):
                        st.success("✅ Action Executed: Fulfillment halted. Automated outreach triggered via CRM.")

with tab2:
    st.subheader("Risk Distribution Analysis")
    
    # Plotly Chart
    fig = px.bar(
        filtered_df, 
        x="SKU", 
        y="Predicted Return Risk (%)", 
        color="Risk Category",
        color_discrete_map={"Critical": "red", "Moderate": "orange", "Low": "green"},
        title="Predicted Return Risk by SKU",
        text="Predicted Return Risk (%)"
    )
    fig.update_traces(textposition='outside')
    fig.update_layout(yaxis_range=[0, 100])
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("**Raw Data Feed**")
    st.dataframe(filtered_df, use_container_width=True)
