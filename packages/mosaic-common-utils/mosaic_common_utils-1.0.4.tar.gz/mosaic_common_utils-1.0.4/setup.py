# -*- coding: utf-8 -*-
from setuptools import find_packages, setup

extras_require = {
    "flavours": [
        "keras==2.2.4",
        "pyspark==2.4.6",
        "sklearn==0.0",
        "tensorflow==2.4.1",
        "tensorflow-probability==0.11.1",
        "torch==1.2.0",
        "torchvision==0.4.0",
        # changing the spacy version as 2.2.1 giving segmentation faults
        "spacy==2.2.2",
        # installing the scikit-learn version 0.21.3 since 0.22 is not stable
        "scikit-learn==0.21.3",
    ],
    "common": [
        "cloudpickle==1.2.2",
        "minio==4.0.18",
        "GitPython==3.1.30",
        "gitdb2==2.0.6",
        "ipython>=7.11.1",
    ],
    "empty": [
        "ipython>=7.11.1",
    ],

    "nb-template-serving": [
        "cloudpickle==1.2.2",
        # "minio==4.0.18",
        # "GitPython==3.0.4",
        # "gitdb2==2.0.6",
        # "ipython>=7.11.1",
        "PyYAML",
        # installing the scikit-learn version 0.21.3 since 0.22 is not stable
        ## Vulnerability fixes
        # "scikit-learn==0.24.0",
    ],
    "metrics": [
        "numpy>=1.16.5",
        "requests==2.22.0",
        "pandas==1.0.4",
        "sklearn==0.0",
        "PyYAML",
        # installing the scikit-learn version 0.21.3 since 0.22 is not stable
        "scikit-learn==0.21.3",
        "ipython>=7.11.1",
    ],
    "k8": [
        "kubernetes==9.0.0",
        "numpy>=1.16.5",
        "pandas==1.0.4",
        "sklearn==0.0",
        "scikit-learn==0.21.3",
    ],
    "mosaicautoml": [
        "numpy>=1.16.5",
        "pandas==1.0.4",
        "sklearn==0.0",
        "category-encoders==2.2.2",
        "nltk==3.5",
        "bs4==0.0.1",
    ],
    "r-jupyter": [
        "torch==1.8.0",
        "torchvision==0.8.0",
        "PyYAML",
        "scikit-learn==0.21.3"
    ],
    "most_common": [
        "ipython>=7.11.1",
        "alembic==1.0.11",
        "celery==5.2.2",
        "flasgger==0.9.4",
        "flask==2.2.5",
        "flask-migrate==3.1.0",
        "flask-cors==3.0.10",
        "gunicorn>20.0.0",
        "kubernetes==24.2.0",
        "marshmallow==2.19.5",
        "pyjwt==2.4.0",
        "requests-toolbelt==1.0.0",
        "sqlalchemy==1.3.22",
        "Cython==0.29.15",
        "Flask-SQLAlchemy==2.5.1",
        "Jinja2==3.0.3",
        "Werkzeug==2.2.3",
        "importlib-metadata==4.12.0",
        "pytest==7.0.0",
        "pytest-cov",
        "importanize==0.7.0",
        "PyYAML",
        "requests==2.26.0",
        "psycopg2-binary",
    ],

}

extras_require["complete"] = sorted(set(sum(extras_require.values(), [])))

extras_require["pmml"] = sorted(
    set([pack for pack in extras_require["complete"] if pack != "pyspark==2.4.6"])
)

extras_require["nb_api"] = sorted(
    set(extras_require["k8"] + ["GitPython==3.1.30","gitdb2==2.0.6"])
)

extras_require["pmml"].append("pypmml==0.9.5")

extras_require["rstudio"] = sorted(
    set([pack for pack in extras_require["complete"] if pack not in [
        "tensorflow==1.14.0",
        "tensorflow==2.4.1",
        "tensorflow-probability==0.11.1",
        "torch==1.2.0",
        "torchvision==0.4.0",
        "pandas==1.0.4"]])
)

not_require = [
    "keras==2.2.4",
    "pyspark==2.4.6",
    "tensorflow==2.4.1",
    "tensorflow==1.14.0",
    "tensorflow-probability==0.11.1",
    "torch==1.2.0",
    "torch==1.8.0",
    "torchvision==0.4.0",
    "torchvision==0.8.0",
    "spacy==2.2.2",
    "sklearn==0.0",
    "scikit-learn==0.21.3",
]


def make_lite(ele):
    return sorted(set(extras_require[ele]) - set(not_require))


extras_require["pmml_lite"] = make_lite("pmml")
extras_require["rstudio_lite"] = make_lite("rstudio")
extras_require["complete_lite"] = make_lite("complete")
extras_require["flavours_lite"] = make_lite("flavours")
extras_require["metrics_lite"] = make_lite("metrics")
extras_require["mosaicautoml_lite"] = make_lite("mosaicautoml")
extras_require["r-jupyter_lite"] = make_lite("r-jupyter")


setup(
    name="mosaic-common-utils",
    version="1.0.4",
    description="Utils library for Mosaic",
    url="https://git.lti-aiq.in/mosaic-ai-logistics/mosaic-common-utils",
    author="Rushikesh Raut",
    author_email="rushikesh.raut@lntinfotech.com",
    classifiers=["Programming Language :: Python :: 3.6"],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    extras_require=extras_require,
    )
