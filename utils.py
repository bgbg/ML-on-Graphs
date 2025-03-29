import os
import shutil
import urllib.request
import zipfile
import gzip

try:
    import google.colab
    from google.colab import drive
except ImportError:
    IN_COLAB = False
else:
    IN_COLAB = True


def download_and_extract_zip(
    *,
    zip_url,
    zip_filename,
    filetype,
    local_folder="./data",
    in_colab=IN_COLAB,
):
    # Determine data folder
    if in_colab:
        from google.colab import drive

        drive.mount("/content/drive")
        data_folder = "/content/drive/MyDrive/Colab Notebooks/Data"
    else:
        data_folder = os.path.abspath(local_folder)
        print("Not running in Colab. Using local folder:", data_folder)

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
        with gzip.open(zip_file_path, "rb") as f_in:
            with open(
                os.path.join(data_folder, os.path.splitext(zip_filename)[0]), "wb"
            ) as f_out:
                shutil.copyfileobj(f_in, f_out)
        print("Extraction complete.")
        extract_file = os.path.join(data_folder, os.path.splitext(zip_filename)[0])
        return extract_file

    else:
        raise ValueError(f"Unsupported file type: {filetype}")
