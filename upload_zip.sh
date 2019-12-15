#!/bin/bash
proj=artificer-extract-materials
aws lambda update-function-code --function-name $proj --zip-file fileb://$proj.zip

