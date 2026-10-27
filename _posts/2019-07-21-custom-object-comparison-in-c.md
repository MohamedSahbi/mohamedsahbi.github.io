---
title: "Custom Object Comparison in C#"
date: 2019-07-21 16:33:59 +0100
description: "A while ago, I needed to compare complex objects in C#. I forget to mention the real reason when I wrote the article and thanks to the feedback that I got, here is the main"
tags: [.NET Core, C#]
archived: true
---

{% raw %}
A while ago, I needed to compare complex objects in C#. I forget to mention the real reason when I wrote the article and thanks to the feedback that I got, here is the main reason: Not only a Boolean result is needed from the comparison but also I need to have as output the properties with different values and the possibility to exclude properties from the comparison, . I looked for such function that would provide the same functionality of string.Compare() but for complex objects of the same type. [Object.Equals()](https://docs.microsoft.com/en-us/dotnet/api/system.object.equals?view=netcore-2.1#System_Object_Equals_System_Object_) Method alone did not satisfy my need and it needed an implementation and overriding of the method which was not convenient. My next stop was **stackoverflow** and I found quite interesting approach in this [discussion](https://stackoverflow.com/questions/42809686/c-sharp-compare-two-objects-for-properties-with-different-values). That did not satisfy my need to the fullest so I took it as a start point and I had to implement my own comparison class (the implementation is available on [GitHub](https://github.com/MohamedSahbi/ObjectComparison) with a running sample).

I created a static class [**Comparer**](https://github.com/MohamedSahbi/ObjectComparison/blob/master/ObjectComparison/Comparer.cs) with a constraint on the generic parameter to a class which satisfies my need. If you do not know what do constraints on type parameters mean, go to [Microsoft docs](https://docs.microsoft.com/en-us/dotnet/csharp/programming-guide/generics/constraints-on-type-parameters) (I recommend reading it and understanding what it is and why it is used because you will need it for sure). Then, reflection was the choice to get things done. [PropertyInfo](https://docs.microsoft.com/en-us/dotnet/api/system.reflection.propertyinfo?view=netcore-2.1) class which belongs to [System.Reflection](https://docs.microsoft.com/en-us/dotnet/api/system.reflection?view=netcore-2.1) namespace was enough to do the work. This class allows us to get the different attributes of a property of an object and its metadata which I use to compare the properties of the 2 objects.

The created class offers different methods that you may find helpful :

`GenerateAuditLog()`method literally generates log. It returns an object of type **ComparisonResult** which can be inserted into logHistory table in your database. This method is overloaded so that you can exclude some properties from the comparison.

`GenerateAuditLogMessages()`method returns a **list** of messages that contains only changes. There is no overload for this method.

`HasChanged()` method simply returns **Boolean** result. You can eventually exclude some properties from the comparison. I found this method useful for updating records in the database.

That is all!! I hope you find it useful. Feel free to use the code or improve it.

**Note:** The code is not optimized (no [DRY](https://en.wikipedia.org/wiki/Don%27t_repeat_yourself) approach) because I take in consideration people who wants to use one method so they can copy the code simply (I personally recopy my code, improve it and adopt it to the case that I have).
{% endraw %}
