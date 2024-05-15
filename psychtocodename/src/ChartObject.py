from src.Paths import Paths
import json

class ChartObject:
    """
    A convenient way to store chart metadata.

    Args:
        file_name (str): The name of the chart file.
    """
    def __init__(self, fileName: str) -> None:
        self.fileName = fileName
        fileName = fileName[:-5].split("-")
        self.json:dict = None

        self.chartDiff = "normal"
        if fileName[-1] in Settings.get("ignoreDiffs"):
            self.chartDiff = fileName[-1]
            fileName = fileName[:-1]

        self.chartName = " ".join(fileName).title()

    def parseJSON(self):
        with open(f'{Settings.path("data/ChartConverter/chart_import")}\{self.fileName}', 'r') as f:
            self.json = json.load(f).get("song")