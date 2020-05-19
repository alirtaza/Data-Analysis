#!/usr/bin/env python
# coding: utf-8

# # Most used Apps
# 
# As our company builts free Android and iOS mobile apps and company's main sourse of revenue is from in apps ads, so this project is about finding apps which are most profitable in Google store and App store. This would help our compnay to understand what type of apps are likely to attract more users. Our goal is to build a minimal Android app and launch it on Google Store. If the app have positive reponse we will make its ios version with some improvements to launch it on Apple Store so we need to find the app profile which fits both Apple Store and Google Store as well.

# In[1]:


from csv import reader

#Data set from Googleplay


opened_file = open('googleplaystore.csv')
read_file = reader(opened_file)
android = list(read_file)
android_header = android[0]
android = android[1:]


#Data set from Appstore

opened_file = open('AppleStore.csv')
read_file = reader(opened_file)
ios = list(read_file)
ios_header = ios[0]
ios = ios[1:]


# We will write a function name as 'explore_data' to explore data in more readable way. It will also print number of rows and columns.

# In[2]:


def explore_data(dataset, start, end, rows_and_columns=False):
    dataset_slice = dataset[start:end]
    for row in dataset_slice:
        print(row)
        print('\n')
    if rows_and_columns:
        print('Number of rows: ', len(dataset))
        print('Number of columns: ', len(dataset[0]))
        
print(android_header)
print('\n')
explore_data(android, 0, 3, True)


# File showing data of Google Play Store have 10841 rows and 13 columns. The important columns for analysis are 'App', 'Category', 'Reviews', 'Installs', 'Type', 'Price', and 'Genres'.

# In[3]:


print(ios_header)
print('\n')
explore_data(ios, 0, 3, True)


# File showing data of App Store have 7197 rows and 16 columns. The important columns are: 'track_name', 'currency', 'price', 'rating_count_tot', 'rating_count_ver', and 'prime_genre'.

# In[4]:


print(android[10472])
print('\n')
print(android_header)
print('\n')
print(android[0])


# Before analysing the data, it is important to clean the data. We will remove or correct any inaccuate data. We will also detect duplicate data and will remove it. As we can see there is a error for row 10472 as it is giving 19 for rating so we will remove this row.  

# In[5]:


print(len(android))
del android[10472]
print(len(android))


# In[6]:


for app in android:
    name = app[0]
    if name == 'Instagram':
        print(app)


# Google play data set have duplicate entries that can be seen above. App name 'Instagram' has multiple entries. 
# 

# In[7]:


duplicate_app = []
unique_app = []

for app in android:
    name = app[0]
    if name in unique_app:
        duplicate_app.append(name)
    else:
        unique_app.append(name)
print('Number of duplicate apps ', len(duplicate_app))
print('\n')
print('Example of duplicate apps \n', duplicate_app[:15])


#  After knowing that we have 1181 duplicate apps and we want to remove it because as it is a deformaty in data and we want our data to be precise and accurate as possible. As you can see 'Instagram' app have different reviews which means the highest reviews are for the latest data so we want this row for analysis. 
#  

# In[8]:


reviews_max = {}

for app in android:
    name = app[0]
    n_reviews = float(app[3])
    
    if name in reviews_max and reviews_max[name] < n_reviews:
        reviews_max[name] = n_reviews
        
    elif name not in reviews_max:
        reviews_max[name] = n_reviews


# In[9]:


print('Expected lenght = ', len(android)-1181)
print('Actual length = ', len(reviews_max))


# As indicated that we have 1181 cases where apps have multiple entries so the length of our dictionary should be equal to difference between length of data minus 1181.

# In[10]:


android_clean = []
already_added = []

for app in android:
    name = app[0]
    n_reviews = float(app[3])
    
    if (reviews_max[name] == n_reviews) and (name not in already_added):
        android_clean.append(app)
        already_added.append(name)


# Now its time to explore data and make sure we have 9656 rows.

# In[11]:


explore_data(android_clean, 0, 3, True)


# As our company wants to make an English app so we do not need apps which are not in English so we would be removing those apps.

# In[12]:


def is_english(string):
    non_ascii = 0
    for character in string:
        if ord(character) > 127:
            non_ascii += 1
            
    if non_ascii > 3:
        return False
    
    else:
        return True
print(is_english('Docs To Go™ Free Office Suite'))
print(is_english('Instachat 😜'))
print(is_english('爱奇艺PPS -《欢乐颂2》电视剧热播'))
print(is_english('Instagram'))


# In[13]:


android_english = []
ios_english = []

for app in android_clean:
    name = app[0]
    if is_english(name):
        android_english.append(app)
        
for app in ios:
    name = app[1]
    if is_english(name):
        ios_english.append(app)

        
explore_data(android_english, 0, 3, True)
print('\n')
explore_data(ios_english, 0, 3, True)


# In[14]:


android_final = []
ios_final = []

for app in android_english:
    price = app[7]
    if price == '0':
        android_final.append(app)
    
for app in ios_english:
    price = app[4]
    if price == '0.0':
        ios_final.append(app)

print(len(android_final))
print(len(ios_final))


# Till here we have clean the data by removing duplicates, removing apps in language other then English and removing inaccurate data. We have also isolated free apps into andoid_final and ios_final.
# 
# As our goal is to build a minimal Android app and launch it on Google Store. If the app have positive reponse we will make its ios version with some improvements to launch it on Apple Store so we need to find the app profile which fits both Apple Store and Google Store as well. To do that we should have a frequency table to know number of apps in each genre.

# In[15]:


def freq_table(dataset, index):
    table = {}
    total = 0
    for row in dataset:
        total += 1
        value = row[index]
        if value in table:
            table[value]+=1
        else:
            table[value] = 1
            
    table_percentage = {}
    for key in table:
        percentage = (table[key]/total)*100
        table_percentage[key] = percentage
    return table_percentage


def display_table(dataset, index):
    table = freq_table(dataset, index)
    table_display = []
    for key in table:
        key_val_as_tuple = (table[key], key)
        table_display.append(key_val_as_tuple)
    
    table_sorted = sorted(table_display, reverse = True)
    for entry in table_sorted:
        print(entry[1], ' : ', entry[0])
    


# In[16]:


display_table(ios_final, -5)


# Limitation of this data : These apps are only English free apps.
# 
# On Apple Store most common genre are 'Games' (more then a half) 58%, Entertainment about 8% followed by Photo & Video about 5%. Educational apps are only 3.7% only and Social Networking apps are 3.3%. 
# 
# The General impression is that App Store is dominated for fun (Games, Entertainment photos and video) but apps having practical purpose (education, lifestyle) are rare.

# In[17]:


display_table(android_final, 1)


# The pattern is different of Google Play Store from App Store as Google Play Store has more practical purpose apps (Family about 19%, Tools 8.5%, Business 4.6%, Lifestyle 3,9%, health and fitness 3%). However, if we investigate this further, we can see that the family category (which accounts for almost 19% of the apps) means mostly games for kids.
# 

# In[18]:


display_table(android_final, -4)


# 'Genre' has more catagory then 'Catagory' column but as we are looking at big picture so we will work with 'Catagory' column. 

# Now we have to know which genre is used most by the users. We will calculate installs for each genre app. In the file of Google play store we have a column name as 'Install' which tells us number of installs but for Apple Store we do not have that column so we will use 'rating_count_tot' column to calculate installs for each genre app. 

# In[19]:


genres_ios = freq_table(ios_final, -5)
for genre in genres_ios:
    total = 0
    len_genre = 0
    for app in ios_final:
        genre_app = app[-5]
        if genre_app == genre:
            n_ratings = float(app[5])
            total += n_ratings
            len_genre += 1
    avg_n_ratings = total/len_genre
    print(genre, ' : ', avg_n_ratings)
    


# As you can see from this data, Navigation apps has most users but this is influenced by Waze or Google maps.

# In[20]:


for app in ios_final:
    if app[-5] == 'Navigation':
        print(app[1], ' : ', app[5])


# This same pattern applies for Social Networking genre as well where few giant companies like Facebook, Skype, Pininterest has influenced that average. We are looking for most popular genre overall. 

# In[21]:


for app in ios_final:
    if app[-5] == 'Reference':
        print(app[1], ' : ', app[5])


# As you can see the Reference genre is also influenced by Bible and Dictionary.com which has skew up the average.

# One thing we could do is take another popular book and turn it into an app where we could add different features besides the raw version of the book. This might include quotes of the day from the book, an audio version of the book etc. We could also add a dictionary within the app, so users don't need to quit our app to look up words.
# 
# This idea seems to fit well with the fact that the App Store is dominated by for-fun apps. This suggests the market might be a bit saturated with for-fun apps, which means a practical app might have more of a chance to stand out among the huge number of apps on the App Store.
# 
# Other genres that seem popular include weather, book, food and drink, or finance. The book genre seem to overlap a bit with the app idea we described above, but the other genres don't seem too interesting to us:
# Weather apps — people generally don't spend too much time in-app, and the chances of making profit from in-app adds are low. Also, getting reliable live weather data may require us to connect our apps to non-free APIs.
# Food and drink — examples here include Starbucks, Dunkin' Donuts, McDonald's, etc. So making a popular food and drink app requires actual cooking and a delivery service, which is outside the scope of our company.
# Finance apps — these apps involve banking, paying bills, money transfer, etc. Building a finance app requires domain knowledge, and we don't want to hire a finance expert just to build an app.
# 

# In[22]:


display_table(android_final, 5)


# For Google Play store data we do have number of installs but the issue with this data is that it is not precise because we dont know 1,000,000+ installs is 1000,000 or 2000,000 or 3000,000. But for our mission we dont need that precision so we would take 1000,000+ as 1000,0000 installs. 

# In[23]:


categories_android = freq_table(android_final, 1)

for category in categories_android:
        total = 0
        len_category = 0
        for app in android_final:
            category_app = app[1]
            if category_app == category:
                n_installs = app[5]
                n_installs = n_installs.replace(',', '')
                n_installs = n_installs.replace('+', '')
                total += float(n_installs)
                len_category += 1
        avg_n_installs = total/len_category
        print(category, ' : ', avg_n_installs)
        


# On average, Communication has most installs 38456119 but this number is skewed because of giant apps like Facebook, Skype, Messenger, Google Chrome that have one over billions of installs. 

# In[31]:


for app in android_final:
    if (app[1] == 'COMMUNICATION') and (app[5] == '1,000,000,000+'
                                    or app[5] == '500,000,000+'
                                    or app[5] == '100,000,000+'):
        print(app[0], ' : ', app[5])


# We will remove communiation apps which have more then 100 million installs which will reduce our average almost ten times. 

# In[26]:


under_100_m = []
for app in android_final:
    n_installs = app[5]
    n_installs = n_installs.replace(',', '')
    n_installs = n_installs.replace('+', '')
    if (app[1] == 'COMMUNICATION') and (float(n_installs) < 100000000):
        under_100_m.append(float(n_installs))
    
print(sum(under_100_m) / len(under_100_m))


# We see the same pattern for the video players category with 24,727,872 installs. The market is dominated by apps like Youtube, Google Play Movies & TV, or MX Player. We can observe the same pattern for social apps (where we have giants like Facebook, Instagram, Google+, etc.), photography apps (Google Photos and other popular photo editors), or productivity apps (Microsoft Word, Dropbox, Google Calendar, Evernote, etc.).
# 
# The game genre seems very popular, but we found out this part of the market seems a bit saturated, so we would like to come up with a different app recommendation if possible.
# 
# The books and reference genre looks fairly popular as well, with an average number of installs of 8,767,811. It's interesting to explore this in more depth, since we found this genre has some potential to work well on the App Store, and our aim is to recommend an app genre that shows potential for being profitable on both the App Store and Google Play.
# Let's take a look at some of the apps from this genre and their number of installs:

# In[27]:


for app in android_final:
    if app[1] == 'BOOKS_AND_REFERENCE':
        print(app[0], ' : ', app[5])


# There is variety of apps in this genre and still there are some popular apps who are skewing the average

# In[34]:


for app in android_final:
    if app[1] == 'BOOKS_AND_REFERENCE' and (app[5] == '1,000,000,000+'
                                           or app[5] == '500,000,000+'
                                           or app[5] == '100,000,000+'):
        print(app[0], ' : ', app[5])


# However, it looks like there are only a few very popular apps, so this market still shows potential. Let's try to get some app ideas based on the kind of apps that are somewhere in the middle in terms of popularity (between 1,000,000 and 100,000,000 downloads):

# In[33]:


for app in android_final:
    if app[1] == 'BOOKS_AND_REFERENCE' and (app[5] == '1,000,000+'
                                           or app[5] == '5,000,000+'
                                           or app[5] == '10,000,000+'
                                           or app[5] == '50,000,000+'):
        print(app[0], ' : ', app[5])


# ## Conclusion
# We also notice there are quite a few apps built around the book Quran, which suggests that building an app around a popular book can be profitable. It seems that taking a popular book (perhaps a more recent book) and turning it into an app could be profitable for both the Google Play and the App Store markets. We also need to add some special features like daily quotes from the book, an audio version of the book, quizzes on the book, a forum where people can discuss the book, etc.
# 
