#!/usr/bin/env python
import zephyr
from firebase import Firebase
import time

#Setup
zephyr.init()
fb = Firebase('http://gamma.firebase.com/mikexstudios/zephyr')

#Subscribe to the most popular zephyr classes
zephyr.Subscriptions().add(('help', '*', '*'))
zephyr.Subscriptions().add(('sipb', '*', '*'))
zephyr.Subscriptions().add(('mxh', '*', '*')) #for testing

#To send a message, ex.
#zephyr.ZNotice(cls='sipb', message="zsig\x00Message body\n", ...).send()

#Wait for messages. It's probably better to poll for messages than to use
#blocking loop.
print 'Listening to zephyr messages...'
while True:
    m = zephyr.receive(True) #True -> blocks up to a minute
    [zsig, body] = m.message.split("\x00")
    body = body.strip()

    #Send message to Firebase
    ref = fb.child(m.cls) #separate by class
    ref.push({'class': m.cls, 
              'instance': m.instance, 
              'sender': m.sender,
              'time': m.time, #seconds since epoch
              'zsig': zsig,
              'body': body,})
    print "%s / %s / %s %s (%s)\n   %s" % (m.cls, m.instance, m.sender, 
                                           time.ctime(m.time), zsig, body)

  
