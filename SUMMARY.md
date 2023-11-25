**BDD100K: A Diverse Driving Dataset for Heterogeneous Multitask Learning (Images 100K)** is a dataset for instance segmentation, semantic segmentation, object detection, and identification tasks. It is used in the automotive industry. 

The dataset consists of 100000 images with 2221128 labeled objects belonging to 12 different classes including *car*, *drivable area*, *lane*, and other: *traffic sign*, *traffic light*, *person*, *truck*, *bus*, *bike*, *rider*, *motor*, and *train*.

Images in the BDD100K: Images 100K dataset have pixel-level instance segmentation annotations. Due to the nature of the instance segmentation task, it can be automatically transformed into a semantic segmentation (only one mask for every class) or object detection (bounding boxes for every object) tasks. There are 20137 (20% of the total) unlabeled images (i.e. without annotations). There are 3 splits in the dataset: *train* (70000 images), *test* (20000 images), and *val* (10000 images). Additionally, every image contains tags with ***weather***, ***scene*** and ***timeofday***, while objects contain dictionary with useful meta-information about their ***attributes*** (area type, occlusion, truncation, etc.). The dataset was released in 2020 by the UC Berkeley, USA, Cornell University, USA, UC San Diego, USA, and Element, Inc.

Here is the visualized example grid with animated annotations:

[animated grid](https://github.com/dataset-ninja/bdd100k/raw/main/visualizations/horizontal_grid.webm)
