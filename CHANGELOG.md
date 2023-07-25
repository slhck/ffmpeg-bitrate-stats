# Changelog


## v1.0.0 (2023-07-25)

* Allow plotting results.


## v0.4.3 (2023-07-25)

* Fix bug with keyframe detection.

  in some cases (when?), keyframes are not 'K_' but 'K__'

* Add .vscode to gitignore.


## v0.4.2 (2023-07-25)

* Fix frame order for bitrate calculation.

  ... in case PTS are unordered, bitrate may be negative for small chunk sizes


## v0.4.1 (2023-02-21)

* Fix readme and add license file.

* Add flake8 to tox, update GH actions.

* Fix tox invocation.

* Fix apt in CI.

* Add tox and fix types.

* Update gitignore.

* Add mypy settings.

* Remove stalebot.

* Fix readme badge.

* Fix changelog.

* Fix setup script.

* Update README.

* Add github workflows.

* Add note on old executable in readme.


## v0.4.0 (2023-01-01)

* Add API, types and docs.

* Bump python version, cleanup.


## v0.3.1 (2022-08-02)

* Update python requirements.


## v0.3.0 (2022-08-02)

* Add another console entry point.

* Update python requirements.


## v0.2.3 (2022-01-09)

* Remove delta-PTS calculation, replace with duration.

  this makes everything conceptually easier

* Update badge link.


## v0.2.2 (2021-03-10)

* Improve setup.py.

* Remove release script.

* Fix syntax error.

* Format setup.py and switch to markdown.

* Update badge URL.

* Remove obsolete file.

* Make test executable.


## v0.2.1 (2020-05-27)

* Fix unit tests after program logic modification, fixes #7.

* Change pip to pip3.

* Fix description of duration calculation.


## v0.2.0 (2020-02-07)

* Add py3.8 compat.

* Add proper handling of PTS and duration/fps calculation.

* Update release script.


## v0.1.3 (2020-01-16)

* Fix casting problem, fixes #3.


## v0.1.2 (2020-01-14)

* Rename changelog.

* Update release script.


## v0.1.1 (2020-01-14)

* Version bump to 0.1.1.

* Add simple test suite.

* Convert into float, fixes #3.

* Add PyPI badge.


## v0.1 (2019-05-25)

* Version bump to 0.1.

* Make python package.

* Fix examples in readme.

* Update README.md.


## v0.0.2 (2019-04-19)

* Version bump to 0.0.2.


## v0.0.1 (2019-04-19)

* Initial commit.


