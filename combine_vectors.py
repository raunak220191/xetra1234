import os
import faiss

# List of folders containing FAISS index files
index_folders = ['folder1', 'folder2', 'folder3']  # Update with your folder names

# Initialize an empty combined index
d = 256  # Dimension of your vectors
index = faiss.IndexFlatL2(d)  # Use IndexFlatL2 for example

# Iterate through each folder
for folder in index_folders:
    # Load the vectors from .faiss file
    vectors_path = os.path.join(folder, 'vectors.faiss')
    loaded_index = faiss.read_index(vectors_path)
    
    # Add vectors from the loaded index to the combined index
    vectors = loaded_index.reconstruct_n(loaded_index.ntotal)
    index.add(vectors)

# Save the combined index to a new .faiss file
combined_index_path = 'combined_index.faiss'
faiss.write_index(index, combined_index_path)
