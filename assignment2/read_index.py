# This file should contain code to receive either a document-id or word or both and output the required metrics. See the assignment description for more detail.
from src.indexreader import IndexReader
from src.vectorspacemodel import VectorSpaceModel
from src.ranker import Ranker
import sys
import timeit

if __name__ == "__main__":
    query_f = "query_list.txt"
    output_f = "./data/output.txt"
    vsm = VectorSpaceModel(query_f, output_f)
    vsm.vectorize()
    ir = IndexReader(vsm.vsm)
    ir.run_command(output=False)
    ranker = Ranker(ir.intermediate_data)
    # start = timeit.default_timer()
    ranker.compute()
    # end = timeit.default_timer()
    # print(ranker.all_query_weights)

    # print(end - start)
    print(ir.print_args())
    # 16 AP891229-0148
    # 2514 16 AP891229-0105 confirmed 16
    # 2237 16 AP891227-0033 confirmed 16
    # 2557 16 AP891229-0148 confirmed 16
    # TODO: don't forget that the bottom is 