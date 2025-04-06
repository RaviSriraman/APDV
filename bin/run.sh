#!/bin/bash

dagster-webserver -h 0.0.0.0 -p 3000 &
dagster-daemon run &