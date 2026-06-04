# Advanced Algorithms and Data Structures

This repository contains my Python solutions and coursework for the university subject **Advanced Algorithms and Data Structures**.

The repository is being developed gradually and includes algorithmic problems, implementations, and result files prepared during laboratory classes and independent work.

## Repository Structure

- `01_knapsack_problem/`
  - `knapsack_problem.py` - Python implementation of the 0/1 knapsack problem with an evolutionary strategy
  - `knapsack_results.txt` - example output/results
  - `README.md` - description of the knapsack task and how to run it

- `02_task_allocation_in_multi-processor_system/`
  - `task_allocation.py` - Python implementation of task allocation for multiple processors with different speeds
  - `output.txt` - example output/results
  - `README.md` - description of the processor scheduling task and how to run it

- `03_asymmetric_traveling_salesman_problem/`
  - `atsp.py` - Python implementation for the Asymmetric Traveling Salesman Problem (ATSP)
  - `atsp_results.txt` - example summary of ATSP run results
  - `README.md` - description of the ATSP task and how to run it

- `04_particle_swarm_optimization/`
  - `pso.py` - Python implementation of the Particle Swarm Optimization algorithm
  - `pso_results.txt` - example output/results
  - `README.md` - description of the PSO task and how to run it

- `05_kohonen_som_swiece/`
  - `kohonen_som_swiece.py` - Python implementation of a Kohonen Self-Organizing Map for clustering Japanese candlestick types
  - `requirements.txt` - list of required external Python libraries
  - `README.md` - description of the Kohonen SOM task and how to run it

## Purpose

The purpose of this repository is to collect and organize solutions to advanced algorithmic and data structure problems in Python.

The implemented tasks include evolutionary strategies, optimization problems, scheduling problems, routing problems, swarm intelligence, and unsupervised neural network algorithms.

## Technologies

- Python 3
- NumPy
- Pandas
- Matplotlib
- Scikit-learn
- yfinance

Some tasks use only the standard Python library. Tasks that require additional packages include their own local `requirements.txt` files.

## How to Run

Go to the selected task folder and run the Python file.

```bash
python 01_knapsack_problem/knapsack_problem.py
python 02_task_allocation_in_multi-processor_system/task_allocation.py
python 03_asymmetric_traveling_salesman_problem/atsp.py
python 04_particle_swarm_optimization/pso.py
```

For task 05, first install the required libraries:

```bash
cd 05_kohonen_som_swiece
python3 -m pip install -r requirements.txt
python3 kohonen_som_swiece.py
```

## Tasks Overview

### 01. Knapsack Problem

Implementation of the 0/1 knapsack problem solved with a `(1+1)` evolutionary strategy.

The goal is to choose a subset of 100 items in such a way that the backpack capacity is used as much as possible without exceeding the given limit.

### 02. Task Allocation in Multi-Processor System

Implementation of a task allocation problem for a heterogeneous multi-processor system.

The goal is to assign 100 tasks to 4 processors with different speeds and minimize the final completion time, defined as the maximum processor load.

### 03. Asymmetric Traveling Salesman Problem

Implementation of an evolutionary strategy for the Asymmetric Traveling Salesman Problem.

The goal is to find a route through 100 cities with the lowest possible total travel cost. The problem is asymmetric, so the cost from city A to city B may be different from the cost from city B to city A.

### 04. Particle Swarm Optimization

Implementation of the Particle Swarm Optimization algorithm for finding the maximum of a two-variable periodic function.

The algorithm works on a population of particles. Each particle has its own position and velocity. During each iteration, particles move through the search space and are guided toward the best solution found so far.

The program:

- defines a periodic function of two variables,
- initializes a swarm of particles,
- updates particle positions and velocities,
- performs multiple independent runs,
- compares the results,
- selects the best result.

### 05. Kohonen SOM - Candlestick Clustering

Implementation of a Kohonen Self-Organizing Map used for unsupervised clustering of Japanese candlestick types based on daily stock market data.

The program:

- downloads OHLC stock data for selected Japanese companies,
- creates candlestick features,
- normalizes the data,
- trains a Kohonen SOM network,
- performs 10 independent runs,
- compares the results,
- selects the best run,
- generates CSV result files after execution.

## Progress

- [x] Knapsack problem
- [x] Task allocation in multi-processor system
- [x] Asymmetric Traveling Salesman Problem (ATSP)
- [x] Particle Swarm Optimization (PSO)
- [x] Kohonen SOM - candlestick clustering
- [ ] Additional advanced algorithms

## Author

Emilia Piotrowska
