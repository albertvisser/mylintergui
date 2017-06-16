# mylintergui
Simple frontend for various Python linters

More an exercise in using git/Github than an interesting software project, actually: I'm primarily
a Mercurial/Bitbucket user.

Also an exercise in getting myself to make more use of static code analysis, by making things
easy (or eas*ier*).

Because I already built a tool ([FileFindr](https://bitbucket.org/avisser/filefindr)) to do text
searches in files and directories from a small GUI
showing some options, I decided to reuse it for this purpose. So first of all this thing should make
it possible to choose which linter to use.

Just like the other thing, when you let it do what it's supposed to do, you get a screen showing
the output, with the possibility to do various things with the results you get.
Alternatively, you can choose to not show them, but write them directly to one or more files
(which you can also do when you do have a look at the results first) .

Along the way a simpler thingy emerged, basically just a parser for some command-line options,
which I also included in this project.

In fact the GUI version can also be started with options already specified, you can even choose
not to show the GUI at all.

