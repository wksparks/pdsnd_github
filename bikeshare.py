import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data! Currently available for Chicago, New York City, and Washington')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    # Since the cities have different first letters, have the user enter the first letter of the city to reduce input errors
    city_choice = input("Please choose a city, \n For Chicago type: c \n For New York City type: n \n For Washington type: w\n ")

    while city_choice not in {'c','n','w'}:
        print("Invalid input - You must choose c, n, or w")
        city_choice = input("Please choose a city, \n For Chicago type: c \n For New York City type: n \n For Washington type: w\n ").lower()
    # assign the input letter to correct city
    if city_choice == 'c':
        city = 'chicago'
    elif city_choice == 'n':
        city = 'new york city'
    elif city_choice == 'w':
        city = 'washington'


    # determine if the user wants to filter by month or date or both or not at all
    time_choice = input('\n\nWould you like to analyze {}\'s data by month, day, both, or none? \nType month or day or both or none: \n '.format(city.title())).lower()

    while time_choice not in {'month','day','both','none'}:
        print("Invalid input")
        time_choice = input('\n\nWould you like to filter {}\'s data by month, day, both, or none? \nType month or day or both or none: \n '.format(city.title())).lower()
    # call two different functions to handle time_choice -- get_month, get_day, and use both functions for all
    if time_choice == 'none':
        month, day = 'all', 'all'
    elif time_choice == 'month':
        month = get_month()
        day = 'all'
    elif time_choice == 'day':
        day = get_day()
        month = 'all'
    elif time_choice == 'both':
        month = get_month()
        day = get_day()



    print('-'*40)
    return city, month, day

# define function that gets the month -- call function get_month
def get_month():
    """
    Asks user to specify a month to analyze.

    Returns:
        (str) month - name of the month to filter by

    """
    print("\nThere are only six months of data - January to June\n")
    print("\nWe hope to add additional months soon")
    month = input("Please enter a value from 1 to 6 to specify the month, \n For example if you want January enter: 1 \n For June, enter 6:\n ")

    while month not in {'1','2','3','4','5','6'}:
        print("You did not choose a number based on January to June (1 to 6)")
        month = input("Please enter a value from 1 to 6 to specify the month, \n For example if you want January enter: 1 \n For June, enter 6:\n")

    return month

# define function that gets the day -- call function get_day
def get_day():
    """
    Asks user to specify a day to analyze.

    Returns:
        (str) day - name of the day to filter by

    """
    print("There are seven days in a week. Please consider Sunday as the first day of the week.")
    day = input("Please enter a value from 1 to 7 for the day of the week beginning with Sunday. \n Sunday is 1, Monday is 2, Tuesday is 3... \n ")

    while day not in {'1','2','3','4','5','6','7'}:
        print("Invalid Input - You must enter a number from 1 to 7 for the day of the week.")
        day = input("Please enter a value from 1 to 7 for the day of the week, \n Sunday is 1, Monday is 2, Tuesday is 3... \n ")

    return day


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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column using datetime from time
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month, hour and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour



    # filter by month if applicable
    if month != 'all':


        # filter by month to create the new dataframe
        df = df[df['month'] == int(month)]

    # filter by day of week if applicable
    if day != 'all':
        # use the index of the days list to get the corresponding int
        days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday','Saturday']
        day = days[int(day)-1]
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print('\nMost Common Month: ' + str(df['month'].mode()[0]))


    # display the most common day of week
    print('\nMost Common Day of Week: ' + str(df['day_of_week'].mode()[0]))


    # display the most common start hour
    print('\nMost Common Start hour: ' + str(df['hour'].mode()[0]))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('\nMost Commonly Used Start Station: ' + str(df['Start Station'].mode()[0]))

    # display most commonly used end station
    print('\nMost Commonly Used End Station: ' + str(df['End Station'].mode()[0]))

    # display most frequent combination of start station and end station trip
    print('\nMost Frequent Combination of Start and End Station Trip: ' + str(df.groupby(['Start Station','End Station']).size().idxmax()))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('\nTotal Travel Time in Seconds: ' + str(df['Trip Duration'].sum()))

    # display mean travel time
    print('\nMean Travel Time in Seconds: ' + str(df['Trip Duration'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('\nCounts of User Types: \n' + str(df['User Type'].value_counts()))

    # display gender counts if the city is not Washington
    if city != 'washington':
        print('\nGender Counts: \n' + str(df['Gender'].value_counts()))

    # Display earliest, most recent, and most common year of birth
    if city != 'washington':
        print('\nEarliest Year of Birth: ' + str(int(df['Birth Year'].min())))
        print('\nLatest Year of Birth: ' + str(int(df['Birth Year'].max())))
        print('\nMost Common Year of Birth: ' + str(int(df['Birth Year'].mode()[0])))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def show_raw_data(city):
    """
    Asks the user if they want to see 5 rows of data
    if yes then it prints 5 rows and then asks the user again
    """
    show_raw = input("Would you like to see 5 rows of raw data? \n Type: yes or no \n ").lower()

    while show_raw not in {'yes','no'}:
        print("Invalid input -- You must answer yes or no.")
        show_raw = input("Would you like to see 5 rows of data? \n Type: yes or no \n ").lower()

    if show_raw == 'no':
        return

    for five_rows in pd.read_csv((CITY_DATA[city]), chunksize=5):
        print(five_rows)
        show_raw = input("Would you like to see 5 more rows of data? \n Type: yes or no \n ").lower()

        while show_raw not in {'yes','no'}:
            print("Invalid input -- You must answer yes or no.")
            show_raw = input("Would you like to see 5 more rows of data? \n Type: yes or no \n ").lower()

        if show_raw == 'no':
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        show_raw_data(city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
