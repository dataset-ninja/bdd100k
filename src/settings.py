from typing import Dict, List, Optional, Union

from dataset_tools.templates import (
    AnnotationType,
    Category,
    CVTask,
    Domain,
    Industry,
    License,
    Research,
)

##################################
# * Before uploading to instance #
##################################
PROJECT_NAME: str = "BDD100K: Images 100K"
PROJECT_NAME_FULL: str = "Berkeley Deep Drive Dataset (BDD100K): A Diverse Driving Dataset for Heterogeneous Multitask Learning (Images 100K)"
HIDE_DATASET = False  # set False when 100% sure about repo quality

##################################
# * After uploading to instance ##
##################################
LICENSE: License = License.Custom(source_url="https://doc.bdd100k.com/license.html")
APPLICATIONS: List[Union[Industry, Domain, Research]] = [Industry.Automotive()]
CATEGORY: Category = Category.SelfDriving(benchmark=True)

CV_TASKS: List[CVTask] = [
    CVTask.InstanceSegmentation(),
    CVTask.SemanticSegmentation(),
    CVTask.ObjectDetection(),
    CVTask.Identification(),
]
ANNOTATION_TYPES: List[AnnotationType] = [AnnotationType.InstanceSegmentation()]

RELEASE_DATE: Optional[str] = None  # e.g. "YYYY-MM-DD"
if RELEASE_DATE is None:
    RELEASE_YEAR: int = 2020

HOMEPAGE_URL: str = "https://www.bdd100k.com/"
# e.g. "https://some.com/dataset/homepage"

PREVIEW_IMAGE_ID: int = 9061624
# This should be filled AFTER uploading images to instance, just ID of any image.

GITHUB_URL: str = "https://github.com/dataset-ninja/bdd100k"
# URL to GitHub repo on dataset ninja (e.g. "https://github.com/dataset-ninja/some-dataset")

##################################
### * Optional after uploading ###
##################################
DOWNLOAD_ORIGINAL_URL: Optional[Union[str, dict]] = "https://www.bdd100k.com/"
# Optional link for downloading original dataset (e.g. "https://some.com/dataset/download")

CLASS2COLOR: Optional[Dict[str, List[str]]] = {
    "car": [230, 25, 75],
    "drivable area": [60, 180, 75],
    "lane": [255, 225, 25],
    "traffic sign": [0, 130, 200],
    "traffic light": [245, 130, 48],
    "person": [145, 30, 180],
    "truck": [70, 240, 240],
    "bus": [240, 50, 230],
    "bike": [210, 245, 60],
    "rider": [250, 190, 212],
    "motor": [0, 128, 128],
    "train": [220, 190, 255],
}
# If specific colors for classes are needed, fill this dict (e.g. {"class1": [255, 0, 0], "class2": [0, 255, 0]})

# If you have more than the one paper, put the most relatable link as the first element of the list
# Use dict key to specify name for a button
PAPER: Optional[Union[str, List[str], Dict[str, str]]] = "https://arxiv.org/abs/1805.04687"
BLOGPOST: Optional[Union[str, List[str], Dict[str, str]]] = None
REPOSITORY: Optional[Union[str, List[str], Dict[str, str]]] = {
    "GitHub": "https://github.com/bdd100k/bdd100k"
}

CITATION_URL: Optional[str] = None
AUTHORS: Optional[List[str]] = [
    "Fisher Yu",
    "Haofeng Chen",
    "Xin Wang",
    "Wenqi Xian",
    "Yingying Chen",
    "Fangchen Liu",
    "Vashisht Madhavan",
    "Trevor Darrell",
]
AUTHORS_CONTACTS: Optional[List[str]] = ["i@yf.io"]

ORGANIZATION_NAME: Optional[Union[str, List[str]]] = [
    "UC Berkeley, USA",
    "Cornell University, USA",
    "UC San Diego, USA",
    "Element, Inc",
]
ORGANIZATION_URL: Optional[Union[str, List[str]]] = [
    "https://www.berkeley.edu/",
    "https://www.cornell.edu/",
    "https://ucsd.edu/",
    "https://www.elementresearch.com/",
]

# Set '__PRETEXT__' or '__POSTTEXT__' as a key with string value to add custom text. e.g. SLYTAGSPLIT = {'__POSTTEXT__':'some text}
SLYTAGSPLIT: Optional[Dict[str, Union[List[str], str]]] = {
    "__PRETEXT__": "Additionally, every image contains tags with ***weather***, ***scene*** and ***timeofday***, while objects contain dictionary with useful meta-information about their ***attributes*** (area type, occlusion, truncation, etc.)"
}
TAGS: Optional[List[str]] = None


SECTION_EXPLORE_CUSTOM_DATASETS: Optional[List[str]] = None

##################################
###### ? Checks. Do not edit #####
##################################


def check_names():
    fields_before_upload = [PROJECT_NAME]  # PROJECT_NAME_FULL
    if any([field is None for field in fields_before_upload]):
        raise ValueError("Please fill all fields in settings.py before uploading to instance.")


def get_settings():
    if RELEASE_DATE is not None:
        global RELEASE_YEAR
        RELEASE_YEAR = int(RELEASE_DATE.split("-")[0])

    settings = {
        "project_name": PROJECT_NAME,
        "project_name_full": PROJECT_NAME_FULL or PROJECT_NAME,
        "hide_dataset": HIDE_DATASET,
        "license": LICENSE,
        "applications": APPLICATIONS,
        "category": CATEGORY,
        "cv_tasks": CV_TASKS,
        "annotation_types": ANNOTATION_TYPES,
        "release_year": RELEASE_YEAR,
        "homepage_url": HOMEPAGE_URL,
        "preview_image_id": PREVIEW_IMAGE_ID,
        "github_url": GITHUB_URL,
    }

    if any([field is None for field in settings.values()]):
        raise ValueError("Please fill all fields in settings.py after uploading to instance.")

    settings["release_date"] = RELEASE_DATE
    settings["download_original_url"] = DOWNLOAD_ORIGINAL_URL
    settings["class2color"] = CLASS2COLOR
    settings["paper"] = PAPER
    settings["blog"] = BLOGPOST
    settings["repository"] = REPOSITORY
    settings["citation_url"] = CITATION_URL
    settings["authors"] = AUTHORS
    settings["authors_contacts"] = AUTHORS_CONTACTS
    settings["organization_name"] = ORGANIZATION_NAME
    settings["organization_url"] = ORGANIZATION_URL
    settings["slytagsplit"] = SLYTAGSPLIT
    settings["tags"] = TAGS

    settings["explore_datasets"] = SECTION_EXPLORE_CUSTOM_DATASETS

    return settings
