from models import Namespace, Pod, ContainerMetric

from kubernetes import client, config
from kubernetes.client.exceptions import ApiException

config.load_kube_config()

api = client.CustomObjectsApi()
v1 = client.CoreV1Api()

from typing import List


def memory_to_megabytes(kibibytes: str) -> str:
    """
    Converts kibibytes to megabytes
    :param kibibytes:
    :return:
    """
    kib = int(kibibytes.lower().replace("ki", ""))

    return f"{round(kib * 1024 / 1000 ** 2, 1)}MB"


def get_namespaces() -> List[Namespace]:
    """
    Returns a list of namespaces, excluding system-reserved namespaces.
    :return:
    """
    namespaces = []

    try:

        for elem in v1.list_namespace().items:
            if not elem.metadata.name.startswith("kube-"):
                namespaces.append(Namespace(name=elem.metadata.name))

        return namespaces

    except ApiException as exc:
        print(f"Unable to fetch namespaces: {exc}")

        return []

    except Exception as exc:
        exit(exc)


def _parse_containers(containers: List) -> List[ContainerMetric]:
    """
    Returns a list of ContainerMetric objects
    :param containers:
    :return:
    """
    ret_containers = []

    for cnt in containers:
        ret_containers.append(
            ContainerMetric(
                name=cnt.get("name"),
                memory=memory_to_megabytes(cnt.get("usage").get("memory")),
                cpu=cnt.get("usage").get("cpu"),
            )
        )

    return ret_containers


def get_pods_in_namespace(namespace: str) -> List[Pod]:
    """
    Returns a list of Pod objects available in a specific namespace
    :param namespace:
    :return:
    """
    namespace = namespace.lower().strip()
    pods = []

    try:
        for elem in api.list_namespaced_custom_object(
            group="metrics.k8s.io",
            version="v1beta1",
            namespace=namespace,
            plural="pods",
        ).get("items"):
            name = elem.get("metadata").get("name")

            pods.append(
                Pod(
                    namespace=namespace,
                    name=name,
                    containers=_parse_containers(elem.get("containers")),
                )
            )

        return pods

    except ApiException as apiexc:
        print(f"Unable to fetch pod metrics: {apiexc}")

    except Exception as exc:
        exit(exc)
