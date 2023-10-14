import time
import pandas as pd
import numpy as np

CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
    }

def get_filters():
    """
    Asks the user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of the week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    while True:
        try:
            # To get user input for city (chicago, new york city, washington). User input are case-insensitive and whitespaces are removed.
            city = input('City: input the name of city to analyze (Hint: Chicago, New York City, Washington): ').strip().lower()
            if city in CITY_DATA:
                break
            else:
                print('City: input not valid. Try again and re-enter a valid city name.')
        except KeyboardInterrupt:
            print('\nProcess interrupted. Returning back to the main menu.')

    while True:
        try:
            # To get user input for month (all, january, february, march, ..., june). User input are case-insensitive and whitespaces are removed.
            month = input('Month: input the month to filter by (all, january, february, march, ..., june): ').strip().lower()
            if month in ['all', 'january', 'february', 'march', 'april', 'may', 'june']:
                break
            else:
                print('Month: input not valid. Try again and re-enter a valid month name or "all".')
        except KeyboardInterrupt:
            print('\nProcess interrupted. Returning back to the main menu.')

    while True:
        try:
            # To get user input for day of the week (all, monday, tuesday, wednesday, ..., sunday. User input are case-insensitive and whitespaces are removed.
            day = input('Day: input the day of the week to filter by (all, monday, tuesday, wednesday, ..., sunday): ').strip().lower()
            if day in ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
                break
            else:
                print('Day: input not valid. Try again and re-enter a valid day name or "all".')
        except KeyboardInterrupt:
            print('\nProcess interrupted. Returning back to the main menu.')

    print('-' * 40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of the week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    try:
        # Load data from the CSV file for the selected city.
        df = pd.read_csv(CITY_DATA[city])

        # Convert the 'Start Time' column to datetime.
        df['Start Time'] = pd.to_datetime(df['Start Time'])

        # Extract month and day of the week from 'Start Time' to create new columns.
        df['Month'] = df['Start Time'].dt.month
        df['Day of Week'] = df['Start Time'].dt.day_name()

        # Filter by month if applicable.
        if month != 'all':
            month_num = ['january', 'february', 'march', 'april', 'may', 'june'].index(month) + 1
            df = df[df['Month'] == month_num]

        # Filter by day of the week if applicable.
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
    """
    Displays statistics on the most frequent times of travel.
    
    Args:
        df - Pandas DataFrame containing city data
    """
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    most_common_month = df['Month'].mode()[0]
    print('Most Common Month:', most_common_month)

    # Display the most common day of the week
    most_common_day = df['Day of Week'].mode()[0]
    print('Most Common Day of Week:', most_common_day)

    # Extract hour from the 'Start Time' column
    df['Hour'] = df['Start Time'].dt.hour

    # Display the most common start hour
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
