import streamlit as st
import helper
import preprocessor
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title('WhatsApp chat Analyzer')
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')

    df = preprocessor.preprocess(data)
    st.dataframe(df)

    # fetch unique users
    user_list = df['User'].unique().tolist()  # not similar users like group_notification
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, 'Overall')
    selected_user = st.sidebar.selectbox('Show Analysis wrt', user_list)
    # Show analysis
    if st.sidebar.button('Show Analysis'):
        num_msgs, words, media_shared, No_links_shared = helper.fetch_col(selected_user, df)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.header('Total Messages')
            st.title(num_msgs)
        with col2:
            st.header('Total Words')
            st.title(words)
        with col3:
            st.header('Media Shared')
            st.title(media_shared)

        with col4:
            st.header('Links Shared')
            st.title(No_links_shared)

    # finding the busiest users in the group(Group level)
    if selected_user == 'Overall':
        st.header('Most Busy Users')
        x, new_df = helper.most_busy_users(df)
        fig, ax = plt.subplots()

        col1, col2 = st.columns(2)

        with col1:
            name = x.index
            counts = x.values
            plt.bar(name, counts, color='red')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.header('Messages in %')
            st.dataframe(new_df)

    # wordcloud
    st.header('WordCloud')
    df_wc = helper.create_wordcloud(selected_user, df)
    fig, axis = plt.subplots()
    axis.imshow(df_wc)
    st.pyplot(fig)

    # Emoji Analyzer

    emoji_df = helper.helper_emoji(selected_user, df)
    st.header('Emoji Analyser')
    col1, col2 = st.columns(2)

    with col1:
        st.dataframe(emoji_df)

    with col2:
        fig, ax = plt.subplots()
        new_emoji_df = emoji_df.head(10)
        my_labels = new_emoji_df[0]

        ax.pie(new_emoji_df[1],labels=my_labels, autopct='%0.2f')
        # ax.pie(emoji_df[0], labels=emoji_df[1].head(len(emoji_df[1])), autopct='%0.2f')
        st.pyplot(fig)



    # Monthly timeline
    st.header("Monthly Timeline")
    timeline = helper.monthly_timeline(selected_user, df)
    fig, ax = plt.subplots()
    ax.plot(timeline['Time'], timeline['Message'], color='green')
    plt.xticks(rotation='vertical')
    st.pyplot(fig)




    # Daily timeline

    st.header("Daily Timeline")
    daily_timeline = helper.daily_timeline(selected_user, df)
    fig, ax = plt.subplots()
    ax.plot(daily_timeline['only_date'], daily_timeline['Message'], color='green')
    plt.xticks(rotation='vertical')
    st.pyplot(fig)
    # Monthly timeline bar chart
    st.header("Monthly bar chart")
    fig, ax = plt.subplots()
    ax.bar(timeline['Time'], timeline['Message'], color='blue')
    plt.xticks(rotation='vertical')
    ax.set_ylabel('Message')
    ax.set_xlabel('Time')
    st.pyplot(fig)

    # Daily timeline bar chart
    st.header("Daily bar Chart")

    fig, ax = plt.subplots()
    ax.bar(daily_timeline['only_date'], daily_timeline['Message'], color='green')
    plt.xticks(rotation='vertical')
    ax.set_ylabel('Message')
    ax.set_xlabel('Time')
    st.pyplot(fig)



    busy_day = helper.weekly_activity(selected_user,df)
    st.header('Weekly Activity')

    col1, col2 = st.columns(2)
    with col1:
        st.header('Visulization')
        fig,ax = plt.subplots()
        ax.bar(busy_day.index,busy_day.values,color='orange')
        plt.xticks(rotation='vertical')
        ax.set_ylabel('Message')
        ax.set_xlabel('Days')
        st.pyplot(fig)
    with col2:
        st.header('Representation')
        st.dataframe(busy_day)


    st.title("Weekly Activity Map")
    user_heatmap = helper.activity_heatmap(selected_user, df)
    fig, ax = plt.subplots()
    ax = sns.heatmap(user_heatmap)
    st.pyplot(fig)

