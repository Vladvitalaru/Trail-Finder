import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import graphviz_layout
from matplotlib.backends.backend_pdf import PdfPages
"""Will be used to calculate pagerank based off of adjacent links file generated from crawler, will later need to store 'pr' as a dictionary to refer to when indexing in mywhoosh.py
as well as removing the plotting and saving figures, only used for debugging right now"""
def main():
    DG = nx.read_gpickle("./adjacent_links.gpickle")
    f = plt.figure(figsize=(100,100))
    plt.subplot(121)
    pr = nx.pagerank_numpy(DG, weight=None)
    print(pr)
    nx.draw(DG, with_labels=True, font_weight='bold')
    plt.show()
    f.savefig("Example1.pdf", bbox_inches='tight')

if __name__ == '__main__':
	main()