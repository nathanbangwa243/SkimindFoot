import unittest
from .. import data_extractor

from .. import main

from .. import skiconfig

from .. import config

import os

file_name = filter(lambda filename: '.pdf' in filename, os.listdir(config.PDF_SAMPLES_DIR))
file_name = list(file_name)[0]

class TestPdfManag(unittest.TestCase):
    def setUp(self):
        self.data_extractor = data_extractor
    
    def test_dataextractor(self):
        print("help")
        self.assertTrue(False)
    
    def test_main(self):
        exist = os.path.isfile(file_name)
        self.assertTrue(exist)

        



if __name__ == "__main__":
    unittest.main()