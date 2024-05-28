
+++
title = 'Simplifying Middleware in Go'
date = 2024-05-28T23:00:00-00:00
draft = false
+++

I want to discuss some of the discoveries, and challenges, I ran into while building a Golang http web server, and making the authentication part of the application. Since I have not been using any frameworks, the process does get a bit deep, far moreso, comparatively to the ease by which other frameworks and languages remove the technical details of an application via abstractions. However, I stand by the idea that understanding a process without abstractions, is the best way to approach bugs, foreign code(code you are unfamiliar with), and also helps you to pick up new concepts quickly when encountering something novel.

`mux.HandleFunc("/", handlers.ServeHomePage)`

This line of code is typically found in a 'routes' package, and HandleFunc takes two arguments:
1. A string definining the endpoint
1. A 'Handler' is a function that takes in a user's request data, and allows us to craft a response.

First, this isn't entirely intuitive to someone who's never made an http server before. So allow me a brief moment to describe the issue.

A user may type https://www.yourwebsite.com/home

What your server sees, once the request has arrives, is '/home'. The server will look for a match, and, if found, will need to create a response. More info may have come to the server, which we call a 'request'. So the server receives a request, and needs to generate some kind of response. Which is where the idea that all of the internet is built around the concept of 'request' and 'response'. If you can get those concepts down, the rest is left to software engineering.

I mentioned that the route needs a 'Handler'. A Handler in this case, is an interface. The Handler interface is very simple. No matter what it is, as long as it has a method of ServeHTTP(w http.ResponseWriter, r *http.Request), it is a Handler! In every case I have ever seen, Handlers are functions, but this is not guarunteed. For as long as we are using a Handler, we can guaruntee we have received the request from the user, and we have an http.ResponseWriter available, to craft our response. Here are the 3 jobs of a 'Handler':

1. assign the correct http status code (200 or 404)
1. write the response headers
1. write the response body

Now that we have learned the high level basics of creating a handler, and what http.HandleFunc() does, let's dive into the meat of what most people find confusing when authenticating routes. Middleware, and http.HandlerFunc().

I think Golang is a fantastic language, it gives you some tools that are very flexible, which allow the language to accomplish some amazing tasks, if you use them wisely. Creating custom types can visually be a little confusing, and then the syntax for a custom type that has a single field that is a function, which has its own parameters, can feel very jarring. I think while building a web server, if this is the first time approaching both of these concepts in the syntax, it can lead to a lot of mental friction. It certainly did for me!

let's define a type...

`
    type ourNums struct {
        wholeNum   int
        decimalNum float32
    }
`
This doesn't look too confusing. We have a type called 'ourNums' which has 2 fields. Now, generally, I am not a fan of multiple ways of writing the same code. We'll call the first method 'alias type' and the second 'struct type'.

`
    types ourNum int

    var newNum ourNum = 1

    type ourBool struct {
        isTrue bool
    }
    var makeBool ourBool{isTrue: true}

`
Not too bad! The second method is the same way you would create and declare types with multiple fields. The alias type instanciation has a very slight benefit on performance, if you are shooting for high performance, this is once of those times where you would want to use alias type. However, readability is important. However, I think while the alias type is not as intuitive as the struct type, either in instantiation or declaration, once you understand the concept, it is no more difficult to understand that the various ways to declare variables.

Let us now take a look at the http.HandlerFunc type:

`
    type HandlerFunc func(ResponseWriter, *Request)
`

When unfamiliar with what a handler is, how types are made, I think this becomes horribly confusing to look at. The first thing we want to do, is understand what HandlerFunc is trying to accomplish... We have a need to create a function who's job is to perform an action before the handler is called, to keep this simple, let's isolate this to just our use case. We may have dozens, or hundreds of routes. We need to authenticate some, or all of them. While we could rewrite authentication code inside each of these, that will add a lot of extra, unncecesary code. So we encapsulate this logic in a 'middleware' package. The middleware to authenticats's job is to authenticate the user, and if they pass, we excecute the corresponding handler, if if fails, we must write a response, and handle what to send back seperately.

So, looking back at HandlerFunc. We have a type that has a single field, which is a function which looks a lot like our Handler type from earlier. Why have all the lengthy syntax of declaring http.HandlerFunc to have a parameter of a function, if that function is a Handler type? Why not say:

` type HandlerFunc Handler `

This is because, not all Handler types are functions! While I mentioned breifly earlier, since this is not guarunteed, to drastically simplify our code, http.HandlerFunc() has explicitly declared that it only deals with functions! http.HandlerFunc() type even comes with its own http.Server.HTTP() method, so that HandlerFunc() is a Handler() interface type as well!

So let's look at a practical example of HandlerFunc in action!

`
func Router() *http.ServeMux {
	mux := http.NewServeMux()

    //example of unprotected route
	mux.HandleFunc("/post", handlers.ServePostPage)

    // protected route
	mux.Handle("/", middleware.AuthMiddleware(http.HandlerFunc(handlers.ServeHomePage)))

    return mux
}


func AuthMiddleware(handler http.HandlerFunc) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        // check if user has valid jwt or cookie
        // if the jet is invalid, send them to a login page, with failure message
        // if the user is validated, send them to the handler we would like to!
    }
}
`

This code above has a few steps that aren't important, so we will use commented pseudocode!

The important bits, are to see how the router protects a route, and then how AuthMiddleware works! Let's take a look at that now.

AuthMiddleware takes in a HandlerFunc type as a parameter, and then returns a Handler interface type as a return value. Since we're returning a Handler, we can use AuthMiddleware function as the function value passed into mux.Handle(). The main job of AuthMiddleware is simply to add a layer of authentication, and handle what happens based on success or failure.

Now that we have put all the peices together, we have a comprehensive view of how Middleware works, and how the different types, interfaces, and functions work to create safe, and effective middleware! 