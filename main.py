import define_params
import feature_extraction
import csv
import os
import numpy as np
def main():
    database_paths = define_params.database_paths

    with open(database_paths, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        image_paths = [path[0] for path in reader]
    # print(image_paths)
    outputs = feature_extraction.feature_extraction(image_paths)

    
    # 保存
    os.makedirs("./result", exist_ok=True)
    with open("./result/features.csv", "w", newline="") as f:
        writer = csv.writer(f)
        for out in outputs:
            writer.writerow(out) 
            
    # x = np.loadtxt("./result/features.csv", delimiter=',',dtype="float32")
    # dbscanで分類
    # 2枚以上ならpathを検索して分類


if __name__ == "__main__":
    main()