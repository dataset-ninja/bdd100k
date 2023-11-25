Dataset **BDD100K: Images 100K** can be downloaded in [Supervisely format](https://developer.supervisely.com/api-references/supervisely-annotation-json-format):

 [Download](https://assets.supervisely.com/supervisely-supervisely-assets-public/teams_storage/p/M/xa/zQBQxBPNm5FolswqMasrdBtS9QRr5UErKGOnpw3qkJD9XeaoSVdhRauF5fGqfTG2JVuooNbYCQo7gGXthj01MQ9N1zOtH1FsUOxWomDfejEyFR7GzfL9AeCAityD.tar)

As an alternative, it can be downloaded with *dataset-tools* package:
``` bash
pip install --upgrade dataset-tools
```

... using following python code:
``` python
import dataset_tools as dtools

dtools.download(dataset='BDD100K: Images 100K', dst_dir='~/dataset-ninja/')
```
Make sure not to overlook the [python code example](https://developer.supervisely.com/getting-started/python-sdk-tutorials/iterate-over-a-local-project) available on the Supervisely Developer Portal. It will give you a clear idea of how to effortlessly work with the downloaded dataset.

The data in original format can be [downloaded here](https://www.bdd100k.com/).