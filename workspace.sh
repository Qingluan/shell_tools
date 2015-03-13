#!/bin/sh

WORKSPACE=$1;

if grep "SB" ~/.zshrc 
then
	sed /SB/ c "export SB=\"$WORKSPACE;\"" ~/.zshrc;
else
	echo "export SB=\"$WORKSPACE\";" >> ~/.zshrc;
fi	

