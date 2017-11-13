#!/usr/bin/env bash

# Copyright (c) 2017 Hitachi, Ltd. All Rights Reserved.
#
# Licensed under the MIT License.
# You may obtain a copy of the License at
#
#    https://opensource.org/licenses/MIT
#
# This file is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OF ANY KIND.

set -eux

source sh/env.sh

${DBBINPATH}/createdb "selinux" -p ${DBPORT}
${DBBINPATH}/psql "selinux" -p ${DBPORT} -v "ON_ERROR_STOP=1" << EOS
  CREATE EXTENSION pg_trgm; 
  
  CREATE TABLE info (json jsonb);
  COPY info (json) from program 'sed ''s/\\\\/\\\\\\\\/g'' < ${JSONDIR}/info.json';
  CREATE TABLE files (id SERIAL PRIMARY KEY, json jsonb);
  COPY files (json) from program 'sed ''s/\\\\/\\\\\\\\/g'' < ${JSONDIR}/files.json';
  CREATE INDEX files_json_index ON files USING GIN(json); 
  CREATE INDEX files_path_index ON files USING GIN((json ->> 'path') gin_trgm_ops); 
  CREATE INDEX files_jsontext_index ON files USING GIN((json::TEXT) gin_trgm_ops); 

  CREATE TABLE contexts (id SERIAL PRIMARY KEY, json jsonb);
  COPY contexts (json) from program 'sed ''s/\\\\/\\\\\\\\/g'' < ${JSONDIR}/contexts.json';
  CREATE INDEX contexts_json_index ON contexts USING GIN(json); 
  CREATE INDEX contexts_json_label_domain_index ON contexts USING BTREE((json ->'label'->>'domain')); 
  CREATE INDEX contexts_jsontext_index ON contexts USING GIN((json::TEXT) gin_trgm_ops); 

  CREATE TABLE processes (id SERIAL PRIMARY KEY, json jsonb);
  COPY processes (json) from program 'sed ''s/\\\\/\\\\\\\\/g'' < ${JSONDIR}/processes.json';
  CREATE INDEX processes_json_index ON processes USING GIN(json); 

  CREATE TABLE attributes (id SERIAL PRIMARY KEY, json jsonb);
  COPY attributes (json) from program 'sed ''s/\\\\/\\\\\\\\/g'' < ${JSONDIR}/attributes.json';
  CREATE INDEX attributes_json_index ON attributes USING GIN(json); 

  CREATE TABLE rules (id SERIAL PRIMARY KEY, json jsonb);
  COPY rules (json) from program 'sed ''s/\\\\/\\\\\\\\/g'' < ${JSONDIR}/rules.json';
  CREATE INDEX rules_json_index ON rules USING GIN(json); 
  CREATE INDEX rules_json_source_index ON rules USING BTREE((json ->> 'source')); 
  CREATE INDEX rules_json_target_index ON rules USING BTREE((json ->> 'target')); 
  CREATE INDEX rules_json_type_index ON rules USING BTREE((json ->> 'type')); 

  CREATE TABLE types (id SERIAL PRIMARY KEY, json jsonb);
  COPY types (json) from program 'sed ''s/\\\\/\\\\\\\\/g'' < ${JSONDIR}/types.json';
  CREATE INDEX types_json_index ON types USING GIN(json); 

  CREATE TABLE bools (id SERIAL PRIMARY KEY, json jsonb);
  COPY bools (json) from program 'sed ''s/\\\\/\\\\\\\\/g'' < ${JSONDIR}/bools.json';
  CREATE INDEX bools_json_index ON bools USING GIN(json); 
  CREATE INDEX bools_jsontext_index ON bools USING GIN((json::TEXT) gin_trgm_ops); 

  CREATE TABLE domains  (id SERIAL PRIMARY KEY, name text);  
  INSERT INTO domains (name)
    SELECT DISTINCT name
    FROM (
      SELECT json->>'name' AS name FROM types
      UNION
      SELECT json->>'name' AS name FROM attributes
      UNION
      SELECT JSONB_ARRAY_ELEMENTS_TEXT(attributes.json->'types')::text AS name FROM attributes
      UNION
      SELECT json->>'source' AS name FROM rules
      UNION
      SELECT json->>'target' AS name FROM rules
    ) AS tmp ORDER BY name;
  CREATE INDEX domains_name_index ON domains USING BTREE(name); 

  CREATE TABLE domain_crews AS
    SELECT * FROM (
	    SELECT name AS domain, name AS crew FROM domains
	    UNION
	    SELECT json->>'name' AS domain, JSONB_ARRAY_ELEMENTS_TEXT(json->'types')::text AS crew FROM attributes
	    UNION
	    SELECT domains.name AS domain, attributes.json->>'name'  AS crew
	    FROM domains JOIN attributes ON attributes.json @> JSONB_BUILD_OBJECT('types', ARRAY[domains.name])
    ) AS tmp ORDER BY domain, crew;
    
  CREATE INDEX domain_crews_domain_index ON domain_crews USING BTREE(domain);
  CREATE INDEX domain_crews_crew_index ON domain_crews USING BTREE(crew);

  CREATE TABLE context_file_refs AS
    SELECT contexts.id AS context_id, files.id AS file_id FROM files, contexts 
      WHERE (files.json->>'path') ~* ( '^' || (contexts.json->>'pattern') || '$')
      AND ( 
      	contexts.json->>'type' = 'all files' 
      	OR (
	      		 (contexts.json->>'type' = 'regular file' AND files.json->>'file_type' = 'f')
	      	OR (contexts.json->>'type' = 'directory' AND files.json->>'file_type' = 'd')
	      	OR (contexts.json->>'type' = 'symbolic link' AND files.json->>'file_type' = 'l')
	      	OR (contexts.json->>'type' = 'named pipe' AND files.json->>'file_type' = 'p')
	      	OR (contexts.json->>'type' = 'character device' AND files.json->>'file_type' = 'c')
	      	OR (contexts.json->>'type' = 'block device' AND files.json->>'file_type' = 'b')
	      	OR (contexts.json->>'type' = 'socket' AND files.json->>'file_type' = 's')
	      )
      )
     ORDER BY contexts.id;
  CREATE INDEX context_file_refs_file_index ON context_file_refs USING BTREE(file_id); 
  CREATE INDEX context_file_refs_context_index ON context_file_refs USING BTREE(context_id);

  CREATE TABLE networks (id SERIAL PRIMARY KEY, json jsonb);
  COPY networks (json) from program 'sed ''s/\\\\/\\\\\\\\/g'' < ${JSONDIR}/tcps.json';
  CREATE INDEX networks_json_index ON networks USING GIN(json); 
  CREATE INDEX networks_json_proto_index ON networks USING BTREE((json->>'Proto')); 

  CREATE TABLE ports (id SERIAL PRIMARY KEY, json jsonb);
  COPY ports (json) from program 'sed ''s/\\\\/\\\\\\\\/g'' < ${JSONDIR}/ports.json';
  CREATE INDEX ports_json_index ON ports USING GIN(json);
  CREATE INDEX ports_json_protocol_index ON ports USING BTREE((json->>'protocol')); 

  CREATE TABLE network_processes  (id SERIAL PRIMARY KEY, json JSONB);  
  INSERT INTO network_processes (json)
    SELECT JSONB_BUILD_OBJECT(
    'id', networks.id
    ,'program', networks.json->>'Program name'
    ,'protocol', networks.json->>'Proto'
    ,'domain', networks.json->'Security Context'->>'domain'
    ,'state', networks.json->>'State'
    ,'local', networks.json->'Local Address'
    ,'foreign', networks.json->'Foreign Address'
    ,'ports', ( 
        SELECT JSONB_AGG(
          JSONB_BUILD_OBJECT(
            'info', local_ports.json
            ,'permlist',(
              SELECT JSONB_AGG(permissions.name) FROM (
                SELECT DISTINCT JSONB_ARRAY_ELEMENTS_TEXT(rules.json->'permlist') AS name FROM rules
                  JOIN domain_crews AS sources ON rules.json->>'source' = sources.crew
                    AND sources.domain = networks.json->'Security Context'->>'domain'
                  JOIN domain_crews AS targets ON rules.json->>'target' = targets.crew
                    AND targets.domain = local_ports.json->>'type'
                    AND (
                          ( local_ports.json->>'protocol' = 'tcp' AND rules.json->>'class' = 'tcp_socket')
                      OR ( local_ports.json->>'protocol' = 'udp' AND rules.json->>'class' = 'udp_socket')
                    )
                ) AS permissions
            )
          )
        ) FROM ports as local_ports
          WHERE 
          (
                ( local_ports.json->>'protocol' = 'tcp' AND  networks.json->>'Proto' in ('tcp', 'tcp6') )
            OR ( local_ports.json->>'protocol' = 'udp' AND  networks.json->>'Proto' in ('udp', 'udp6') )
          )
          AND (local_ports.json->>'low')::int <= (networks.json->'Local Address'->>'port')::int
          AND (networks.json->'Local Address'->>'port')::int <= (local_ports.json->>'high')::int
      )
    ) AS json
    FROM networks
    ORDER BY networks.id; 
  CREATE INDEX network_processes_json_index ON network_processes USING GIN(json);
  CREATE INDEX network_processes_jsontext_index ON network_processes USING GIN((json::TEXT) gin_trgm_ops); 

  CREATE TABLE rule_context_refs AS
    SELECT rules.id AS rule_id, contexts.id AS context_id
    FROM rules 
    JOIN domain_crews AS targets ON targets.domain = rules.json->>'target'
    JOIN contexts ON contexts.json->'label'->>'domain' = targets.crew
    WHERE contexts.json->>'type' = 'all files' 
    AND   rules.json->>'class' IN ('file', 'dir', 'lnk_file', 'sock_file', 'fifo_file', 'chr_file', 'blk_file');
    
  INSERT INTO rule_context_refs (rule_id, context_id)
    SELECT rules.id AS rule_id, contexts.id AS context_id
    FROM rules 
    JOIN domain_crews AS targets ON targets.domain = rules.json->>'target'
    JOIN contexts ON contexts.json->'label'->>'domain' = targets.crew
    WHERE contexts.json->>'type' = 'regular file' AND rules.json->>'class' IN ('file');
    
  INSERT INTO rule_context_refs (rule_id, context_id)
    SELECT rules.id AS rule_id, contexts.id AS context_id
    FROM rules 
    JOIN domain_crews AS targets ON targets.domain = rules.json->>'target'
    JOIN contexts ON contexts.json->'label'->>'domain' = targets.crew
    WHERE contexts.json->>'type' = 'directory' AND rules.json->>'class' IN ('dir');
    
  INSERT INTO rule_context_refs (rule_id, context_id)
    SELECT rules.id AS rule_id, contexts.id AS context_id
    FROM rules 
    JOIN domain_crews AS targets ON targets.domain = rules.json->>'target'
    JOIN contexts ON contexts.json->'label'->>'domain' = targets.crew
    WHERE contexts.json->>'type' = 'symbolic link' AND rules.json->>'class' IN ('lnk_file');

  INSERT INTO rule_context_refs (rule_id, context_id)
    SELECT rules.id AS rule_id, contexts.id AS context_id
    FROM rules 
    JOIN domain_crews AS targets ON targets.domain = rules.json->>'target'
    JOIN contexts ON contexts.json->'label'->>'domain' = targets.crew
    WHERE contexts.json->>'type' = 'socket' AND rules.json->>'class' IN ('sock_file');
    
  INSERT INTO rule_context_refs (rule_id, context_id)
    SELECT rules.id AS rule_id, contexts.id AS context_id
    FROM rules 
    JOIN domain_crews AS targets ON targets.domain = rules.json->>'target'
    JOIN contexts ON contexts.json->'label'->>'domain' = targets.crew
    WHERE contexts.json->>'type' = 'character device' AND rules.json->>'class' IN ('chr_file');
    
  INSERT INTO rule_context_refs (rule_id, context_id)
    SELECT rules.id AS rule_id, contexts.id AS context_id
    FROM rules 
    JOIN domain_crews AS targets ON targets.domain = rules.json->>'target'
    JOIN contexts ON contexts.json->'label'->>'domain' = targets.crew
    WHERE contexts.json->>'type' = 'block device' AND rules.json->>'class' IN ('blk_file');
    
  CREATE INDEX rule_context_refs_rule_index ON rule_context_refs USING BTREE(rule_id); 
  CREATE INDEX rule_context_refs_context_index ON rule_context_refs USING BTREE(context_id);
EOS
