# Modules Repository for the Prey Bash Client

These modules provide the core functionality for the Prey Bash client.
They are run when triggered remotely, either the official Control Panel
(panel.preyproject.com) or through the [Standalone Panel](https://github.com/prey/prey-standalone-control-panel).

# How they work

When enabled, Prey will call the ./run script located in the module's core/
directory, so in essence the only needed thing for a module to run is that
file. However, Prey will also load additional scripts in case they are found
in the module's path. These are:

 - /[module_name]/config -> For keeping settings
 - /[module_name]/functions -> Shared functions
 - /[module_name]/platform/{mac,linux,windows}/functions -> Platform-specific functions

This way you can separate shared logic from that which is platform specific.

# When called

Prey runs modules in paralell, by calling the ./core/run scripts daemonized.
Since they are called in the context of the running script (the main core logic), 
modules can access all variables previously defined by Prey. The most useful
ones are:

 - $os (linux, mac or windows)
 - $logged_user
 - $root_path
 - $users_path
 - $home_path
 - $tmpbase
 - $tmpdir (random directory created by Prey for storing temporary data)

Additionally, Prey will also provide modules with utility variables for modules:

 - $module_path: /[module_name]/
 - $module_platform_path: /[module_name]/platform/{mac,linux,windows}

# Available functions

Modules also get the helper functions defined in Prey's core/framework and 
core/functions files. A good way to see what you can do is to look at any
of the existing modules and see how they store data or perform different actions.

(c) 2011 - Fork Ltd. Licensed under the GPLv3.
