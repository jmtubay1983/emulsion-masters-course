# Disease Modeling with EMULSION (Master's Edition)

**Course Lead:** Jerrold Tubay | **Date:** 31 December 2025  
**Adapted from:** [EMULSION Training](https://forge.inrae.fr/dynamo/software/emulsion-training) by Sébastien Picault (INRAE).  
**License:** [CC-BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)

---

## 🌟 Overview
This workshop provides a hands-on introduction to epidemiological modeling. We have simplified the original doctoral-level curriculum to focus on core concepts:
* **Building Models:** Learn to construct SIR and SEIR compartmental models.
* **Stochasticity:** Understand the difference between random and deterministic disease spread.
* **Age Structure:** Simulate how diseases move differently through various age groups.

---

## 🚀 How to Run the Exercises

You do not need to install any software on your computer. We use **Binder**, which provides a pre-configured environment in your web browser.

### Option 1: Use the Web Browser (Recommended)
Click the button below to launch your private lab session:

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/jmtubay1983/emulsion-masters-course/master)

**Instructions for Binder:**
1.  **Wait for the Build:** It may take 2–5 minutes to start the first time.
2.  **Verify Setup:** Once the terminal opens, type `emulsion --version`. It should return `1.2rc5`.
3.  **Open the Notebook:** Locate and open `EMULSION-training.ipynb` in the file browser on the left.

> **⚠️ Warning:** Binder sessions are **ephemeral**. If you are inactive for more than 10 minutes, the session will close. **Download your modified YAML files** to your local computer to save your work!

---

### Option 2: Local Installation (Advanced)
If you prefer to run the models on your own machine:

1.  **Install Python & Graphviz:** Ensure you have Python 3.8+ and [Graphviz](https://graphviz.org/) installed.
2.  **Install EMULSION:**
    ```bash
    pip install -U emulsion==1.2rc5
    ```
3.  **Clone this Repository:**
    ```bash
    git clone [https://github.com/jmtubay1983/emulsion-masters-course.git](https://github.com/jmtubay1983/emulsion-masters-course.git)
    ```

---

## 📚 Learning Resources
* [Official EMULSION Documentation](https://sourcesup.renater.fr/www/emulsion-public)
* [Original Research Paper (Picault et al.)](https://doi.org/10.1371/journal.pcbi.1007342)
* [DYNAMO Research Group](https://www6.angers-nantes.inrae.fr/bioepar/Equipes/DYNAMO)
* [Original Doctoral Training Repo](https://forge.inrae.fr/dynamo/software/emulsion-training)

---
*This repository is a derivative of the EMULSION training materials created by the DYNAMO team at INRAE. It has been modified for educational use in Master-level courses.*
