# app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter
import re

# Set page configuration
st.set_page_config(
    page_title="CORD-19 Data Explorer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_data
def load_data():
    """Load and cache the dataset"""
    try:
        df = pd.read_csv('metadata.csv')
        return df
    except FileNotFoundError:
        st.error("File 'metadata.csv' not found. Please make sure it's in the same directory.")
        return None

@st.cache_data
def clean_data(df):
    """Clean the dataset"""
    # Basic cleaning for the app
    df_clean = df.copy()
    df_clean['publish_time'] = pd.to_datetime(df_clean['publish_time'], errors='coerce')
    df_clean['publication_year'] = df_clean['publish_time'].dt.year
    df_clean['title'] = df_clean['title'].fillna('Unknown Title')
    df_clean['abstract'] = df_clean['abstract'].fillna('')
    df_clean['journal'] = df_clean['journal'].fillna('Unknown Journal')
    df_clean['abstract_word_count'] = df_clean['abstract'].apply(lambda x: len(str(x).split()))
    df_clean['has_abstract'] = df_clean['abstract'].apply(lambda x: len(str(x).strip()) > 0)
    
    return df_clean

def main():
    st.title("📊 CORD-19 Research Papers Explorer")
    st.markdown("""
    Explore the COVID-19 Open Research Dataset (CORD-19) containing research papers 
    about COVID-19, SARS-CoV-2, and related coronaviruses.
    """)
    
    # Load data
    with st.spinner('Loading data...'):
        df = load_data()
    
    if df is None:
        st.stop()
    
    # Clean data
    df_clean = clean_data(df)
    
    # Sidebar
    st.sidebar.title("Filters")
    
    # Year filter
    min_year = int(df_clean['publication_year'].min())
    max_year = int(df_clean['publication_year'].max())
    year_range = st.sidebar.slider(
        "Select Year Range",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year)
    )
    
    # Journal filter
    all_journals = ['All'] + sorted(df_clean['journal'].unique().tolist())
    selected_journal = st.sidebar.selectbox("Select Journal", all_journals)
    
    # Has abstract filter
    abstract_filter = st.sidebar.radio("Abstract Filter", ['All', 'With Abstract', 'Without Abstract'])
    
    # Apply filters
    filtered_df = df_clean[
        (df_clean['publication_year'] >= year_range[0]) & 
        (df_clean['publication_year'] <= year_range[1])
    ]
    
    if selected_journal != 'All':
        filtered_df = filtered_df[filtered_df['journal'] == selected_journal]
    
    if abstract_filter == 'With Abstract':
        filtered_df = filtered_df[filtered_df['has_abstract'] == True]
    elif abstract_filter == 'Without Abstract':
        filtered_df = filtered_df[filtered_df['has_abstract'] == False]
    
    # Main content
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Papers", f"{len(filtered_df):,}")
    
    with col2:
        st.metric("With Abstracts", f"{filtered_df['has_abstract'].sum():,}")
    
    with col3:
        st.metric("Time Range", f"{year_range[0]} - {year_range[1]}")
    
    with col4:
        avg_words = filtered_df[filtered_df['abstract_word_count'] > 0]['abstract_word_count'].mean()
        st.metric("Avg Abstract Words", f"{avg_words:.0f}")
    
    # Tabs for different visualizations
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Publication Trends", 
        "Journal Analysis", 
        "Title Analysis",
        "Source Analysis",
        "Sample Data"
    ])
    
    with tab1:
        st.header("Publication Trends Over Time")
        
        # Yearly publications
        yearly_data = filtered_df['publication_year'].value_counts().sort_index()
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=yearly_data.index,
            y=yearly_data.values,
            name="Publications"
        ))
        fig.update_layout(
            title="Publications by Year",
            xaxis_title="Year",
            yaxis_title="Number of Publications"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Monthly trends (if we have the data)
        if 'publish_time' in filtered_df.columns:
            monthly_data = filtered_df.set_index('publish_time').resample('M').size()
            fig2 = go.Figure()
            fig2.add_trace(go.Scatter(
                x=monthly_data.index,
                y=monthly_data.values,
                mode='lines',
                name="Monthly Publications"
            ))
            fig2.update_layout(
                title="Monthly Publication Trends",
                xaxis_title="Date",
                yaxis_title="Number of Publications"
            )
            st.plotly_chart(fig2, use_container_width=True)
    
    with tab2:
        st.header("Journal Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Top journals
            top_journals = filtered_df['journal'].value_counts().head(15)
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                y=top_journals.index,
                x=top_journals.values,
                orientation='h'
            ))
            fig.update_layout(
                title="Top 15 Journals by Publication Count",
                xaxis_title="Number of Publications",
                yaxis_title="Journal"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Journal distribution
            journal_counts = filtered_df['journal'].value_counts()
            top_10 = journal_counts.head(10)
            others = journal_counts[10:].sum()
            
            labels = list(top_10.index) + ['Others']
            values = list(top_10.values) + [others]
            
            fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
            fig.update_layout(title="Journal Distribution")
            st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.header("Title Analysis")
        
        # Word cloud
        st.subheader("Word Cloud of Paper Titles")
        all_titles = ' '.join(filtered_df['title'].dropna().astype(str))
        words = re.findall(r'\b[a-zA-Z]{3,}\b', all_titles.lower())
        
        stop_words = {'the', 'and', 'of', 'in', 'to', 'a', 'for', 'with', 'on', 'by'}
        filtered_words = [word for word in words if word not in stop_words]
        
        if filtered_words:
            wordcloud = WordCloud(width=800, height=400, background_color='white').generate(' '.join(filtered_words))
            
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.imshow(wordcloud, interpolation='bilinear')
            ax.axis('off')
            st.pyplot(fig)
        else:
            st.warning("No titles available for word cloud generation.")
        
        # Most common words
        st.subheader("Most Common Words in Titles")
        if filtered_words:
            word_freq = Counter(filtered_words)
            common_words = word_freq.most_common(15)
            
            words, counts = zip(*common_words)
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=counts,
                y=words,
                orientation='h'
            ))
            fig.update_layout(
                title="Top 15 Most Common Words",
                xaxis_title="Frequency",
                yaxis_title="Words"
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.header("Source Analysis")
        
        # Top sources
        top_sources = filtered_df['source_x'].value_counts().head(15)
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=top_sources.index,
            y=top_sources.values
        ))
        fig.update_layout(
            title="Top 15 Sources by Publication Count",
            xaxis_title="Source",
            yaxis_title="Number of Publications"
        )
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)
    
    with tab5:
        st.header("Sample Data")
        
        st.subheader("Filtered Dataset Sample")
        st.dataframe(filtered_df[['title', 'journal', 'publication_year', 'has_abstract']].head(100))
        
        # Dataset statistics
        st.subheader("Dataset Statistics")
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Column Information:**")
            st.write(f"Number of columns: {len(filtered_df.columns)}")
            st.write(f"Number of rows: {len(filtered_df):,}")
            
        with col2:
            st.write("**Data Types:**")
            dtype_counts = filtered_df.dtypes.value_counts()
            for dtype, count in dtype_counts.items():
                st.write(f"- {dtype}: {count}")
    
    # Footer
    st.markdown("---")
    st.markdown(
        "**CORD-19 Dataset** from [Allen Institute for AI](https://www.kaggle.com/allen-institute-for-ai/CORD-19-research-challenge)"
    )

if __name__ == "__main__":
    main()