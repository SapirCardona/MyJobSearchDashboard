import streamlit as st
import pandas as pd
import plotly.express as px

st.markdown("""
<div style='text-align:center; margin-top:20px;'>
  <img src='https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExMWZ2aDl6eWdtZG13YTFmd3lqeXJ6emhncWFpa3Z4cWFvYjl1MHpsMCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/OTpXM142KtTJ6/giphy.gif' alt='job gif' style='max-width:100%; height:auto;'>
</div>
""", unsafe_allow_html=True)

# Page configuration
st.set_page_config("My Job Search Dashboard", layout="wide")
st.title("My Job Search Dashboard")

# File uploader
uploaded_file = st.file_uploader("Upload your job tracker Excel file", type=["xlsx"])

def load_data(file):
    df = pd.read_excel(file)
    df['Application Date'] = pd.to_datetime(df['Application Date'], errors='coerce')
    df = df.dropna(subset=['Application Date'])
    return df

if uploaded_file:
    df = load_data(uploaded_file)

    # KPI cards
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.markdown(f"""
            <div style='text-align:center; padding:15px; border:1px solid #DDD; border-radius:10px;'>
                <div style='font-size:24px; font-weight:bold;'>Total Applications</div>
                <div style='font-size:28px;'>{len(df)}</div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        fit_score = round(df['Fit Score (1-5)'].mean(), 2)
        color = "#4CAF50" if fit_score >= 3.5 else "#F44336"
        st.markdown(f"""
            <div style='text-align:center; padding:15px; border:1px solid #DDD; border-radius:10px;'>
                <div style='font-size:24px; font-weight:bold;'>Avg Fit Score</div>
                <div style='font-size:28px; color:{color};'>{fit_score}</div>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        interest = round(df['My Interest Level (1-5)'].mean(), 2)
        color = "#4CAF50" if interest >= 4 else "#F44336"
        st.markdown(f"""
            <div style='text-align:center; padding:15px; border:1px solid #DDD; border-radius:10px;'>
                <div style='font-size:24px; font-weight:bold;'>Avg Interest Score</div>
                <div style='font-size:28px; color:{color};'>{interest}</div>
            </div>
        """, unsafe_allow_html=True)

    with col4:
        if not df.empty:
            days_range = (df['Application Date'].max() - df['Application Date'].min()).days
            avg_per_month = len(df) / (days_range / 30) if days_range > 0 else len(df)
            status_icon = "✅" if avg_per_month >= 40 else "❌"
            color = "#4CAF50" if avg_per_month >= 40 else "#F44336"
        else:
            avg_per_month = 0
            status_icon = "❌"
            color = "#F44336"

        st.markdown(f"""
            <div style='text-align:center; padding:15px; border:1px solid #DDD; border-radius:10px;'>
                <div style='font-size:24px; font-weight:bold;'>Avg/Month</div>
                <div style='font-size:28px; color:{color};'>{avg_per_month:.2f} {status_icon}</div>
            </div>
        """, unsafe_allow_html=True)

    with col5:
        alignment = df['Alignment with Career Goals (Y/N)'].value_counts(normalize=True) * 100
        yes = alignment.get('Y', 0)
        no = alignment.get('N', 0)
        st.markdown(f"""
            <div style='text-align:center; padding:15px; border:1px solid #DDD; border-radius:10px;'>
                <div style='font-size:24px; font-weight:bold;'>Career Alignment</div>
                <div style='font-size:15px;'>✅: {yes:.1f}%<br>❌: {no:.1f}%</div>
            </div>
        """, unsafe_allow_html=True)

    # Status overview
    st.markdown("""
    <h2 style='margin-top:40px; text-align:center;'>Status Overview</h2>
    """, unsafe_allow_html=True)
    status_counts = df['Current Status'].value_counts()
    status_colors = {'on-going': 'green', 'Sent': 'orange', 'Rejected': 'red'}
    for status in ['on-going', 'Sent', 'Rejected']:
        count = status_counts.get(status, 0)
        color = status_colors[status]
        st.markdown(f"<div style='color:{color}; font-size:32px; font-weight:bold; text-align:center;'>■ {status}: {count}</div>", unsafe_allow_html=True)

    # Timeline graph
    st.subheader("Applications Over Time")
    if not df.empty:
        timeline = df.groupby('Application Date').size().reset_index(name='Applications')
        fig_timeline = px.line(timeline, x='Application Date', y='Applications', markers=True)
        st.plotly_chart(fig_timeline, use_container_width=True)
    else:
        st.info("No applications to display.")

    # Bar charts
    col6, col7 = st.columns(2)

    with col6:
        st.subheader("Applications by Location")
        loc_counts = df['Location'].value_counts().reset_index()
        loc_counts.columns = ['Location', 'Count']
        fig_loc = px.bar(loc_counts, x='Location', y='Count')
        st.plotly_chart(fig_loc, use_container_width=True)

    with col7:
        st.subheader("Applications by Channel")
        source_counts = df['Source of Posting'].value_counts().reset_index()
        source_counts.columns = ['Source', 'Count']
        fig_source = px.bar(source_counts, x='Source', y='Count')
        st.plotly_chart(fig_source, use_container_width=True)


    # Personalized Tips Section
    st.markdown("<h2 style='margin-top:40px;'>Personalized Tips</h2>", unsafe_allow_html=True)

    # Tip 1: Only one source used
    unique_sources = df['Source of Posting'].dropna().nunique()
    if unique_sources <= 2:
        st.info("Consider expanding to other channels – employee referrals can significantly increase your chances!")
    else:
        st.success("Great job using multiple job platforms!")

    # Tip 2: Only one or two locations used
    unique_locations = df['Location'].dropna().nunique()
    if unique_locations <= 3:
        st.info("Most roles today offer hybrid or remote options – don’t limit your search by geography.")
    else:
        st.success("Nice variety of job locations – stay open!")

    # Tip 3: All interest levels are 5
    interest_values = df['My Interest Level (1-5)'].dropna().unique()
    if set(interest_values) == {5}:
        st.info("Are you truly excited about every role? Use the interest score to prioritize smarter.")
    else:
        st.success("You're using interest level to guide decisions – awesome!")

    # Tip 4: No roles aligned with career goals
    if df['Alignment with Career Goals (Y/N)'].dropna().eq('N').all():
        st.warning("You deserve roles aligned with your long-term goals. Try filtering more deliberately.")
    else:
        st.success("You're aligning your search with your long-term goals – well done!")

    # Tip 5: Many applications but no on-going processes
    if len(df) > 50 and df['Current Status'].dropna().eq('on-going').sum() == 0:
        st.warning("If you're not getting callbacks, consider tailoring your CV or cover letter.")

    # Weekly progress check - enlarged
    st.markdown("""
    <h2 style='margin-top:40px; text-align:center;'>⏰ Weekly Target Tracker</h2>
    """, unsafe_allow_html=True)
    df['Application Week'] = df['Application Date'].dt.isocalendar().week
    current_week = pd.Timestamp.now().isocalendar().week
    apps_this_week = df[df['Application Week'] == current_week].shape[0]
    if apps_this_week >= 10:
        st.markdown(f"<div style='font-size:30px; color:green; font-weight:bold; text-align:center;'>You submitted {apps_this_week} applications this week! Great job! 🎉</div>", unsafe_allow_html=True)
    else:
        remaining = 10 - apps_this_week
        st.markdown(f"<div style='font-size:30px; color:red; font-weight:bold; text-align:center;'>You have {remaining} applications left to reach your weekly goal of 10!</div>", unsafe_allow_html=True)
else:
        st.info("Please upload your Excel file to get started.")
        st.markdown("""
            <div style='font-size:18px; line-height:1.6;'>
            This dashboard works with a specific Excel template created by <strong>Sapir Cardona</strong>.<br>
            Don't have it yet? No worries!<br><br>
            📩 <strong>Want the template?</strong><br>
            <a href='https://www.linkedin.com/in/sapircardona' target='_blank'>Message me on LinkedIn</a> – happy to share it with you!
            </div>
            """, unsafe_allow_html=True)

