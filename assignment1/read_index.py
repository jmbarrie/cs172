# This file should contain code to receive either a document-id or word or both and output the required metrics. See the assignment description for more detail.
from indexreader import IndexReader
import sys

if __name__ == "__main__":
    ir = IndexReader(sys.argv[1:])
    ir.run_command()