import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

possible_months = ["january", "february", "march", "april", "may", "june", "all"]

possible_days = ["all", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

# function was provided by udacity
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    got_data = False
    possibile_cities = ["chicago", "new york city", "washington", "new york"]
    while not got_data:
        try:
            input_city = input("Would you like to see data for Chicago, New York, or Washington?\n")
            input_city = input_city.strip().lower()
            if input_city in possibile_cities:
                if input_city == "new york city" or input_city == "new york":
                    city = "new_york_city"
                else:
                    city = input_city
                got_data = True
            else:
                print("Bad input, must be city in list\n")
        except:
            print("Bad input. Try Again\n")

    got_data = False
    possible_filters = ["month", "day", "not at all"]
    input_filter = ""
    while not got_data:
        try:
            inputfilter = input("Would you like to filter the data by month, day, or not at all?\n")
            inputfilter = inputfilter.strip().lower()
            if inputfilter in possible_filters:
                got_data = True
                input_filter = inputfilter
            else:
                print("Please select option from list\n")
        except:
            print("Bad input. Try Again\n")

    # get user input for month (all, january, february, ... , june)
    got_data = False
    
    if(input_filter == "month"):
        while not got_data:
            try:
                input_month = input("Which month - January, February, March, April, May, or June?\n")
                input_month = input_month.strip().lower()
                if input_month in possible_months:
                    got_data = True
                    month = input_month
                else:
                    print("Please select option from list\n")
            except:
                print("Bad input. Try Again\n")
    else:
        month = "all"

    # get user input for day of week (all, monday, tuesday, ... sunday)
    got_data = False
    
    if(input_filter == "day"):
        while not got_data:
            try:
                input_day = input("Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?\n")
                input_day = input_day.strip().lower()
                if input_day in possible_days:
                    day = input_day
                    got_data = True
                else:
                    print("Please select option from list\n")
            except:
                print("Bad input. Try Again\n")
    else:
        day = "all"

    print('-'*40)
    return city, month, day

#This function def was also done by udacity
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
    df = pd.read_csv("./" + city + ".csv")
    df["Start Time"] = pd.to_datetime(df["Start Time"])

    if month != "all":
        df = df[df["Start Time"].dt.month == possible_months.index(month)+1]

    if day != "all":
        df = df[df["Start Time"].dt.dayofweek == possible_days.index(day)-1]

        


    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print("\nThe most common month is: ", possible_months[df["Start Time"].dt.month.mode()[0] - 1])


    # display the most common day of week
    print("\nThe most common day is: ", possible_days[df["Start Time"].dt.dayofweek.mode()[0] + 1])


    # display the most common start hour
    print("\nThe most common hour is: ", df["Start Time"].dt.hour.mode()[0])


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("\nThe most common start station is: ", df["Start Station"].value_counts()[0])

    # display most commonly used end station
    print("\nThe most common end station is: ", df["End Station"].value_counts()[0])

    # display most frequent combination of start station and end station trip
    combination = df.groupby(["Start Station", "End Station"]).size().reset_index(name="count")
    combination = combination.sort_values("count", ascending = False)
    print("\nThe most common combination is: ", combination.iloc[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print("\nThe total trip duration is: ", df["Trip Duration"].sum())

    # display mean travel time
    print("\nThe average trip duration is: ", df["Trip Duration"].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("\nThe counts of user types are: ", df["User Type"].value_counts())

    # Display counts of gender
    print("\nThe counts of gender are: ", df["Gender"].value_counts())

    # Display earliest, most recent, and most common year of birth
    print("\nThe earliest birth year is: ", df["Birth Year"].min())
    print("\nThe latest birth year is: ", df["Birth Year"].max())
    print("\nThe most common birth year is: ", df["Birth Year"].mode())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        tracking_index = 0
        while True:
            try:
                answer = input("\nWould you like to see 5 lines of raw input data? yes or no\n")
                if answer.strip().lower() == "yes" or answer.strip().lower() == "y":
                    print(df.iloc[tracking_index:tracking_index+5])
                    tracking_index += 5
                elif answer.strip().lower() == "no" or answer.strip().lower() == "n":
                    break
                else:
                    print("Bad input try again")
            except:
                print("Bad input try again")

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
