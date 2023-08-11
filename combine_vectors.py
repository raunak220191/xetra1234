import os
import faiss
import pickle

# List of folders containing FAISS index files
index_folders = ['folder1', 'folder2', 'folder3']  # Update with your folder names

# Initialize an empty combined index
combined_index = None

# Iterate through each folder
for folder in index_folders:
    # Load index from .pkl and .faiss files
    index_path = os.path.join(folder, 'index.pkl')
    vectors_path = os.path.join(folder, 'vectors.faiss')
    
    with open(index_path, 'rb') as index_file:
        index = pickle.load(index_file)
    
    vectors = faiss.read_index(vectors_path)
    
    # Append or merge the vectors and metadata
    if combined_index is None:
        combined_index = index
    else:
        combined_index.merge_from(index)
    
    combined_index.add(vectors)

# Save the combined index to new .pkl and .faiss files
combined_index_path = 'combined_index.pkl'
combined_vectors_path = 'combined_vectors.faiss'

with open(combined_index_path, 'wb') as combined_index_file:
    pickle.dump(combined_index, combined_index_file)

faiss.write_index(combined_index, combined_vectors_path)
