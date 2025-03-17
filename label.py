import os
import pandas as pd
data=[]
hairtype=['CurlyHair','KinkyHair', 'StraightHair', 'WavyHair']
for type in hairtype:
    folder_path= f"Dataset/{type}"
    for img_name in os.listdir(folder_path):
        img_path = f"{folder_path}/{img_name}"
        data.append([img_path, type])
df = pd.DataFrame(data, columns=["Image Path", "Label"])

# Save CSV
df.to_csv("hair_dataset.csv", index=False)
