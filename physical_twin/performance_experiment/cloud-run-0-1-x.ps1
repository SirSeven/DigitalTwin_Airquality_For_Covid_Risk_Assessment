$appResourceName = "at-davemar-dipl-master-thesis";
$appResourceGroup = "master-thesis";
$inputs ="inputs/0-1-10.json","inputs/0-1-20.json","inputs/0-1-30.json","inputs/0-1-40.json","inputs/0-1-50.json","inputs/0-1-60.json","inputs/0-1-70.json","inputs/0-1-80.json","inputs/0-1-90.json","inputs/0-1-100.json";

function Get-ApplicationInsightQueryResult {
    param ($Timestamp)
    $apiKey="45nhs0aqctb10yaoupmdamd7pvsskaad5lxfl5yn";
    $appId="0beee547-8cff-4045-afc1-fc9810fb2ca8"

    $query="requests | project timestamp,operation_Name,resultCode,duration | where timestamp > datetime('"+$Timestamp+"') | where operation_Name =~ 'AzureDigitalTwinBridgeFunction' | order by timestamp asc | take 10"

    return (Invoke-WebRequest -UseBasicParsing -Method POST -Uri https://api.applicationinsights.io/v1/apps/$($appId)/query -ContentType application/json -Body $('{"query":"' + $query + '"}') -Headers @{"X-Api-Key"=$apiKey}).Content | ConvertFrom-Json;
}

$inputs | foreach {
    Write-Host "Running $_";
    az appconfig kv import -s file --format json --path $_ --separator : --content-type application/json -y -n $appResourceName --only-show-errors
    az appconfig kv set --key Validators:Settings:Sentinel --value $(Get-Date -Format "o") -y -n $appResourceName --only-show-errors
    
    Start-Sleep -Seconds 300;

    ##warm up
    python Main-cloud.py;
    python Main-cloud.py;

    Start-Sleep -Seconds 10.0;

    $timestampStr = $((Get-Date).ToUniversalTime().ToString("o"));
    python Main-cloud.py;

    $deleteAppConfigKeysResult = az appconfig kv delete --key "validators:Sensor*" -y -n $appResourceName --only-show-errors

    Write-Host "Results from no earlier than $timestampStr";
    Start-Sleep -Seconds 180;

    do {
        $queryResult = Get-ApplicationInsightQueryResult -Timestamp $timestampStr;
        $resultLength = $queryResult.tables.rows.Length;
        if($resultLength -lt 10) {
            Write-Host "To little results gotten: $resultLength. Sleeping for another 1 minute.";
            Start-Sleep -Seconds 60;
        }
    } while($resultLength -lt 10);

    $outputString = "$_";
    $queryResult.tables.rows | foreach {
        $outputString = $outputString + ";$($_[0]);$($_[3])";
    }

    Add-Content -Path "cloud-0-1-x.results.csv" -Value $outputString;
}