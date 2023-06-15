#!/bin/bash

#Read arguments, or exit if not given
if [ $# -gt 1 ]; then
  src=$1
  dst=$2
  echo "Moving files from $src to $dst"
  #Specify file-type
  if [ $# -gt 2 ]; then
    type="$3"
    echo "Filetype is specified, $type"
  else
    echo "No filetype is specified, moving all files in $src"
  fi
else
  echo "To run the program add src and dst directory as arguments"
  echo "It is optional to add filetype"
  echo "./move.sh src dst (type)"
  exit
fi

#Run if src exist, if not the program exit
if [ -d $src ]; then
  #If dst does not exist, user can choose to create it as dst or as date
  if ! [ -d $dst ]; then
    echo "$dst does not exist, do you want do create it? [y/n]"
    read create_dir

    if [ $create_dir = 'y' ]; then
      echo "Do you want the directory to have the current date and time in the format YYYY-MM-DD-hh-mm [y/n]"
      read name

      #Naming dst directory as the user wants
      if [ $name = 'y' ]; then
        dst=$(date +%Y-%m-%d-%H-%M)
        echo "Creating $dst"
        mkdir $dst
      else
        echo "Creating $dst"
        mkdir $dst
      fi
    else
      echo "You dont want a new directory, exit"
      exit
    fi
  fi
else
  echo "$src does not exist, exit"
  exit
fi


files=$(ls $src)
#Moving file
for file in $files; do
  if [ $# -gt 2 ]; then
    if [[ $file == *"${type}"* ]]; then
      echo "Moving $file from $src to $dst"
      mv $src/$file $dst
    fi
  else
    echo "Moving $file from $scr to $dst"
    mv $src/$file $dst
  fi
done
