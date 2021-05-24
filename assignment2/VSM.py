# This file should contain code to receive either a document-id or word or both and output the required metrics. See the assignment description for more detail.
from src.indexreader import IndexReader
from src.vectorspacemodel import VectorSpaceModel
from src.ranker import Ranker
import sys
import timeit

if __name__ == "__main__":
    query_f = sys.argv[1]
    output_f = sys.argv[2]
    vsm = VectorSpaceModel(query_f)
    vsm.vectorize()
    ir = IndexReader(vsm.vsm)
    ir.run_command(output=False)
    ranker = Ranker(ir.intermediate_data, output_f)
    ranker.compute()
