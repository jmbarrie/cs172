# This file should contain code to receive either a document-id or word or both and output the required metrics. See the assignment description for more detail.
from src.indexreader import IndexReader
from src.vectorspacemodel import VectorSpaceModel
import sys
import timeit

if __name__ == "__main__":
    query_f = "query_list.txt"
    output_f = "\data\output.txt"
    vsm = VectorSpaceModel(query_f, output_f)
    vsm.vectorize()
    ir = IndexReader(vsm.vsm)
    start = timeit.default_timer()
    ir.run_command(output=False)
    end = timeit.default_timer()
    ir.intermediate_data['91'][-1].sort()
    print(ir.intermediate_data['91'])

    print(end - start)