import os
import pandas as pd
data=[]
hairtype=['CurlyHair','KinkyHair', 'StraightHair', 'WavyHair']

if __name__=="__main__":
    for type in hairtype:
        folder_path= f"../Dataset/{type}"
        for img_name in os.listdir(folder_path):
            img_path = f"{folder_path}/{img_name}"
            data.append([img_path, type])
    df = pd.DataFrame(data, columns=["Image Path", "Label"])

    #saved as csv
    output_dir = "../csv_datasets"
    os.makedirs(output_dir,exist_ok=True)
    df.to_csv(f"{output_dir}/hair_dataset.csv", index=False)
