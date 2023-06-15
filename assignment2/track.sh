#!/bin/bash

if ! [ "$(cat $HOME/.bashrc | grep "export LOGFILE")" ]; then
  echo 'export LOGFILE="$HOME/.local/share/timer_logfile"' >> $HOME/.bashrc
fi

source $HOME/.zshrc
#Create LOGFILE if it doesn't  already exist
touch $LOGFILE


function track {
  #Reading argument and calling the correct function
  if [ $# -gt 0 ]; then
    option=$1
    shift;
    case "$option" in
      start)
        if [ $# -gt 0 ]; then
          label=$1
          start
        else
          echo "Usage: track start [label]"
        fi
        ;;
      stop)
        stop
        ;;
      status)
        status
        ;;
      log)
        log
        ;;
      *)
        echo $@
        echo "To start a new task, type track start"
        echo "To stop a running task, type track stop"
        echo "To see status, type track status"
        echo "To see the logfile with all tasks, type track log"; return
        ;;
    esac
  fi
}


#Assuming every task occupies 4 lines in the logfile
#Counter is the number of tasks that has finished
number_of_lines=$(< $LOGFILE wc -l)
number_of_tasks=$((number_of_lines / 4))
counter=$number_of_tasks

#checks if there is a running task when the program starts
#2 lines are added when a task starts, and two lines are added when a task stops
if [ $((number_of_lines % 4)) -eq 0 ]; then
  running=false
elif [ $((number_of_lines % 4)) -eq 2 ]; then
  running=true
else
  echo "Something wierd happened, check logfile"
fi


function start {
  #Starts a new task if no other task is running
  if [ $running = false ]; then
    echo "START" `date` >> $LOGFILE
    echo "$label This is task" $counter >> $LOGFILE
    ((counter+=1))
    running=true

  else
    echo "Already a task running. Stop current task to start a new one"
  fi
}

function stop {
  #Stops running task if a task is running
  if [ $running = true ]; then
    echo "END" `date` >> $LOGFILE
    echo "" >> $LOGFILE
    running=false
  else
    echo "No running task, nothing to stop"
  fi
}


function status {
  #Prints the current status
  if [ $running = true ]; then
    echo "Task $((counter)), $label is currently running"
  else
    echo "No running tasks"
  fi
}

function log {
  #Prints out total time every task has used
  task_number=0
  cat $LOGFILE | while read line; do
    nextline=$(echo "$line" | cut -d " " -f 1)
    if [ "$nextline" = "START" ]; then
      #Convert the start-time to seconds
      start_time=$(echo "$line" | cut -d " " -f 5)
      start_day=$(echo "$line" | cut -d " " -f 4)

      hour=$(echo $start_time | cut -c1-2)
      min=$(echo $start_time | cut -c4-5)
      sec=$(echo $start_time | cut -c7-8)

      start_sec=$(expr $start_day \* 86400 + $hour \* 3600 + $min \* 60 + $sec)
    fi

    if [ "$nextline" = "END" ]; then

      #Convert the stop_time to seconds
      stop_time=$(echo "$line" | cut -d " " -f 5)
      stop_day=$(echo "$line" | cut -d " " -f 4)

      hour2=$(echo $stop_time | cut -c1-2)
      min2=$(echo $stop_time | cut -c4-5)
      sec2=$(echo $stop_time | cut -c7-8)

      stop_sec=$(expr $stop_day \* 86400 + $hour2 \* 3600 + $min2 \* 60 + $sec2)

      #Total number of seconds for a task
      time_in_sec=$((stop_sec-start_sec))

      #Calculate back to format hh:mm:ss
      h=$((time_in_sec / 3600))
      new_s=$((time_in_sec % 3600))
      m=$((new_s / 60))
      new_s=$((new_s % 60))

      #Adding 0 in front if only one digit
      if [ ${#h} -eq 1 ]; then
        h=0$h
      fi
      if [ ${#m} -eq 1 ]; then
        m=0$m
      fi
      if [ ${#new_s} -eq 1 ]; then
        new_s=0$new_s
      fi

      echo "Task ${task_number} ${label}: ${h}:${m}:${new_s}"
      ((task_number+=1))
    fi

  done
}
