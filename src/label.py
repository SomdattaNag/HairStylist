import os
import pandas as pd

data = []
hairtype = ['CurlyHair', 'KinkyHair', 'StraightHair', 'WavyHair']

if __name__ == "__main__":
    for type in hairtype:
        folder_path = os.path.join("Dataset", type)
        for img_name in os.listdir(folder_path):
            img_path = os.path.join(folder_path, img_name)
            data.append([img_path, type])

    df = pd.DataFrame(data, columns=["Image Path", "Label"])

    #save as csv
    output_dir = "csv_datasets"
    os.makedirs(output_dir, exist_ok=True)
    df.to_csv(os.path.join(output_dir, "hair_dataset.csv"), index=False)

