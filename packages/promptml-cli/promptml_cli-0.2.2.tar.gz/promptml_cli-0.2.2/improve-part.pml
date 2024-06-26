@prompt
    @context
        You are an excellent SQL Developer
    @end

    @objective
        Explain the below SQL query. The Joins are very hard to understand. Break down the query and explain it in simple terms.
        origin_osm is a schema that contains tables for OpenStreetMap data.

        After explanation, improve the query. Do you think filtering the relation_type upfront will improve the performance?

        ```sql
        CREATE SCHEMA IF NOT EXISTS proc_osm;


        CREATE MATERIALIZED VIEW IF NOT EXISTS proc_osm.multipolygon_relations as (
        SELECT origin_osm.relations.osm_id, ST_BuildArea(ST_Collect(origin_osm.ways.geometry)) AS geometry
        FROM origin_osm.relations
        JOIN origin_osm.relation_members ON origin_osm.relations.osm_id = origin_osm.relation_members.parent_id AND origin_osm.relation_members.member_type = 1
        JOIN origin_osm.ways ON origin_osm.relation_members.osm_id = origin_osm.ways.osm_id
        WHERE origin_osm.relations.relation_type = 'multipolygon'
        GROUP BY origin_osm.relations.osm_id
        ) WITH NO DATA;
        ```
    @end

    @category
        SQL Programming
    @end
@end
