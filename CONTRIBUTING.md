---

# ⚙️ Contributing to AutoEDA

Welcome to **AutoEDA** – an automated toolkit designed to streamline **exploratory data analysis (EDA)** and **data preprocessing** workflows. Whether you’re here to squash bugs, optimize algorithms, add new modules, improve documentation, or suggest new ideas, **we're excited to collaborate with you**! 📊🤝

This guide will help you contribute effectively and respectfully to the project.

---

## 📜 Code of Conduct

We are committed to fostering an inclusive and respectful community. Please take a moment to review our [Code of Conduct](CODE_OF_CONDUCT.md).

---

## 💡 How You Can Contribute

AutoEDA has room for contributions in many areas:

* 🐛 Bug reporting and fixing
* ⚙️ Adding new preprocessing features or EDA modules
* 📊 Improving visualizations or summary stats
* 🧪 Writing unit tests and improving test coverage
* 📝 Enhancing documentation and tutorials
* 📦 Packaging or deployment improvements
* 🔍 Reviewing pull requests

---

## 🚀 Getting Started

### 1️⃣ Fork the Repository

Click the **Fork** button in the upper right to copy this repo to your GitHub account.

### 2️⃣ Clone Your Fork

```bash
git clone https://github.com/<your-username>/AutoEDA-Automated-Data-Preprocessing-Toolkit.git
cd AutoEDA-Automated-Data-Preprocessing-Toolkit
```

### 3️⃣ Create a New Branch

Use a clear and descriptive branch name:

```bash
git checkout -b feat/missing-value-imputation
```

### 4️⃣ Make Your Changes

Edit or add code, tests, docs, or configurations as needed. Check the **Project Structure** section below if unsure where to place your files.

### 5️⃣ Stage and Commit Your Work

```bash
git add .
git commit -m "feat: added KNN imputer for missing value handling"
```

### 6️⃣ Push and Open a Pull Request

```bash
git push origin feat/missing-value-imputation
```

Then go to your fork on GitHub, click **"Compare & pull request"**, and submit your PR.

---

## 🧪 Testing Guidelines

Help keep AutoEDA stable by writing or updating tests:

* Use `pytest` for new or modified features.
* Cover edge cases (e.g., missing columns, mixed data types).
* Run all tests before pushing your changes.

```bash
pip install -r requirements.txt
pytest tests/
```

---

## 🐛 Reporting Bugs

Found a bug? Let us know!

1. [Open an issue](https://github.com/Nidhi-Satyapriya/AutoEDA-Automated-Data-Preprocessing-Toolkit/issues/new)
2. Include:

   * ✅ Clear steps to reproduce
   * 🧪 Sample data if possible
   * 🖼️ Screenshots or logs
3. Use the appropriate labels (`bug`, `enhancement`, `question`, etc.)

> 🔒 **Note**: Please wait until the issue is assigned to you before starting to work on it.

---

## 🙌 First-Time Contributors

We love seeing new contributors join the open-source community!

* [GitHub Forking Guide](https://docs.github.com/en/get-started/quickstart/fork-a-repo)
* [Creating a Pull Request](https://opensource.com/article/19/7/create-pull-request-github)
* [Beginner Git Tutorial](https://www.freecodecamp.org/news/learn-the-basics-of-git-in-under-10-minutes/)

If you're stuck, create an issue with the `help wanted` or `question` label.

---

## ✅ Pull Request Checklist

Before opening a PR, make sure:

* [ ] Your code runs without errors
* [ ] Tests are added or updated (if applicable)
* [ ] You followed consistent code style and structure
* [ ] Your PR title is clear and descriptive
* [ ] You linked a related issue (e.g., `Closes #12`)
* [ ] You've been assigned the issue

---

## 🙏 A Note from the Maintainer

Thank you for your interest in improving **AutoEDA**! Your time and effort mean a lot to this project. Please avoid spammy or low-effort PRs — we review contributions carefully to maintain quality.

Got an idea or need feedback? Open an issue or start a discussion!

---

<div align="center">
  <img src="https://media.giphy.com/media/xUPGcguWZHRC2HyBRS/giphy.gif" width="100" />
  <br />
  <em><b>Let’s automate EDA, one smart contribution at a time!</b></em>
</div>

---
