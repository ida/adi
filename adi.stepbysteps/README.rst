TODOS:

- On site crea throws "KeyError linkable", seems not configurable,
commented out in tinymce.xml for now, added manually in controlpanel.


Step by step
============

What
----

A Plone-addon for managing processes, including collaboration,
setting priority, track time (new, paused, playing, stopped),
assign responsibilities and get overviews and reports.

Why
---

- There are a lot of ticket-systems I have met, they all sucked in
representing priority, cluster tickets as subtickets of a ticket,
and assigning user-permissions. The latter is Plone's strength, let's
take advantage of it. Priority is represented by the hierarchy of
the steps, meaning if a step, respectively process, contains at least
one other step, that one must be finished first, before the parent
can be finished. Otherwise, if there are no children-steps, the
order inside of the folder rules, so for changing priority of a step,
change the order or add and remove substeps. For clustering subtasks,
add substeps.

- Because multi-tasking is a myth, as it is provenly not
possible to focus on several things at once. Provide a tool, helping to
enforce doing things step by step and focus with devotion on each step,
one at a time, by inhibiting to be active on several steps at once.

- Be fully functional, also when Javascript is not available or disabled
in the browser, enhance progressively.

- Navigate quickly through items by using the tab-key and when hitting
a selected item, show children and also grand-children, if tabbing further.
Tabbing backwards after page-load, will focus the edit-buttons at bottom,
immediately. You can also use the mouse and click your way, of course.


How
---

After installation (see docs/INSTALL.txt), add a step, name it after your
project or anything you like and add more steps in it.
The moment a step contains steps, it is regarded to be a process.


Usage
-----

- Install and add items of type 'Step', set permissions for other users,
via the sharing-tab.

- Every step has at least one responsible person to take care of it, by default
it is the creator of the step, you change it in edit-mode of step,
by clicking the persons-tab and enter the wanted username in the field
'Responsibles'. More persons can be added, seperate usernames with a linebreak,
first username is regarded to be most responsible, can have a seconder, a.s.o.

- When you start working on a step, click the 'Play'-button, when you make a break,
click the 'Pause-button', when you return to work on it, click 'Play' again, until
you're finished, then click the 'Stop'-button.

- A stepbystep is folderish, thus you can add to it:

    - Files as attachments (screenshots, tracebacks, PDF's, etc.)

    - More Stepbysteps for splitting things up in subtasks.

    - Pages for documentation.

    - Any other content-type available in the Plone-site.

Only steps and files will be shown in a step's view.

- In your personaltools (the dropdown showing your username), click
  on 'My stepbysteps' to get an overview of the stepbysteps you are responsible of.

- Create your own reports (predefined searchresults) by adding collections and 
  setting their criteria as you wish.

- Use keywords (a.k.a. 'tags'), to classify components 
  (f.e.'bug', 'proposal', etc.).


Behaviours
----------

- The creator of a stepbystep is set as default responsible person.

- Reporters get notified via E-Mail of changes made by others.


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
