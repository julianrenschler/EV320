import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

file = '/Users/jrensch22/Desktop/EVPython/EV320_Final/LocalWind_WA.csv'

file2 = '/Users/jrensch22/Desktop/EVPython/EV320_Final/LocalRH_WA.csv'

df = pd.read_csv(file, encoding = 'utf-8')
df2 = pd.read_csv(file2, encoding = 'utf-8')

N = 3
W = 2
S = 1
E = 0

#CHOOSE MONTH OF FIRE (1-12)
month = 11

#CHOOSE REGION OF STATE (N, W, S, E)
region = N

#CHOOSE DURATION OF THE FIRE (1-7) hours
hours = 24

aws = df.iloc[region, month] #average wind speed
print(aws)

direction = df.iloc[(region+4), month]
print(direction)

humidity = df2.iloc[region, month] #relative humidity #use in smoke generated variable/ add vegetation if you have time
print(humidity)

title = 'Wildfire Smoke Movement ' + direction

#------#

## INITIAL CONDITIONS
dx = 20
x = np.arange(0, 3000, dx) # grid from 0mi to 1000mi
nodes = len(x)
# dx = 1 mile

C = np.zeros(nodes)

smoke_concentration = 100 #hmmm

C[x==0] = smoke_concentration

velocity = aws

dt = 1. #0.5 * dx / velocity
courant = dt * float(velocity) / dx
print('courant =', courant)
print(dx)

## CREATE THE A MATRIX
A = np.zeros((nodes, nodes))

for i in range(1, nodes):
    A[i,i]= 1-courant
    A[i,i-1] = courant
A[0,0] = 1 # boundary condition that first node stays the same

## RUN THE MODEL THROUGH TIME

for i in range(4):
    totalhours = hours*(i+1)

    fig, ax = plt.subplots(1,1)
    #ax.plot(x, C, label = 'initial')

    time = 0
    while time <= totalhours:
        newC = np.dot(A, C)
        C[:] = newC*1
        time += dt

    ax.plot(x, C, label = totalhours) 
   
    ax.set_title(title, fontsize = 14)   
    ax.set_xlabel('Distance (miles)')
    ax.set_ylabel('Smoke concentration')
    fig.legend()
    



#------#
"""
totalhours = 100

fig, ax = plt.subplots(1,1)
ax.plot(x, C, label = 'initial')

time = 0
while time <= totalhours:
    newC = np.dot(A, C)
    C[:] = newC*1
    time += dt

ax.plot(x, C, label = '100 years')
ax.set_xlabel('Distance (m)')
ax.set_ylabel('Bedload concentration (kg/m^3)')
ax.set_title('Landslide sediment movement', fontsize = 14)
fig.legend()
"""
