#!/bin/bash
rfiles=`ls *.html`
for file in $rfiles ; 
do
    #mv $file $file.old
    sed -i '.html' s:/~ashander::g $file
    #rm -f $file.old
done

# for tree: find ~/sites/ashander.github.com/musing/Date/  -type f -exec sed -i '.html' 's:/~ashander::g' {} \;
