#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scene-cat problem set for PSY 1210 - Fall 2018

@author: Michael Mack
"""

#%% import block 
import numpy as np
import scipy as sp
import scipy.stats
import os
import shutil


#%%
# copy files from testing room folders to raw data, rename files to include
# testing room letter in the filename
#
testingrooms = ['A','B','C'] #three different rooms for the loop to go through
for room in testingrooms:
    path_testingroom='testingroom'+ room + '\experiment_data.csv' #Current directory you want to move
    path_rawdata='rawdata\experiment_data_'+room+'.csv.' #Rename the files and what new directory will be
    shutil.copy('path_testingroom','path_rawdata') #Copys the files into the new directory 
#%%
# read in all the data files in rawdata directory using a for loop
# columns: subject, stimulus, pairing, accuracy, median RT
#

data = np.empty((0,5)) #Creates an empty first column of 5 variables in your dataframe. Will be populated by the loop below
for room in testingrooms: #loop to go through each testingroom and complete the below info
    filename = 'rawdata/experiment_data_'+room+'.csv'#telling you which file to merge. +room+ will be changed to the testingroom throughout the looping process
    print(filename)
    tmp = sp.loadtxt(filename,delimiter=',') #creates a temporary file 
    data = np.vstack([data,tmp])#takes each testingroom data file and puts them together with A on top, then B, then C. 


#%%
# calculate overall average accuracy and average median RT

#Naming each column in the data to the specific variable 
sbjt= data[:,0] #1st row of data is your subject 
stim= data[:,1]#2nd row is stimulus
pair= data[:,2]#3rd row is pairing condition
acc= data[:,3]#4th row is accuracy
mrt= data[:,4]#5th row is median reaction time


acc_avg = np.mean(acc*100) #average of all accuracy data. Multiply by 100 to convert to a percentage ANS: 91.48%
mrt_avg = np.mean(mrt)#average of all median rt data. ANS: 477.3ms


#%%
# calculate averages (accuracy & RT) split by stimulus using a for loop and an 
# if statement. (i.e., loop through the data to make a sum for each condition, 
# then divide by the number of data points going into the sum)

#defining variables for the for loop to place data into
sum_w_acc=0 #empty integer bin
sum_w_mrt=0 #""
sum_f_acc=0 #""
sum_f_mrt=0 #""

words=0 #""
faces=0 #""

for x in range(len(sbjt)): #looping through your subject list in data that matches the below code conditions 
    if stim [x]==1:  #indicating stimulus of 1 is words. If follows this do the below 3 lines.
        words +=1  
        sum_w_acc += acc[x] # Sum of acc for words
        sum_w_mrt += mrt[x] #Sum of mrt for word
    else:  #if not equal to 1 then equal to 2 which is faces. If follows this do the below 3 lines.
        faces +=1
        sum_f_acc += acc[x]#Sum of acc for faces
        sum_f_mrt += mrt[x]#Sum of mrt for faces

avg_acc_w= (sum_w_acc / words)*100 #Mean of acc for words (dividing by number of participants in the words condition). 
avg_mrt_w = (sum_w_mrt / words) #same as above but for mrt
avg_acc_f=(sum_f_acc / faces)*100 #same as above but acc for faces 
avg_mrt_f=(sum_f_mrt /faces)#same as above but mrt for faces 



# words: 88.6%, 489.4ms   faces: 94.4%, 465.3ms


#%%
# calculate averages (accuracy & RT) split by congruency using indexing, 
# slicing, and numpy's mean function 
# wp - white/pleasant, bp - black/pleasant
# (hint: only one line of code is needed per average)

#indexing data to calculate averages
acc_wp = np.mean(data[data[:,2]==1,3])*100 #Pairing variable data equal to 1 (to get wp). The 3 gets the accuracy data. ANS:94.0%
acc_bp = np.mean(data[data[:,2]==2,3])*100# same as above line but data equal to 2 (bp). ANS:88.9%
mrt_wp = np.mean(data[data[:,2]==1,4])#same as above line but data equal to 1 (wp) and for the mrt data (4). ANS: 469.6ms
mrt_bp = np.mean(data[data[:,2]==2,4])# same as above line but data equal to 2(bp). ANS: 485.1ms


#%% 
# calculate average median RT for each of the four conditions
# use for loops, indexing/slicing, or both!
# (hint: might be easier to slice data into separate words and faces datasets)
#

#Create an empty list for data
w_wp_mrt=list() 
w_bp_mrt=list()
f_wp_mrt=list()
f_bp_mrt=list()



for x in range(len(sbjt)): #looping through the below conditions
    if pair[x] ==1 and stim[x]==1: #wp and words
        w_wp_mrt.append(mrt[x])#adds total of x to end of w_wp_mrt list 
       
    elif pair[x] ==2 and stim[x]==1:#bp and words
        w_bp_mrt.append(mrt[x])#adds total of x to end of w_bp_mrt list 
        
    elif pair[x] ==1 and stim[x]==2:#wp and faces
        f_wp_mrt.append(mrt[x])#adds total of x to end of f_wp_mrt list 
        
    elif pair[x] ==2 and stim[x]==2:#bp and faces
        f_bp_mrt.append(mrt[x])#adds total of x to end of f_bp_mrt list 

mean_w_wp_mrt=np.mean(w_wp_mrt) #mean of mrt for words and wp
mean_w_bp_mrt=np.mean(w_bp_mrt) #mean of mrt for words and bp
mean_f_wp_mrt=np.mean(f_wp_mrt) #mean of mrt for faces and wp
mean_f_bp_mrt=np.mean(f_bp_mrt) #mean of mrt for faces and bp

# words - white/pleasant: 478.4ms
# words - black/pleasant: 500.3ms
# faces - white/pleasant: 460.8ms
# faces - black/pleasant: 469.9ms


#%%        
# compare pairing conditions' effect on RT within stimulus using scipy's 
# paired-sample t-test: scipy.stats.ttest_rel()
#
import scipy.stats

#need to first convert to an array
wordswp_array=np.asarray(w_wp_mrt)
wordsbp_array=np.asarray(w_bp_mrt)
faceswp_array=np.asarray(f_wp_mrt)
facesbp_array=np.asarray(f_bp_mrt)

t1=words_mrt= scipy.stats.ttest_rel(wordswp_array,wordsbp_array) #looking at the effect of each pairing condition within words on mrt 

t2=faces_mrt=scipy.stats.ttest_rel(faceswp_array,facesbp_array) # same as above t-test but within faces 



# words: t=-5.36, p=2.19e-5
# faces: t=-2.84, p=0.0096


#%%
# print out averages and t-test results
# (hint: use the ''.format() method to create formatted strings)
#
print('\nOVERALL: {:.2f}%, {:.1f} ms'.format(acc_avg,mrt_avg)) #prints overall average of acc and mrt scores
print('\nAvg_Stim: {:.1f}%, {:.1f}%, {:.1f} ms,{:.1f} ms'.format(avg_acc_w,avg_acc_f,avg_mrt_w,avg_mrt_f)) #prints average acc of words and faces, and average mrt for words and faces 
print('\nAvg_Pair: {:.1f}%, {:.1f}%, {:.1f} ms,{:.1f} ms'.format(acc_wp,acc_bp,mrt_wp,mrt_bp)) #prints acc for wp and bp and mrt for wp and bp 
print('\nAvg_Mrt: {:.1f} ms, {:.1f} ms, {:.1f} ms,{:.1f} ms'.format(w_wp_mrt,w_bp_mrt,f_wp_mrt,f_bp_mrt)) #prints mrt for words and wp, words and bp, faces and wp, faces and bp. 

print("t-test [wordswp_array,wordsbp_array]",t1) #prints t-test and p-value
print("t-test [faceswp_array,facesbp_array]",t2) #prints t-test and p-value 
