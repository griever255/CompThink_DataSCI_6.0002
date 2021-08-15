# -*- coding: utf-8 -*-
# Problem Set 5: Experimental Analysis
# Name: 
# Collaborators (discussion):
# Time:

import pylab
import re

#set line width
pylab.rcParams['lines.linewidth'] = 4
#set font size for titles 
pylab.rcParams['axes.titlesize'] = 18
#set font size for labels on axes
pylab.rcParams['axes.labelsize'] = 18
#set size of numbers on x-axis
pylab.rcParams['xtick.labelsize'] = 16
#set size of numbers on y-axis
pylab.rcParams['ytick.labelsize'] = 16
#set size of ticks on x-axis
pylab.rcParams['xtick.major.size'] = 7
#set size of ticks on y-axis
pylab.rcParams['ytick.major.size'] = 7
#set size of markers
pylab.rcParams['lines.markersize'] = 10

# cities in our weather data
CITIES = [
    'BOSTON',
    'SEATTLE',
    'SAN DIEGO',
    'PHILADELPHIA',
    'PHOENIX',
    'LAS VEGAS',
    'CHARLOTTE',
    'DALLAS',
    'BALTIMORE',
    'SAN JUAN',
    'LOS ANGELES',
    'MIAMI',
    'NEW ORLEANS',
    'ALBUQUERQUE',
    'PORTLAND',
    'SAN FRANCISCO',
    'TAMPA',
    'NEW YORK',
    'DETROIT',
    'ST LOUIS',
    'CHICAGO'
]

TRAINING_INTERVAL = range(1961, 2010)
TESTING_INTERVAL = range(2010, 2016)

"""
Begin helper code
"""
class Climate(object):
    """
    The collection of temperature records loaded from given csv file
    """
    def __init__(self, filename):
        """
        Initialize a Climate instance, which stores the temperature records
        loaded from a given csv file specified by filename.

        Args:
            filename: name of the csv file (str)
        """
        self.rawdata = {}

        f = open(filename, 'r')
        header = f.readline().strip().split(',')
        for line in f:
            items = line.strip().split(',')

            date = re.match('(\d\d\d\d)(\d\d)(\d\d)', items[header.index('DATE')])
            year = int(date.group(1))
            month = int(date.group(2))
            day = int(date.group(3))

            city = items[header.index('CITY')]
            temperature = float(items[header.index('TEMP')])
            if city not in self.rawdata:
                self.rawdata[city] = {}
            if year not in self.rawdata[city]:
                self.rawdata[city][year] = {}
            if month not in self.rawdata[city][year]:
                self.rawdata[city][year][month] = {}
            self.rawdata[city][year][month][day] = temperature
            
        f.close()

    def get_yearly_temp(self, city, year):
        """
        Get the daily temperatures for the given year and city.

        Args:
            city: city name (str)
            year: the year to get the data for (int)

        Returns:
            a 1-d pylab array of daily temperatures for the specified year and
            city
        """
        temperatures = []
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        for month in range(1, 13):
            for day in range(1, 32):
                if day in self.rawdata[city][year][month]:
                    temperatures.append(self.rawdata[city][year][month][day])
        return pylab.array(temperatures)

    def get_daily_temp(self, city, month, day, year):
        """
        Get the daily temperature for the given city and time (year + date).

        Args:
            city: city name (str)
            month: the month to get the data for (int, where January = 1,
                December = 12)
            day: the day to get the data for (int, where 1st day of month = 1)
            year: the year to get the data for (int)

        Returns:
            a float of the daily temperature for the specified time (year +
            date) and city
        """
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        assert month in self.rawdata[city][year], "provided month is not available"
        assert day in self.rawdata[city][year][month], "provided day is not available"
        return self.rawdata[city][year][month][day]

def se_over_slope(x, y, estimated, model):
    """
    For a linear regression model, calculate the ratio of the standard error of
    this fitted curve's slope to the slope. The larger the absolute value of
    this ratio is, the more likely we have the upward/downward trend in this
    fitted curve by chance.
    
    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by a linear
            regression model
        model: a pylab array storing the coefficients of a linear regression
            model

    Returns:
        a float for the ratio of standard error of slope to slope
    """
    assert len(y) == len(estimated)
    assert len(x) == len(estimated)
    EE = ((estimated - y)**2).sum()
    var_x = ((x - x.mean())**2).sum()
    SE = pylab.sqrt(EE/(len(x)-2)/var_x)
    return SE/model[0]

"""
End helper code
"""

def generate_models(x, y, degs):
    """
    Generate regression models by fitting a polynomial for each degree in degs
    to points (x, y).

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        degs: a list of degrees of the fitting polynomial

    Returns:
        a list of pylab arrays, where each array is a 1-d array of coefficients
        that minimizes the squared error of the fitting polynomial
    """
    reg_vals = []
    for deg in degs:
        reg_vals.append(pylab.polyfit(x, y, deg))
    return reg_vals

def r_squared(y, estimated):
    """
    Calculate the R-squared error term.
    
    Args:
        y: 1-d pylab array with length N, representing the y-coordinates of the
            N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the R-squared error term
    """
    error = ((y - estimated)**2).sum()
    mean = sum(y)/len(y)
    variability = ((y- mean)**2).sum()
    return 1 - error/variability

def evaluate_models_on_training(x, y, models):
    """
    For each regression model, compute the R-squared value for this model with the
    standard error over slope of a linear regression line (only if the model is
    linear), and plot the data along with the best fit curve.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        R-square of your model evaluated on the given data points,
        and SE/slope (if degree of this model is 1 -- see se_over_slope). 

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    for model in models:
        pylab.figure()
        pylab.plot(x, y, "bo", label = "Data Points")
        pylab.xlabel("Year")
        pylab.ylabel("Temperature, degC")
        deg = len(model)-1
        estimated = pylab.polyval(model, x)
        r2 = r_squared(y, estimated)
        if deg == 1:
            se_slope = se_over_slope(x, y, estimated, model)
            pylab.plot(x, estimated, "r-", label = "Model")
            pylab.title(f"Model of Degree {deg} \n R2 = {str(round(r2, 5))}, SE/Slope = {str(round(se_slope,5))}")
        else:
            pylab.plot(x, estimated, label = "Model")
            pylab.title(f"Model of {deg}, R2 = {r2}")
        pylab.legend(loc = 'best')
    pylab.show()

def gen_cities_avg(climate, multi_cities, years):
    """
    Compute the average annual temperature over multiple cities.

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to average over (list of str)
        years: the range of years of the yearly averaged temperature (list of
            int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the average annual temperature over the given
        cities for a given year.
    """
    city_avg_temps = []
    for year in years:
        avg_yearly_temps = []
        for city in multi_cities:
            avg_yearly_temps.append(climate.get_yearly_temp(city, year).sum()/len(climate.get_yearly_temp(city, year)))
        avg_yearly_temps = pylab.array(avg_yearly_temps)
        city_avg_temps.append(avg_yearly_temps.sum()/len(avg_yearly_temps))
    city_avg_temps = pylab.array(city_avg_temps)
    return city_avg_temps


def moving_average(y, window_length):
    """
    Compute the moving average of y with specified window length.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        window_length: an integer indicating the window length for computing
            moving average

    Returns:
        an 1-d pylab array with the same length as y storing moving average of
        y-coordinates of the N sample points
    """
    moving_average = []
    LENGTH = len(y)
    for index in range(LENGTH):
        sum = 0
        if window_length-1 >= index:
            for i in range(index+1):
                sum += y[i]
            moving_average.append(sum/(index+1))
        else:
            for i in range(index-(window_length-1), index+1):
                sum += y[i]
            moving_average.append(sum/window_length)
    moving_average = pylab.array(moving_average)
    return moving_average


def rmse(y, estimated):
    """
    Calculate the root mean square error term.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the root mean square error term
    """
    error = ((y - estimated)**2).sum()
    n = len(y)
    return (error/n)**0.5

def gen_std_devs(climate, multi_cities, years):
    """
    For each year in years, compute the standard deviation over the averaged yearly
    temperatures for each city in multi_cities. 

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to use in our std dev calculation (list of str)
        years: the range of years to calculate standard deviation for (list of int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the standard deviation of the average annual 
        city temperatures for the given cities in a given year.
    """
    city_avg_temps = []
    city_sd_temps = []
    for year in years:
        days_in_year = len(climate.get_yearly_temp("NEW YORK", year))
        avg_temp_that_day = []
        for day in range(days_in_year):
            temperatures_that_day = []
            for city in multi_cities:
                temperatures_that_day.append(climate.get_yearly_temp(city, year)[day])
            temperatures_that_day = pylab.array(temperatures_that_day)
            avg_temp_that_day.append(temperatures_that_day.sum()/len(temperatures_that_day))
        avg_temp_that_day = pylab.array(avg_temp_that_day)
        variance = avg_temp_that_day.var()
        city_sd_temps.append(variance**0.5)
    city_sd_temps = pylab.array(city_sd_temps)
    return city_sd_temps

def evaluate_models_on_testing(x, y, models):
    """
    For each regression model, compute the RMSE for this model and plot the
    test data along with the model’s estimation.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        RMSE of your model evaluated on the given data points. 

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    for model in models:
        pylab.figure()
        pylab.plot(x, y, "bo", label = "Data Points")
        pylab.xlabel("Year")
        pylab.ylabel("Temperature, degC")
        deg = len(model)-1
        estimated = pylab.polyval(model, x)
        RMSE = rmse(y, estimated)
        pylab.plot(x, estimated, label = "Model")
        pylab.title(f"Model of {deg}, rmse = {RMSE}")
        pylab.legend(loc = 'best')
    pylab.show()

if __name__ == '__main__':
    
    climate = Climate("data.csv")
    x_vals = pylab.array(TRAINING_INTERVAL)

    # # Part A.4
    # training_daily_temps = []
    # for year in TRAINING_INTERVAL:
    #     training_daily_temps.append(climate.get_daily_temp("NEW YORK", 1, 10, year))
    # training_daily_temps = pylab.array(training_daily_temps)
    # model = generate_models(x_vals, training_daily_temps, [1])
    # evaluate_models_on_training(x_vals, training_daily_temps, model)

    # # Part B
    # cities_avg = gen_cities_avg(climate, CITIES, TRAINING_INTERVAL)
    # model = generate_models(x_vals, cities_avg, [1])
    # evaluate_models_on_training(x_vals, cities_avg, model)

    # # Part C
    # cities_avg = gen_cities_avg(climate, CITIES, TRAINING_INTERVAL)
    # moving_avg = moving_average(cities_avg, 5)
    # model = generate_models(x_vals, moving_avg, [1])
    # evaluate_models_on_training(x_vals, moving_avg, model)

    # # Part D.2
    # cities_avg = gen_cities_avg(climate, CITIES, TRAINING_INTERVAL)
    # moving_avg = moving_average(cities_avg, 5)
    # model = generate_models(x_vals, moving_avg, [1, 2, 20])
    # evaluate_models_on_training(x_vals, moving_avg, model)

    # test_x_vals = pylab.array(TESTING_INTERVAL)
    # test_cities_avg = gen_cities_avg(climate, CITIES, TESTING_INTERVAL)
    # test_moving_avg = moving_average(test_cities_avg, 5)
    # evaluate_models_on_testing(test_x_vals, test_moving_avg, model)

    # Part E
    cities_sd = gen_std_devs(climate, CITIES, TRAINING_INTERVAL)
    moving_avg = moving_average(cities_sd, 5)
    model = generate_models(x_vals, moving_avg, [1])
    evaluate_models_on_training(x_vals, moving_avg, model)
