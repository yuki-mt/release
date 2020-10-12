#!/bin/bash

aws ecs register-task-definition \
  --cli-input-json file://task_definition.json
