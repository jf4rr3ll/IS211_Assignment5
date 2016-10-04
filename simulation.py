#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Assignment 5 Module"""


import urllib2
import csv
import argparse

class Request:
    def __init__(self, req_time, req_url, req_process):
        self.req_time = int(req_time)
        self.req_url = req_url
        self.req_process = int(req_process)
        self.waitTime = 0

    def getTime(self):
        return self.req_time

    def getRequestURL(self):
        return self.req_url

    def getProcessTime(self):
        return self.req_process

    def getWaitTime(self, req_time):
        return self.req_time - self.req_process


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
        self.time_remaining = new_task.getTime()


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
    server = Server()
    server_queue = Queue()
    waiting_times = []

    for i in filename:
        req_sec = i[0]
        req_url = i[1]
        req_process = i[2]
        request = Request(req_sec, req_url, req_process)
        server_queue.enqueue(request)

        if (not server.busy()) and (not server_queue.is_empty()):
            next_request = server_queue.dequeue()
            waiting_times.append(next_request.getWaitTime(req_sec))
            server.start_next(next_request)

        server.tick()

    average_wait = sum(waiting_times) / len(waiting_times)

    print("Average Wait %6.2f secs for %3d tasks remaining." % (average_wait, server_queue.size()))


def simulateManyServers(filename, server_num):
    """Defines a function to print the average wait time for multiple servers with load balancing"""
    server = [Server() * server_num]
    server_queue = Queue()
    waiting_times = []

    for i in filename:
        req_sec = i[0]
        req_url = i[1]
        req_process = i[2]
        request = Request(req_sec, req_url, req_process)
        server_queue.enqueue(request)

    for i in server:
        if (not server.busy()) and (not server_queue.is_empty()):
            next_request = server_queue.dequeue()
            waiting_times.append(next_request.getWaitTime(req_sec))
            server.start_next(next_request)

        server.tick()

    average_wait = sum(waiting_times) / len(waiting_times)

    print("Average Wait %6.2f secs for %3d tasks remaining." % (average_wait, server_queue.size()))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", help="Enter the filename to get the CSV file.")
    parser.add_argument("--server", help="Enter the number of servers for load balancing.")
    args = parser.parse_args()
    csvData = csv.reader(urllib2.urlopen(args.file))

    if not args.server:
        simulateOneServer(csvData)
    else :
        simulateManyServers(csvData)

if __name__ == "__main__":
    main()