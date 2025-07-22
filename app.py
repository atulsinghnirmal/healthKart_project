import streamlit as st

st.set_page_config(layout="wide")
st.title('HealthKart Influencer Campaign Dashboard')

import streamlit as st
import pandas as pd

# ... (keep title code from above)

st.sidebar.header('Upload Campaign Data')
uploaded_influencers = st.sidebar.file_uploader("Upload influencers.csv", type="csv")
uploaded_posts = st.sidebar.file_uploader("Upload posts.csv", type="csv")
uploaded_tracking = st.sidebar.file_uploader("Upload tracking_data.csv", type="csv")
uploaded_payouts = st.sidebar.file_uploader("Upload payouts.csv", type="csv")

if uploaded_influencers and uploaded_posts and uploaded_tracking and uploaded_payouts:
    df_influencers = pd.read_csv(uploaded_influencers)
    df_posts = pd.read_csv(uploaded_posts)
    df_tracking = pd.read_csv(uploaded_tracking)
    df_payouts = pd.read_csv(uploaded_payouts)

    st.success("All data loaded successfully!")
    # All other code will go inside this 'if' block
else:
    st.info("Please upload all four CSV files to begin analysis.")
    
# ... inside the 'if' block
st.sidebar.header('Filters')

# Platform Filter
selected_platform = st.sidebar.multiselect(
    'Platform',
    options=df_influencers['platform'].unique(),
    default=df_influencers['platform'].unique()
)

# Influencer Category Filter
selected_category = st.sidebar.multiselect(
    'Influencer Category',
    options=df_influencers['category'].unique(),
    default=df_influencers['category'].unique()
)

# Filter data based on selections
df_influencers_filtered = df_influencers[
    df_influencers['platform'].isin(selected_platform) &
    df_influencers['category'].isin(selected_category)
]
# You must also filter your other dataframes
# For example, filter tracking data based on the selected influencers
filtered_influencer_ids = df_influencers_filtered['ID'].unique()
df_tracking_filtered = df_tracking[df_tracking['influencer_id'].isin(filtered_influencer_ids)]
df_payouts_filtered = df_payouts[df_payouts['influencer_id'].isin(filtered_influencer_ids)]    

# ... inside the 'if' block after filters

# Calculate total revenue per influencer from the filtered data
influencer_revenue = df_tracking_filtered.groupby('influencer_id')['revenue'].sum().reset_index()

# Merge data to create a summary table
summary_df = pd.merge(df_influencers_filtered, df_payouts_filtered, left_on='ID', right_on='influencer_id')
summary_df = pd.merge(summary_df, influencer_revenue, on='influencer_id', how='left').fillna(0)

# Calculate ROAS
# Avoid division by zero if payout is 0
summary_df['ROAS'] = summary_df.apply(
    lambda row: row['revenue'] / row['total_payout'] if row['total_payout'] > 0 else 0,
    axis=1
)

# --- Show Key Metrics ---
st.header("Campaign Performance Overview")
col1, col2, col3 = st.columns(3)
total_revenue = summary_df['revenue'].sum()
total_payout = summary_df['total_payout'].sum()
overall_roas = total_revenue / total_payout if total_payout > 0 else 0

col1.metric("Total Revenue", f"${total_revenue:,.2f}")
col2.metric("Total Payout", f"${total_payout:,.2f}")
col3.metric("Overall ROAS", f"{overall_roas:.2f}x")

# --- Show Insights Table ---
st.header("Influencer Insights")
st.dataframe(summary_df[['name', 'category', 'follower_count', 'platform', 'total_payout', 'revenue', 'ROAS']])

# ... at the end, inside the 'if' block
st.header("Top & Poor Performing Influencers")

top_5 = summary_df.nlargest(5, 'ROAS')

st.subheader("Top 5 Influencers by ROAS")
st.bar_chart(top_5.set_index('name')['ROAS'])