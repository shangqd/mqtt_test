for ((i=1; i<=1000; i ++))
do
sleep 1
./webapi_c.py > "log/lwc"$i &
echo $i
done