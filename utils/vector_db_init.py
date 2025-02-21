import faiss
import numpy as np

# Create a random FAISS index and store vectors
dimension = 128
index = faiss.IndexFlatL2(dimension)
vectors = np.random.random((100, dimension)).astype("float32")
index.add(vectors)  # Add vectors to the index

# Save the FAISS index to a file
faiss.write_index(index, "faiss_index.index")

# Load the FAISS index from a file
loaded_index = faiss.read_index("faiss_index.index")
print("Index loaded with", loaded_index.ntotal, "vectors.")
