import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

"Wildfire smoke spread from Washington state based on regional wind speed data," 
"including month of fire, duration of fire, and location of fire"

#FOR USER VARIATION#
#------------------#

#CHOOSE MONTH OF FIRE (1-12)
month = 11

#CHOOSE DURATION OF THE FIRE (1-12) #days
days = 5

#CHOOSE COORDINATES OF FIRE (WA latitude 117W - 124W), longitude (46N - 49N) #use full degrees as dx = 1
lat = 118
long = 47

#IMPORTING AND IMPLEMENTING CODE
#------------------#

#import Washington State wind data csv file. Source = https://wrcc.dri.edu/cgi-bin/clilcd.pl?wa24243
file = '/Users/jrensch22/Desktop/EVPython/EV320_Final/LocalWind_WA.csv'

#Create dataframe of file. Specify type of encoding
df = pd.read_csv(file, encoding = 'utf-8')

#Determine rough region of WA using lat/long inputs
#Region IDs used to reference csv
N = 3 #Seattle
W = 2 #Quilliayute
S = 1 #Yakima
E = 0 #Spokane

#Conditions to determine region of state
if long >= 48: #it is first determined if the fire is N/S
    region = N #if it isn't far in either direction, it is classifed as an W or E
elif long <= 47:
    region = S
elif lat < 121:
    region = E
elif lat > 121:
    region = W
print(region)

#extract average wind speed by indexing the df by its region and month
aws = df.iloc[region, month] #average wind speed 

#2D ADVECTION
#----------#

### INITIAL CONDITIONS
nx = 12 #degrees #gives perspective to size of smoke cloud
ny = 12 #degrees

dx = 1 #degrees 
dy = 1 #degrees

x = np.arange(0, nx*dx, dx) + 117 # creates the 1-D array of x positions
y = np.arange(0, ny*dy , dy) + 46 # add after the array is made to properly position coordinates around WA
X, Y = np.meshgrid(x, y, indexing = 'ij') #mesh x and y into 2-D coordinate system

u = float(aws)/69 #convert mph to degrees per hours #69 miles per latitudinal degree

dt = 1 #hours

#Create 3rd variable -- Z
Z = np.zeros((nx, ny)) #array of 0s
Z[(x==float(lat)),(y==float(long))] = 100 #set intial concentration at fire coordinates
z = Z.flatten() # 1-D flattened array

#lower case = 1-D
#upper case = 2-D

#STABILITY CHECK
#-------------#
cx = dt * u / dx #check courant for both x and y
cy = dt * u / dy

import sys
if cx > 1:
    print('x is unstable')
    sys.exit()
elif cy > 1:
    print('y is unstable')
    sys.exit() 
#if the courant is unstable in either case, interupt the model

#A MATRIX
#------------#
A = np.zeros((nx*ny, nx*ny)) #Create matrix of 0s

for i in range(nx): 
    for k in range(ny):
        ik = i*ny + k
        #Boundary Conditions
        if i == 0:
            A[ik, ik] = 1 # no change
        elif k == 0:
            A[ik, ik] = 1
        else:
            #Coefficients
            A[ik, ik] = 1 - cx - cy
            A[ik, (i-1)*ny + k] = cx
            A[ik, i*ny + k - 1] = cy

#PLOTTING
#------------#
totaltime = days*24 #hours
time = 0 #hours
while time <= totaltime: #While loop. Model run each hour until 
    newz = np.dot(A, z) #dot product of A matrix and 1-D array z
    z[:] = newz #update z
    
    if time == 0: #plot the intial conditions
        Z = z.reshape(X.shape)
        fig, ax = plt.subplots()
        plt.gca().invert_xaxis() #switch the x axis because we are in degrees W or negatives
        ax.contour(X, Y, Z, cmap = 'Greys') #use a contour map, smoke coloring
        ax.set_xlabel('Longitude (ºW)')
        ax.set_ylabel('Latitude (ºN)')
        ax.set_title('Start of fire')
        
    if time == totaltime: #plot smoke after total time
        Z = z.reshape(X.shape)
        fig, ax = plt.subplots() #new plot
        plt.gca().invert_xaxis()
        ax.contour(X, Y, Z, cmap = 'Greys')
        ax.set_xlabel('Longitude (ºW)') #label all axises and add title
        ax.set_ylabel('Latitude (ºN)')
        ax.set_title('Final Condition')
        
    Z[(x==float(lat)),(y==float(long))] = 100 #the fire is still burning so continue to add smoke to the environment
    time += dt #add one hour to the total time