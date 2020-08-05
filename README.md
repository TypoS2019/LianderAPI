# Python REST API Skeleton

## Quickstart
- Install Python dependencies with: `pip install -r requirements.txt`
- Start the API: `python -m app.main`

## Introduction
The Python API Skeleton provides an easy to use project structure - and a library with useful functionality - to quickly build REST APIs.
It comes with the necessary files to quickly deploy your project to the Forza [Kubernetes](https://kubernetes.io/docs/home/) platform, or the [OpenShift](https://docs.openshift.com/) platform in the Alliander data center.

Several [cookiecutter](https://cookiecutter.rea
dthedocs.io/en/latest/) templates are generated from this project, to allow for teams to quickly customize the API Skeleton to their project.

## Templates and repos
The templates, in Cookiecutter format, can be found here:
- *removed from file* 

The master project, used to generate the templates, is located here:
- *removed from file*

## Structure
The API Skeleton is composed of the following files and folders:

```
.
├── app
|   ├── core                        (API Skeleton library)
|   ├── routers                     (API endpoints and their implementation)
|   |   └── {router_name}           (Collection of endpoints)
|   |   |   ├── api_models.py       (Defines request and response formats)
|   |   |   ├── api_view_v1.py      (Defines API endpoints. Uses controller.py to handle the actual (business) logic.)
|   |   |   ├── controller.py       (Defines the (business) logic of the API. Uses repository.py to handle data.)
|   |   |   └── repository.py       (Exposes read and write access to datasets, external APIs and databases.)
|   ├── versions                    (Define API versions)
|   └── main.py                     (Entrypoint of the aplication)
├── bin                             (additional scripts)
├── data                            included data. Tip: only include some small data samples)
├── docker_deps                     (additional files needed to construct the Docker images, for some templates)
├── docs                            (documentation)
├── k8s                             (files for deployment to the Forza platform)
|   ├── {namespace}-{env}           (Kubernetes configuration per Forza namespace and environment)
|   |   └── ingress.template.yaml   (Kubernetes Ingress configuration. Controls URLs, certificates, authentication, and so on.)
|   ├── deployment.template.yaml    (Kubernetes Deployment configuration. Also contains details on the pod to create.)
|   └── service.template.yaml       (Kubernetes Service configuration. Abstraction to expose pods as a service.)
├── tests                           (unit tests)
├── .dockerignore                   (Docker ignore file, speeds up the creation of images by excluding data which isn't required)
├── .gitignore                      (Git ignore file)
├── app_config(.sample).py          (API configuration)
├── Dockerfile                      (Definition of Docker image)
├── Jenkinsfile                     Jenkinsfile for the Forza platform)
├── Jenkinsfile.OpenShift           (Jenkinsfile for OpenShift in the Alliander DC)
├── README.md                       (This readme)
├── requirements.txt                (Required Python packages. Can be installed using e.g. `pip install -r requirements.txt`
└── setup.py                        (File to create a package of the API. Not necessary in most cases.)
```

### app.core
Core functionality and helper function of the API Skeleton. Provides additions to FastAPI and adds Alliander specific functionality.

This package will be turned into a stand-alone Python package, once a central Alliander PyPI mirror has been setup.

### app.routers
The routers contain the actual logic of your API.
These contain the API endpoints (_api_view_v1.py_), business logic (_controller.py_), code to e.g. access databases or call external APIs (_repository.py_), and optionally some DTOs (_api_models.py_).

Each router is commonly used to handle a group of related API endpoints. For instance, one router could expose weather predictions, while another router only deals with measured weather factors.
You can structure your API by creating one or multiple routers. For most applications, a single router suffices.

### app.version
Most APIs aren't static. They are changed over time, with endpoints being updated, added, or removed. This package helps you to define and maintain multiple API versions.
Each version is described in a model, as a composition of router views, tied to a specific endpoint URL. The example model is quite self explanatory.

### k8s
In order to make it easy to deploy APIs built using the skeleton to Forza / DICE, a basic Kubernetes configuration is provided.
For each DTAP environment a folder should be created to hold the environment specific configurations. 

### app_config.py
The application config file contains all configuration parameters of your API. You can set these in the file manually, or override
the defaults using environment variables. These can be defined in e.g. the Dockerfile, the Kubernetes config, or loaded from
Kubernetes ConfigMaps or secrets.

### Dockerfile
On Forza / DICE and the OpenShift platform in the Alliander DC, your API needs to run within a Docker container.
This file describes how to build the Docker image used to create these containers. Please check-out the [Docker documentation](https://docs.docker.com/get-started/)
if you want to learn more about this file.

### Jenkinsfile
This file describes the steps that need to be taken to deploy the app on Forza or OpenShift in DC.
