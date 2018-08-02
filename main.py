# ######################################################################################################################
# Project Imports
import pandas as pd
import numpy as np
import plotly
import random
import plotly.plotly as py
from plots import *
from fine_printer import fine_print
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
# --- Connect to plot.ly
plotly.tools.set_credentials_file(username='paulprokhorenko', api_key='AHz2OqXUe8cSlBYcmsat')


# ######################################################################################################################
# Emulation of real data
data_set = np.random.uniform(1, 5, 31)
data_set = [round(value, 2) for value in data_set]

# --- Creating of missing values (I propose up to 3 values, to avoid spoiling of data)
random_missing_values = [random.randint(0, 30) for number in range(3)]

# --- Instead of initial values making a zero values
for index in random_missing_values:
    data_set[index] = 0

# --- Creating a numpy array
data_set = np.array(data_set)

# --- Pass data to plot
trace = go.Scatter(y=data_set, mode='lines')
data = [trace]

# --- Creating of the plot
fig = go.Figure(data=data, layout=get_layout('1. Prices distribution', 750, 400))

# --- Pass it to Plot.ly
url = py.plot(fig, filename='prices-distribution', height=750)

print('\n--------------- 1. Initial data ---------------\n')
print('\t Baseline data available on link: ', url)

# --- Saving data to csv file
np.savetxt("data_set.csv", data_set, delimiter=",")

# ######################################################################################################################
# ETL process
# --- Reading data from csv file

data_frame = pd.read_csv("data_set.csv", header=None, names=['Prices'])

# Univariate analysis
# --- Creating copy of dataframe to use it in univariate analysis
data_for_univariate_analysis = data_frame.copy()
data_for_univariate_analysis['Days'] = range(1, 32)

# --- Pass data to plot
data = [
    go.Histogram2dContour(
        x=data_for_univariate_analysis['Prices'],
        y=data_for_univariate_analysis['Days'],
        colorscale=get_colorscale('YlGnBu'),
    )
]

# --- Creating of the plot
fig1 = go.Figure(data=data, layout=get_layout('2. Univariate analysis of prices', 700, 750))
url1 = py.plot(fig1, filename='2d-histogram', height=750)

print('\n--------------- 2. Univariate analysis of prices ---------------\n')
print('\t Histogram of baseline data available on link: ', url1)

# --- Central tendency
prices = data_for_univariate_analysis['Prices']
mean, median = prices.mean(), prices.median()
mode = prices.mode()  # For this data is useless
maximum, minimum = prices.max(), prices.min()
print('Central tendencies\n')
print('Mean is: {}\n'
      'Median is: {} \n'
      'Mode is: {}\n'
      'Min is: {}\n'
      'Max is:{}'.format(mean, median, mode, minimum, maximum))

# Bi-variate analysis
# --- Pass it to Plot.ly
data_for_bi_variate_analysis = data_frame.copy()
day_list = [str(day) for week in range(5) for day in range(7)]
data_for_bi_variate_analysis['Days'] = day_list[:31]
corr = data_for_bi_variate_analysis.corr()

np_array = np.array(data_frame['Prices'].values)
np_array = np.reshape(np_array[:28], (4, 7))
categorial_data_frame = pd.DataFrame(np_array,
                                     index=['Week 1: ', 'Week 2: ', 'Week 3: ', 'Week 4: '],
                                     columns=['Mon', 'Tue', 'Wed', 'Thur', 'Fri', 'Sat', 'Sun'])

correl_of_price_by_days = categorial_data_frame.corr()

trace = go.Heatmap(z=correl_of_price_by_days.values,
                   x=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
                   y=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
data = [trace]
fig2 = go.Figure(data=data, layout=get_layout('3. Correlation heat map', 700, 750))
url2 = py.plot(fig2, filename='correl-heatmap', height=750)

print('\n--------------- 3. Correlation heat map ---------------\n')
print('\t Heatmap of correlation between days available on link: ', url2)
print('\nDataframe what show vision of data by researcher:\n')
fine_print(categorial_data_frame)
print('\nCorrelation of above dataframe, it show relation of values beetwen days:\n')
fine_print(correl_of_price_by_days)

# Processing of outliers and missing values (Replacing on mean value)
upper_border = median + median * 0.45
lower_border = median * 0.05

clean_data_frame = data_for_bi_variate_analysis.copy()
for value in clean_data_frame['Prices']:
    if upper_border < value or lower_border > value:
        clean_data_frame = clean_data_frame.replace(value, round(mean, 2))


# ######################################################################################################################
# Creating prediction models

# --- Preprocessing of data
reshaped_prices = np.reshape(clean_data_frame['Prices'].values, (-1, 1))
reshaped_days = np.reshape(clean_data_frame['Days'].values, (-1, 1))
reshaped_prices = reshaped_prices.ravel()
label_encoder = LabelEncoder()
encoded_prices = label_encoder.fit_transform(reshaped_prices)


# --- Using RandomForestClassifier to make a predict
random_forest_classifier = RandomForestClassifier(n_estimators=1000)
random_forest_classifier.fit(reshaped_days, encoded_prices)
prediction_days = np.array(['0', '1', '2', '3', '4', '5', '6'])  # Values according to days in week
reshaped_prediction_days = np.reshape(prediction_days, (-1, 1))
result = random_forest_classifier.predict(reshaped_prediction_days)

reshaped_result = np.array(label_encoder.inverse_transform(result))
reshaped_result = np.reshape(reshaped_result, (1, -1))
rfc_frame = pd.DataFrame(reshaped_result,
                         columns=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
                         index=['Predict'])
print('\n--------------- 4. Predicted values by using Random Forest Classifier ---------------\n')
fine_print(rfc_frame)

# --- Using RandomForestRegressor to make a predict
regr = RandomForestRegressor(max_depth=2, random_state=0)
regr.fit(reshaped_days, reshaped_prices)

print('\n--------------- 5. Predicted values by using Random Forest Regression ---------------\n')
reshaped_regr_result = np.array(regr.predict(reshaped_prediction_days))
reshaped_regr_result = np.reshape(reshaped_regr_result, (1, -1))
rfr_frame = pd.DataFrame(reshaped_regr_result,
                         columns=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
                         index=['Predict'])
fine_print(rfr_frame)

trace0 = go.Scatter(
    x=[day for day in range(36)],
    y=clean_data_frame['Prices'].values,
    mode='lines',
    name='Initial values')

trace1 = go.Scatter(
    x=[day for day in range(29, 36)],
    y=rfc_frame.values[0],
    mode='lines',
    name='Values predicted by Random Forest Classifier')

trace2 = go.Scatter(
    x=[day for day in range(29, 36)],
    y=rfr_frame.values[0],
    mode='lines',
    name='Values predicted by Random Forest Regression')

data = [trace0, trace1, trace2]

# --- Creating of the plot
fig4 = go.Figure(data=data, layout=get_layout('4. Prediction results', 950, 400))
url4 = py.plot(fig4, filename='prediction-results', height=750)


print('\t Prediction results available on link: ', url1)
