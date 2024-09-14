import ffmpeg
import torch
import numpy as np
import matplotlib.pyplot as plt
from pyannote.audio import Inference
from spectralcluster import SpectralClusterer
from sklearn.decomposition import PCA

HUGGING_FACE_TOKEN = "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"

if torch.backends.mps.is_available():
    device = torch.device("mps")  # Use Metal (MPS) if available
else:
    device = torch.device("cpu")

def convert_mp4_to_wav(input_mp4, output_wav):
    try:
        ffmpeg.input(input_mp4).output(output_wav, format='wav', acodec='pcm_s16le', ac=1, ar='16k').run(overwrite_output=True)
        print(f"Converted {input_mp4} to {output_wav}")
    except ffmpeg.Error as e:
        print(f"Error: {e}")

def extract_speaker_embeddings(wav_file):
    # Load a pre-trained speaker embedding model
    model = Inference("pyannote/embedding", use_auth_token=HUGGING_FACE_TOKEN, device=device)
    embedding = model(wav_file)
    # embeddings = np.vstack([seg.data.numpy() for seg in embedding]) 

    if isinstance(embedding, tuple):
        # The first element is usually the actual embeddings; adjust this based on your output structure
        embeddings = np.vstack([seg.data.numpy() for seg in embedding[0]])  # Use the first element of the tuple
    else:
        # Handle if it's not a tuple (fallback)
        embeddings = np.vstack([seg.data.numpy() for seg in embedding])
    return embeddings

def cluster_speakers(embeddings, min_clusters=2, max_clusters=10):
    """
    Perform speaker clustering on extracted embeddings using Spectral Clustering.
    """
    # Initialize SpectralClusterer
    clusterer = SpectralClusterer(
        min_clusters=min_clusters,  # Minimum number of clusters (speakers)
        max_clusters=max_clusters,  # Maximum number of clusters (speakers)
        p_percentile=0.95,
        gaussian_blur_sigma=1.0)

    # Perform clustering
    labels = clusterer.predict(embeddings)
    
    return labels

def visualize_clusters(embeddings, labels):
    """
    Visualize the clustering results in a 2D plot using PCA.
    """

    pca = PCA(n_components=2)
    embeddings_2d = pca.fit_transform(embeddings)

    for i in set(labels):
        plt.scatter(embeddings_2d[labels == i, 0], embeddings_2d[labels == i, 1], label=f"Speaker {i}")

    plt.title("Speaker Clustering Visualization")
    plt.legend()
    plt.show()

def main():
    input_mp4 = 'test1.mp4'  # Replace with your .mp4 file path
    output_wav = 'output_audio.wav'

    convert_mp4_to_wav(input_mp4, output_wav)

    embeddings = extract_speaker_embeddings(output_wav)
    labels = cluster_speakers(embeddings)
    print("Clustering Results:")
    for i, label in enumerate(labels):
        print(f"Segment {i}: Speaker {label}")
    visualize_clusters(embeddings, labels)

if __name__ == "__main__":
    main()
