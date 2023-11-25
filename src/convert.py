# https://bdd-data.berkeley.edu/


import csv
import os
import shutil
from collections import defaultdict
from urllib.parse import unquote, urlparse

import supervisely as sly
from dotenv import load_dotenv
from supervisely.io.fs import get_file_name, get_file_name_with_ext, get_file_size
from supervisely.io.json import load_json_file
from tqdm import tqdm

import src.settings as s
from dataset_tools.convert import unpack_if_archive


def download_dataset(teamfiles_dir: str) -> str:
    """Use it for large datasets to convert them on the instance"""
    api = sly.Api.from_env()
    team_id = sly.env.team_id()
    storage_dir = sly.app.get_data_dir()

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, str):
        parsed_url = urlparse(s.DOWNLOAD_ORIGINAL_URL)
        file_name_with_ext = os.path.basename(parsed_url.path)
        file_name_with_ext = unquote(file_name_with_ext)

        sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
        local_path = os.path.join(storage_dir, file_name_with_ext)
        teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

        fsize = api.file.get_directory_size(team_id, teamfiles_dir)
        with tqdm(
            desc=f"Downloading '{file_name_with_ext}' to buffer...",
            total=fsize,
            unit="B",
            unit_scale=True,
        ) as pbar:
            api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)
        dataset_path = unpack_if_archive(local_path)

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, dict):
        for file_name_with_ext, url in s.DOWNLOAD_ORIGINAL_URL.items():
            local_path = os.path.join(storage_dir, file_name_with_ext)
            teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

            if not os.path.exists(get_file_name(local_path)):
                fsize = api.file.get_directory_size(team_id, teamfiles_dir)
                with tqdm(
                    desc=f"Downloading '{file_name_with_ext}' to buffer...",
                    total=fsize,
                    unit="B",
                    unit_scale=True,
                ) as pbar:
                    api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)

                sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
                unpack_if_archive(local_path)
            else:
                sly.logger.info(
                    f"Archive '{file_name_with_ext}' was already unpacked to '{os.path.join(storage_dir, get_file_name(file_name_with_ext))}'. Skipping..."
                )

        dataset_path = storage_dir
    return dataset_path


def count_files(path, extension):
    count = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(extension):
                count += 1
    return count


def convert_and_upload_supervisely_project(
    api: sly.Api, workspace_id: int, project_name: str
) -> sly.ProjectInfo:
    # project_name = "BDD100K 100k images"
    train_images_path = "/mnt/d/datasetninja-raw/bdd100k/bdd100k/images/100k/train"
    val_images_path = "/mnt/d/datasetninja-raw/bdd100k/bdd100k/images/100k/val"
    test_images_path = "/mnt/d/datasetninja-raw/bdd100k/bdd100k/images/100k/test"
    train_bboxes_path = (
        "/mnt/d/datasetninja-raw/bdd100k/bdd100k/labels/bdd100k_labels_images_train.json"
    )
    val_bboxes_path = (
        "/mnt/d/datasetninja-raw/bdd100k/bdd100k/labels/bdd100k_labels_images_val.json"
    )
    batch_size = 30

    ds_name_to_data = {
        "val": (val_images_path, val_bboxes_path),
        "train": (train_images_path, train_bboxes_path),
        "test": (test_images_path, None),
    }

    def create_ann(image_path):
        labels = []
        tags = []

        image_np = sly.imaging.image.read(image_path)[:, :, 0]
        img_height = image_np.shape[0]
        img_wight = image_np.shape[1]

        file_name = get_file_name_with_ext(image_path)

        attributes = name_to_attributes.get(file_name)
        if attributes is not None:
            weather_value = attributes.get("weather")
            weather = sly.Tag(weather_meta, value=weather_value)
            scene_value = attributes.get("scene")
            scene = sly.Tag(scene_meta, value=scene_value)
            timeofday_value = attributes.get("timeofday")
            timeofday = sly.Tag(timeofday_meta, value=timeofday_value)
            tags.extend([weather, scene, timeofday])

        data = name_to_data.get(file_name)
        if data is not None:
            for curr_data in data:
                obj_class = meta.get_obj_class(curr_data[0])
                info_value = str(curr_data[1])
                info = sly.Tag(info_meta, value=info_value)
                coords = curr_data[2]
                if type(coords) is dict:
                    left = int(coords["x1"])
                    top = int(coords["y1"])
                    right = int(coords["x2"])
                    bottom = int(coords["y2"])
                    rect = sly.Rectangle(left=left, top=top, right=right, bottom=bottom)
                    label = sly.Label(rect, obj_class, tags=[info])
                    labels.append(label)
                else:
                    for curr_coords in coords:
                        polygons_coords = curr_coords["vertices"]
                        exterior = []
                        for coords in polygons_coords:
                            for i in range(0, len(coords), 2):
                                exterior.append([int(coords[i + 1]), int(coords[i])])
                        if len(exterior) > 3:
                            figure = sly.Polygon(exterior)
                        else:
                            figure = sly.Polyline(exterior)

                        label_poly = sly.Label(figure, obj_class, tags=[info])
                        labels.append(label_poly)

        return sly.Annotation(img_size=(img_height, img_wight), labels=labels, img_tags=tags)

    classes_names = [
        "car",
        "bus",
        "drivable area",
        "lane",
        "traffic sign",
        "truck",
        "person",
        "traffic light",
        "rider",
        "bike",
        "motor",
        "train",
    ]  # get from train, val json(check all classes)

    weather_meta = sly.TagMeta("weather", sly.TagValueType.ANY_STRING)
    scene_meta = sly.TagMeta("scene", sly.TagValueType.ANY_STRING)
    timeofday_meta = sly.TagMeta("timeofday", sly.TagValueType.ANY_STRING)
    info_meta = sly.TagMeta("attributes", sly.TagValueType.ANY_STRING)

    meta = sly.ProjectMeta(tag_metas=[weather_meta, scene_meta, timeofday_meta, info_meta])
    for class_name in classes_names:
        obj_class = sly.ObjClass(class_name, sly.AnyGeometry)
        meta = meta.add_obj_class(obj_class)

    project = api.project.create(workspace_id, project_name, change_name_if_conflict=True)

    api.project.update_meta(project.id, meta.to_json())

    for ds_name, ds_data in ds_name_to_data.items():
        dataset = api.dataset.create(project.id, ds_name, change_name_if_conflict=True)

        images_path, bboxes_path = ds_data

        name_to_data = defaultdict(list)
        name_to_attributes = {}

        if bboxes_path is not None:
            ann_data = load_json_file(bboxes_path)
            for curr_ann_data in ann_data:
                name_to_attributes[curr_ann_data["name"]] = curr_ann_data["attributes"]
                for curr_label in curr_ann_data["labels"]:
                    curr_data = []
                    curr_data.append(curr_label["category"])
                    curr_data.append(curr_label["attributes"])
                    coords = curr_label.get("box2d")
                    if coords is None:
                        coords = curr_label.get("poly2d")
                    curr_data.append(coords)
                    name_to_data[curr_ann_data["name"]].append(curr_data)

        images_names = os.listdir(images_path)

        progress = sly.Progress("Create dataset {}".format(ds_name), len(images_names))

        for images_names_batch in sly.batched(images_names, batch_size=batch_size):
            images_pathes_batch = [
                os.path.join(images_path, im_name) for im_name in images_names_batch
            ]

            img_infos = api.image.upload_paths(dataset.id, images_names_batch, images_pathes_batch)
            img_ids = [im_info.id for im_info in img_infos]

            if bboxes_path is not None:
                anns = [create_ann(image_path) for image_path in images_pathes_batch]
                api.annotation.upload_anns(img_ids, anns)

            progress.iters_done_report(len(images_names_batch))
    return project
