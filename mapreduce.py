import pandas as pd
from mrjob.job import MRJob
from mrjob.step import MRStep

class MRValidation(MRJob):

    def steps(self):
        return [
            MRStep(mapper = self.mapper_get_data)
        ]

    def mapper_get_data(self, _, line):
        data = line.split(",")
        # Check for valid non-header data
        if data and "|" not in data[0]:
            # Create dict of form {"P": "P10", ...}
            data_dict = {
                value[0] if value else None: value
                for value in data
            }
            
            # For now just check of rule # 2. Can add more later
            yield ("SP", data_dict.get("S")), data_dict.get("P")


if __name__ == "__main__":
    MRValidation.run()
