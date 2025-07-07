# CHANGELOG


## v0.1.1 (2025-07-07)

### Bug Fixes

* fix: get version dynamically

* docs: update screenshot and use absolute path
* ci: remove workflow_dispatch for release and pwd for publishing to pypi
* fix: get version dynamically ([`19eaf46`](https://github.com/kcmr/ticket-please/commit/19eaf4608e3ec31507636f43de9c53a86db79fd8))


## v0.1.0 (2025-07-07)

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
