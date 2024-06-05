
+++
title = 'Techincal: Templating in Golang'
date = 2024-05-31
draft = true
+++


this blog is meant to act as a draft for a post, and my learnings, on Go templating so I can learn it better and implement what I am learning for the web server project at work.

What is a 'pipeline'

Create a template:
{{ define "templateName" . }} <h1>Stuff inside the template</h1> {{ end }}
define is best used when you have a static piece of information, like a navbar, or footer, that doesn't change between pages.
{{ block "templateName" . }} <h1>Another template, using block shorthand.</h1> {{ end }}
block is used for pages that do have customized data

Understand:
Functions:
Parse - parses a string into a template
ParseFile - parses a file contents into a template
ParseFiles - Same as before, but multi-files
Execute 
Must
New - Creates template 
t := template.New("name")
Found it mildly important to consider, that if a template with the specified name exists, it we be replaced. So be careful in loops.

Creating variables in templates
You can actually create variables in templates. Can be useful if you are ranging, or any other scoped action that limits access to fields.
{{ $name .Name }}
{{ range .Email }}
  {{ $name }}: {{ . }} // in the range, you can't access {{ .Name }}, as it's out of scope.
{{ end }}
// look into how scoping works in templates. Not 100% sure why {{ .Name }} is out of scope.

? the syntax .  seems to have special meaning. We use it to nab values like .FieldName , but we use it in ranges like:
{{ range .Email }}
  {{ . }}
{{ end }}

I'd like to understand the . , why can it be alone on its own? I understand in a range, it stands for a single Email, since Email is going to be an array, slice, or map. Apparently, the . in the range is 'occupied' by the values inside the Email field. Want to look more into it.