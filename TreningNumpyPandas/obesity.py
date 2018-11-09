import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data = pd.ExcelFile("obesity.xlsx")
# print (data.sheet_names)

################Cleanup#################
# show only nedeed data
data_age = data.parse(u'Table 2',skiprows=7,skip_footer=17)
# print (data_age)

################Edit table#################
    # Renaming the header - just playing
    # Get rid of any empty rows.

# inplace = True modifies the existing object. Without this, Pandas will create a new object and return that.
data_age.rename(columns={u'Year4,5': u'Year'}, inplace=True)
data_age.rename(columns={u'All persons6': u'Total'}, inplace=True)
data_age.dropna(inplace=True)
data_age.set_index('Year',inplace=True)
# print (data_age)

################matplotlib#################
################Charts#################

# Plot whole table of data_age
# data_age.plot()
# plt.show()

# Get read of total axe
# axis =1 is slightly confusing, but all it really means is - drop the columns, as described from this Stack Overflow question.
# https://stackoverflow.com/questions/25773245/ambiguity-in-pandas-dataframe-numpy-array-axis-definition

# data_age_minus_total = data_age.drop('Total', axis=1)
# data_age_minus_total.plot()
# plt.show()
# plt.close()

# children under the age of 16 and grown ups in the age range of 35-44.

data_age['Under 16'].plot(label="Under 16")
data_age['35 to 44'].plot(label="35-44")
plt.legend(loc="upper right")
# plt.show()
plt.close()

################Future#################
kids_values = data_age['Under 16'].values
x_axis = range(len(kids_values))
x_axis2 = range(15)

poly_degree = 3 #change different polynome
curve_fit = np.polyfit(x_axis, kids_values, poly_degree)
poly_interp = np.poly1d(curve_fit)

poly_fit_values = []

for i in range(len(x_axis2)):
    poly_fit_values.append(poly_interp(i))

plt.plot(x_axis2, poly_fit_values, "-r", label = "Fitted")
plt.plot(x_axis, kids_values, "-b", label = "Orig")

plt.legend(loc="upper right")
plt.show()