import re
import pandas as pd


def preprocess(data):
    pattern = '\d{1,2}/\d{1,2}/\d{1,2},\s\d{1,2}:\d{1,2}\s\w+\s-\s'
    dates = re.findall(pattern, data)
    modified_dates = [s.replace('\u202f', '').replace(',', '').replace(' - ', '') for s in dates]
    messages = re.split(pattern, data)[1:]
    df = pd.DataFrame({'message': messages, 'date': modified_dates})

    df['date'] = pd.to_datetime(df['date'], format='%m/%d/%y %I:%M%p')
    df['date'] = df['date'].dt.strftime('%Y-%m-%d %I:%M:%S %p')
    user_column = []
    message_column = []
    for msg in df['message']:
        entry = re.split('([\w\W]+?):\s', msg)
        if entry[1:]:  # checks whether our messages are splited successfully
            user_column.append(entry[1])
            message_column.append(entry[2])
        else:
            user_column.append('group_notification')
            message_column.append(entry[0])

    df['User'] = user_column
    df['Message'] = message_column
    df.drop(columns=['message'], inplace=True)

    date = []
    time = []

    for date_time in df['date']:
        # Use a regular expression to match the date and time components
        entry = re.split(r'(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2} [APMapm]{2})', date_time)

        if entry[1:]:
            date.append(entry[1])
            time.append(entry[2])
        else:
            date.append('')
            time.append('')

    df['Date'] = date
    df['Time'] = time
    df.drop(columns=['date'], inplace=True)





    # Year, Month and Day
    df['Date'] = pd.to_datetime(df['Date'])
    df['Time'] = pd.to_datetime((df['Time']))

    # Extract year, month, and day
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month
    df['Day'] = df['Date'].dt.day
    df['only_date'] = df['Date'].dt.date
    # Create a new column for month names
    df['day_name'] = df['Date'].dt.day_name()
    df['Month_Name'] = df['Date'].dt.strftime('%B')
    # Extract hour and minute
    df['Hour'] = df['Time'].dt.hour
    df['Minute'] = df['Time'].dt.minute

    # Format the 'Date' column without extra zeros
    df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')

    period = []

    for hour in df[['day_name', 'Hour']]['Hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period
    # Ends here

    return df
