while read p; do 
    echo Pulling "$p" ..
    echo "------------"
    docker image pull $p 
done < docker-images.txt