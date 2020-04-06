# mylintergui

## Simple frontend for various Python linters

The GUI version is started by calling **start.py** in the project root directory.
Its main purpose is to show the results of checking your code with a static analysis tool in a screen, and being able to save the results to a file afterwards.


The arguments you provide control what you might call the execution mode:

- bij specifying a directory you get the basic version, which allows you to check files in that directory.

- by specifying a filename you get the single-file version, which will check that specific file. This was originally built to be called from within a text editor like SciTE.

- by specifying a list of files or a file that contains such a list, you get the multiple file version. This was originally designed to be called from within a file manager like Double Commander.

Without any of these arguments, you get the basic version in which you can choose a directory.


The choices to be made in the GUI (which linter to use, where to send output to) can also be passed
using arguments, it's even possible to not have the GUI shown at all.

During development I also made a script version ( **lint-this**  in the project root) that always
saves the results into files.
A variant on this is **lint-all** that relies on my personal software project structure.


It all started more as an exercise in using git/Github than an interesting software project, actually: I was primarily a Mercurial/Bitbucket user, and no doubt there a lots of programs like this around.

It's also an exercise in getting myself to make more use of static code analysis, by making things
easy (or eas*ier*).

Because I already built a tool ([FileFindr](https://bitbucket.org/avisser/filefindr)) to do text
searches in files and directories from a small GUI showing some options, I decided to reuse it for this purpose.

# Usage

Call ``start.py`` in the top directory. Use --help to get an overview of options.

# Requirements

- Python
- PyQt(5)
- obviously you should also install a version control system (git and mercurial are supported) and define one or more repositories
