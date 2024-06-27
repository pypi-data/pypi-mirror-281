# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['spectral_encoding']

package_data = \
{'': ['*'], 'spectral_encoding': ['data/*']}

setup_kwargs = {
    'name': 'spectral-encoding',
    'version': '0.0.1',
    'description': 'This is a template repository for Python projects that use Poetry for their dependency management.',
    'long_description': '# spectral-encoding\n\n[![Release](https://img.shields.io/github/v/release/csaybar/spectral-encoding)](https://img.shields.io/github/v/release/csaybar/spectral-encoding)\n[![Build status](https://img.shields.io/github/actions/workflow/status/csaybar/spectral-encoding/main.yml?branch=main)](https://github.com/csaybar/spectral-encoding/actions/workflows/main.yml?query=branch%3Amain)\n[![codecov](https://codecov.io/gh/csaybar/spectral-encoding/branch/main/graph/badge.svg)](https://codecov.io/gh/csaybar/spectral-encoding)\n[![Commit activity](https://img.shields.io/github/commit-activity/m/csaybar/spectral-encoding)](https://img.shields.io/github/commit-activity/m/csaybar/spectral-encoding)\n[![License](https://img.shields.io/github/license/csaybar/spectral-encoding)](https://img.shields.io/github/license/csaybar/spectral-encoding)\n\nThis is a template repository for Python projects that use Poetry for their dependency management.\n\n- **Github repository**: <https://github.com/csaybar/spectral-encoding/>\n- **Documentation** <https://csaybar.github.io/spectral-encoding/>\n\n## Getting started with your project\n\nFirst, create a repository on GitHub with the same name as this project, and then run the following commands:\n\n```bash\ngit init -b main\ngit add .\ngit commit -m "init commit"\ngit remote add origin git@github.com:csaybar/spectral-encoding.git\ngit push -u origin main\n```\n\nFinally, install the environment and the pre-commit hooks with\n\n```bash\nmake install\n```\n\nYou are now ready to start development on your project!\nThe CI/CD pipeline will be triggered when you open a pull request, merge to main, or when you create a new release.\n\nTo finalize the set-up for publishing to PyPi or Artifactory, see [here](https://fpgmaas.github.io/cookiecutter-poetry/features/publishing/#set-up-for-pypi).\nFor activating the automatic documentation with MkDocs, see [here](https://fpgmaas.github.io/cookiecutter-poetry/features/mkdocs/#enabling-the-documentation-on-github).\nTo enable the code coverage reports, see [here](https://fpgmaas.github.io/cookiecutter-poetry/features/codecov/).\n\n## Releasing a new version\n\n- Create an API Token on [Pypi](https://pypi.org/).\n- Add the API Token to your projects secrets with the name `PYPI_TOKEN` by visiting [this page](https://github.com/csaybar/spectral-encoding/settings/secrets/actions/new).\n- Create a [new release](https://github.com/csaybar/spectral-encoding/releases/new) on Github.\n- Create a new tag in the form `*.*.*`.\n\nFor more details, see [here](https://fpgmaas.github.io/cookiecutter-poetry/features/cicd/#how-to-trigger-a-release).\n\n---\n\nRepository initiated with [fpgmaas/cookiecutter-poetry](https://github.com/fpgmaas/cookiecutter-poetry).\n',
    'author': 'Cesar Aybar',
    'author_email': 'fcesar.aybar@uv.es',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/csaybar/spectral-encoding',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
