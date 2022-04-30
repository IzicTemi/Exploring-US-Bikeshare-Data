import time
import pandas as pd
import numpy as np
from tabulate import tabulate

months = ['january', 'february', 'march', 'april', 'may', 'june']
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
    while True:
        try:
            city = input('\nInput the city you want to explore from Chicago, New York City, Washington: ').lower()
            if city not in ['chicago', 'new york city', 'washington']:
                raise Exception
            break
        except KeyboardInterrupt:
            break
        except:
            print('\nInput a valid city')
        
    while True:
        try:
            filters = input('\nDo you want to filter by day, month, both or none: ')
            if filters not in ['day', 'month', 'both', 'none']:
                raise Exception
            break
        except KeyboardInterrupt:
            break
        except:
            print('\nInput a valid option')        

    # TO DO: get user input for month (all, january, february, ... , june)
    if filters == 'month':
        while True:
            try:
                month = input('\nInput the month you want to view from January, February, ... , June: ').lower()
                if month not in ['january', 'february', 'march', 'april', 'may' , 'june']:
                    raise Exception
                break
            except KeyboardInterrupt:
                break
            except:
                print('Pls input a valid month')
        
        day = 'all'
    elif filters == 'day':
        while True:
            try:
                day = input('Pls input the day you want to explore from Monday, Tuesday, ... , Sunday: ').lower()
                if day not in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday' , 'saturday', 'sunday']:
                    raise Exception
                break
            except KeyboardInterrupt:
                break
            except:
                print('Pls input a valid day')
        
        month = 'all'
    elif filters == 'both':
        while True:
            try:
                month = input('Pls input the month you want to view from all, january, february, ... , june: ').lower()
                if month not in ['all', 'january', 'february', 'march', 'april', 'may' , 'june']:
                    raise Exception
                break
            except KeyboardInterrupt:
                break
            except:
                print('Pls input a valid month')
        
        while True:
            try:
                day = input('Pls input the day you want to explore from all, monday, tuesday, ... , sunday: ').lower()
                if day not in ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday' , 'saturday', 'sunday']:
                    raise Exception
                break
            except KeyboardInterrupt:
                break
            except:
                print('Pls input a valid day')
        
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
