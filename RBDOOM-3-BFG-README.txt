 ____  ____  ____   ___   ___  __  __      _____       ____  _____ ____ 
|  _ \| __ )|  _ \ / _ \ / _ \|  \/  |    |___ /      | __ )|  ___/ ___|
| |_) |  _ \| | | | | | | | | | |\/| |_____ |_ \ _____|  _ \| |_ | |  _ 
|  _ <| |_) | |_| | |_| | |_| | |  | |_____|__) |_____| |_) |  _|| |_| |
|_| \_\____/|____/ \___/ \___/|_|  |_|    |____/      |____/|_|   \____|
 
** Doom 3 BFG Edition GPL source modification

For the additional features and fixes introduced by this great modification,
please see the original page at:

 https://github.com/RobertBeckebans/RBDOOM-3-BFG

======== Game data

It DOES NOT include game data required to run the game, you have to get the data
yourself buying the game.

To launch the engine pointing at your data files you can use the following
command:

 doom3bfg-engine +set fs_basepath "/path/to/game/content" "$@"

A sample nosrc rpm that can be used to build a binary rpm using the DVD data
files is at: http://slaanesh.fedorapeople.org/

To rebuild it, add the required files to your SOURCES directory and remove the
"NoSource" lines in the spec file. The tarball it's the contents of the "base"
directory from your Doom 3 BFG installation with patch 1.1 applied.

A high resolution icon has been generated from the game assets, to have a look
at how the resulting menu entries look like see:

 http://slaanesh.fedorapeople.org/doom3bfg-menus.png

You should end up with something like this:

 $ rpm -qa RBDOOM-3-BFG* doom3bfg*
 doom3bfg-1.1-1.fc23.noarch
 RBDOOM-3-BFG-1.1.0-1.1275984.fc21.x86_64

======== Options defined at compile time

- Uses system libraries for all components.
- Provides a doom3bfg-engine symlink through the alternatives system to easily
  switch between additional variations.
