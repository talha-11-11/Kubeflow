# Simple Kubeflow Pipeline

This repository contains a simple Kubeflow pipeline that echoes a message.

## Files

- `simple_pipeline.py`: The Python script that defines the pipeline.
- `simple_pipeline.yaml`: The compiled pipeline definition.

## How to Run

1. Install [Minikube](https://minikube.sigs.k8s.io/docs/start/) and start a Kubernetes cluster:
    ```sh
    minikube start --driver=docker
    ```

2. Install [Kubeflow](https://www.kubeflow.org/docs/started/getting-started/).

3. Install the Kubeflow Pipelines SDK:
    ```sh
    pip install kfp
    ```

4. Compile the pipeline:
    ```sh
    python simple_pipeline.py
    ```

5. Upload the `simple_pipeline.yaml` file to Kubeflow Pipelines and run it.
