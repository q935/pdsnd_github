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
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = ''
    while city not in CITY_DATA:
        city = input("Please type in the city name for the analysis (Chicago, New York City, Washington): ").lower()

    # TO DO: get user input for month (all, january, february, ... , june)
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december','all']	
    month = ''
    while month not in months:
        month = input("Please type in the month name for the analysis (type all to see all months): ").lower()

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['monday', 'tuesday', 'wednesday','thursday', 'friday','saturday', 'sunday', 'all']
    day = ''
    while day not in days:
        day = input("Please type in the weekday for the analysis (type all to see all weekdays):").lower()

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
        no_of_lines - interger with number of lines that are beeing analyzed in total
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month] # boolean indexing as filter

    # filter by day of week if applicable
    if day != 'all':
    # filter by day of week to create the new dataframe
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        df = df[df['day_of_week'] == day.title()]

    # get the number of total lines to analyze (from 'Start Station' as it does not contain NaN values)
    no_of_lines = df['Start Station'].count()
    print("You are analyzing {} lines of data".format(no_of_lines))
    print('-'*40)

    return df, no_of_lines

def occurrence_stats(df,column,no_of_lines):
    """Calculates occurrence and percentage of the mode for a column."""

    occurrence = df[column].isin(df[column].mode()).sum()
    percentage = occurrence / no_of_lines * 100
    print("occuring {} times - that is {:.2f} %".format(occurrence,percentage))

    return occurrence, percentage

def time_stats(df,no_of_lines):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
    most_common_month = months[df['month'].mode()[0]-1].title()
    print("The most common month is {}".format(most_common_month))
    occurrence, percentage = occurrence_stats(df, 'month', no_of_lines)

    # TO DO: display the most common day of week
    most_common_weekday = df['day_of_week'].mode()[0]
    print("The most common weekday is {}".format(most_common_weekday))
    occurrence, percentage = occurrence_stats(df, 'day_of_week', no_of_lines)

    # TO DO: display the most common start hour
    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    # find the most popular hour
    most_common_hour = df['hour'].mode()[0]
    print("The most common hour is {}".format(most_common_hour))
    occurrence, percentage = occurrence_stats(df, 'hour', no_of_lines)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df, no_of_lines):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print("The most common start station is {}".format(most_common_start_station))
    occurrence, percentage = occurrence_stats(df, 'Start Station', no_of_lines)

    # TO DO: display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print("The most common end station is {}".format(most_common_end_station))
    occurrence, percentage = occurrence_stats(df, 'End Station', no_of_lines)

    # create a column for combining start and end stations
    df['start-end-station'] = df['Start Station'] + " / " + df['End Station']

    # TO DO: display most frequent combination of start station and end station trip
    most_common_combination_of_stations = (df['start-end-station']).mode()[0]
    print("The most common combination of start and end station trip is {}".format(most_common_combination_of_stations))
    occurrence, percentage = occurrence_stats(df, 'start-end-station', no_of_lines)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()/60/60/24
    print("The total travel time is {:.2f} days".format(total_travel_time))

    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()/60
    print("The mean travel time is {:.2f} minutes".format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,no_of_lines):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print("\nOverview on user types:")
    print(df['User Type'].value_counts())

    # TO DO: Display counts of gender
    print("\nOverview on gender:")
    print(df['Gender'].value_counts())

    # TO DO: Display earliest, most recent, and most common year of birth
    min_year_of_birth = df['Birth Year'].min()
    print("\nThe minimum year of birth is {:.0f}".format(min_year_of_birth))

    max_year_of_birth = df['Birth Year'].max()
    print("\nThe maximum year of birth is {:.0f}".format(max_year_of_birth))

    most_common_year_of_birth = df['Birth Year'].mode()[0]
    print("\nThe most common year of birth is {:.0f}".format(most_common_year_of_birth))
    occurrence, percentage = occurrence_stats(df, 'Birth Year', no_of_lines)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def get_chunk(dataframe: pd.DataFrame, chunk_size: int, start_row: int = 0):
    """Gets slice of dataframe by chunk size"""
    end_row  = min(start_row + chunk_size, dataframe.shape[0])

    return dataframe.iloc[start_row:end_row, :]

def show_raw_data(df):
    """Shows lines of raw data including user prompt"""
    chunk_size = 5
    start_row = 0
	while True:
		raw_data_prompt = input("\nWould you like to see {} more lines of raw data? (Y/N) ".format(chunk_size)).lower()
		if raw_data_prompt == 'y':
			chunk = get_chunk(df,chunk_size,start_row)
			chunk = chunk.iloc[:,1:8] # show only raw data columns and not calculated columns in this programm
			print(chunk)
			start_row += chunk_size
		else:
			break

def main():
    while True:
        city, month, day = get_filters()
        df,no_of_lines = load_data(city, month, day)

        time_stats(df,no_of_lines)
        station_stats(df,no_of_lines)
        user_stats(df,no_of_lines)
        trip_duration_stats(df)
        show_raw_data(df)

        restart = input('\nWould you like to restart? ? (Y/N)')
        if restart.lower() != 'y':
            break

if __name__ == "__main__":
	main()