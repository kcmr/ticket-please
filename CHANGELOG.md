# CHANGELOG


## v0.1.0 (2025-07-07)

### Chores

* chore: remove publish = true from pyproject.toml [skip ci] ([`0e3bfa0`](https://github.com/kcmr/ticket-please/commit/0e3bfa0edf78f221684745fe4694d27baaf435ac))

* chore: disable upload_to_pypi in pyproject.toml [skip ci] ([`51f8321`](https://github.com/kcmr/ticket-please/commit/51f8321d90476352f296e37e9925fbb7ce523e98))

* chore: trigger build ([`58eb14e`](https://github.com/kcmr/ticket-please/commit/58eb14e568550575ee51bb05646dce87e0cfc263))

* chore: update version variables in pyproject.toml and setup semantic-release

* chore: initial commit

* chore: update version variables in pyproject.toml [skip ci]

* chore: add comment about version in cli module ([`dfc8ca7`](https://github.com/kcmr/ticket-please/commit/dfc8ca7f3773ba72f12c78cf7146a588eeb8e182))

* chore: change demo gif (#3) ([`65787e9`](https://github.com/kcmr/ticket-please/commit/65787e9ae81aee73b1c381efa44d1f0ea0c4cfb2))

* chore: initial commit ([`d825f72`](https://github.com/kcmr/ticket-please/commit/d825f7207aaeaed0dde48f6e1971253dc2579291))

### Continuous Integration

* ci: change token ([`d9577f6`](https://github.com/kcmr/ticket-please/commit/d9577f6b10897f5535ea72fadfad33d1f6e3b4ef))

* ci: ensure publish to main from github ([`af54328`](https://github.com/kcmr/ticket-please/commit/af54328fe6c99f61abf7131d04b19ded456387d4))

* ci: fix release wf ([`ef6684f`](https://github.com/kcmr/ticket-please/commit/ef6684fb9891956a6a30745a103195663589ef42))

* ci: setup release ([`8ba039c`](https://github.com/kcmr/ticket-please/commit/8ba039c5091cd3f561e991c9ad592e36c169dce8))

* ci: configure release workflow with PyPI token authentication

- Enable upload_to_pypi in pyproject.toml
- Add PYPI_TOKEN environment variable to release workflow
- Configure semantic-release for automated versioning and PyPI publication ([`3f5d310`](https://github.com/kcmr/ticket-please/commit/3f5d310873b1c84c3bc6e8290b1e8e4760637f0e))

* ci: allow to manually trigger release for testing purposes ([`da8003f`](https://github.com/kcmr/ticket-please/commit/da8003f8ca2dd79507475273990f6204462d04cb))

* ci: add basic wf for release (pending complete implementation)

* chore: initial commit

* ci: allow pr-validation wf to be triggered manually

* ci: add basic wf for release (pending complete implementation) ([`db1efc9`](https://github.com/kcmr/ticket-please/commit/db1efc9cd600449a408309682185b43acc9fb762))

* ci: add basic wf for pr validation (#4) ([`caf1a0c`](https://github.com/kcmr/ticket-please/commit/caf1a0c7fe6ae2dbd40cc4668ea7bdc89b8a70e1))

### Documentation

* docs: add animated gif as demo (#2) ([`2c1913c`](https://github.com/kcmr/ticket-please/commit/2c1913c030b1a3f5b871a21aaac74f5494c926ad))

* docs: update link to license ([`f9edaa3`](https://github.com/kcmr/ticket-please/commit/f9edaa38a11a9df0fa6c59ec976e9895d1eba3a4))

### Features

* feat: include multiline support for task descriptions

Multiline editing accepts Enter or (Ctrl/Cmd + Enter) for new lines.
To finish edition the word "DONE" should be typed on a new line.
This behavior has chosen due to worst performance of other approaches
(Ctrl + Enter to submit, etc.) ([`e3573d2`](https://github.com/kcmr/ticket-please/commit/e3573d258b229b9ad7ac325764bb1aa039fe9f9c))

* feat: enable text wrapping for generated task descriptions

* chore: initial commit

* feat: enable text wrapping for generated task descriptions

- Add word_wrap=True to Rich Syntax component in _display_result method
- Prevents horizontal overflow of long lines in terminal output
- Improves readability by ensuring text fits within terminal width
- Add test to verify word_wrap parameter is properly configured

Closes #5 ([`2f82a98`](https://github.com/kcmr/ticket-please/commit/2f82a98553f35d72a666489864ab7eac0b69b005))

* feat: change CLI name and commands (#1)

* feat: change CLI name and commands

* test: remove unused param and decorator

* docs: remove extra colon ([`9b58538`](https://github.com/kcmr/ticket-please/commit/9b58538b5438694034462aa1de110b0a0a5e40d1))

* feat: initial implementation ([`b81bc03`](https://github.com/kcmr/ticket-please/commit/b81bc03b79c8bebe856d7ba52e48e7e93d801d49))

### Unknown

* Initial commit ([`031088c`](https://github.com/kcmr/ticket-please/commit/031088c68df935b4d89f8b5e788efffad2d47dce))
