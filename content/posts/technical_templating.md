
+++
title = 'Making Sense of Golangs Templating'
date = 2024-06-01
draft = false
+++

![gopher constructs a ball of light in pixel art style](/templating_technical.webp)

In this article, I want to discuss a flexible approach to templating in Golang. By keeping a flexible approach, I mean my aim is to avoid complicated explanations, in favor of explaining the surface level of the main approaches I see myself, and others take when templating. One of the great parts of Golang is that it strives towards simplicity, and in that pursuit, there should generally be one straightforward way of doing things. When reading many articles, and skimming through other Golang tutorials, I found many ways to approach the same problem of templating correctly in a way I could understand. Thus, this is aimed to take someone who has no experience messing with templating, to a point where they feel confident building any templating with any approach they think is best.

Before diving in, I think the baseline for being able to comprehend what we are doing is: Basic understanding of Golang syntax, as well as some understanding of how an http server works. As well as understanding the structure of HTML syntax.

## Templating Syntax:

template/navbar.html:
```
{{ define "navbar" }}
  <nav>
    <ul>
      {{ range .ListItems }}
        {{ . }}
      {{ end }}
    </ul>
  </nav>
{{ end }}
```

index.html:
```
{{ define "baseDocument" }}
  {{ template "navbar" }}
  {{ template "content" }}
  {{ template "footer" }}
{{ end }}
```
The above syntax contains all of the elements of core templating, at least for the scope of this article. So let us step through this... 

Delimiters: These look like {{ }}, you have leftDelim and rightDelim. What's important here is that whatever is contained within is templating syntax only, and is not part of the typical html document.

Actions: 'define' 'range' 'template'
These actions are declared on the far-left of the delims. While you can add multiple actions within a single set of delims, that is beyond the scope of this article. You may have assertained what these do.
### Define: 

Tells us that we are creating a template, and giving the template a name between parenthises.
```
{{ define "templateName" }}
  <h1>TemplateContent</h1>
{{ end }}
```

Range:
Declare that we will be looping over a piece of data, which we will explain where that comes from soon. In this case we are looping over individual Users. You declare a single User with a . notation. Assume for now that this is just a string containing a user's name.
```
{{ range .UserNames }}
  <p>{{ . }}</p>
{{ end }}
```

Let's see a more gopher-like syntax for this:
```
userNames := make([]string, "john", "jane")

_, currentName := range(userNames) {
  fmt.Println(currentName)
}
```

### Template:
Allows us to reference that an existing template with a name declares within quotation marks should exist here, likely the data is dynamic, or repeated, such as the case with a 'navbar' & 'footer', or dynamic, in the likely case of 'content'.
```
{{ template "navbar" }}
```

Just like that, we have overcome the basic syntax for templating. Just like any tool, there is much more you can learn, but for getting through your first few endpoints, this is more than enough to get you where you're trying to go.

Now, let's turn our attention to the text/template & html/template packages. 

### Simple Folder Structure:
```
projectName
--/cmd
----/server
------main.go
--/internal
----/handlers
------handlers.go
----/router
------router.go
--/templates
----baseTemplate.html
----home.html
----content.html
----footer.html
----navbar.html
```

For the sake of brevity, let's assume main.go & router.go do nothing unusual where templating is concerned. If you haven't used, or seen templates used before, we normally encapsulate them into a single templates directory so we can access them all easily. One alternative to this is to split the templates up into multiple subdirectories, however, you need a reasonably complex project to explain the reason for that level of complexity. If you get to a place where you feel confident with templating in the form I exemplify, I recommend evolving to that point if your project provides good reason for it, but for now, let's get the basics handled.

Now that we have the basic folder structure setup, most of our work will take place in the handlers.go file. Let's make some example code to extrapolate from.

### handlers.go:
```
package handlers

import (
  net/http
  text/template
  template
)

func RenderTemplate(w http.ResponseWriter, templateName string, data []string) {

  template, err := template.ParseGlob(filepath.Join("../templates", "*.html))

  // handle error here

  err = template.ExecuteTemplate(w, templateName, data)

  // handle error here
}

func ServeHomePage(w http.ResponseWriter, r *http.Request) {
  // here, you could go get a list of anything from the database, let's do usernames locally for brevity
  userNames := make([]string, "john", "jane")
  templateName := "home"

  RenderTemplate(w, templateName, userNames)

}
```

Great! If you're anything like me, this is an overwhelming amount of confusion. This might not be 100% of what you're going for, and you need some options to swap out the way I decided to make this happen, with your own style. Let's go over this implementation, how it's functioning, and my reasoning, so you can alter it after I give you alternative options for accomplishing similar tasks with templates. Let's take a look at the main two lines of RenderTemplate, and what they are doing from a high level.

1. ServeHomePage is a handler that can be called by the "/" path. It's job is simply to serve the Homepage to the user. But all of the necessary html to send to the user is in the baseTemplate.html file
2. Why is RenderTemplate in its own function? Because we may have dozens, or trillions of Handler functions that need to render html to the user from templates, so let's encapsulate the logic into its own function so it's readable.
3. What does RenderTemplate do? Its main job is to create the response to the user via the w http.ResponseWriter we pass in in ServeHomePage. We also pass in the name of the template that will serve as the base. In this case, the 'home' template. We also pass in some data, in this case, a slice of strings called userNames. 
4. What is template.ParseGlob()? This functions job is to create a template! Simple as that. In our implementation, we pass in every template from our template directory from the filepath.Join() function. The important part to know is that we retreived *every* template from the templates directory, and placed them into a template. Whether we use every template isn't our concern. We'll leave that work up to the final important line of this function.
5. What does ExecuteTemplate do? This function finds the base template from templateName, in this case the "home" template, and consolidates them all into a single template, discarding unnecessary templates, fills any data in the template we need from the 'data', and sets this as this as the response to send back to the user.

Great! Having a very shallow, high level understanding of the core parts of this application is all we needed for this section. After reading through the above code and abstract, you have the core peices of a templating project together. 

The steps go as follows:

1. handler sets any required data the template will need.
2. handler sets the name of the template we want.
3. handler calls the RenderTemplate function with the response, template name, and data the template will need.
4. RenderTemplate func retreives all the templates we'll need, saving them into a single template.
5. RenderTemplate writes the response by using the base template name, and populating it with any other templates and data required.

No matter how your application may differ, these are the core components of creating a handler. Now is the section where I want to briefly go over the different functions you can use to acheive different results because, undoubtedly, your project will differ from my own in some way. Not to mention, it is very important that you can comprehend what these functions are doing so that you can flexibly adapt your code, even if you plan to follow my project structure 99% of the way, even a small change might seem insurmountable if you don't understand the functions and underlying type structs that they are built on.

### template.ParseGLob:
This has several variations, let's talk about the two I see most often, template.Parse, and template.ParseFiles. 
func (t *Template) Parse(text string) (*Template, error) 

Parse will return a template, just like all of these template-creating functions. It takes in a pure string, which is expected to be a full template. Whether you're writing it yourself, like 
```
var myTemp string = `{{ define "tmpl" }}<h1>A Template Example</h1>{{ end }}`
```

Or you're retreiving a string that has a template within it from a database, it doesn't matter, Parse will search the string for the template, and save it to a template varaible, or produce a non-nil error in the attempt.
```
func (t *Template) ParseFiles(filenames ...string) (*Template, error)
```

This is the variation I often see in tutorials. I am not a big fan of the use of variadic params, I think a simple slice is perfectly readable, so let's take a look at the param:
```
...string 
 ```

In ParseFiles, you pass in the file paths as strings to all the templates you know you'll need. If your "home" template only needs a "footer" and "navbar" template, for example, you can write:
```
template, err := template.ParseFiles("home", "navbar", "footer")
```

Now, let's return to the glob pattern we used earlier:
```
func (t *Template) ParseGlob(pattern string) (*Template, error)
```

This is the method we use to collect and parse all templates found within a glob of files (a glob is a pattern used to match file names). Functionally performing the same task as ParseFiles and Parse, but if you have a large number of templates (Even medium sized websites may have 10+ templates, and you don't want to have to name them each with ParseFiles every time you make a handler). Since tutorials are normally demos, this is the template-creator that I see used least often.

Now we have a variety of options for creating a template. Now we have made a template, but what have we created exactly? A slice of templates? A map? When we want to manipulate these templates, what are our options? These were the first questions I asked when encountering a template, especially for debugging, and making sure the correct templates were created. I'll say that your intuition was wrong on all accounts... At least mine was. Instead of a map or slice, we created a parse.Tree . Before encountering this, the only exposure I have had to trees were the vague understanding that the DOM is a tree of Nodes. Now that we are here, I won't include an image, but simply say it looks much like a family tree. Our tree is made up of template nodes containing the contents of the template, a description of the template type (such as a normal template, from defining a template, or a template type like range, which needs to be treated differently than other templates, for example), and some other specifics. However, let's continue to dig into the next stage of templating, which is going from this parse.Tree structure of templates, to making the final HTML output, with the correct data matched in to the user.

While there are many ways to create html files to send to the user, ways to create data, there is really only one way to send a template to the user. Once you have a base template, in our case, "home", we perform the function ExecuteTemplate. Let's take a look at it:
```
func (t *Template) ExecuteTemplate(wr io.Writer, name string, data any) error

```

Our method is performed on a template. Returns an error for us to check if/when things behave unexpectedly. Taking in an io.Writer, which I have never strayed from the http.ResponseWriter, which matches the io.Writer interface, this way we map the template to our response to the user. We give the name of our base template, because as of now, the template we are calling template.ExecuteTemplate on, does not distinguish, or understand which of the templates in the parse.Tree is the base template, it simply grabbed them all. Once it knows the base template, it begins filling the response with the contents of the base template, when that template requests more information, such as .Email, it will look in the data for that field. When it sees: {{ temaplate "footer" }}, it will search through the tree for a template with the name "footer", and attempt to slot that in.

While ExecuteTemplate does a lot of heavy lifting, this is the basic high abstraction layer of what's happening. It's ingenious and beautiful how simple it is from that surface layer. I hope this has given you some deeper insights to the methods and types used the the text/template & html/template packages. I have always found a thorough dive into the documentation of a package, and understanding the methods, functions, and types, to be the pinacle of turning a tutorial into something useful. A tutorial is only as helpful as it is specifically tuned to showing the results you are trying to create. If the tutorial shows you how to make a Netflix Clone, and your goal is to make a Netflix Clone, it's probably a great tutorial. However, if you're following a Netflix Clone, and your goal is to make a video streaming platform, it will fall miles short of your expectations, because I very rarely find even the simplest of tutorials, to be good for much more than seeing code examples. Code examples without understanding, and options, is a recipe for becoming stuck debugging code you don't understand. The only way you can debug code is by understanding it, which is why the entire developer community fights against 'tutorial hell', and more and more, I think we'll see a new war again 'debugging code in AI hell', which is where you introduce complex bugs in code that not even ChatGPT understands anymore. I think this is a significant danger, and it's part of what I am hoping I can use this blog to confront. A persistent push to help people find documentation more approachable.