#!/bin/bash

if [ "$(uname)" == "Darwin" ]
then
    export CXXFLAGS="-stdlib=libc++ ${CXXFLAGS}"
    export LDFLAGS="-Wl,-rpath,$PREFIX/lib"
fi

pip install --no-binary :all: -r "${RECIPE_DIR}/component-requirements.txt"

$PYTHON setup.py install --prefix=$PREFIX
