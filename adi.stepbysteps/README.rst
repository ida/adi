TODOS:

- On site crea throws "KeyError linkable", seems not configurable,
commented out in tinymce.xml for now, added manually in controlpanel.

- provide skins/plone_deprecated/document_icon.gif in a skinfolder.

- validations in subscribers.setBlock() (id exists, no self reference, etc.)


Adi Stepbysteps
===========

A stepbystepsystem for Plone, inspired by trac and Redmine.


Usage
-----

- Assign the 'Can edit'-permissions to each user,
  who is supposed to be part of the team, via the sharing-tab
  of a folder. These users will show up as possibly selected
  in the 'responsible person'-field.
  This applies also to Editors of parent folders (local inheritance).

- A stepbystep is folderish, thus you can add to it:

    - Files as attachments (screenshots, tracebacks, PDF's, etc.)

    - More Stepbysteps for splitting things up in subtasks.

    - Pages for documentation.

- In your personaltools (the dropdown showing your username), click
  on 'My stepbysteps' to get an overview of the stepbysteps you are responsible of.

- Create your own reports (predefined searchresults) by adding collections and 
  setting their criteria as you wish.

- Use keywords (a.k.a. 'tags'), to classify components 
  (f.e.'bug', 'proposal', etc.).


Behaviours
----------

- The creator of a stepbystep is set as default responsible person.

- Editors are selectable to be responsible person.

- If the reponsible person is changed, s/he will be set as the 
  only local Owner of the Stepbystep.

- Owners get notified via E-Mail of changes made by others.



Fields
------

- Title

- Rich-Textfield (applies your TTW-editor) for all the details.

- 'Priority' provides three static values: low, normal, high.

- Responsible person equals the owner of a stepbystep.
  Default is Owner, selectable are all locally assigned (via sharing-tab) Editors,
  also inherited ones.
  Will ne notified, if changes are made on a stepbystep by another person.


Workflow
--------

- States: new, invalid, confirmed, postponed, finished successfully
  
  Transitions: close, confirm, postpone (sleeping mode with given date possible?),
  reject.
  
  Permissions: We have the four common permissions:
	Access contents information
	Change portal events 
	Modify portal content
	View
  granted on all states for editors and no 
  permisssion-conditions in the transitions.
  ---> As workflow for our type.


Content rules
-------------

A contentrule is assigned on siteroot and informs the responsible
person of a stepbystep via E-Mail, if the stepbystep was modifed by someone else.


Stepbystep ID's
-----------
A stepbystep index-number is stored in the registry, 
it is increased by one (+1) on each creation of 
a stepbystep and sets this number as the identifier (id)
of a stepbystep.

This is a convention to ease referencing stepbysteps.

If a user enters an Integer as the Title in any other 
ATContentType, its Id gets 'n' as prefix, to exclude
ambiguity.
