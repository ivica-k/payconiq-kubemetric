from dataclasses import dataclass
from typing import List


@dataclass
class Namespace:
    name: str


@dataclass
class ContainerMetric:
    name: str
    cpu: str  # https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/#meaning-of-cpu
    memory: str  # in MB


@dataclass
class Pod:
    name: str
    containers: List[ContainerMetric]
    namespace: str
