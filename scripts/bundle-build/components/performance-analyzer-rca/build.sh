#!/bin/bash

./gradlew build -x test
./gradlew publishToMavenLocal
