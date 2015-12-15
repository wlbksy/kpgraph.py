#!/usr/bin/zsh

filename=$1

pivot_str=""
kidList=""

while read -r line
do
    arr=($line)
    qid=${arr[0]}
    kid=${arr[1]}

    if [[ $pivot_str == $qid ]]; then
        kidList=$kidList","$kid
    else
        echo $pivot_str" "$kidList
        pivot_str=$qid
        kidList=$kid
    fi
done < $filename

