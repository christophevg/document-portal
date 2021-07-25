# TODO

[ x ] basic setup: viewer <-> gw <=> archive

[   ] implement authentication + acl endpoint
[   ] introduce status + update capability
[   ] apply properties typing info (string, guids,...)
[   ] implement selection of documents
[   ] implement PDF merge on archive
[   ] add more and meaningful example documents
[   ] clean up navigation (add hierarchy)
[   ] add search capabilities (aka construct custom query arguments)
[   ] add welcome page
[   ] add creation/update timestamp attributes + query on "last week"

## DOC GW v1: search and update

[ x ] GET   /meta/types           lists type names
[ x ] GET   /documents?{k=v}      lists documents matching attributes

[   ] PATCH /documents/(guid)     apply changes to document identified by guid
