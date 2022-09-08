# Explorations for A Sustainable Future

**A place for exploratory and micro data science projects for Nesta's Sustainable Future Mission**

This repository is for work that is very small and self-contained, is not part of a specific Sustainable Future project or is exploratory in nature. Examples of what might be included are exploring the potential for a new dataset, testing out a modelling approach or handling an ad-hoc request for data analysis.

Each exploration is in its own sub-directory, which can be navigated using the Directory below. Contributing guidelines are below.

## 📖 Directory

**< Project name (with link to sub-directory) >**
< Short description of project and links to any key resources >


## 🎮 User guidelines

1. Use the directory above to find the exploration that you are looking for.
2. Create an environment for that exploration. This will probably involve running `conda create -n <exploration>_<name> python=3` and installing some requirements, but check each exploration for its installation instructions.

## 📝  Contributor guidelines

To add a new exploration to this repository:

1. Determine whether this is the right place for the work. As a rule of thumb it should be:
  a. Executed with a fairly small codebase (e.g. 1 notebook and a utils module).
  b. Exploratory in nature (e.g. a small analysis for internal project scoping).
  c. Not contributing to a signifcant external output for the organisation.
2. Create an issue for the exploration. For example, _Exploration of RECC complaints data_.
3. Create a new branch from `dev` and check it out with `git checkout -b <issue number>_<short>_<exploration>_<name>`
4. Create a subdirectory for this exploration.
5. Write and commit all code, data and documentation inside this sub-directory. Make sure to add a `README.md`.
6. Once development is finished, add the name and description of the exploration to the Directory above.
7. Create a pull request into `dev`.

When writing your exploration, the following requirements must be met.

**👍 Development standards**
- Adhere to the [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html).
- All requirements to run exploratory projects should be independent and defined within the sub-directory (e.g. in a `requirements.txt` or `environment.yml`). A user should be able to create an environment from scratch to run the code.
- The code must run from start to finish without error.
- Modularised and refactored code is preferred over notebooks. If using notebooks, use `jupytext`.
- There should be no imports from other explorations.
- Each exploration should contain its own `README.md` that gives a comprehensive description of the work.

**🔀 Workflow**
- Make pull requests and request code reviews.
- Use the [Nesta Git/GitHub guidelines](https://github.com/nestauk/github_support/blob/dev/guidelines/README.md). If your code is simple and short, then you may work in one branch and merge into `dev` with one PR. If there are a few development steps then consider breaking the code down into smaller issues, branches and PRs.

**💾 Data**
- It is preferable that data are stored on S3.
- Very small datasets (~1Mb) can be stored in the repository.

If you find that you are revisiting a project here, or beginning to do significant development, you may want to review the decision to have the work in its own repository. 

Many of these guidelines require judgement on your part. If in doubt, chat to someone else in the team 🙂