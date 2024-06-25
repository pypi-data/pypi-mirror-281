README
######


NAME

::

    OBJD - object daemon


SYNOPSIS

::

    objd <cmd> [key=val] [key==val]
    objd


DESCRIPTION

::

    OBJD is a python3 irc bot, it can connect to IRC, fetch and display RSS
    feeds, take todo notes, keep a shopping list and log text. You can also
    copy/paste the service file and run it under systemd for 24/7 presence
    in a IRC channel.


    OBJD has all you need to program a unix cli program, such as disk
    perisistence for configuration files, event handler to handle the
    client/server connection, code to introspect modules for
    commands, deferred exception handling to not crash on an error, a
    parser to parse commandline options and values, etc.

    OBJD contains python3 code to program objects in a functional way. It
    provides a base Object class that has only dunder methods, all methods
    are factored out into functions with the objects as the first
    argument. I call it Object Programming (OP), OOP without the oriented.

    OBJD  allows for easy json save//load to/from disk of objects. It
    provides an "clean namespace" Object class that only has dunder
    methods, so the namespace is not cluttered with method names. This
    makes storing and reading to/from json possible.

    OBJD is Public Domain.


INSTALL


    $ pipx install objd
    $ pipx ensurepath


USAGE

::

    without any argument the program starts a daemon

    $ objd
    $


    use objd <arguments> program to manage objd


CONFIGURATION

::

    the cfg command is used for configuration of the IRC bot

    $ objd cfg 
    channel=#objd commands=True nick=objd port=6667 server=localhost

    irc

    $ objd cfg server=<server>
    $ objd cfg channel=<channel>
    $ objd cfg nick=<nick>

    sasl

    $ objd pwd <nsvnick> <nspass>
    $ objd cfg password=<frompwd>

    rss

    $ objd rss <url>
    $ objd dpl <url> <item1,item2>
    $ objd rem <url>
    $ objd nme <url> <name>


COMMANDS

::

    $ objd cmd
    cfg,cmd,dne,dpl,err,flt,log,mod,mre,nme,pwd,rem,req,res,rss,tdo,thr,tmr


    cmd - commands
    cfg - irc configuration
    dlt - remove a user
    dpl - sets display items
    fnd - find objects 
    log - log some text
    met - add a user
    mre - displays cached output
    pwd - sasl nickserv name/pass
    rem - removes a rss feed
    rss - add a feed
    thr - show the running threads


SYSTEMD

::

    save the following it in /etc/systemd/system/objd.service and
    replace "<user>" with the user running pipx

::

    [Unit]
    Description=object daemon
    Requires=network-online.target
    After=network-online.target

    [Service]
    Type=simple
    User=<user>
    Group=<user>
    WorkingDirectory=/home/<user>/.objd
    ExecStart=/home/<user>/.local/pipx/venvs/objd/bin/objd
    RemainAfterExit=yes

    [Install]
    WantedBy=default.target

::

    then run this::

    $ mkdir ~/.objd
    $ sudo systemctl enable objd --now

    default channel/server is #objd on localhost


FILES

::

    ~/.objd
    ~/.local/bin/objd
    ~/.local/pipx/venvs/objd/


AUTHOR

::

    xobjectz <objx@proton.me>


COPYRIGHT

::

    OBJD is Public Domain.
