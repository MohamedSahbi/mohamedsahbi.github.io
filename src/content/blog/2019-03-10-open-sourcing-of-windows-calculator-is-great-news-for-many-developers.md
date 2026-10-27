---
title: "Open Sourcing of Windows Calculator is great news for many developers"
date: 2019-03-10T14:51:28+01:00
description: "Microsoft announced on Wednesday 6 th of March 2019 that it made Windows Calculator an open source software (you can find it on GitHub ). Suddenly, the internet went crazy with memes and posts mocking"
tags: ["Microsoft", "open source"]
archived: true
---

Microsoft [announced](https://blogs.windows.com/buildingapps/2019/03/06/announcing-the-open-sourcing-of-windows-calculator/) on Wednesday 6th of March 2019 that it made Windows Calculator an open source software (you can find it on [GitHub](https://github.com/Microsoft/calculator/tree/master/src/Calculator)). Suddenly, the internet went crazy with memes and posts mocking the last announcement judging it as a small piece of code, it’s not worth it and blah blah blah.

![](/images/wp/2019/03/image.png)

Figure 1: Windows Calculator. *source: me*

I understand why some people are frustrated and see it as a small project and it is not worth it when comparing the project size with .NET or VS Code, but these people are narrow-minded. They did not look at it from a different angle. Well, let me explain the real value of the Windows Calculator in the open source world.

The calculator is a
simple project that new developers and students make as one of their first
projects, and they feel proud of it (at least I was proud of my Calculator
project). You start with simple operations, but you find out that Parsing is
needed and some conditions are a must so that the app does not crash.

![](/images/wp/2019/03/students-99506_640.jpg)

Figure 2: young boys on computers. *source: [pixabay](https://pixabay.com/photos/students-computer-young-boy-99506/)*

Later on, complex operations can be added and the real dev
problems appear, such as different
results using different types (Float vs Double vs Decimal), or saving the last operations.
And it keeps getting bigger and bigger. At this moment, beginners don’t know how
to choose the right project structure or how to improve their code and write
clean code. Imagine you have the source code of the most used calculator in the
world made by the biggest Software Company worldwide! That’s insane.  Wait! Microsoft offered more than source code,
it included the project Architecture, unit tests, and the build system.

The Application Architecture is useful even for junior
developers and students. Solid use of the
MVVM design pattern in a real application
is helpful to plan their first applications.

Moreover, the Calculator application is written in Visual
C++ (C++/CX), a set of extensions to the C++ language using for Win Apps and Win
Runtime components, which is a solid programming language and it most students
in universities have C++ classes. Microsoft offered them the semestral project
to have great grades :D This is just joke, do not do it if you are a new learner,
do it yourself and then you can compare your work. That way, you improve your
skills and it is great to learn from your own mistakes 😉

 Windows calculator is
built for the Universal Windows Platform using **XAML** UI framework. Developers
can learn more about making their own custom controls and **VisualStates**,
and that comes in handy for creating and publishing apps in Microsoft Store.

Finally, they won’t stop in the development phase, but they will learn Azure Pipelines for the build,
deployment and release phases. This is so important because it can be hard to
apply CI/CD in the first projects.

![](/images/wp/2019/03/hands-2227857_640.jpg)

Figure 3: thumbs up. *source*: *[pixabay](https://pixabay.com/photos/hands-fingers-positive-bracelets-2227857/)*

To conclude, the Windows
Calculator is the best example to learn Microsoft’s
full development lifecycle.
