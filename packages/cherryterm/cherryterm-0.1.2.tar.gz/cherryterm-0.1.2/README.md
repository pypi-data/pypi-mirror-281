CherryTerm is a simple CLI tool for managing terminal recordings using `asciinema`.

# to publish package

```bash
$ docker build -t cherryterm .
```

```bash
$ docker run -it --rm -v $(pwd):/app cherryterm
```

Inside docker

```bash
$ rm -rf dist 
$ python setup.py sdist bdist_wheel
$ twine upload dist/* 
```

