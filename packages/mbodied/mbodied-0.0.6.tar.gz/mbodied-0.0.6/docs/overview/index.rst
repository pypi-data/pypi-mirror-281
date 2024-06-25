Overview
================

Welcome to **mbodied agents**, a toolkit for integrating state-of-the-art transformers into robotics systems. **mbodied agents** is designed to provide a consistent interface for calling different AI models, handling multimodal data, using/creating datasets trained on different robots, and work for arbitrary observation and action spaces. It can be seamlessly integrated into real hardware or simulation.

The goals for this repo are to minimize the ambiguity, heterogeneity, and data scarcity currently holding generative AI back from wide-spread adoption in robotics. It provides strong type hints for the various types of robot actions and provides a unified interface for:

- Streaming to and from vision models e.g. GPT4-o, OpenVLA, etc.
- Handling multimodal data pipelines for setting up continual learning.
- Automatically recording observations and actions to hdf5.
- Exporting to the most popular ML formats such as `Gym Spaces <https://gymnasium.farama.org/index.html>`_ and `Huggingface Datasets <https://huggingface.co/docs/datasets/en/index>`_.

And most importantly, the entire library is **100% configurable to any observation and action space**. With **mbodied agents**, the days of wasting precious engineering time on tedious formatting and post-processing are over. Jump to `Getting Started <#getting-started>`_ to get up and running on `real hardware <https://colab.research.google.com/drive/16liQspSIzRazWb_qa_6Z0MRKmMTr2s1s?usp=sharing>`_ or a `mujoco simulation <https://colab.research.google.com/drive/1Fh6RNJ-eFOzzXBfyVC3wyqJfCI-t09ZJ?usp=sharing>`_.
