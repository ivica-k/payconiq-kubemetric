#!/usr/bin/env python3
import os

from data_layer import get_namespaces, get_pods_in_namespace


def cls():
    os.system("cls" if os.name == "nt" else "clear")


namespaces = get_namespaces()

cls()
print("Available namespaces:\n")
print(f"{'Name' : <50}")
print("-" * 50)

for ns in namespaces:
    print(f"{ns.name : <50}")

input("\nUser chooses the 'dev' namespace. Press Enter key to continue")
cls()

pods = get_pods_in_namespace("dev")

print("Available pods:\n")
print(f"{'Name' : <30}{'Namespace' : ^15}{'Number of containers' : >10}")
print("-" * 80)

for pod in pods:
    print(f"{pod.name : <30}{pod.namespace : ^15}{len(pod.containers) : >20}")

input("\nUser chooses the 'web-84fb9498c7-cxxnp' pod. Press Enter key to continue")
cls()

chosen_pod = [pod for pod in pods if pod.name == "web-84fb9498c7-cxxnp"][0]

print(f"Metrics for pod '{chosen_pod.name}':\n")
print(f"{'Container name' : <30}{'CPU' : >20}{'Memory (MB)' : >20}")
print("-" * 90)

for cnt in chosen_pod.containers:
    print(f"{cnt.name : <30}{cnt.cpu : >20}{cnt.memory : >20}")
