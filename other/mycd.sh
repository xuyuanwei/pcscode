#!/bin/bash
# this piece of code is used to record the directories you want to shift often,
# and cd to them easily
# you need to add "alias mycd='. /the/path/of/this/script'"in .bashrc,
# or it does do nothing to the current shell

dirlogfile=/tmp/dirlogfile
declare -a linearray
linecount=0
maxrecord=5
currentpwd=`pwd`

#echo there $# variables
if [ $# -gt 1 ];then 
    cat << END
    Usage: \$mycd /dir/name # current dir will be remebered
    \$mycd           # print last $maxrecord directories,and prompt to choose
END
fi

# if no argument,then print all history for choose
if [ $# -eq 0 ];then
    if [ -f $dirlogfile ];then
        historylines=`cat $dirlogfile | wc -l`
        if [ $historylines -eq 0 ];then
            echo No history
            return 1
        fi
        #only preserve $maxrecord in logfile
        if [ $historylines -gt $maxrecord ]; then
            tail -n $maxrecord $dirlogfile > $dirlogfile.tmp
            mv $dirlogfile.tmp $dirlogfile
        fi
    else
        touch $dirlogfile
        echo No history
        return 1
    fi
    # read logfile and print
    while read line; do
        linearray[$linecount]=$line
        # export the DIR varible to the current shell,so you can use them
        # in cp/rm commands
        export DIR$linecount=${linearray[$linecount]}
        echo $linecount ${linearray[$linecount]} DIR$linecount
        ((linecount++))
    done < $dirlogfile

    echo "Please choose one directory:"
    read choose

    # press enter to do nothing
    if [ "$choose" == "" ];then
        echo No change
        return 0
    fi

    if [ "$choose" -ge "0" ] && [ "$choose" -lt "$linecount" ];then
        # if choose is effective,then save current path to history
        isinhistory=0
        if [ "currentpwd" != "${HOME}" ];then
            while read line; do
                if [ "$line" == "$currentpwd" ]; then
                    isinhistory=1
                    break
                fi
            done < $dirlogfile
            if [ $isinhistory -eq 0 ];then
                echo $currentpwd >> $dirlogfile
            else
                echo "Already in history"
            fi
        fi
        cd ${linearray[$choose]}
        return 0
    else
        echo unkown choose
        return 2
    fi
fi

if [ -d $1 ]; then
    isinhistory=0
    if [ ! -f $dirlogfile ];then
        touch $dirlogfile
    else
        while read line; do
            if [ "$line" == "$currentpwd" ]; then
                isinhistory=1
                break
            fi
        done < $dirlogfile
    fi
    if [ $isinhistory -eq 0 ] && [ "$currentpwd" != "${HOME}" ];then
        echo $currentpwd >> $dirlogfile
    else
        echo "Already in history"
    fi
    # you need to add "alias mycd='. /the/path/of/this/script'"in .bashrc
    cd $1
    return 0
else
    echo Error: $1 is not a direction
    return 3
fi



