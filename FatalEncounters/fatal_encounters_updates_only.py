import urllib.request
import json
import time
import re
import sys

#Setup some stateful variables.

#The time the spreadsheet was last modified. If we've already run this script
#after the last_modified time, there's no point doing any real work as the state
#of the world doesn't change.
last_modified_time = None

#The main reason as to why this exists is to check if there are new entries or
#amended entries when the last_modified_time changes. For example, if the
#last_modified_time changes, we run the script. However, if the number of
#fatalities have decreased or remained unchanged, it means that one of the
#existing entries has been modified. While we won't iterate through the entire
#dataset to check which entry has been changed for this assignment, it's
#probably worth bearing in mind.
size_of_data = 0

#processed_entries holds the "UniqueID" (as per the spreadsheet) of
#all entries processed.
#There is a massive assumption made here: the UniqueID for
#a subject can never change, i.e. if someone's got a UniqueID of 100, no one
#else will get that ID/the ID will always be associated with the said person.
#I reached out to the person who owns the database, and he said:
#"Generally speaking, no, they wouldn't change. This week, though, I had to redo
#them. I wasn't able to diagnose the cause--human error or a quirk with the Google
#sheet--but a formula somehow made it into the Unique IDs, so there were differences
#between Column A and Column W. So, since we both research past incidents and current
#ones, the IDs will grow increasingly disordered beginning with the next update."
processed_entries = [];

#We want to continuously poll this spreadsheet to see if there are any changes.
#In between each request, we can sleep for a couple of minutes, as this isn't a
#critical application.
while(True):
  #print(time.strftime("%H:%M:%S") + ": Retrieving the spreadsheet.")
  #Requests the "Fatal Encounters" spreadsheet in a JSON format so that we can
  #parse it easily, and then reads the response in, in a human-intelligible
  #format (i.e. utf-8 or the charset that the spreadsheet's metadata has.).
  response = urllib.request.urlopen("https://spreadsheets.google.com/feeds/list/"
      +
          "1dKmaV_JiWcG8XBoRgP8b4e9Eopkpgt7FL7nyspvzAsE/od6/public/basic?alt=json")
  data = response.read().decode(response.info().get_param('charset') or 'utf-8')

  data_in_dictionary = json.loads(data)

  #Extracts the headers from the metadata in the response. Amongst other things,
  #the metadata contains the last-modified time. If this time is different to
  #the last_modified_time, we need to run through the file and find the new
  #entries to push out.
  #Alternatively, we could've cross-validated this with the Content-Length attribute, but
  #that doesn't seem to exist?
  headers = response.info()._headers
  for header in headers:
    if header[0].lower() == "last-modified":
      new_last_modified_time = header[1]
      break;

  #If the last_modified_time has changed, we need to amend the value we are
  #storing, so that the next run checks against the _correct_
  #last_modified_time.
  #Additionally, only if the last_modified_time is different do we do some work.
  if (last_modified_time != new_last_modified_time):
    #print(time.strftime("%H:%M:%S") + ": The Last Modified time has not changed between versions.")
  #else:
    #print(time.strftime("%H:%M:%S") + ": The Last Modified time has changed between the two "
    #                                    "versions, so there's work to do.")
    #First set the last_modified_time to the new_last_modified_time so that we have the correct timestamp when we do
    #the next iteration.
    last_modified_time = new_last_modified_time;

    #Then, pull out list of fatalities...
    fatalities = data_in_dictionary["feed"]["entry"]
    #...and get the total number of fatalities that exist in the spreadsheet, i.e.
    #not just the changes.
    new_size_of_data = len(fatalities)
    if (new_size_of_data == size_of_data):
      #Is this a sensible solution? For example, an entry could've been deleted
      #and a new one added, but then does that go beyond the scope of this
      #assignment?
      continue;
    else:
      for fatality in fatalities:
      #Searches forI the term "uniqueidentifier:" in the string and returns the
      #number that follows. 
        unique_id_match = re.search('uniqueidentifier: (\w+)',
          fatality["content"]["$t"])

        if (unique_id_match != None):
          unique_id = unique_id_match.groups(0)[0]

        #If we've already processed this fatality, we don't need to do anything.
        if unique_id in processed_entries:
          continue
        else:
          #Else, we need to add it to the list of entries we've processed.
          processed_entries.append(unique_id)

          #Searches for the term "locationofdeathstate:" in the string and returns the
          #word that appears immediately after. As it's just the state shortcode, we
          #don't really need anything else, so this regex can be relatively simple.
          state_match = re.search('locationofdeathstate: (\w+)',
              fatality["content"]["$t"])

          if (state_match != None):
            state = state_match.groups(0)[0]

          #Searches the string for the term "subjectsrace:" and extracts everything that
          #appears after the colon until a comma appears. So, for example:
          #"subjectsrace: Hispanic/Latino, dateofinjuryresultingindeathmonthdayyear:..."
          #will result in race = Hispanic/Latino. If we used the same solution as state,
          #we'd end up dropping the Latino, which would be sub-optimal.
          race_match = re.search('subjectsrace: ([^,]+)', fatality["content"]["$t"])

          #...because every now and again, the data we have is incomplete, so we could
          #drop it entirely or keep the limited data that is available.
          if (race_match != None):
            race = race_match.groups(0)[0]

          #Pulls out the date of the injury that eventually led to the subject's death.
          #It uses logic similar to the race, but needs to extract the date, month and
          #year, which is in the format Month, DD, YYYY (e.g. February 18, 2016).
          #Note: There's some data inconsistency here where for a couple of entries, the
          #data is in the format MM/DD/YYYY.
          date_match = re.search('dateofinjuryresultingindeathmonthdayyear: ([^,]*,[^,]*)',
              fatality["content"]["$t"])

          if (date_match != None):
            date = date_match.groups(0)[0]

          #Dictionary with all the details, that'll eventually be flushed out.
          details = {}
          details["race"] = race
          details["state"] = state
          details["date"] = date

          #Normally, with this kind-of batch processing, one would steer clear of 15K
          #flushes, but instead batch the dumps in a sensible manner -- say by year?
          #However, for the purpose of this assignment, this script attempts to emulate
          #the polling API such that it is easy to see data flow through, while not
          #waiting endlessly.
          print(json.dumps(details))
          sys.stdout.flush()
  time.sleep(120)

