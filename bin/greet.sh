#!/bin/bash

function greet () {

  echo Hello ${salutation}.${name}! This is the ${lang} world!
}


for ARGUMENT in "$@"
do
    KEY=$(echo $ARGUMENT | cut -f1 -d=)
    VALUE=$(echo $ARGUMENT | cut -f2 -d=)
    case "$KEY" in
            salutation)         salutation=${VALUE};;
            name)               name=${VALUE};;
            lang)               lang=${VALUE};;
            *)
    esac
done

greet
