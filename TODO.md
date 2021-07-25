# TODO

[ x ] basic setup: viewer <-> gw <=> archive

[   ] implement authentication + acl endpoint
[   ] introduce status + update capability
[   ] apply properties typing info (string, guids,...)
[ x ] implement selection of documents
[ x ] implement PDF merge on archive
[   ] add more and meaningful example documents
[ x ] clean up navigation (add hierarchy)
[   ] add search capabilities (aka construct custom query arguments)
[   ] add creation/update timestamp attributes + query on "last week"
[   ] extend welcome page to dashboard with "new" documents

## DOC GW v1: search and update

[ x ] GET   /meta/types           lists type names
[ x ] GET   /documents?{k=v}      lists documents matching attributes

[   ] PATCH /documents/(guid)     apply changes to document identified by guid
