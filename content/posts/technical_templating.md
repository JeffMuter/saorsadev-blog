
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
ParseGlob - parses many different files, pulls out the templates, and merges them into a single template
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

. Notation: In each template, may contain data.
Like any struct, there are fields, that are set by the handler. These fields can be any data type, including other custom structs. While fields can look as simple as .ImageUrl (string containing the url for an image), they may also become complex when accessing a struct with its own fields: 

{{ range .User.Calendar.PastEvents. }} // range through this User, which has a Calendar type, which has a slice of PastEvents types, each of those with fields of their own, but we'll grab those through the range.
  {{ .Title }} //grab the title of the individual past event
  {{ .Date }}
  {{ .Time }}
  {{ .Notes }}
{{ end }}

Now let us shift to talking about the process of dissecting templates for creating a Template type. There are 3 main functions I see when most developers use, or make tutorials on this process:
ParseFile
ParseFiles()
ParseGlob(string filename)

We also may need to dig into the template.Template type,
Understanding the type reveals a lot of the functions built around it. So here it goes.
the template.Template type has many core features. After diving into the source cody myself, I decided to leave much of it off for the sake of brevity. 

type Template struct {
  name string // name of the template
  *parse.Tree // an AST (abstract syntax tree). Basically contains a name, a list of nodes, and other information. Nodes come in several forms, but they are categorized into Action nodes, and Element nodes. The latter being the node structure for an HTML document, the Action nodes handle the different types of control structures, like when you see 'range' in delims: {{ range .Users }} {{ . }} {{ end }}. This structure allows template.Execute to perform the heavy lifting after the template is setup.
  *common // complex functionality. Important for me that it contains a map[nameofFunction]reflect.Value  reflect.Value contains an excecutable function, nameofFunction contains the text string you'll find as a flag in a template delimiters like {{ length . }}, length corresponds to the function excecutable in the map, such as func length(s string) int { return len(s) }, in this case, . represents the string param for length. Needless to say, this feels complex to look at, and I have yet to run into a situation where this is populated with anything of note.
  leftDelim string // looks like {{
  rightDelim string // looks like }}
}

After the parsing that occurs from one of the parsing functions (ParseFile, ParseFiles, ParseGlob), it creates a tree that contains individual branches that contain each template. Once all templates are contained in a single text string, a function like template.ExecuteTemplate handles the final step to turn the parse.Tree into an html


In this article, I want to discuss a flexible approach to templating in Golang. By keeping a flexible approach, I mean my aim is to avoid complicated explanations, in favor of explaining the surface level of the main approaches I see myself, and others take when templating. One of the great parts of Golang is that it strives towards simplicity, and in that pursuit, there should generally be one straightforward way of doing things. When reading many articles, and skimming through other Golang tutorials, I found many ways to approach the same problem of templating correctly in a way I could understand. Thus, this is aimed to take someone who has no experience messing with templating, to a point where they feel confident building any templating with any approach they think is best.

