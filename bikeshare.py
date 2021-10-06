import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
months    = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
days      = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city  - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day   - name of the day of week to filter by, or "all" to apply no day filter
    """

    
    print('Hello! Let\'s explore some US bikeshare data!')
    # Get user input for city (chicago, new york city, washington).
    while True:
        city = input("Which City would you like to explore? Chicago, New York City, or Washington?: ").lower()
        if not city in CITY_DATA:
            print("\nSorry that is not a valid city. Valid cities are Chicago, New York City, and Washington.\n")
            continue
        else:
            break

    # Get user input for month (all, january, february, ... , june)     
    while True:
        month = input("Would you like to filter by month, or view all data? (e.g. all, january, february, ... , june): ").lower()
        if not month in months:
            print("\nSorry that is not a valid month. Valid months are all, january, february, ... , june.\n")
            continue
        else:
            break

    # Get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("Would you like to filter by day, or view all data? (all, monday, tuesday, ... sunday): ").lower()
        if not day in days:
            print("\nSorry that is not a valid day. Valid days are all, monday, tuesday, ... sunday.\n")
            continue
        else:
            break

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city  - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day   - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day'] = df['Start Time'].dt.weekday_name
    
    # filter by month if user did not input all
    if month != 'all':
        # use the index of the months list to get the corresponding int because month_name doesnt work :(
        month = months.index(month)
        df = df[df['month'] == month]

    # filter by month if user did not input all
    if day != 'all':
        df = df[df['day'] == day.title()]
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    popular_month = months[df['month'].mode()[0]].title()
    print('Most Popular Month: {}'.format(popular_month))
    
    # Display the most common day of week
    print('Most Popular Day: {}'.format(df['day'].mode()[0]))
    
    # Extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour
          
    # Display the most common start hour
    print('Most Popular Start Hour: {}'.format(df['hour'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    print('Most Popular Start Station: {}'.format(df['Start Station'].mode()[0]))

    # Display most commonly used end station
    print('Most Popular End Statuion: {}'.format(df['End Station'].mode()[0]))

    # Display most frequent combination of start station and end station trip
    popular_station_combo = (df['Start Station'] + ';' + df['End Station']).mode()
    print('The most popular combination of start and end stations is: {}'.format(popular_station_combo[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    print("Total Tavel Time: {}".format(df["Trip Duration"].sum()))

    # Display mean travel time
    print("Mean Tavel Time: {}".format(df["Trip Duration"].mean()))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("Counts of User Types:")
    print('{}\n'.format(df['User Type'].value_counts()))

    # Display counts of gender
    if 'Gender' in df.columns:
        print("Counts of User's Gender:")
        print("{}\n".format(df['Gender'].value_counts()))
    else:
        print('There is no Gender data for this city')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print("Earliest Birth Year: {}".format(df['Birth Year'].min()))
        print("Most Recent Birth Year: {}".format(df['Birth Year'].max()))
        print("Most Common Birth Year: {}".format(df['Birth Year'].mode()[0]))
    else:
        print('There is no Birth data for this city')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    
def load_raw_data(df):
    """Displays raw data upon user request until the user quits."""
    
    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n').lower()
    start_loc = 0
    while (view_data == 'yes'):
        print(df.iloc[start_loc:start_loc+5])
        start_loc += 5
        view_data = input("Do you wish to continue?: ").lower()

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        load_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
