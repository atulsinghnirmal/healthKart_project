import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta

# Initialize Faker
fake = Faker()

# Number of records to create
NUM_INFLUENCERS = 50
NUM_POSTS = 200
NUM_TRACKING_RECORDS = 5000

# --- 1. influencers.csv ---
influencers = []
for i in range(1, NUM_INFLUENCERS + 1):
    influencers.append({
        'ID': i,
        'name': fake.name(),
        'category': random.choice(['Fitness', 'Wellness', 'Nutrition', 'Bodybuilding']),
        'gender': random.choice(['Male', 'Female']),
        'follower_count': random.randint(10000, 1000000),
        'platform': random.choice(['Instagram', 'YouTube'])
    })
df_influencers = pd.DataFrame(influencers)

# --- 2. posts.csv ---
posts = []
for _ in range(NUM_POSTS):
    influencer = df_influencers.sample(1).iloc[0]
    posts.append({
        'post_id': len(posts) + 1,
        'influencer_id': influencer['ID'],
        'platform': influencer['platform'],
        'date': fake.date_time_between(start_date='-6m', end_date='now'),
        'URL': f"http://{influencer['platform']}.com/post/{fake.uuid4()}",
        'caption': fake.text(max_nb_chars=200),
        'reach': random.randint(5000, influencer['follower_count']),
        'likes': random.randint(100, int(influencer['follower_count'] * 0.1)),
        'comments': random.randint(10, int(influencer['follower_count'] * 0.01))
    })
df_posts = pd.DataFrame(posts)

# --- 3. tracking_data.csv ---
tracking_data = []
for _ in range(NUM_TRACKING_RECORDS):
    post = df_posts.sample(1).iloc[0]
    tracking_data.append({
        'source': 'influencer_campaign',
        'campaign': 'Q2_Promotion',
        'influencer_id': post['influencer_id'],
        'user_id': fake.uuid4(),
        'product': random.choice(['MuscleBlaze Whey', 'HKVitals Multivitamin', 'Gritzo SuperMilk']),
        'date': post['date'] + timedelta(days=random.randint(1, 14)),
        'orders': 1,
        'revenue': round(random.uniform(20.0, 100.0), 2)
    })
df_tracking_data = pd.DataFrame(tracking_data)

# --- 4. payouts.csv ---
payouts = []
for _, influencer in df_influencers.iterrows():
    basis = random.choice(['post', 'order'])
    rate = 0
    total_payout = 0

    influencer_posts = df_posts[df_posts['influencer_id'] == influencer['ID']]
    influencer_revenue = df_tracking_data[df_tracking_data['influencer_id'] == influencer['ID']]['revenue'].sum()

    if basis == 'post':
        rate = round(random.uniform(100.0, 1000.0), 2) # Flat rate per post
        total_payout = rate * len(influencer_posts)
    else: # 'order' basis
        rate = round(random.uniform(0.08, 0.15), 2) # Commission rate
        total_payout = rate * influencer_revenue

    payouts.append({
        'influencer_id': influencer['ID'],
        'basis': basis,
        'rate': rate,
        'orders': df_tracking_data[df_tracking_data['influencer_id'] == influencer['ID']]['orders'].sum(),
        'total_payout': round(total_payout, 2)
    })
df_payouts = pd.DataFrame(payouts)

# --- Save to CSV ---
df_influencers.to_csv('influencers.csv', index=False)
df_posts.to_csv('posts.csv', index=False)
df_tracking_data.to_csv('tracking_data.csv', index=False)
df_payouts.to_csv('payouts.csv', index=False)

print("CSV files generated successfully!")