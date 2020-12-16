#!/bin/bash
VERBOSE=0
SCAN_ID=""

for arg in "$@"
do
    case $arg in
    -h|--help)
        echo "Usage: show-scans-status [options] [arguments]"
        echo "options:"
        echo "-h, --help               show help"
        echo "-v, --verbose            show verbose output"
        echo "arguments:"
        echo "-i, --scan-id [SCAN_ID]  show only status of the provided scan"
        echo "examples:"
        echo "get logs from .env file LOG_LOCATION:"
        echo "$ sh show-scans-status.sh"
        echo "$ sh show-scans-status.sh -i 28919862-0479-4e25-8363-df1b36ae7bf5"
        echo "$ sh show-scans-status.sh --short"
        exit 0
        ;;
    -v|--verbose)
        VERBOSE=1
        shift 
        ;;
    -i|--scan-id)
        SCAN_ID="$2"
        shift
        shift
        ;;
    esac
done


logLocation=$(grep LOG_LOCATION .env | cut -d'=' -f 2)
echo "Taking sca-agent logs from: $logLocation/sca-agent-*"
echo 
logFiles="$logLocation/sca-agent-*"

ScanIds=$SCAN_ID
if [ "$SCAN_ID" = '' ]; then
    ScanIds=$(grep -Po '(?<=ScanId: )[^ ,}]*' $logFiles | sort -u)
    if [ -z "$ScanIds" ]; then
        echo "No logs found"
        exit 0
    fi
else
    ScanIds=$(grep -Po '(?<=ScanId: )[^ ,}]*' $logFiles | sort -u | grep $SCAN_ID)
    if [ -z "$ScanIds" ]; then
        echo "No logs found for scan $SCAN_ID"
        exit 0
    fi
fi

numOfIds=$(echo "$ScanIds" | wc -l)
echo "Found $numOfIds scans"

if [ $VERBOSE -eq 0 ]; then
    echo "Project ID                              Scan ID                                 Status     Related errors"
fi

counter=1
while IFS=':' read -r file id
do 
    scanLogs=$(grep $id $file)
    scanDir=$(echo "$scanLogs" | grep -Po '(?<=ScanDir=")[^"]*' | head -1)
    scanMessages=$(grep $scanDir $file| grep SourceResolverBouncer | grep -Po '(?<=1 )\w*|finished')
    projectId=$(echo "$scanLogs" | grep -Po '(?<=ProjectId: )[^ ,}]*' | head -1)
    relatedErrors=$(echo "$scanLogs" | grep '"Level":"Error"' | wc -l)
    if [ $VERBOSE -eq 1 ]; then
        echo "$counter ------------Project: $projectId    Scan: $id ------------"
        echo "$scanMessages"
        echo
        echo "$relatedErrors errors"
        echo
        counter=$((counter+1))
    else
        lastStatus=$(echo "$scanMessages" | tail -n1)
        echo "$projectId    $id    $lastStatus    $relatedErrors"
    fi
done <<< "$ScanIds"
