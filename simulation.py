#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Assignment 5 Module"""


import urllib2
import csv
import argparse

class Request:
    def __init__(self, request):
        self.timestamp = request[0]
        self.time = request[2]

    def get_stamp(self):
        return self.timestamp

    def get_time(self):
        return self.time

    def wait_time(self, current_time):
        return current_time - self.timestamp


class Server:
    def __init__(self):
        self.current_task = None
        self.time_remaining = 0

    def tick(self):
        if self.current_task != None:
            self.time_remaining = self.time_remaining - 1
            if self.time_remaining <= 0:
                self.current_task = None

    def busy(self):
        if self.current_task != None:
            return True
        else: return False

    def start_next(self,new_task):
        self.current_task = new_task
        self.time_remaining = new_task.get_time()


class Queue:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0, item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)


def simulateOneServer(filename):
    """Defines a function to print the average wait time for the request"""
    return avg


def simulateManyServers(filename):
    """Defines a function to print the average wait time for multiple servers with load balancing"""
    return avg


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", help="Enter the filename to get the CSV file.")
    parser.add_argument("--server", help="Enter the number of servers for load balancing.")
    args = parser.parse_args()

    if args.file:
        try:
            csvData = csv.reader(urllib2.urlopen(args.file))
            simulateOneServer(csvData)

        except urllib2.URLError as URLError:
            print "This URL entered is invalid."
            raise URLError
    elif args.servers:
        try:
            csvData = csv.reader(urllib2.urlopen(args.server))
            simulateManyServers(csvData)
    else:
        print "Please enter a valid URL."

if __name__ == "__main__":
    main()