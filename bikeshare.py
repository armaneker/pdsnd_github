import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
MONTHS = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
DAYS = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("Please type a city name you want to analyze (chicago, new york city, washington): ").strip().lower()
        if city in ['chicago', 'new york city', 'washington']:
            break
        else:
            print("Incorrect input. Please try again.")

    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        month = input("Please type the name of the month to filter by, or \"all\" to apply no month filter: ").strip().lower()
        if month in MONTHS:
            break
        else:
            print("Incorrect input. Please try again.")

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("Please type the name of the day of week to filter by, or \"all\" to apply no day filter: ").strip().lower()
        if day in DAYS:
            break
        else:
            print("Incorrect input. Please try again.")

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])                 # convert 'Start Time' column type from object to datetime64. This will provide the option of using dt methods
    
    df['month'] = df['Start Time'].dt.month                             # extract month index and insert as new column
    df['day_of_week'] = df['Start Time'].dt.weekday_name.str.lower()    # extract day name and insert as new column
    
    if month != 'all':                                                  # check if month filter is available
        month = MONTHS.index(month)
        df = df[df['month'] == month]                                   # filter month
    if day != 'all':                                                    # check if day filter is available
        df = df[df['day_of_week'] == day]                               # filter day
        
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    popular_month = MONTHS[df['month'].mode()[0]].title()
    print('Most common month: {}'.format(popular_month))

    # TO DO: display the most common day of week
    popular_day = df['day_of_week'].mode()[0].title()
    print('Most common day of week: {}'.format(popular_day))

    # TO DO: display the most common start hour
    popular_hour = df['Start Time'].dt.hour.mode()[0]
    print('Most common start hour: {}'.format(popular_hour))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    
    # TO DO: display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('Most common used start station: {}'.format(popular_start_station))

    # TO DO: display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('Most common used end station: {}'.format(popular_end_station))

    # TO DO: display most frequent combination of start station and end station trip
    comb_result = df.groupby(['Start Station', 'End Station']).size().sort_values(ascending=False).head(1)
    start_station = comb_result.index[0][0]
    end_station = comb_result.index[0][1]
    print('Most frequent combination of start station and end station trip: Start Station: {}, End Station: {}'.format(start_station, end_station))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    
    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total travel time is: {} seconds'.format(int(total_travel_time)))

    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Mean travel time is: {} seconds'.format(int(mean_travel_time)))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    
    # TO DO: Display counts of user types
    count_usertypes = df['User Type'].value_counts()   
    for count, user_type in count_usertypes.items():
        print('Count of {}: {}'.format(count, user_type))
        
    # TO DO: Display counts of gender
    try:
        count_gender = df['Gender'].value_counts()   
        for count, user_gender in count_gender.items():
            print('Count of {}: {}'.format(count, user_gender))
    except:
        print("Gender not available in data file")

    # TO DO: Display earliest, most recent, and most common year of birth
    try:
        earliest_yearofbirth = int(df['Birth Year'].min())
        mostrecent_yearofbirth = int(df.tail(1).iloc[0]['Birth Year'])
        mostcommon_yearofbirth = int(df['Birth Year'].mode()[0])
        print('Earliest year of birth: {}'.format(earliest_yearofbirth))
        print('Most recent year of birth: {}'.format(mostrecent_yearofbirth))
        print('Most common year of birth: {}'.format(mostcommon_yearofbirth))
    except:
        print("Birth Year not available in data file")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    """Displays raw data of filtered bikeshare data if user asks for it."""
    
    while True:
        user_answer = input("Do you want to see raw data?\n").strip().lower()
        
        if user_answer == 'yes':
            last_line = 5
            print(df.iloc[0:last_line])
            while True:
                continue_raw = input("\nWould you like to see 5 more lines of raw data? Enter yes or no: ").strip().lower()
                if continue_raw == 'yes':
                    print(df.iloc[last_line:last_line + 5])
                    last_line += 5
                elif continue_raw == 'no':
                    break
                else:
                    print("Incorrect input. Please only enter yes or no.")
        elif user_answer == 'no':
            break
        else:
            print("Incorrect input. Please only enter yes or no.")
            continue
        break
        
        
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
