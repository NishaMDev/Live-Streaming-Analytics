cmd="curl -X POST 'https://id.twitch.tv/oauth2/token' -H 'Content-Type: application/x-www-form-urlencoded' -d 'client_id=0ftpptipb81nn0sh38vofh3s040bbf&client_secret=vsmsld266om7ij791fyjn4cj2pgqzh&grant_type=client_credentials'"
result=`$cmd`
echo $result