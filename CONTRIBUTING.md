# Contributing to AskIT-CLI

First off, thank you for considering contributing to AskIT-CLI! It's people like you that make AskIT-CLI such a great tool.

## Where do I go from here?

If you've noticed a bug or have a feature request, [make one](https://github.com/your-repo/askit-cli/issues/new)! It's generally best if you get confirmation of your bug or approval for your feature request this way before starting to code.

## Fork & create a branch

If you're ready to contribute, fork the repository and create a new branch from `main`. A good branch name would be `(docs|feat|fix)/what-you-are-working-on`.

## Get the project running

We use Poetry to manage dependencies. You can get everything installed by running:

```bash
poetry install
```

## Make your changes

Make your changes in your forked repository. Make sure to follow the coding style and conventions.

### Forbidden Functions

To ensure the security and stability of the project, the use of the following Python functions is strictly prohibited. Pull requests containing them will not be merged.

| Function                   | Reason for Prohibition                                                              | Recommended Alternative                                         |
| -------------------------- | ----------------------------------------------------------------------------------- | --------------------------------------------------------------- |
| `eval()`, `exec()`         | Can execute arbitrary code, creating a major security risk.                         | Use safe data structures like dictionaries or `ast.literal_eval`. |
| `pickle.load()`, `pickle.loads()` | Can lead to arbitrary code execution when deserializing untrusted data.       | Use `json` for data serialization.                                 |
| `os.system()`              | Vulnerable to shell injection attacks.                                              | Use the `subprocess` module with `shell=False`.                 |
| `subprocess.run(shell=True)` | Also vulnerable to shell injection if the command is built from external input. | Construct commands as a list of arguments for `subprocess.run()`. |
| `tempfile.mktemp()`        | Creates a temporary file insecurely (race condition).                               | Use `tempfile.mkstemp()` or `tempfile.TemporaryFile()`.         |

This list is not exhaustive. Use your judgment and prioritize secure coding practices.

## Commit your changes

Commit your changes with a descriptive commit message. We follow the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) specification.

Example: `feat: Add new command for history`

## Submit a Pull Request

When you're ready, submit a pull request to the main repository. We'll review it as soon as we can.

Thank you for your contribution! 