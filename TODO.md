# TODO

## MVP

- viewer <-> doc gw <=> archive api

## DOC GW v1: search and update

GET   /meta/types               lists type names
GET   /meta/types/(type name)   provides configuration of type (schema)
GET   /documents?q              lists documents matching attributes
PATCH /documents/(guid)         apply changes to document identified by guid
