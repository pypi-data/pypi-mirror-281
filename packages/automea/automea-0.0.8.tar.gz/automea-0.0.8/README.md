# autoMEA

*autoMEA* (Automated analysis of MEA datasets) is a open-source Python package for the analysis of Micro-Electrode Array (MEA) datasets. 

## How does autoMEA work?

Bursts are detected using the *Max Interval Method*. Users can manually set *Max Interval Parameters*, or can use a machine learning model that dynamically predicts optimal parameters for specific recording times. Several models are distributed with *automea*, and users are free to fine-tune the existing models for their specific needs, or upload new models completely.  

The machine-learning-based burst detection routine is explained in the paper accompanying the package. 

Tutorials and documentation can be found on [https://automea.readthedocs.io](https://automea.readthedocs.io).


## Installation

The preferred way of installing `autoMEA` is to use `pip`:


```bash
pip install automea
```


<!-- ## Citing

If you have used autoMEA for work that has lead to a scientific publication,
please cite it as

```bibtex
@misc{Hernandes2024_automea,
  title={automea},
  author={V. Hernandes et al},
  year={2024},
  eprint={2404.00000},
  archivePrefix={arXiv},
}
``` -->

## Authors

Here is a list of authors who have contributed to this project:
- Vinicius Hernandes
- Anouk M. Heuvelmans
- Valentina Gualtieri
- Dimphna H. Meijer
- Geeske M. van Woerden
- Eliska Greplova

## Contributing

autoMEA is an open source package, and we invite you to contribute!
You contribute by opening [issues](https://gitlab.com/QMAI/papers/autoMEA),
fixing them, and spreading the word about `autoMEA`.

## License

This work is licensed under a [MIT License](https://opensource.org/licenses/MIT)