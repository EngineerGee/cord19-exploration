import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

st.title("CORD-19 Data Explorer")
st.write("Simple exploration of COVID-19 research papers")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("metadata.csv")
    df['publish_time'] = pd.to_datetime(df['publish_time'], errors='coerce')
    df['year'] = df['publish_time'].dt.year
    return df.dropna(subset=['title','publish_time'])

df = load_data()

# Year slider
min_year, max_year = int(df['year'].min()), int(df['year'].max())
year_range = st.slider("Select year range", min_year, max_year, (2020,2021))

filtered = df[(df['year']>=year_range[0]) & (df['year']<=year_range[1])]

st.write("Sample of Data")
st.dataframe(filtered.head())

# Plot publications by year
year_counts = filtered['year'].value_counts().sort_index()
fig, ax = plt.subplots()
ax.bar(year_counts.index, year_counts.values)
ax.set_title('Publications by Year')
st.pyplot(fig)

# Top journals
top_journals = filtered['journal'].value_counts().head(10)
fig2, ax2 = plt.subplots()
ax2.barh(top_journals.index, top_journals.values)
ax2.set_title('Top Journals')
st.pyplot(fig2)

# Word cloud of titles
titles = ' '.join(filtered['title'].dropna()).lower()
from collections import Counter
import re
words = re.findall(r'\b[a-z]{3,}\b', titles)
from collections import Counter
word_counts = Counter(words)
wc = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(word_counts)
fig3, ax3 = plt.subplots(figsize=(15,7))
ax3.imshow(wc, interpolation='bilinear')
ax3.axis('off')
st.pyplot(fig3)
