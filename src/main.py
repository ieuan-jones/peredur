from fitparse import FitFile
from activity import Activity
import sys

with open(sys.argv[1], 'rb') as f:
    fitfile = f.read()

activity = Activity(file_data = fitfile, file_format='fit')
print(activity.records)
