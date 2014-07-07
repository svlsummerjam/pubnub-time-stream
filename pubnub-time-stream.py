#!/usr/bin/env python
#Copyright (c) 2014 James Beedy
import os
from Pubnub import Pubnub
from argparse import ArgumentParser
from time import time, sleep
from json import dumps

def arg_parser():
    parser = ArgumentParser(
        description='pubnub timestamp publisher for arduino',
        prog='pubnub-time-stream'
    )
    parser.add_argument(
        'channel',
        metavar='channel',
        help='channel',
    )
    parser.add_argument(
        'publish',
        metavar='publish',
        help='publish'
    )
    parser.add_argument(
        'subscribe',
        metavar='subscribe',
        help='subscribe'
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        '-p',
        '--pub',
        nargs='?',
        help="Value must be yes"
    )
    group.add_argument(
        '-s',
        '--sub',
        nargs='?',
        help="Value must be yes",
    )
    parser.add_argument(
        '-v',
        '--version',
        action='version',
        version='%(prog)s v0.1a'
    )
    return parser


class Streamteam(object):

    def __init__(self, args):
        self.channel = args.channel
        self.pubnub = Pubnub(
            args.publish,
            args.subscribe,
            None,
            False
        )

    def publish(self, m):
        def callback(message):
            return message

        self.pubnub.publish(
            self.channel,
            m,
            callback=callback,
            error=callback
        )

    def subscribe(self):

        def callback(message, channel):
                print(message)

        def error(message):
            print("ERROR : " + str(message))

        def connect(message):
            print("CONNECTED")

        def reconnect(message):
            print("RECONNECTED")

        def disconnect(message):
            print("DISCONNECTED")

        self.pubnub.subscribe(
            self.channel,
            callback=callback,
            error=callback,
            connect=connect,
            reconnect=reconnect,
            disconnect=disconnect
        )

if __name__ == "__main__":

    # Create ArgumentParser to get input that initializes Streamteam
    parser = arg_parser()
    args = parser.parse_args()

    #initialize Pubnub
    pub_stream = Streamteam(args)


    if args.sub:
        try:
            while True:
                pub_stream.subscribe()
        except KeyboardInterrupt:
            pass
        finally:
            pass

    if args.pub:
        try:
            while True:
                ts = time() 
                time_dict = dumps({"time": ts})
                pub_stream.publish(str(time_dict))
                sleep(1)
        except KeyboardInterrupt:
            pass
