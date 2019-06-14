IFS=$'\n'

while :
do
	for j in $(cat nohup.out)
	do
		echo "$j"
	done
done
