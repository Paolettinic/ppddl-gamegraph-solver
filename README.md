# ppddl-gamegraph-solver

FOND game against nature solver, described in [ppddl](http://reports-archive.adm.cs.cmu.edu/anon/2004/CMU-CS-04-167.pdf), solved using simplex method.

Please note it currently only supports the ```:requirements :strips, :typing, :equality, :probabilistic-effects``` for the PPDDL description


# Install


```bash
$ git clone https://github.com/Paolettinic/ppddl-gamegraph-solver
```

Please make sure you have the ```ply``` and ```networkx``` libraries installed on your system. If you don't have them, you can use pip3 to install them.

```bash 
$ pip3 install ply
$ pip3 install networkx
```


# Usage

```bash
$ python3 main.py -h
usage: python3 main.py <DOMAIN> <INSTANCE>

ppddl-gamegraph-solver is a PPDDL to game graph converter, based on ply and solved with simplex method.

positional arguments:
  domain      path to PDDL domain file
  problem     path to PDDL problem file

optional arguments:
  -h, --help  show this help message and exit
```
Further details are in the file [Report_ReasoningAgents.pdf](https://github.com/Paolettinic/ppddl-gamegraph-solver/blob/master/Report_ReasoningAgents.pdf)
