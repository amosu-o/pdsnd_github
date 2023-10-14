import time
import pandas as pd
import numpy as np

CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
    }

def get_user_input(prompt, valid_inputs):
    while True:
        try:
            user_input = input(prompt).strip().lower()
            if user_input in valid_inputs:
                return user_input
            else:
                print(f'Input not valid. Try again and re-enter a valid {prompt.strip(":").lower()} name or "all".')
        except KeyboardInterrupt:
            print('\nProcess interrupted. Returning back to the main menu.')

def get_filters():
    print('Hello! Let\'s explore some US bikeshare data!')

    city = get_user_input('City: input the name of city to analyze (Hint: Chicago, New York City, Washington): ', CITY_DATA.keys())
    month = get_user_input('Month: input the month to filter by (all, january, february, march, ..., june): ', ['all', 'january', 'february', 'march', 'april', 'may', 'june'])
    day = get_user_input('Day: input the day of the week to filter by (all, monday, tuesday, wednesday, ..., sunday): ', ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'])

    print('-' * 40)
    return city, month, day

def load_data(city, month, day):
    try:
        df = pd.read_csv(CITY_DATA[city])

        df['Start Time'] = pd.to_datetime(df['Start Time'])
        df['Month'] = df['Start Time'].dt.month
        df['Day of Week'] = df['Start Time'].dt.day_name()

        # Combine month and day filtering
        if month != 'all':
            month_num = ['january', 'february', 'march', 'april', 'may', 'june'].index(month) + 1
            df = df[df['Month'] == month_num]

        if day != 'all':
            df = df[df['Day of Week'] == day.title()]

        if df.empty:
            print('No data available for the selected filters. Returning to the main menu.')
            return None

        return df
    except Exception as e:
        print('An error occurred while loading data:', str(e))
        return None

def time_stats(df):
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Calculate most common month, day, and start hour
    common_values = df[['Month', 'Day of Week', 'Start Time']].mode().iloc[0]
    most_common_month, most_common_day, _ = common_values

    print('Most Common Month:', most_common_month)
    print('Most Common Day of Week:', most_common_day)

    df['Hour'] = df['Start Time'].dt.hour
    most_common_hour = df['Hour'].mode()[0]
    print('Most Common Start Hour:', most_common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def station_stats(df):
    """
    Displays statistics on the most popular stations and trips.
    
    Args:
        df - Pandas DataFrame containing city data
    """
    print('\nCalculating Station Statistics...\n')
    start_time = time.time()

    # Display the most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print('Most Commonly Used Start Station:', most_common_start_station)

    # Display the most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print('Most Commonly Used End Station:', most_common_end_station)

    # Display the most frequent combination of start station and end station
    most_common_trip = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print('Most Common Trip (Start Station to End Station):', most_common_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def trip_duration_stats(df):
    """
    Displays statistics on the total and average trip duration.
    
    Args:
        df - Pandas DataFrame containing city data
    """
    print('\nCalculating Trip Duration Statistics...\n')
    start_time = time.time()

    # Display the total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total Travel Time:', total_travel_time, 'seconds')

    # Display the average travel time
    average_travel_time = df['Trip Duration'].mean()
    print('Average Travel Time:', average_travel_time, 'seconds')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def user_stats(df):
    """
    Displays statistics on bikeshare users.
    
    Args:
        df - Pandas DataFrame containing city data
    """
    print('\nCalculating User Statistics...\n')
    start_time = time.time()

    # Display counts of user types
    user_type_counts = df['User Type'].value_counts()
    print('User Type Counts:\n', user_type_counts)

    # Display counts of gender (if available)
    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
        print('\nGender Counts:\n', gender_counts)
    else:
        print('\nGender information not available for this dataset.')

    # Display earliest, most recent, and most common year of birth (if available)
    if 'Birth Year' in df.columns:
        earliest_birth_year = df['Birth Year'].min()
        most_recent_birth_year = df['Birth Year'].max()
        most_common_birth_year = df['Birth Year'].mode()[0]

        print('\nEarliest Birth Year:', int(earliest_birth_year))
        print('Most Recent Birth Year:', int(most_recent_birth_year))
        print('Most Common Birth Year:', int(most_common_birth_year))
    else:
        print('\nBirth year information not available for this dataset.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def display_raw_data(df):
    """
    Displays raw data in chunks of 5 rows upon user request.

    Args:
        df - Pandas DataFrame containing city data
    """
    try:
        start_idx = 0
        chunk_size = 5
        while True:
            user_input = input('\nWould you like to see 5 lines of raw data? Enter yes or no: ').strip().lower()
            if user_input == 'yes':
                print(df.iloc[start_idx:start_idx + chunk_size])
                start_idx += chunk_size
            elif user_input == 'no':
                break
            else:
                print('Input not valid. Re-enter "yes" or "no".')
    except KeyboardInterrupt:
        print('\nProcess interrupted. Returning back to the main menu.')

# The main function (modified)
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        if df is not None:
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)
            display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()
