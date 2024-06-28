# Making a new release of jupyterlab-elice-theme

The extension can be published to `PyPI` and `npm` manually or using the [Jupyter Releaser](https://github.com/jupyter-server/jupyter_releaser).

## Manual release

### Recommended Dependencies

- nodejs v20.12.1
- python 3.7.17

### Python package

This extension can be distributed as Python
packages. All of the Python
packaging instructions in the `pyproject.toml` file to wrap your extension in a
Python package. Before generating a package, we first need to install `build`.

```bash
pip install build twine hatch
```

Bump the version using `hatch`. By default this will create a tag.
See the docs on [hatch-nodejs-version](https://github.com/agoose77/hatch-nodejs-version#semver) for details.

```bash
hatch version <new-version>
```

To create a Python source package (`.tar.gz`) and the binary package (`.whl`) in the `dist/` directory, do:

```bash
python -m build
```

> `python setup.py sdist bdist_wheel` is deprecated and will not work for this package.

Then to upload the package to PyPI, do:

```bash
twine upload dist/*
```

### NPM package

To publish the frontend part of the extension as a NPM package, do:

```bash
npm login
npm publish --access public
```

## Automated releases with the Jupyter Releaser

The extension repository should already be compatible with the Jupyter Releaser.

Check out the [workflow documentation](https://github.com/jupyter-server/jupyter_releaser#typical-workflow) for more information.

Here is a summary of the steps to cut a new release:

- Fork the [`jupyter-releaser` repo](https://github.com/jupyter-server/jupyter_releaser)
- Add `ADMIN_GITHUB_TOKEN`, `PYPI_TOKEN` and `NPM_TOKEN` to the Github Secrets in the fork
- Go to the Actions panel
- Run the "Draft Changelog" workflow
- Merge the Changelog PR
- Run the "Draft Release" workflow
- Run the "Publish Release" workflow

## Publishing to `conda-forge`

If the package is not on conda forge yet, check the documentation to learn how to add it: https://conda-forge.org/docs/maintainer/adding_pkgs.html

Otherwise a bot should pick up the new version publish to PyPI, and open a new PR on the feedstock repository automatically.

## Release guide

> last update at 2024-06-28

### pypi

you should need pypi account for release jupyterlab-elice-theme.  
and set api token in your local `~/.pypirc`

```conf
[pypi]
  username = __token__
  password = pypi-{{some 174 length string with no special character}}
```

### Simple workflow

```shell
nvm use 20
# install nodejs dependencies
yarn

python3 --version # 3.7.x
# you can use alternatives like pyenv
python3 -m venv venv
source ./venv/bin/activate
# install python dependencies
pip3 install build twine hatch
# set release version. this command update package.json
hatch version <new-version>
# build. result stored in /dist
python -m build
# upload to pypi
twine upload dist/*
```