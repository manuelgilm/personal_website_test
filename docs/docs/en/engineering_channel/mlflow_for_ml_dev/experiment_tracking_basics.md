# Basics of experiment tracking with MLflow

When working on a machine learning project, the number of **parameters**, **configurations**, and moving parts we need to track is considerable. This creates the need for a **mechanism to manage and monitor** all the changes made during project development. MLflow provides two **important concepts** that are essential to understanding its workflow: a **Run** and an **Experiment**.

## The MLflow Run

A **run** refers to a **single execution of machine learning code**. Why is defining this important? When working on machine learning projects, we typically focus on two main areas:

* **Data Processing and Feature Engineering**: This area is in charge of fetching data from database systems and transforming it into a usable state for model training.

* **Model Training and Evaluation**: Here, we use the processed data to train a machine learning model, which is usually part of a broader solution.

When executing machine learning code, plenty of **parameters and configurations** are needed to control the behavior of feature generation and, especially, model training. Not only do parameters and configurations change, but the orchestration code changes as well.

TODO: <inser animation here>

MLflow's **Run concept** helps **track all these variables** across multiple executions of your code. Within an MLflow run, you can track **metrics**, **parameters**, **tags**, and **artifacts** (like data files or model weights). Different runs can then be easily compared to highlight their differences and performance improvements.

## The MLflow Experiment

When you have multiple runs associated with a single task or project, it is necessary to **organize them**; otherwise, there is no logical way to review your progress. An **MLflow experiment** is used to **organize multiple runs** associated with the same task. The **experiment object** serves as a **logical container** for these MLflow runs.