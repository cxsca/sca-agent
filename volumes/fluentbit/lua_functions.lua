function append_date_to_tag(tag, timestamp, record)
    new_record = record
    new_tag = "sca-agent-" .. os.date("%Y-%m-%d") .. ".log"
    new_record["log_file_name"] = new_tag
    return 1, timestamp, new_record
 end

 function append_date_if_missing(tag, timestamp, record)
    if record["timestamp"] ~= nil then
      return 1, timestamp, record
    end
    new_record = record
    new_record["timestamp"] = os.date("%Y-%m-%dT%H:%M:%S+00:00", timestamp)
    return 1, timestamp, new_record
 end

 function create_metric_message(tag, timestamp, record)
    new_record = record
    dimensions = ""
    for key, value in pairs(record["dimensions"]) do
      dimensions = dimensions .. key .. "=\"" .. value .. "\" "
    end
    new_record["message"] = "Metric    " .. record["name"] .. "  " .. record["value"] .. "  dimensions={ " .. dimensions .. " }"
    return 1, timestamp, new_record
end

function normfields_traefik(tag, timestamp, record)
    new_record = record
    if record["msg"] ~= nil then
      new_record["timestamp"] = record["time"]
      new_record["message"] = record["level"] .. "    " .. record["msg"]
    else
      new_record["timestamp"] = os.date("%Y-%m-%dT%H:%M:%S+00:00", timestamp)
      new_record["message"] = record["log"]
    end
    return 1, timestamp, new_record
 end

function check_message_exists(tag, timestamp, record)
  if record["message"] ~= nil then
    return 1, timestamp, record
  end
  new_record = record
  new_record["message"] = record["log"]
  return 1, timestamp, new_record
end