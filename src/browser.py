# Browser for data passes

# iterate over all files in the data directory and decode their timestamps
import datetime
from pathlib import Path
import pandas as pd
from metadata import ReceiverMeta

data_dir = "data"
file_timestamp_format = "%y%m%d-%I%M%S"

def parse_run_timestamp(run_timestamp: str) -> datetime.datetime:
    return datetime.datetime.strptime(unparsed_timestamp, file_timestamp_format)

# get the string timestamp prefix of a test run
def get_all_test_run_timestamps() -> List[str]:
    directory = Path("data")
    all_timestamps = []

    for file in directory.iterdir():
        if file.is_file() and file.suffix == ".csv":
            unparsed_timestamp = file.stem[:len(file_timestamp_format)]
            all_timestamps.append(unparsed_timestamp)
    return all_timestamps

class TestRun:
    def __init__(self, data, metadata):
        self.data = data
        self.metadata = metadata

    @classmethod
    def from_timestamp(cls, timestamp: str):
        data_filename = f"{data_dir}/{timestamp}-recv.csv"
        data_run = pd.read_csv(data_filename)

        metadata = ReceiverMeta.read_recv_metadata(timestamp)
        return cls(data_run, metadata)


all_test_run_timestamps = get_all_test_run_timestamps()

for run_timestamp in all_test_run_timestamps:
    run = TestRun.from_timestamp(run_timestamp)
    pd.display(run.data)
