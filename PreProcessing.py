# -*- coding: utf-8 -*-
"""
Created on Thu Mar  3 21:08:56 2022

@author: DELL
"""

import pandas as pd

df = pd.read_csv(r"C:\Users\DELL\Desktop\Project\Data.csv")

'''As the column names are more complex and lengthy it will be difficult to analyse and 
also there is a chance of throwing an error sometime...so I am renaming the columns in general form'''


df.rename(columns={"Are you still going to school?":"GoingToSchool","Do you have any other children living in your house with you?":"AnotherChildHome","How many people live in your home with you (including adults)?":"PeopleInHome",
                   "What year are you in now?":"age","6. In the last 7 days, how many days did you do sports or exercise for at least 1 hour in total. This includes doing any activities (including online activities) or playing sports where your heart beat faster, you breathed faster and you felt warmer?":"SportsDaysInWeek","7. In the last 7 days, how many days did you watch TV/play online games/use the internet etc. for 2 or more hours a day (in total)?":"GadgetInWeek",
                  "9. In the last 7 days, how many days did you feel like you could concentrate/pay attention well on your school work?":"ConcentraionDays","17. How often do you go out to play outside?":"PlayOutside","18. Do you have enough time for play?":"EnoughPlayTime","21. Do you have somewhere at home where you have space to relax?":"RelaxSpace",
                  "22. Tell us if you agree or disagree with the following: [I am doing well with my school work]":"SchoolWork","22. Tell us if you agree or disagree with the following: [I feel part of my school community]":"SchoolCommunity","22. Tell us if you agree or disagree with the following: [I have lots of choice over things that are important to me]":"ChoicesOnThing","22. Tell us if you agree or disagree with the following: [There are lots of things I'm good at]":"ImGoodAtThings",
                   "Your Health ":"Health","Your School":"School","Your Family":"Family","Your Friends":"Friends","Your Appearance (how you look)":"Appearance","Your Life":"Life","24. Remember, there are no right or wrong answers, just pick which is right for you. [I feel lonely]":"Lonely",
                   "24. Remember, there are no right or wrong answers, just pick which is right for you. [I cry a lot]":"Cry","24. Remember, there are no right or wrong answers, just pick which is right for you. [I am unhappy]":"Unhappy","24. Remember, there are no right or wrong answers, just pick which is right for you. [I feel nobody likes me]":"NobodyLikesMe","24. Remember, there are no right or wrong answers, just pick which is right for you. [I worry a lot]":"Worry","24. Remember, there are no right or wrong answers, just pick which is right for you. [I have problems sleeping]":"Insomnia", 
                   "24. Remember, there are no right or wrong answers, just pick which is right for you. [I wake up in the night]":"WakeupNight","24. Remember, there are no right or wrong answers, just pick which is right for you. [I am shy]":"shy","24. Remember, there are no right or wrong answers, just pick which is right for you. [I feel scared]":"Scared","24. Remember, there are no right or wrong answers, just pick which is right for you. [I worry when I am at school]":"WorryAtSchool","24. Remember, there are no right or wrong answers, just pick which is right for you. [I get very angry]":"Anger","24. Remember, there are no right or wrong answers, just pick which is right for you. [I lose my temper]":"Temper",
                   "24. Remember, there are no right or wrong answers, just pick which is right for you. [I hit out when I am angry]":"HitoutOnAnger","24. Remember, there are no right or wrong answers, just pick which is right for you. [I do things to hurt people]":"HurtPeople","24. Remember, there are no right or wrong answers, just pick which is right for you. [I am calm]":"Calm","24. Remember, there are no right or wrong answers, just pick which is right for you. [I break things on purpose]":"BreakThings","25. Are you able to keep in touch with your family that you don't live with? (grand parents, Uncle, Aunt, Cousins, etc)?":"InTouchWithFamily","26. Are you able to keep in touch with your friends?":"IntouchWithFriends"},inplace=True)

###################################DATE AND TIME#############################3
 

'''
HERE TO RUN FOR LOOP ,INDEX SHOULD START FROM 0,BUT AFTER DELETING
DUPLICATES AND NULLS INDEX WILL CHANGE AND INDEX NUMBERS WONT BE IN ORDER...
eg: IF 5th RECORD IS DUPLICATE THEN IN INDEX AFTER 4 NEXT WILL BE 6 AS 5 IS DELETED
NOW FOR LOOP DOESNT FIND 5 HERE....SO RUN FOR LOOP BEFORE DELETING OR ELSE RESET 
THE INDEX VALUES AND THEN RUN THE FOR LOOP

SO NOW ONLY RUNNING FOR LOOP FOR DATES,BREAKFAST

if we want to run for loop somewhere in the middle then we can reset index
eg:
test_X=test_X.reset_index()
test_X =test_X.drop(['index'], axis = 1) #bcuz if we reset index previous index values
                                          will be added as new column

'''
#converting into date time format
df['wakeup'] = pd.to_datetime(df['wakeup'], errors='coerce')
df['sleep'] = pd.to_datetime(df['sleep'], errors='coerce')

#repalceing wakeup day to next day

import datetime
#df['wakeup']= df['wakeup']+datetime.timedelta(days=1)

d=datetime.datetime.now().strftime("%d")

d=int(d)

df['wakeup'] = df['wakeup'].apply(lambda dt: dt.replace(day=d+1))

#converting into hours
df['sleeptime'] = (df['wakeup'] - df['sleep']).dt.total_seconds()/60/60

#Caluculating appropriate time of sleep

for i in range(len(df['sleeptime'])):
    if df['sleeptime'][i] > 24:
        df['sleeptime'][i]= (df['sleeptime'][i]) - 24
    else:
        df['sleeptime'][i]= df['sleeptime'][i]


######################################BREAKFAST###############################
s=df.breakfast.value_counts()
#Here we got health = 192,toast =185,sugary=159,nothing=23, and reaming we will thik as others

df['breakfast']=df['breakfast'].str.lower()

#Classifying according to food
# using if condition to find pattern in string and classify accordingly

for i in range(len(df['breakfast'])):
    if 'health' in df['breakfast'][i] or 'fruit' in df['breakfast'][i] :
        df['breakfast'][i]= 5
    elif 'toast' in df['breakfast'][i] :
        df['breakfast'][i]= 4
    elif 'sugar' in df['breakfast'][i] :
        df['breakfast'][i]= 3
    elif 'nothing' in df['breakfast'][i] :
        df['breakfast'][i]= 2
    else:
        df['breakfast'][i]= 1



df['breakfast']=df['breakfast'].astype('int')
df.dtypes
s=df.breakfast.value_counts()


########################################################################



df.isna().sum() ###looking for null values

df=df.dropna() #here i m removing null values

#checking for duplicates
duplicate = df.duplicated()
duplicate
sum(duplicate)

# Removing Duplicates
df = df.drop_duplicates()

duplicate = df.duplicated()
duplicate
sum(duplicate)



###############Now we dont have any null values and duplicates###############3

###########We will not have outliers as each feature is categorical ###############


df['Lonely'].replace('Never', 0 , inplace=True)
df['Lonely'].replace('Sometimes', 1 , inplace=True)
df['Lonely'].replace('Always', 2 , inplace=True)

'''
list1=['Lonely','Cry','Unhappy','NobodyLikesMe','Worry','Insomnia','WakeupNight','shy','Scared','WorryAtSchool','Anger','Temper','HitoutOnAnger','HurtPeople','BreakThings']

for i in range(0,len(list1)):
    if df[list1[i]] == 'Never' :
      df[list1].replace('Never', 0 , inplace=True)
'''     
df['Cry'].replace('Never', 0 , inplace=True)
df['Cry'].replace('Sometimes', 1 , inplace=True)
df['Cry'].replace('Always', 2 , inplace=True)

df['Unhappy'].replace('Never', 0 , inplace=True)
df['Unhappy'].replace('Sometimes', 1 , inplace=True)
df['Unhappy'].replace('Always', 2 , inplace=True)

df['NobodyLikesMe'].replace('Never', 0 , inplace=True)
df['NobodyLikesMe'].replace('Sometimes', 1 , inplace=True)
df['NobodyLikesMe'].replace('Always', 2 , inplace=True)

df['Worry'].replace('Never', 0 , inplace=True)
df['Worry'].replace('Sometimes', 1 , inplace=True)
df['Worry'].replace('Always', 2 , inplace=True)

df['Insomnia'].replace('Never', 0 , inplace=True)
df['Insomnia'].replace('Sometimes', 1 , inplace=True)
df['Insomnia'].replace('Always', 2 , inplace=True)

df['WakeupNight'].replace('Never', 0 , inplace=True)
df['WakeupNight'].replace('Sometimes', 1 , inplace=True)
df['WakeupNight'].replace('Always', 2 , inplace=True)

df['shy'].replace('Never', 0 , inplace=True)
df['shy'].replace('Sometimes', 1 , inplace=True)
df['shy'].replace('Always', 2 , inplace=True)

df['Scared'].replace('Never', 0 , inplace=True)
df['Scared'].replace('Sometimes', 1 , inplace=True)
df['Scared'].replace('Always', 2 , inplace=True)

df['WorryAtSchool'].replace('Never', 0 , inplace=True)
df['WorryAtSchool'].replace('Sometimes', 1 , inplace=True)
df['WorryAtSchool'].replace('Always', 2 , inplace=True)


df['Anger'].replace('Never', 0 , inplace=True)
df['Anger'].replace('Sometimes', 1 , inplace=True)
df['Anger'].replace('Always', 2 , inplace=True)

df['Temper'].replace('Never', 0 , inplace=True)
df['Temper'].replace('Sometimes', 1 , inplace=True)
df['Temper'].replace('Always', 2 , inplace=True)

df['HitoutOnAnger'].replace('Never', 0 , inplace=True)
df['HitoutOnAnger'].replace('Sometimes', 1 , inplace=True)
df['HitoutOnAnger'].replace('Always', 2 , inplace=True)

df['HurtPeople'].replace('Never', 0 , inplace=True)
df['HurtPeople'].replace('Sometimes', 1 , inplace=True)
df['HurtPeople'].replace('Always', 2 , inplace=True)

df['BreakThings'].replace('Never', 0 , inplace=True)
df['BreakThings'].replace('Sometimes', 1 , inplace=True)
df['BreakThings'].replace('Always', 2 , inplace=True)

df['Calm'].replace('Never', 2 , inplace=True)
df['Calm'].replace('Sometimes', 1 , inplace=True)
df['Calm'].replace('Always', 0 , inplace=True)


df['InTouchWithFamily'].replace('Yes', 1 , inplace=True)
df['InTouchWithFamily'].replace('No', 0 , inplace=True)

df['IntouchWithFriends'].replace('Yes', 1 , inplace=True)
df['IntouchWithFriends'].replace('No', 0 , inplace=True)
      
      
df['GoingToSchool'].replace('No, I am at home', 0 , inplace=True)
df['GoingToSchool'].replace('I am in a different school from my own school', 1 , inplace=True)
df['GoingToSchool'].replace('Yes, sometimes', 2 , inplace=True)      
df['GoingToSchool'].replace('Yes, most days of the week', 3 , inplace=True)      
      
      
df['AnotherChildHome'].replace('Yes', 1 , inplace=True)
df['AnotherChildHome'].replace('No', 0 , inplace=True)
            
      
      
df['PeopleInHome'].replace('1', 1 , inplace=True)
df['PeopleInHome'].replace('2', 2 , inplace=True)
df['PeopleInHome'].replace('3', 3 , inplace=True)
df['PeopleInHome'].replace('4', 4 , inplace=True)
df['PeopleInHome'].replace('5', 5 , inplace=True)
df['PeopleInHome'].replace('6+', 6 , inplace=True)



df['age'].replace('Year 3', 3 , inplace=True)
df['age'].replace('Year 4', 4 , inplace=True)
df['age'].replace('Year 5', 5 , inplace=True)
df['age'].replace('Year 6', 6 , inplace=True)


df['SportsDaysInWeek'].replace('0 days', 0 , inplace=True)
df['SportsDaysInWeek'].replace('1-2 days', 1 , inplace=True)
df['SportsDaysInWeek'].replace('3-4 days', 2 , inplace=True)
df['SportsDaysInWeek'].replace('5-6 days', 3 , inplace=True)
df['SportsDaysInWeek'].replace('7 days', 4 , inplace=True)



df['GadgetInWeek'].replace('0 days', 0 , inplace=True)
df['GadgetInWeek'].replace('1-2 days', 1 , inplace=True)
df['GadgetInWeek'].replace('3-4 days', 2 , inplace=True)
df['GadgetInWeek'].replace('5-6 days', 3 , inplace=True)
df['GadgetInWeek'].replace('7 days', 4 , inplace=True)


df['ConcentraionDays'].replace('0 days', 0 , inplace=True)
df['ConcentraionDays'].replace('1-2 days', 1 , inplace=True)
df['ConcentraionDays'].replace('3-4 days', 2 , inplace=True)
df['ConcentraionDays'].replace('5-6 days', 3 , inplace=True)
df['ConcentraionDays'].replace('7 days', 4 , inplace=True)


df['PlayOutside'].replace('I don\'t play', 0 , inplace=True)
df['PlayOutside'].replace('Hardly ever', 1 , inplace=True)
df['PlayOutside'].replace('A few days each week', 2 , inplace=True)
df['PlayOutside'].replace('Most days', 3 , inplace=True)



df['EnoughPlayTime'].replace('No, I need a lot more', 0 , inplace=True)
df['EnoughPlayTime'].replace('No, I would like to have a bit more', 1 , inplace=True)
df['EnoughPlayTime'].replace('Yes, it\'s just about enough', 2 , inplace=True)
df['EnoughPlayTime'].replace('Yes, I have loads', 3 , inplace=True)


df['RelaxSpace'].replace('No', 0 , inplace=True)
df['RelaxSpace'].replace('Sometimes but not all the time', 1 , inplace=True)
df['RelaxSpace'].replace('Yes', 2 , inplace=True)




df['SchoolWork'].replace('Strongly disagree', 0 , inplace=True)
df['SchoolWork'].replace('Disagree', 1 , inplace=True)
df['SchoolWork'].replace('Don\'t agree or disagree', 2 , inplace=True)
df['SchoolWork'].replace('Agree', 3 , inplace=True)
df['SchoolWork'].replace('Strongly agree', 4 , inplace=True)



df['SchoolCommunity'].replace('Strongly disagree', 0 , inplace=True)
df['SchoolCommunity'].replace('Disagree', 1 , inplace=True)
df['SchoolCommunity'].replace('Don\'t agree or disagree', 2 , inplace=True)
df['SchoolCommunity'].replace('Agree', 3 , inplace=True)
df['SchoolCommunity'].replace('Strongly agree', 4 , inplace=True)

df['ChoicesOnThing'].replace('Strongly disagree', 0 , inplace=True)
df['ChoicesOnThing'].replace('Disagree', 1 , inplace=True)
df['ChoicesOnThing'].replace('Don\'t agree or disagree', 2 , inplace=True)
df['ChoicesOnThing'].replace('Agree', 3 , inplace=True)
df['ChoicesOnThing'].replace('Strongly agree', 4 , inplace=True)

df['ImGoodAtThings'].replace('Strongly disagree', 0 , inplace=True)
df['ImGoodAtThings'].replace('Disagree', 1 , inplace=True)
df['ImGoodAtThings'].replace('Don\'t agree or disagree', 2 , inplace=True)
df['ImGoodAtThings'].replace('Agree', 3 , inplace=True)
df['ImGoodAtThings'].replace('Strongly agree', 4 , inplace=True)





#Finding score of emotional difficulties
df['EmotionalDifficulties']= df['Lonely']+df['Cry']+df['Unhappy']+df['NobodyLikesMe']+df['Worry']+df['Insomnia']+df['WakeupNight']+df['shy']+df['Scared']+df['WorryAtSchool']

#Finding score of behavioural difficulties
df['BehaviourDifficulties']=df['Anger']+df['Temper']+df['HitoutOnAnger']+df['BreakThings']+df['HurtPeople']+df['Calm']

###dropping EmotionalDifficulties and BehaviourDifficulties individual columns as they are not required from now on
df.drop(['Lonely','Cry','Unhappy','NobodyLikesMe','Worry','Insomnia','WakeupNight','shy','Scared','WorryAtSchool','Calm','HurtPeople','BreakThings','HitoutOnAnger','Temper','Anger'], axis=1, inplace=True)


'''
for i in range(0,len(df['EmotionalDifficulties'])):
    if df['EmotionalDifficulties'][i] <10 :
        df['EmotionalDifficulties'][i] = "Expected"        
'''

#Discretising according to score
    
df.loc[df.EmotionalDifficulties < 10, 'EmotionalScore'] = "Expected"
df.loc[df['EmotionalDifficulties'].between(10, 11 ) , 'EmotionalScore'] = "Borderline"
df.loc[df.EmotionalDifficulties >11 , 'EmotionalScore'] = "Significant"

df.EmotionalScore.value_counts()


df.loc[df.BehaviourDifficulties < 6, 'BehaviouralScore'] = "Expected"
df.loc[df['BehaviourDifficulties'] == 6 , 'BehaviouralScore'] = "Borderline"
df.loc[df.BehaviourDifficulties >6 , 'BehaviouralScore'] = "Significant"

df.BehaviouralScore.value_counts()

#Dropping scores columns
df.drop(['EmotionalDifficulties','BehaviourDifficulties','sleep','wakeup'], axis = 1, inplace = True) 
   

df.info()
 
###################################DATA CLEANING IS DONE###############

#df.to_csv('df_final.csv', index=False) #exporting cleaned dataframe

bdf = df.copy(deep=True)
bdf.drop(['EmotionalScore'], axis = 1, inplace = True) 

edf = df.copy(deep=True)
edf.drop(['BehaviouralScore'], axis = 1, inplace = True) 


#bdf.to_csv('df_behavioural.csv', index=False) #exporting cleaned dataframe
#edf.to_csv('df_emotional.csv', index=False) #exporting cleaned dataframe


 

# Data Visualization
import matplotlib.pyplot as plt
import seaborn as sns

''' 
If a feature(continous/discrete) has particular range...as long as data is in that range we shldn't
consider it as an outlier....even if all the values are around 8 and only one value is at 2
we shldnt consider outlier as an outlier......but if we dont have any specified range then we
can consider outlires as outliers 
'''

df.Health.mean() #First Moment Business Decision
df.Health.std() #Second Moment Business Decision
df.Health.skew() #Third Moment Business Decision
df.Health.kurt() #Fourth Moment Business Decision
plt.hist(df.Health) #histogram

			
df.School.mean() #First Moment Business Decision
df.School.std() #Second Moment Business Decision
df.School.skew() #Third Moment Business Decision
df.School.kurt() #Fourth Moment Business Decision
plt.hist(df.School) #histogram


df.Family.mean() #First Moment Business Decision
df.Family.std() #Second Moment Business Decision
df.Family.skew() #Third Moment Business Decision
df.Family.kurt() #Fourth Moment Business Decision
plt.hist(df.Family) #histogram



df.Friends.mean() #First Moment Business Decision
df.Friends.std() #Second Moment Business Decision
df.Friends.skew() #Third Moment Business Decision
df.Friends.kurt() #Fourth Moment Business Decision
plt.hist(df.Friends) #histogram



df.Appearance.mean() #First Moment Business Decision
df.Appearance.std() #Second Moment Business Decision
df.Appearance.skew() #Third Moment Business Decision
df.Appearance.kurt() #Fourth Moment Business Decision
plt.hist(df.Appearance) #histogram



df.Life.mean() #First Moment Business Decision
df.Life.std() #Second Moment Business Decision
df.Life.skew() #Third Moment Business Decision
df.Life.kurt() #Fourth Moment Business Decision
plt.hist(df.Life) #histogram

df.sleeptime.mean() #First Moment Business Decision
df.sleeptime.std() #Second Moment Business Decision
df.sleeptime.skew() #Third Moment Business Decision
df.sleeptime.kurt() #Fourth Moment Business Decision
plt.hist(df.sleeptime) #histogram

df.var() # variance is obtained for numeric variables only 

#We can remove the field which has variance of almost zero
























































