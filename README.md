# python-file-server
##A small engineering project for a python LAN file server.

###This server implements a sqlite/ext4 hybrid database, allowing for quick file access and smart semantic file indexing.
###Planned features:
-multi-user support including a permissions system
-content-addressed-storage via sqlite metadata table
-web frontend
-full asynchronous cli support
-safe worker threads for sqlite and disk state using work queues
-support for usage of multiple connected drives and customizable partitioning
-remote multimedia file viewers 
-robust user authentication with JWT tokens and password hashing
-3-stage multilevel codebase for easier stack tracing/debugging
-robust support for scalability
