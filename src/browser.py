# Browser for data passes

# iterate over all files in the data directory and decode their timestamps
import datetime
from pathlib import Path

file_timestamp_format = "%y%m%d-%I%M%S"
directory = Path("data")

for file in directory.iterdir():
    if file.is_file():
        filename = file.stem
        timestamp = datetime.datetime.strptim(filename)

        # read both the data and metadata file and display information

# iterate over every item in the data directory
# for each of them construct an object that contains a pandas dataframe for the data, 
#   and a constructed metadata object for other information
