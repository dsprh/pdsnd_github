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
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). 
    while True:
        city = input("Would you like to see data for Chicago, New York City, or Washington?\n").lower()

        if city not in ('chicago','new york city','washington'):
            print("\nSorry! We don't have data for that city. ")
        else:
            break

    # get user input for filter (month, day, no filter)
    while True:
        filter = input("\nWould you like to filter by month, day, or show all data? Type 'all' for no filter.\n").lower()

        if filter not in {'month','day','all'}:
            print("\nSorry, that's not a valid filter.")
        else:
            break
        
    if filter == 'month':
        while True:
            # get user input for month (january, february, ... , june)
            month = input("\nWhich month would you like to see data for? January, February, March, April, May, or June?\n").lower()
            day = 'all' 

            if month not in {'january', 'february', 'march', 'april', 'may', 'june'}:
                print("\nSorry, we don't have data for that month. Please enter a valid selection.\n")
            else:
                break
    elif filter == 'day':
        while True:
            # get user input for day of week (monday, tuesday, ... sunday)
            day = input("\nWhich day would you like to see data for? ").lower()
            month = 'all' 

            if day not in {'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'}:
                print("\nPlease enter a valid day of the week!\n")
            else:
                break       
    elif filter == 'all':
        month = 'all'
        day = 'all'

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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    
    return df


def time_stats(df, city, month, day):
    """Displays statistics on the most frequent times of travel."""

    print(f'\nCalculating The Most Frequent Times of Travel for {city.title()}...\n')
    start_time = time.time()

    # display the most common month if data is not filtered by month
    if month == 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        popular_month = df['month'].mode()[0]
        print(f"The most popular month for travel is: {months[popular_month - 1].title()}")

    # display the most common day of week if data is not filtered by day
    if day == 'all':
        popular_day = df['day_of_week'].mode()[0]
        print(f"The most popular day to travel is: {popular_day}")

    # find the most common hour (from 0 to 23)
    popular_hour = df['hour'].mode()[0]
    print(f"The most popular start time is: {popular_hour}:00")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df, city):
    """Displays statistics on the most popular stations and trip."""

    print(f'\nCalculating The Most Popular Stations and Trip Info for {city.title()}...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start = df['Start Station'].mode()[0]
    print(f"The most popular start station is: {popular_start}")

    # display most commonly used end station
    popular_end = df['End Station'].mode()[0]
    print(f"The most popular end station is: {popular_end}")

    # display most frequent combination of start station and end station trip
    combo = df.groupby(['Start Station','End Station']).size().idxmax()
    combo_start, combo_end = combo
    print(f"The most frequent combination of start and end stations is: {combo_start} (start) & {combo_end} (end)")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df, city):
    """Displays statistics on the total and average trip duration in minutes."""

    print(f'\nCalculating Trip Duration stats for {city.title()}...\n')
    start_time = time.time()

    # display total travel time
    tot_trip = df['Trip Duration'].sum() / 60
    print(f"The total travel time was: {round(tot_trip)} minutes")

    # display mean travel time
    avg_trip = df['Trip Duration'].mean() / 60
    print(f"The average trip duration was: {round(avg_trip)} minutes")

    #display min and max trip lengths, rounded to hudredths place for readability
    print(f"The shortest trip length was: {round(np.min(df['Trip Duration'], axis=0) / 60, 2)} minutes")
    print(f"The longest trip length was: {round(np.max(df['Trip Duration'], axis=0) / 60, 2)} minutes")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users. Gender and birth year stats are only displayed for Chicago and NYC."""

    print(f'\nCalculating User Stats for {city.title()}...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()

    print(user_types)

    # Display counts of gender only if the user chose Chicago or New York City
    if city in {'chicago', 'new york city'}:
        gender_ct = df['Gender'].value_counts()

        print(gender_ct)

        # Display earliest, most recent, and most common year of birth
        print("The earlest birth year in this data set is: ", np.min(df['Birth Year'], axis=0))
        print("The most recent birth year in this data set is: ", np.max(df['Birth Year'], axis=0))
        print("The most common birth year in this data set is: ", df['Birth Year'].mode()[0])


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    """Displays raw data for city and filter chosen, 5 rows at a time."""

    show_data = input("\nWould you like to see the raw data for the city and filter selected? Enter yes or no.\n").lower()
    row_ct = 0

    while True:
        if show_data == 'yes':
            row_ct += 5
            print(df.iloc[row_ct - 5:row_ct])
            show_data = input("\nWould you like to view 5 more rows of raw data?\n")

        else:
            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, city, month, day)
        station_stats(df, city)
        trip_duration_stats(df, city)
        user_stats(df, city)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
