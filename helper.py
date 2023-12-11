from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import emoji

extract = URLExtract()


def fetch_col(selected_user, df):
    if selected_user == 'Overall':
        # fetch number of messages
        number_msgs = df.shape[0]
        # number of words
        words = []
        for msgs in df['Message']:
            words.extend(msgs.split())

        # fetch number of media shared
        media_count = 0
        for media_shared in df['Message']:
            if media_shared == '<Media omitted>\n':
                media_count = media_count + 1
        # fetch the number of links
        links = []
        for message in df['Message']:
            links.extend(extract.find_urls(message))

        return number_msgs, len(words), media_count, len(links)
    else:
        # fetch number of messages
        specific_user = df[df['User'] == selected_user]
        number_msgs = specific_user.shape[0]
        # number of words
        words = []
        for msgs in specific_user['Message']:
            words.extend(msgs.split())
        # fetch number of media shared
        media_count = 0
        for media_shared in specific_user['Message']:
            if media_shared == '<Media omitted>\n':
                media_count = media_count + 1
        # fetch the number of links
        links = []
        for message in specific_user['Message']:
            links.extend(extract.find_urls(message))

        return number_msgs, len(words), media_count, len(links)


# most busiest user
def most_busy_users(df):
    x = df['User'].value_counts().head()
    df = round(df['User'].value_counts() / df.shape[0] * 100, 2)  # 100,2 represent 2 digits after decimal
    return x, df


# WordCloud

def create_wordcloud(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]
    wc = WordCloud(width=500, height=500, background_color='white')
    df_wc = wc.generate(df['Message'].str.cat(sep=" "))
    return df_wc


# Emoji analyzing

def helper_emoji(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    emojis = []
    for message in df['Message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df


# monthly timeline

def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    timeline = df.groupby(['Year', 'Month', 'Month_Name', 'Day']).count()['Message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['Month_Name'][i] + '-' + str(timeline['Year'][i]))

    timeline['Time'] = time

    return timeline


def daily_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['Message'].reset_index()
    return daily_timeline

# Weekly acitivities
def weekly_activity(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    return df['day_name'].value_counts()


#
def activity_heatmap(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    activity_heatmap = (df.pivot_table(index='day_name', columns='period', values='Message', aggfunc='count').fillna(0))
    return activity_heatmap
