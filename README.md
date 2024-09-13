# GRNDP-server

The backend of Gene Regulatory Network Design Platform (GRNDP).

Licensed under BSD 3-Clause License. The licence text can be found in file [LICENSE](./LICENSE).

## Dependencies

### Installing dependencies

It is recommended to install the depended packages through conda:

```
conda install --file src/requirements.txt
```

Packages of other versions might also work, but without guarantee.

### Runtime dependencies

Following python packages are required for running:

- python: 3.10.6
- scipy: 1.9.1
- matplotlib-base: 3.5.2
- uvicorn: 0.20.0
- fastapi: 0.112.2
- pydantic: 2.8.2

## Running

### Using the Uvicorn server

Launching the uvicorn server:

```
cd src
uvicorn main:app
```

The application can be then accessed via [127.0.0.1](http://127.0.0.1).
