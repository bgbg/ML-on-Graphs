import os
import shutil
from typing import Literal
import urllib.request
import zipfile
import gzip
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

try:
    import google.colab
    from google.colab import drive
except ImportError:
    IN_COLAB = False
else:
    IN_COLAB = True


def download_and_extract_data(
    *,
    zip_url,
    zip_filename=None,
    filetype: Literal["zip", "csv.gz"],
    local_folder="./data",
    in_colab=IN_COLAB,
):
    """
    Download and extract data from a compressed file.

    Args:
        zip_url: The URL of the compressed file.
        zip_filename: The name of the compressed file. If the specified value is either None or empty string,
            the function will use the basename of the zip_url as the filename.
        filetype: The type of the file to extract ("zip" or "csv.gz").
        local_folder: The local folder to save the data.
        in_colab: Whether running in Google Colab environment.

    Returns:
        str: Path to the extracted directory if filetype is "zip",
             or path to the extracted file if filetype is "csv.gz".
    """
    if in_colab:
        from google.colab import drive

        drive.mount("/content/drive")
        data_folder = "/content/drive/MyDrive/Colab Notebooks/Data"
    else:
        data_folder = os.path.abspath(local_folder)
        print("Not running in Colab. Using local folder:", data_folder)

    if zip_filename is None or zip_filename == "":
        zip_filename = os.path.basename(zip_url)

    os.makedirs(data_folder, exist_ok=True)
    print(f"Using data folder: {data_folder}")

    # Download if necessary
    zip_file_path = os.path.join(data_folder, zip_filename)
    if not os.path.exists(zip_file_path):
        print("Downloading ZIP file...")
        urllib.request.urlretrieve(zip_url, zip_file_path)
        print("Download complete.")
    else:
        print("ZIP file already exists.")

    # Extract
    if filetype == "zip":
        with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
            zip_ref.extractall(data_folder)
            print("Extraction complete.")
            extract_dir = os.path.join(data_folder, os.path.splitext(zip_filename)[0])
            return extract_dir
    elif filetype == "csv.gz":
        output_filename = os.path.splitext(zip_filename)[0]
        extract_file = os.path.join(data_folder, output_filename)
        with gzip.open(zip_file_path, "rb") as f_in:
            with open(extract_file, "wb") as f_out:
                shutil.copyfileobj(f_in, f_out)
        print("Extraction complete.")
        return extract_file
    else:
        raise ValueError(f"Unsupported file type: {filetype}")


def get_giant_component(G: nx.Graph) -> nx.Graph:
    """
    Get the giant component of a graph.
    """
    return G.subgraph(max(nx.connected_components(G), key=len))


def print_graph_info(G: nx.Graph):
    """
    Print information about a graph.
    """
    is_directed = G.is_directed()
    is_weighted = nx.is_weighted(G)
    str_directed = "directed" if is_directed else "undirected"
    str_weighted = "weighted" if is_weighted else "unweighted"

    print(f"Graph is {str_directed} and {str_weighted}.")
    if not is_directed:
        is_connected = nx.is_connected(G)
        str_connected = "connected" if is_connected else "disconnected"
        print(f"Graph is {str_connected}.")
    print(f"Number of nodes:\t{G.number_of_nodes():7,d}")
    print(f"Number of edges:\t{G.number_of_edges():7,d}")
    print(f"Density:\t\t{nx.density(G):.3f}")


def log_log_plot(
    data,
    normalize=False,
    str_xlabel="Degree",
    str_ylabel="Count",
    str_title="Log-Log Degree Distribution",
    ax=None,
):
    if ax is None:
        ax = plt.gca()
    counts = np.bincount(data)
    x = np.nonzero(counts)[0]
    y = counts[x]
    if normalize:
        y = y / len(data)
    ax.loglog(x, y, "ok", linestyle="None")
    if normalize:
        ax.set_ylabel("Fraction")
    else:
        ax.set_ylabel("Count")
    if str_xlabel is not None:
        ax.set_xlabel(str_xlabel)
    if str_ylabel is not None:
        ax.set_ylabel(str_ylabel)
    if str_title is not None:
        ax.set_title(str_title)
    return ax
