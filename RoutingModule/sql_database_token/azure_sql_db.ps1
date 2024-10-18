$TenantID = "20cb5e13-90c8-40c4-859e-a08fc1df3c0c"
$clientId = "3adfc06b-abca-42ae-a682-fd1b66a50850"
$clientSecret = "b608Q~L_Jvf8Brpz2wtP3SnKJMgNcRA4lA~OybT2"
$resourceAppIdURI = "https://database.windows.net/"
$sqlServerFQN = "accelitas-sql-server-01-dev-wus.database.windows.net"
$sqlDatabaseName = "accelitas-reporting-db-merged"
 
$tokenResponse = Invoke-RestMethod -Method Post -UseBasicParsing `
  -Uri "https://login.windows.net/$($TenantID)/oauth2/token" `
  -Body @{
         resource=$resourceAppIdURI
         client_id=$clientId
         grant_type='client_credentials'
         client_secret=$clientSecret
  } -ContentType 'application/x-www-form-urlencoded'
 
if ($tokenResponse) {
   Write-debug "Access token type is $($tokenResponse.token_type), expires $($tokenResponse.expires_on)"
   Write-Host "##vso[task.setvariable variable=Token;]$tokenResponse.access_token"
   $Token = $tokenResponse.access_token
}