# Validation

### **HTML**

W3C HTML validator returns the Jinja templating as bad values, such as {{ url_for }}, {% if ... %} and missing DOCTYPE etc. These errors (like below) can be ignored:

![](documentation/screenshots/errors.png)

This list contains errors that were immediately fixable within the HTML.

---

### ***Error handling pages***

Errors produced:

* All three (403.html, 404.html and 500.html) produce the same error messages which are flagging Jinja as incorrect syntax

Action taken:
* Ignore

### ***all-groups-members.html***

Errors produed:
* Stray ``` </a> ``` tag
* End tag ```div``` seen, but there were open elements
* Unclosed element ```div```
* Unclosed elemnt ```div```

Action taken:
* HTML fixed and errors resolved

### ***base.html***
Errors prouced:
* Stray end tag ```i```

Action taken:
* HTML fixed and errors resolved

### ***contact.html***

Errors produced:
* A slash was not immediately followed by ```>```
* Element ```p``` not allowed as child of element ```i``` in this context
* End tag ```div``` seen, but there were open elements
* Unclosed element ```i```
* Unclosed element ```h3```
* Duplicate attribute ``id`` (3x)

### ***create-group.html***

No errors produced, no action needed

### ***edit-group***

No errors produced, no action needed

### ***edit-profile***

Errors produced:
* The value of the ```for``` attribute of the ```label``` element must be the ID of a non-hidden form control

Action taken: 
* HTML fixed and errors resolved

### ***group.html***

Errors produced:
* Stray end tag ```span```
* Stray end tag ```textarea``` (2x)
* Stray end tag ```input``` (2x)
* Bad value for attribute ```action``` on element ```form```: Must be non-empty
* An ```img``` element must have an ```alt``` attribute, except under certain conditions
* Stray end tag ```a``` (3x)
* Unclosed element ```div```

Action taken:
* HTML fixed and errors resolved










