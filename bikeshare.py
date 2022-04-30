import time
import pandas as pd
import numpy as np
from tabulate import tabulate

months = ['january', 'february', 'march', 'april', 'may', 'june']
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def check_data_entry(prompt, valid_entries): 
    """
    Asks user to type some input and verify if the entry typed is valid.
    Since we have 3 inputs to ask the user in get_filters(), it is easier to write a function.
    Args:
        (str) prompt - message to display to the user
        (list) valid_entries - list of string that should be accepted 
    Returns:
        (str) user_input - the user's valid input
    """
    try:
        user_input = str(input(prompt)).lower()

        while user_input not in valid_entries : 
            print('Sorry... it seems like you\'re not typing a correct entry.')
            print('Let\'s try again!')
            user_input = str(input(prompt)).lower()

        print('Great! the chosen entry is: {}\n'.format(user_input))
        return user_input

    except:
        print('Seems like there is an issue with your input')

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
    valid_cities = CITY_DATA.keys()
    prompt_cities = 'Please choose one of the 3 cities (chicago, new york city, washington): '
    city = check_data_entry(prompt_cities, valid_cities)

    valid_filters = ['day', 'month', 'both', 'none']
    prompt_filters = 'Do you want to filter by day, month, both or none:  '
    filters = check_data_entry(prompt_filters, valid_filters)    
            
    # TO DO: get user input for month (all, january, february, ... , june)
    if filters == 'month':
        valid_months = ['all','january','february','march','april','may','june']
        prompt_month = 'Please choose a month (all, january, february, ... , june): '
        month = check_data_entry(prompt_month, valid_months)
        
        day = 'all'
    elif filters == 'day':
        valid_days = ['all','monday','tuesday','wednesday','thursday','friday','saturday', 'sunday']
        prompt_day = 'Please choose a day (all, monday, tuesday, ... sunday): '
        day = check_data_entry(prompt_day, valid_days)
        
        month = 'all'
    elif filters == 'both':
        valid_days = ['all','monday','tuesday','wednesday','thursday','friday','saturday', 'sunday']
        prompt_day = 'Please choose a day (all, monday, tuesday, ... sunday): '
        day = check_data_entry(prompt_day, valid_days)

        valid_months = ['all','january','february','march','april','may','june']
        prompt_month = 'Please choose a month (all, january, february, ... , june): '
        month = check_data_entry(prompt_month, valid_months)
        
    else:
        day, month = 'all', 'all'

        

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

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['hour'] = df['Start Time'].dt.hour
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

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


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    print('\nMost common month: ', months[df['month'].mode()[0]-1].title())


    # TO DO: display the most common day of week
    print('\nMost common day of the week: ', df['day_of_week'].mode()[0])


    # TO DO: display the most common start hour
    print('\nMost common start hour: ', df['hour'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print('\nMost commonly used start station: ',df['Start Station'].mode()[0])


    # TO DO: display most commonly used end station
    print('\nMost commonly used end station: ',df['End Station'].mode()[0])

    # TO DO: display most frequent combination of start station and end station trip
    station_df = df['Start Station'] + "---" + df[ 'End Station']
    combo = station_df.mode()[0].split('---')
    print('\nMost frequent combination of start station and end station trip is {} to {} '.format(combo[0], combo[1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    print('\nTotal travel time: ', df['Trip Duration'].sum())


    # TO DO: display mean travel time
    print('\nMean travel time: ', df['Trip Duration'].mean())


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print('\nCounts of User Types: ', df['User Type'].value_counts())


    # TO DO: Display counts of gender
    try:
        print('\nCounts of gender: ', df['Gender'].value_counts())
    except KeyError:
        print('\nGender column not in data') 

    # TO DO: Display earliest, most recent, and most common year of birth
    try:
        print('\nEarliest year of birth: ', df['Birth Year'].min())
        print('\nMost recent year of birth: ', df['Birth Year'].max())
        print('\nMost common year of birth: ',df['Birth Year'].mode()[0])
    except KeyError:
        print('No Birth Year in data')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
   
def print_data(df):
    while True:
        try:
            view_data = input('\nDo you want to continue viewing the data? Enter yes or no: ')
            if view_data not in ['yes', 'no']:
                raise Exception
            break
        except KeyboardInterrupt:
            break
        except:
            print('Pls choose btw yes and no')
        
    return view_data
    

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        
        n = 0
        while True:
            view_data = print_data(df)  
            if view_data == 'yes':
                print(tabulate(df.iloc[np.arange(0+n,5+n)], headers ="keys"))
            
            else:
                break
            n += 5

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
