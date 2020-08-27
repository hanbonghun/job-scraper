import csv
import os

#Saves imported job information in csv file format
def save_to_file(jobs):
    file = open("jobs.csv", mode='w', encoding='utf8',newline='')
    writer = csv.writer(file)
    writer.writerow(['title','company','location','link'])
    for job in jobs:
        writer.writerow(list(job.values()))
    return
