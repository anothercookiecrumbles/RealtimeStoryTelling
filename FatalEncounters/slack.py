from slackclient import SlackClient
import time
import sys

#The access token needed by Slack to connect. This access token can be created
#by following the instructions at: https://api.slack.com/docs/oauth. For
#security reasons, this shouldn't be stored in plaintext in a file but instead
#it should be pulled from configuration, which isn't easily accessible. .
token = "ENTER TOKEN HERE"

#Initialise the slackClient. This opens a connection to Slack, and validates
#the access token that's passed in. If the access token has been revoked or is
#invalid, the slackClient will not connect, and therefore, we will not be able
#to publish messages to any Slack channel(s).
slackClient = SlackClient(token)

#This checks if our connection to Slack was successfully established. We connect
#to the RTM, which is an acronym for Slack's Realtime Messaging (RTM) API. More
#details can be found at: https://api.slack.com/rtm.
#It is desirable to use the RTM API as we will create a connection that'll stay
#open indefinitely (ideally), and stream messages to the channel as they come
#in.
if slackClient.rtm_connect():
    #Ideally, we are going to pipe messages into this script _forever_.
    #Therefore, we have a while loop that continuously runs, and pushes messages
    #to the Slack channel, provided there are messages to send.
    #It's worth noting that the flood of messages expected is relatively low.
    #Hence, there are no attempts to conflate messages (i.e. send messages in
    #batches. Additionally, as this information isn't critical, we can afford to
    #sleep for a minute (60 seconds) between iterations.
    while True:
        message = sys.stdin.readline()
        slackClient.rtm_send_message('pri_slack_dev', message)
        time.sleep(60)
else:
    print("Connection Failed, invalid token?")

