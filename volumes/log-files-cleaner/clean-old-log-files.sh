#!/bin/sh

crontab -l
echo "0 */12 * * * echo cleaning logs older then ${LOG_FILES_EXPIRATION_IN_DAYS}  days; find /var/log/sca/* -mtime +${LOG_FILES_EXPIRATION_IN_DAYS} -delete" | crontab -
/usr/sbin/crond -f
