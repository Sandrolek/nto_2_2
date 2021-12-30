#!/usr/bin/env python
# -*- coding: utf-8 -*-

import networkx as nx
import matplotlib.pyplot as plt

# g=nx.complete_graph(5)

g1 = nx.petersen_graph()
nx.draw(g1)
plt.show()
