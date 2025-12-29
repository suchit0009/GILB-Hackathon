import torch
import torch.nn.functional as F
from torch_geometric.nn import SAGEConv
from torch_geometric.data import Data
import pandas as pd
import numpy as np
import sys
import os
from sklearn.preprocessing import LabelEncoder

# Add project root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from data_pipeline.loader import load_paysim_data

MODEL_OUTPUT_PATH = "deep_lane/sentinel_gnn.pt"

class FraudSage(torch.nn.Module):
    """
    GraphSAGE Model for Fraud Detection.
    Aggregates features from 2 hops of neighbors.
    """
    def __init__(self, in_channels, hidden_channels, out_channels):
        super().__init__()
        self.conv1 = SAGEConv(in_channels, hidden_channels)
        self.conv2 = SAGEConv(hidden_channels, out_channels)

    def forward(self, x, edge_index):
        # Hop 1
        x = self.conv1(x, edge_index)
        x = F.relu(x)
        x = F.dropout(x, p=0.5, training=self.training)
        
        # Hop 2
        x = self.conv2(x, edge_index)
        
        return F.log_softmax(x, dim=1)

def train_gnn():
    print("🧠 Starting Sentinel GNN Training (GraphSAGE)...")
    
    # 1. Load Data
    df = load_paysim_data()
    # Sample for demo speed
    df = df.head(100000) 
    
    print("🏗️  Constructing Graph Tensors (PyG Data)...")
    
    # Encode Nodes
    le = LabelEncoder()
    # Fit on all possible accounts
    all_accounts = pd.concat([df['nameOrig'], df['nameDest']]).unique()
    le.fit(all_accounts)
    
    src = le.transform(df['nameOrig'])
    dst = le.transform(df['nameDest'])
    
    edge_index = torch.tensor([src, dst], dtype=torch.long)
    
    # Features: For demo, we use 'Amount' and 'Type' as node features
    # In reality, you'd aggregate transaction history per node first
    # Here we initialized random embeddings for simplicity of the demo script
    num_nodes = len(all_accounts)
    x = torch.randn((num_nodes, 16), dtype=torch.float) # 16-dim embedding
    
    # Labels: We map 'isFraud' from edges back to source nodes
    # (Simplified assumption: If you send fraud, you are fraud)
    y = torch.zeros(num_nodes, dtype=torch.long)
    fraud_senders = df[df['isFraud'] == 1]['nameOrig']
    fraud_indices = le.transform(fraud_senders)
    y[fraud_indices] = 1
    
    data = Data(x=x, edge_index=edge_index, y=y)
    
    # 2. Initialize Model
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = FraudSage(in_channels=16, hidden_channels=32, out_channels=2).to(device)
    data = data.to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
    
    model.train()
    print("🔥 Training for 50 Epochs...")
    
    for epoch in range(50):
        optimizer.zero_grad()
        out = model(data.x, data.edge_index)
        loss = F.nll_loss(out, data.y)
        loss.backward()
        optimizer.step()
        
        if epoch % 10 == 0:
            pred = out.argmax(dim=1)
            correct = (pred == data.y).sum()
            acc = int(correct) / int(data.num_nodes)
            print(f"   Epoch {epoch:02d} | Loss: {loss:.4f} | Accuracy: {acc:.4f}")
            
    # 3. Save
    print(f"💾 Saving GNN Model to {MODEL_OUTPUT_PATH}...")
    torch.save(model.state_dict(), MODEL_OUTPUT_PATH)
    print("🎉 Graph Neural Network Trained Successfully.")

if __name__ == "__main__":
    train_gnn()
