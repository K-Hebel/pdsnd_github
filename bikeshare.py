import time
import pandas as pd
import numpy as np
import calendar
import datetime
from matplotlib import pyplot as plt

#This program presents Bikeshare Data from three cities, Chicago, New York and Washington.  Users may view descriptive statistics of this data filtered by city or as an aggregation of all cities.   Users may also choose to filter data by month (January - June) and/or by day (Sunday-Saturday).

#This interactive program requires user input for user's name, data filter types, request for raw_data (viewed in lines of five), and request to repeat or end the program.

#Below is the dictionary of all data files available for search key= city and value= city.csv (data file).  Additional city data files may be added here in 'city':'file_name.csv' format.
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }


#Below are interactive questions for the user to provide user name and filter information. This will return City, Month, Day.
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    #Input User name
    name = input('What is your name? \n')
    print('\nHello {}! Are you ready to explore some US bikeshare data with me?  Let\'s go!\n'.format(name.title()))


    #Input City filter type, cities are contained in a list 'cities'. Additional city names may be added to the list as their data files are added to the CITY_DATA dictionary at the top of this file.
    i = 0
    wrong_answer = 0
    while i == 0:
        city = input('What city would you like to view:  All, Chicago, New York, Washington? \n').lower()
        cities =['chicago','new york','washington','all']
        if city in cities:
            i+= 1
            print('Perfect, you chose to view data for {}. Next Question......\n'.format(city.title()))
        else :
            print('The city name you entered is incorrect please try again.\n')
            wrong_answer += 1
            if wrong_answer >= 3 :
                city_error=input('You have entered an incorrect city name 3 times, do you want to continue?  yes or no \n\n').lower()
                if city_error == 'yes':
                    continue
                else :
                    raise SystemExit('This program has now ended.  Thank you for participating.\n\n')

    #Input Month filter type (all, january, february, ... , june)
    while i==1:
        month = input('\nWhat month of data would you like to review (All, January, February,....June)?\n').title()
        if month == 'All' or month in list(calendar.month_name[1:7]):
            print('\nGreat, we will be looking at data for this month: {}   Now on to our final question ->\n'.format(month.title()))
            i+=1
        else :
            print('\nThe month you entered is invalid, please try again.  Thanks\n')


    #Input Day of Week filter type (all, monday, tuesday, ... sunday)
    while i==2:
        day = input('\nWhat day of the week would you like to review (All, Sunday, Monday, Tuesday,....Saturday)?   \n').title()
        if day in list(calendar.day_name) or day =='All':
            print('\nGot it, we will be looking the following day: {}\n'.format(day.title()))
            i+=1
        else :
            print('\nThe day of the week you entered is incorrect, please try again.  I appreciate you.\n')

    print('-'*40)

    return city, month, day


#The following code loads CITY_DATA .csv files and converts them to filtered dataframes based on the City, Month, Day perameters returned by def get_filters
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

    #Reads CITY_DATA files based on the filter for a specific city.
    if city != 'all':
        df = pd.read_csv(CITY_DATA[city])

    #Reads and Combines all files in CITY_DATA into one dataframe df based on the 'All' filter for City
    else:
        i=0
        df_files = []
        while i < len(CITY_DATA):
            for city, csv_file in CITY_DATA.items():
                df_files.append(pd.read_csv(csv_file))
                i+=1
        df =pd.concat(df_files, sort=True)

    #Converts string values to datetime and adds additional columns for Month, Day of Week and Start Hour
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['Month'] =df['Start Time'].dt.month
    df['Day of Week'] =df['Start Time'].dt.dayofweek
    df['Start Hour'] = df['Start Time'].dt.hour


    # filter by month if applicable
    if month != 'All':
        months = list(calendar.month_name[:7])
        month = months.index(month)

    # filter by month to create the new dataframe
        df = df[df['Month']==month]


    # filter by day of week if applicable
    if day != 'All':
        days = list(calendar.day_name)
        day= days.index(day)
        df = df[df['Day of Week']==day]

    return df


#Displays statistics on the most frequent times of travel.
def time_stats(df,month,day):

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    #Display line Chart of total number of users per month when 'month' =='All'
    if month == 'All':
        df_month= df.groupby(['Month']).count()
        plt.plot(list(calendar.month_name[1:7]),df_month['Start Time'])
        plt.xlabel('Months')
        plt.ylabel('# of Users')
        plt.title('Trend Line of Users Per Month')
        plt.show()

    # Display the most frequent month
    print('\nThe busiest month was:  ',calendar.month_name[(df['Month'].mode()[0])])

    #Display line Chart of total number of users per day when 'day' =='All'
    if day == 'All':
        df_day= df.groupby(['Day of Week']).count()
        plt.plot(list(calendar.day_abbr),df_day['Start Time'])
        plt.xlabel('Day of Week')
        plt.ylabel('# of Users')
        plt.title('Trend Line of Users Per Day')
        plt.show()

    # Display the most common day of week
    print("\nThe busiest day of the week was:  ",calendar.day_name[(df['Day of Week'].mode()[0])])


    #Display line Chart of total Usage over 24 hours
    df_hour= df.groupby(['Start Hour']).count()
    plt.plot(pd.date_range(start='1/1/2020', periods=24 ,freq='H').strftime('%I:00 %p'),df_hour['Start Time'])
    plt.xlabel('Time of Day')
    plt.ylabel('# of Users')
    plt.title('Trend Line of Users By Hour')
    plt.show()

    # Display the most common start hour
    start_hour = df['Start Hour'].mode()[0]
    print("\nThe most common starting hour was:   ", datetime.time(start_hour).strftime("%I:00 %p"))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


#Displays statistics on the most popular stations and trip.
def station_stats(df):

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    print('Most Commonly Used Start Station was: ',df['Start Station'].mode()[0], '\n\n')

    # Display most commonly used end station
    print('Most Commonly Used End Station was:  ', df['End Station'].mode()[0], '\n\n')

    # Display most frequent combination of start station and end station trip
    df["Combo"] = df['Start Station'] + " / " + df['End Station']
    print('The most frequent combination of start / end station trips was:  ',df['Combo'].mode()[0]  ,'\n\n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


 #Displays statistics on the total and average trip duration.
def trip_duration_stats(df):

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    print('\nTotal travel time on bikes was: ', time.strftime("%H hours: %M minutes: %S seconds", time.gmtime(int(df['Trip Duration'].sum()))))

    # Display mean travel time
    print('\nAverage travel time on bikes was: ', time.strftime("%H hours: %M minutes: %S seconds", time.gmtime(int(df['Trip Duration'].mean()))))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


#Displays statistics on bikeshare users.
def user_stats(df):

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('\nThe count of users by user type is:\n',df['User Type'].value_counts())


    #Display bar chart of Users based on Gender, if gender column is included in data
    if 'Gender' in df.columns:
        df_gender= df.groupby(['Gender']).count()
        plt.bar(['Female','Male'],df_gender['Start Time'])
        plt.ylabel('Number of Users')
        plt.title('All Users by Gender')
        plt.show()

    # Display counts of gender if data available
        print('\n\nThe count of users by gender is:\n', df['Gender'].value_counts())
    else :
        print('\nThis data set does not contain information on gender.\n\n')


    # Display earliest, most recent, and most common year of birth if data available
    if 'Birth Year' in df.columns:
        print('\nThe earliest year of user birth is: ',int(df['Birth Year'].min()), '\n\nThe most recent birth year is: ',int(df['Birth Year'].max()), '\n\nAnd the most common birth year was:  ',int(df['Birth Year'].mean()))

    else:
        print('\nThis data set does not contain information on birth year.\n\n')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


#Display 5 lines of raw data from filtered dataframe based on user input (yes/no)
def more_raw_data(df):
    more = input('\n\nWould you like to see 5 lines of data from the raw data set?  Yes or No\n').lower()
    i=0
    if more == 'yes':
        while i < len(df.index):
            print(df.iloc[i:i+5])
            i+= 5
            more = input('\n\nWould you like to see another 5 lines of raw data?  Yes or No\n').lower()
            if more == 'no':
                break
    else :
        print('\n\nThank you for looking at this data.  We hope that it was useful and informative.  Have a great day')


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df,month,day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        more_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
