# README.md Assignment2 

## Task 2.1

### Prerequisites

The user needs to be able to run a bash program. 

### Functionality

The function moves files from a directory to another directory. 
You can move all files or all files of a spesific type. 
If the directory you want to move from does noe exist, the program will exit. 
If the directory you want to move to does not exist, you have some options:
1. If you dont want to create it, the program exit. 
2. Create a directory with the name given.
3. Create a directory with the date as name.


### Missing Functionality

If you want to move all files of more than one type, this is not possible. 

### Usage

To run the program the user needs run the following command

```bash
chmod a+x ./move.sh
./move.sh src dst (type)

```

src is the name of the source directory, dst is the name of the dst directory. 
It is optional to add the third argument type, if you do it should include ".", eks .txt or .py. 

### Kommentarer 

Tror alt skal funke som beskrevet. Er også testet på ifi-maskin og skal funke der. 


## Task 2.2

### Prerequisites

The user needs to be able to run a bash program. 
 

### Functionality

The function keeps track on differnt tasks, and save the information in a logfile. 
The user can start and stop tasks, see current status,
get an overview of all tasks that has finished and the time each task took to finish. 

### Missing Functionality

Maybe user needs to create the logfile because Im not sure if my code does that right.

The log function calculate the time used for each task, here we assume that every task starts and stops in the same month. 


### Usage

Not 100% sure about how this works with sourse and stuff, but this is how I run the program on my mac: 

User should maybe run the following command the first time

```bash
chmod a+x ./track.sh
```

To start the program the user needs to run the following command

```bash
source track.sh
```

To use the program for tracking the user can run the following commands

```bash
track start
track stop
track status
track log
```

These commands can be run in any order, and as many times as the user want, one at a time. 
 
track start   (starts a new task if no task is running) 

track stop    (stops the running task if any task is running)

track status  (shows the runnig status, tells the user witch task is running, if any)

track log     (shows all tasks and their running time)


### Kommentarer 

Kjører også som forventet på ifi-maskin. Noe rart med opprettelsen av logfilen, måtte mauelt gå inn i local share og lage denne filen for at det skulle funke. 

