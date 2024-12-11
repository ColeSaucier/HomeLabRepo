SELECT
  sm.entity_id,
  FROM_UNIXTIME(s.last_reported_ts, '%Y-%m-%d %H:%i:%s.%f') AS UTC_Last_Reported,
  s.state,
  sa.shared_attrs,
  et.event_type,
  e.time_fired_ts,
  s.last_changed_ts,
  s.last_updated_ts,
  s.old_state_id,
  s.attributes_id,
  e.event_id,
  ed.shared_data,
  s.state_id
FROM 
  events e
JOIN 
  event_types et ON e.event_type_id = et.event_type_id
JOIN
	event_data ed ON e.data_id = ed.data_id
RIGHT JOIN
  states s ON s.context_id_bin = e.context_id_bin
JOIN
  states_meta sm ON s.metadata_id = sm.metadata_id
JOIN
  state_attributes sa ON s.attributes_id = sa.attributes_id
ORDER BY 
  s.last_reported_ts DESC;
