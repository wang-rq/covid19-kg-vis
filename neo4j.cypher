LOAD CSV WITH HEADERS FROM 'file:///data/encounters_clean.csv' AS row FIELDTERMINATOR ','
    MERGE (e:Encounter {id:row.Id})
          SET e.code=row.CODE,
            e.description=row.DESCRIPTION,
            e.reasondescription=row.REASONDESCRIPTION,
            e.class=row.ENCOUNTERCLASS,
            e.date=datetime(row.START),
            e.baseCost=toFloat(row.BASE_ENCOUNTER_COST),
            e.claimCost=toFloat(row.TOTAL_CLAIM_COST),
            e.coveredAmount=toFloat(row.PAYER_COVERAGE),
            e.isEnd=false
        FOREACH (ignore in CASE WHEN row.STOP IS NOT NULL AND row.STOP <> '' THEN [1] ELSE [] END |
          SET e.end=datetime(row.STOP)
        )
        MERGE (p:Patient {id:row.PATIENT})
        MERGE (p)-[:HAS_ENCOUNTER]->(e)
        FOREACH (ignore in CASE WHEN row.PROVIDER IS NOT NULL AND row.PROVIDER <> '' THEN [1] ELSE [] END |
          MERGE (o:Organization {id: row.PROVIDER})
          MERGE (e)-[:HAS_PROVIDER]->(o))
        WITH e,row
        MATCH (pa:Payer {id:row.PAYER})
        MERGE (e)-[:HAS_PAYER]->(pa)


LOAD CSV WITH HEADERS FROM 'file:///data/payers.csv' AS row FIELDTERMINATOR ','
    MERGE (p:Payer {id:row.Id})
      SET p.name=row.NAME,
        p.address=row.ADDRESS,
        p.city=row.CITY,
        p.zip=row.ZIP,
        p.state=row.STATE_HEADQUARTERED


LOAD CSV WITH HEADERS FROM 'file:///data/providers.csv' AS row FIELDTERMINATOR ','
    MERGE (p:Provider {id: row.Id})
    SET p.name=row.NAME,
        p.speciality=row.SPECIALITY
    MERGE (o:Organization {id: row.ORGANIZATION})
    MERGE (p)-[:BELONGS_TO]->(o)
    MERGE (a:Address {address: row.ADDRESS})
    SET a.location = point({latitude:toFloat(row.LAT), longitude:toFloat(row.LON)})
    MERGE (p)-[:HAS_ADDRESS]->(a)


LOAD CSV WITH HEADERS FROM 'file:///data/patients.csv' AS row FIELDTERMINATOR ','
    MERGE (p:Patient {id:row.Id})
      SET
        p.birthDate=datetime(row.BIRTHDATE),
        p.deathDate=row.DEATHDATE,
        p.firstName=row.FIRST,
        p.lastName=row.LAST,
        p.SSN=row.SSN,
        p.marital=row.MARITAL,
        p.gender=row.GENDER,
        p.race=row.RACE,
        p.ethnicity=row.ETHNICITY,
        p.city=row.CITY
    MERGE (a:Address {address: row.ADDRESS})
    SET a.location = point({latitude:toFloat(row.LAT), longitude:toFloat(row.LON)})
    MERGE (p)-[:HAS_ADDRESS]->(a)



LOAD CSV WITH HEADERS FROM 'file:///data/payer_transitions.csv' AS row FIELDTERMINATOR ','
    MATCH (p:Patient {id:row.PATIENT})
    MATCH (payer:Payer {id:row.PAYER})
    CREATE (p)-[s:INSURANCE_START]->(payer)
    SET s.year=toInteger(row.START_YEAR)
    CREATE (p)-[e:INSURANCE_END]->(payer)
    SET e.year=toInteger(row.END_YEAR)


LOAD CSV WITH HEADERS FROM 'file:///data/allergies.csv' AS row FIELDTERMINATOR ','
        MATCH (p:Patient {id:row.PATIENT})
        MERGE (a:Allergy {code:row.CODE})
        SET a.description=row.DESCRIPTION
        MERGE (as:Encounter {id:row.ENCOUNTER, isEnd: false})
        ON CREATE
            SET as.date=datetime(row.START), as.code=row.CODE
        ON MATCH
            SET as.code=row.CODE
        MERGE (p)-[:HAS_ENCOUNTER]->(as)
        MERGE (as)-[:HAS_ALLERGY]->(a)
        WITH p,a,as,row
        WHERE row.STOP IS NOT NULL and row.STOP <> ''
        MERGE (ae:Encounter {id:row.ENCOUNTER, date:datetime(row.STOP)})
        SET ae.code=row.CODE, ae.isEnd=true
        MERGE (p)-[:HAS_ENCOUNTER]->(ae)
        MERGE (ae)-[:HAS_ALLERGY]->(a)
        MERGE (as)-[:HAS_END]->(ae)


LOAD CSV WITH HEADERS FROM 'file:///data/conditions_clean.csv' AS row FIELDTERMINATOR ','
        MATCH (p:Patient {id:row.PATIENT})
        MERGE (c:Condition {code:row.CODE})
        SET c.description=row.DESCRIPTION
        MERGE (cs:Encounter {id:row.ENCOUNTER, isEnd: false})
        ON CREATE
          SET cs.date=datetime(row.START), cs.code=row.CODE
        ON MATCH
          SET cs.code=row.CODE
        MERGE (p)-[:HAS_ENCOUNTER]->(cs)
        MERGE (cs)-[:HAS_CONDITION]->(c)
        WITH p,c,cs,row
        WHERE row.STOP IS NOT NULL and row.STOP <> ''
        MERGE (ce:Encounter {id:row.ENCOUNTER, date:datetime(row.STOP)})
        SET ce.code=row.CODE, ce.isEnd=true
        MERGE (p)-[:HAS_ENCOUNTER]->(ce)
        MERGE (ce)-[:HAS_CONDITION]->(c)
        MERGE (cs)-[:HAS_END]->(ce)


LOAD CSV WITH HEADERS FROM 'file:///data/medications_clean.csv' AS row FIELDTERMINATOR ','
        MERGE (p:Patient {id:row.PATIENT})
        MERGE (d:Drug {code:row.CODE})
        SET d.description=row.DESCRIPTION
        MERGE (ps:Encounter {id:row.ENCOUNTER, isEnd: false})
        ON CREATE
        SET ps.code=row.CODE, ps.date=datetime(row.START)
        ON MATCH
        SET ps.code=row.CODE
        MERGE (p)-[:HAS_ENCOUNTER]->(ps)
        MERGE (ps)-[:HAS_DRUG]->(d)
        WITH p,d,ps,row
        WHERE row.STOP IS NOT NULL and row.STOP <> ''
        CREATE (pe:Encounter {id:row.ENCOUNTER, date:datetime(row.STOP)})
        SET pe.code=row.CODE, pe.isEnd=true
        MERGE (p)-[:HAS_ENCOUNTER]->(pe)
        MERGE (pe)-[:HAS_DRUG]->(d)
        MERGE (ps)-[:HAS_END]->(pe)


LOAD CSV WITH HEADERS FROM 'file:///data/procedures_clean.csv' AS row FIELDTERMINATOR ','
        MERGE (p:Patient {id:row.PATIENT})
        MERGE (r:Procedure {code:row.CODE})
        SET r.description=row.DESCRIPTION
        MERGE (pe:Encounter {id:row.ENCOUNTER, isEnd: false})
        ON CREATE
        SET pe.date=datetime(row.START), pe.code=row.CODE
        ON MATCH
        SET pe.code=row.CODE
        MERGE (p)-[:HAS_ENCOUNTER]->(pe)
        MERGE (pe)-[:HAS_PROCEDURE]->(r)

LOAD CSV WITH HEADERS FROM 'file:///data/careplans_clean.csv' AS row FIELDTERMINATOR ','
        MATCH (p:Patient {id:row.PATIENT})
        MERGE (c:CarePlan {code:row.CODE})
        SET c.description=row.DESCRIPTION
        MERGE (cs:Encounter {id:row.ENCOUNTER, isEnd: false})
        ON CREATE
        SET cs.code=row.CODE, cs.date=datetime(row.START)
        ON MATCH
        SET cs.code=row.CODE
        MERGE (p)-[:HAS_ENCOUNTER]->(cs)
        MERGE (cs)-[:HAS_CARE_PLAN]->(c)
        WITH p,c,cs,row
        WHERE row.STOP IS NOT NULL and row.STOP <> ''
        CREATE (ce:Encounter {id:row.ENCOUNTER, date:datetime(row.STOP)})
        SET ce.code=row.CODE, ce.isEnd=true
        MERGE (p)-[:HAS_ENCOUNTER]->(ce)
        MERGE (ce)-[:HAS_CARE_PLAN]->(c)
        MERGE (cs)-[:HAS_END]->(ce)

LOAD CSV WITH HEADERS FROM 'file:///data/organizations.csv' AS row FIELDTERMINATOR ','
        MATCH (o:Organization {id:row.Id})
          SET o.name=row.NAME
        MERGE (a:Address {address: row.ADDRESS})
          SET a.location = point({latitude:toFloat(row.LAT), longitude:toFloat(row.LON)})
        MERGE (o)-[:HAS_ADDRESS]->(a)

MATCH (p)-[:HAS_ENCOUNTER]->(e)
    WITH e
    ORDER BY e.date
    WITH collect(e) AS encounters
    WITH encounters, encounters[1..] as nextEncounters
    UNWIND range(0,size(nextEncounters)-1,1) as index
    WITH encounters[index] as first, nextEncounters[index] as second
    CREATE (first)-[:NEXT]->(second)


MATCH (c)<-[:HAS_CONDITION]-(:Encounter)<-[:HAS_ENCOUNTER]-(p:Patient)
      WITH c,count(p) AS NUM
      SET c.num=NUM