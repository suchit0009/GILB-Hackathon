import networkx as nx
import pandas as pd
import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from data_pipeline.loader import load_paysim_data

class GraphIntel:
    def __init__(self):
        self.G = None
        print("🕸️  Initializing Graph Intelligence Engine...")

    def build_graph(self):
        """
        Loads PaySim data and builds a Directed Graph.
        Nodes: Users (nameOrig, nameDest)
        Edges: Transactions (with amount as weight)
        """
        print("⏳ Loading Data for Graph Construction...")
        df = load_paysim_data()
        
        # Take a sample to keep it fast for Demo (e.g., first 50k txns)
        # In prod, this would be a time-window sliding graph
        df_sample = df.head(50000)
        
        print(f"🏗️  Building Graph from {len(df_sample)} transactions...")
        self.G = nx.from_pandas_edgelist(
            df_sample, 
            source='nameOrig', 
            target='nameDest', 
            edge_attr='amount', 
            create_using=nx.DiGraph()
        )
        print(f"✅ Graph Built: {self.G.number_of_nodes()} Nodes, {self.G.number_of_edges()} Edges")

    def detect_cycles(self):
        """
        Layer A: Deterministic Cycle Detection (The "Hundi" Loop).
        Finds simple cycles: A -> B -> C -> A
        """
        if not self.G: self.build_graph()
        
        print("🔄 Running Cycle Detection (DFS)...")
        try:
            # simple_cycles is computationally expensive, so we limit exposure in demo
            # We look for cycles
            cycles = list(nx.simple_cycles(self.G))
            if cycles:
                print(f"🚨 FRAUD DETECTED: Found {len(cycles)} Circular Money Loops!")
                for i, cycle in enumerate(cycles[:3]):
                    print(f"   Loop {i+1}: {' -> '.join(cycle)}")
            else:
                print("✅ No suspicious circular loops found in this sample.")
        except Exception as e:
            print(f"⚠️ Cycle detection timed out or error: {e}")

    def sort_pagerank(self):
        """
        Layer B: MuleRank (PageRank Centrality).
        Identifies high-traffic bridge nodes.
        """
        if not self.G: self.build_graph()
        
        print("📊 Calculating MuleRank (PageRank)...")
        pagerank = nx.pagerank(self.G, weight='amount', alpha=0.85)
        
        # Sort by Score
        sorted_nodes = sorted(pagerank.items(), key=lambda x: x[1], reverse=True)
        
        print("🚨 TOP 5 SUSPICIOUS 'MULE' ACCOUNTS (High Centrality):")
        for i, (node, score) in enumerate(sorted_nodes[:5]):
            print(f"   {i+1}. {node} (Score: {score:.6f})")

if __name__ == "__main__":
    intel = GraphIntel()
    intel.build_graph()
    intel.sort_pagerank()
    intel.detect_cycles()
