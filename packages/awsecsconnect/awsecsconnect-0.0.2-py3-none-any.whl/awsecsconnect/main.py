import inquirer
import boto3
import subprocess


def ask(name, choices):
    q = [
        inquirer.List(
            name=name,
            message="Select {}:".format(name).title(),
            choices=choices
        )
    ]
    a = inquirer.prompt(q)[name]
    return a


def get_clusters():
    client = boto3.client('ecs')
    return client.list_clusters()['clusterArns']


def get_tasks(cluster_arn):
    client = boto3.client('ecs')
    task_arns = client.list_tasks(cluster=cluster_arn)
    if not task_arns['taskArns']:
        return

    task_descriptions = client.describe_tasks(cluster=cluster_arn, tasks=task_arns['taskArns'])
    tasks = task_descriptions['tasks']
    task_choices = []
    for task in tasks:
        arn = task['taskArn']
        started = task['startedAt']
        container_count = len(task['containers'])
        task_choices.append(("{} ({}): {} Containers".format(arn, started, container_count), arn))
    return task_choices

def get_containers(cluster_arn, task_arn):
    client = boto3.client('ecs')
    task = client.describe_tasks(cluster=cluster_arn, tasks=[task_arn])['tasks'][0]
    container_choices = []
    for container in task['containers']:
        container_choices.append(container['name'])
    return container_choices


def main():
    clusters = get_clusters()
    if not clusters:
        print("No ECS Clusters. Set Profile and Log In.")
        return
    cluster_arn = ask('cluster', clusters)

    tasks = get_tasks(cluster_arn)
    task_arn = ask('task', tasks)

    containers = get_containers(cluster_arn, task_arn)
    container = ask('container', containers)

    subprocess.run('aws ecs execute-command '
                   '--cluster {} '
                   '--task {} '
                   '--container {} '
                   '--command "/bin/bash" '
                   '--interactive'.format(cluster_arn, task_arn, container), shell=True)


if __name__ == "__main__":
    main()
