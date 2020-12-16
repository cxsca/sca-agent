#!/bin/sh

echo Trying to connect to minio...
while ! /usr/bin/mc config host add myminio http://minio:9000 ${MINIO_ACCESS_KEY_ID} ${MINIO_SECRET_ACCESS_KEY} >/dev/null 2>&1
do
  sleep 2s
  echo Failed to initialize connection to minio, trying again
done

echo Connected successfully to minio, creating required buckets...
/usr/bin/mc mb myminio/${UPLOADS_BUCKET}

echo Setting buckets lifecycle policies up...
echo "{\"Rules\":[{\"ID\":\"Cleanup\",\"Expiration\":{\"Days\":${BUCKET_EXPIRATION_IN_DAYS}},\"Status\":\"Enabled\"}]}" | /usr/bin/mc ilm import myminio/${UPLOADS_BUCKET}
/usr/bin/mc ilm list myminio/${UPLOADS_BUCKET}

exit 0
