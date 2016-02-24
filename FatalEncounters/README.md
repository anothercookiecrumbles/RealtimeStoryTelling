##Introduction
[Fatal Encounters](http://www.fatalencounters.org) was conceived by D. Brian Burghart after the 2012 killing of an unarmed college student in Alabama. The mission is to build the database containing all lives lost during police encounters starting at the turn of the millennium. This is similar to The Guardian's project, [The Counted](http://www.theguardian.com/us-news/2015/oct/06/suicide-by-cop-the-counted). Like The Guardian's project, it also crowdsources the data and cross-validates it before putting it on the master spreadsheet. There are three big differences though:

- While The Guardian's The Counted dataset is available as multiple CSVs (one for each year), this is in a Google Spreadsheet, which makes it accessible through JSON. 
- This project has data going back to 2000, while The Counted only has data for the last couple of years. 
- There is a lot more context around each situation in this dataset, which I found appealing. 

For me, coming from a country where the police don't use guns but tasers, this subject is incredibly fascinating. Looking through the records, here are some highlights (with caveats): 
- The average number of people who die each year is 750. 
- In the early noughties, this number was under the 500 mark. 
- In the last three years, the number has constantly been greater than 1,200. 

It's worth noting that one of the reasons for this discrepency could be because all the details of the older killings haven't been verified. 

Burghart, on his website, says that by the end of 2016, there'll be over 20,000 fatalities, and he wants to systematically work towards capturing them all. 

This assignment starts by grabbing all the data from the spreadsheet and filtering out data that's older than two weeks. It then continuously polls the spreadsheet looking for modifications. On finding any modification, it simply checks the date of the event, and if it's within the last fourteen days, it filters it through. All events that are filtered through are inserted into Redis with an expiry of 14 days. This means that we're continuously calculating the average for every fourteen day period. 

Depending on the average calculated, two notifications are sent out: "Good news" if the average is less than 2 and "Bad news" if it's more than 7. These notifications are sent to a Slack channel. The thresholds are based on the observed trends. 

##Technical Specification 
The project was built using Python 3. 
It also needs Redis and the official SlackClient for Python.

**Files**

Four files are included in this project:
- fatal_encounters_updates_only.py which loads the entire dataset from the Google Spreadsheet and then looks for updates. 
- insert_into_redis.py which inserts the data into Redis (much as the name suggests). 
- calculate_moving_average.py which calculates the moving average over periods of fourteen days. 
- slack.py which pushes notifications out to Slack based on the whether the moving average calculated breaches the thresholds. 

**Running the project**

The files can run in sets of two: 
- To poll the database and update Redis:
`python3 fatal_encounters_updates_only.py | python3 insert_into_redis.py`
- To calculate the moving averages and push the notifications to Slack: 
`python3 calculate_moving_average.py | python3 slack.py`

Note: To get the Slack integration to work, you'll have to enter your access token and channel – I could've added mine/driven it out of configuration, but then that would involve adding you to a(n) (ephemeral) channel. I wasn't sure if that was the right thing to do. 

##Additional Notes
- Looking at the spreadsheet, it looks like the data is sorted chronologically and at first glance, it looks like the keys are also chronological. However, Burghart confirmed that this wasn't going to be the case, and the reason why it was this way was due to a technical/human bug earlier, which he'd had to fix manually. 
- Unlike my first assignment, I've adopted the convention used in class, where multiple scripts are piped together instead of a it being a monolithic application. 
- There's a lot more interesting things that we can do with this data, specially in terms of making interactive visualisations. It's something I'd like to explore in upcoming assignments if the opportunity arises. 
- I acknowledge that perhaps Slack isn't the best medium for these notifications, but my rationale was twofold:
  - I've never experimented with the Slack API before, and now seemed as good a time as any. The other option was using Twitter, but I'd used that in my first assignment. 
  - As it's simply a notification on hitting a certain threshold, creating a webview which people have to go to seemed excessive. 
