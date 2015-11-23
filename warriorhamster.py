#!/usr/bin/env python
import argparse
from taskw import TaskWarrior
import subprocess

def main(task_id, action):
    w = TaskWarrior()
    # First, make sure that the task id is valid.

    if action == 'start':
        task = w.get_task(id=task_id)
        if task[0] is None:
            print "Invalid task ID."
            return
        task = task[1]
        print task

        name = task['description'].replace(",","") # get rid of commas 
        name = "%s %s" % (task_id, name) # store task_id in the name so we can find it again later when we want to mark a task as 'done'...
        category = ""
        if 'tags' in task: # preserve tags from TaskWarrior
            name = "%s, %s " % (name, " ".join(task['tags']))

        if 'project' in task: # if there is a project assigned in TW, make it a Project Hamster category
            name = "%s@%s" % (name, task['project'])

        subprocess.check_output(['hamster', action, name])

        return

    if action == 'done':
        if task_id == 0:
            cur_hamster = subprocess.check_output(['hamster', 'current']).strip().split()
            task_id = int(cur_hamster[2])

        subprocess.check_output(['hamster', 'stop'])
        w.task_done(id=task_id)
        return


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('task_id', help="TaskWarrior task id. Enter '0' to stop current Hamster task.", type=int) 
    parser.add_argument('action', choices=['start', 'done'], help="'start' begins the task. 'done' stops the task and marks it as complete in TaskWarrior.") #  'stop' stops the task, but does not mark it as being completed. '   
    args = parser.parse_args()

    main(args.task_id, args.action)
