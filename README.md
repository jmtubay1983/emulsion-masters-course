# Introduction to the exploration of epidemiological models using EMULSION

| Author: **Sébastien Picault, INRAE** | June 2-4, 2021 (upd. March 28, 2022) |
|---|---|
| License: [CC-BY-NC-SA](https://en.wikipedia.org/wiki/Creative_Commons_license) | ![CC-BY-NC-SA](https://upload.wikimedia.org/wikipedia/commons/1/12/Cc-by-nc-sa_icon.svg "License CC-BY-NC-SA") |

This training (see details [here](https://sourcesup.renater.fr/www/emulsion-public/EGAAL2021/)) is part of the doctoral formation proposed at the [EGAAL doctoral school](https://ed-egaal.doctorat-bretagneloire.fr/).



<table style="border: none;">
    <tr style="border: none;">
        <td style="padding: 25px; border: none;"><img alt="bloc marque Etat" src="img/Republique_Francaise.jpg" width="300px"></td>
        <td style="padding: 25px; border: none;"><img alt="logo INRAE" src="img/Logo-INRAE.jpg" width="400px"></td>
        <td style="padding: 25px; border: none;"><img alt="logo Oniris" src="img/Logo_Oniris.png" width="350px"></td>
        <td style="padding: 25px; border: none;"><img alt="logo Pays de la Loire" src="img/Logo-EGAAL.png" width="500px"></td>
    </tr>
</table>
</span>

## Documentation for EMULSION 1.2b10

The documentation for this version is available [here](https://spicault.pages.mia.inra.fr/emulsion-training/)

---

## Software configuration for the training

Exercises can be run either on your own machine on through a virtual environment provided by [Binder](https://mybinder.readthedocs.io/en/latest/).


### Solution 1: do everything on-line

We provide a pre-configured virtual environment thanks to Binder, which ensures that all participants work with the same software environment.

This on-line environment can be launched by clicking this button: [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/git/https%3A%2F%2Fforgemia.inra.fr%2Fspicault%2femulsion-training/HEAD?urlpath=lab)

When the environment is built, you should get the following environment:

![Jupyter Lab](img/jupyterlab.png)

- Open a terminal and type:

```bash
emulsion --version
```

Your configuration is correct if you get this:

![emulsion vesion](img/version.png)


- You can also test the notebook


**IMPORTANT NOTES:**

- At the very first time, Binder has to build the virtual environment before launching it, which takes some time (about 10 minutes). After that, the Binder environment is cached, hence taking only 1-2 min to launch
- The Binder environment is **ephemeral**, with a short timeout period (about 10 min). Thus, you have to periodically save (download) the files you modify (e.g. EMULSION model files, or possibly the notebook), to be able to restore them after a break.

> You can either **download** the notebook on your machine or download/upload its state through your web browser

![notebook](img/notebook.png)


> You can also download/upload the exercises (YAML files) on your
> machine

![exercises](img/exercises.png)


---

### Solution 2: install on your own machine

Choose this approach if you are already familiar with software installation on your machine.

1. Install and test EMULSION version **1.2b10** (with Graphviz) on your own machine following the [installation instructions](https://spicault.pages.mia.inra.fr/emulsion-training/pages/Install.html) and the [section regarding development versions](https://spicault.pages.mia.inra.fr/emulsion-training/pages/Install.html#alternative-2-install-development-version).
2. Download this repository (see button above) or clone it with `git`
   (`git clone
   https://forgemia.inra.fr/spicault/emulsion-training.git`)

   - Download: ![download](img/download.png)
   - Clone: ![clone](img/clone.png)

3. For the exercises, follow the instructions provided in the notebook [Getting started](Getting%20started.ipynb). By default, this notebook will be displayed in a read-only mode. To have it work interactively, you need to install [Jupyter lab](https://jupyter.org/) on your machine.
4. To run the exercises themselves, copy-paste commands in your favourite terminal.


---

## Additional resources

- [EMULSION website](https://sourcesup.renater.fr/www/emulsion-public) and [software paper](https://doi.org/10.1371/journal.pcbi.1007342)
- [DYNAMO team](https://www6.angers-nantes.inrae.fr/bioepar/Equipes/DYNAMO)
- follow us:
  [![https://img.shields.io/twitter/follow/bioepar_dynamo?label=DYNAMO%20research%20group&amp;style=plastic&amp;logo=twitter](https://img.shields.io/twitter/follow/bioepar_dynamo?label=DYNAMO%20research%20group&amp;style=plastic&amp;logo=twitter)](http://twitter.com/intent/follow?screen_name=bioepar_dynamo)
