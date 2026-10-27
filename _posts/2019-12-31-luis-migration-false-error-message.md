---
title: "LUIS Migration – False Error Message: Module {..} already exists"
date: 2019-12-31 11:44:54 +0100
description: "How to solve the error \"BadArgument: The models: {  } already exist in the specified application version.\""
tags: [AI, Azure, Cognitive Services]
archived: true
---

{% raw %}
Here I am back with another story from my daily work problems. We have been using Language Understanding (LUIS) for one of our solutions for a while. Recently, Microsoft made some upgrades and created a new platform that benefits from resource authoring based on Role-Based Access Control (RBAC), Azure Active Directory (Azure AD) and custom domains. So, we had to migrate our LUIS app. And that did not go well.

For those who are not familiar with LUIS, Azure offers Azure cognitive services offer a set of REST APIs that helps you build intelligent applications without the need to develop your own models with Machine Learning or Deep Network, etc. One of these services is Language Understanding (LUIS). It is a cloud-based API service that applies custom machine-learning intelligence to natural language text to predict overall meaning, and pull out relevant, detailed information. For more details, check the official [site](https://azure.microsoft.com/en-us/services/cognitive-services/language-understanding-intelligent-service/).

The Luis portal is being changed because it cannot keep up with Azure services. So, Microsoft decided to connect the new upgrades with creation of a new portal. The bad part is that every user, who has been using the old portal, has to migrate to the new one by himself/herself, so that it decommissions the old portal by June 2020. See the unofficial announcement here <https://github.com/azure-deprecation/dashboard/issues/26>.

To help with the Migration Microsoft offered some documentation such as this one <https://docs.microsoft.com/en-us/azure/cognitive-services/luis/luis-migration-authoring>.

We decided to export the application from the old portal and add it to the new portal. In other words, we are not following Microsoft’s migration workflow because it is not the smartest for a professional environment. We chose the best approach that is possible to keep the solution in production running with the LUIS app in the old portal. Meanwhile, we create another one in the new portal and hoping that everything goes smooth.

(For the demo, I used [Travel Agent Sample](https://github.com/microsoft/LUIS-Samples/blob/master/documentation-samples/Examples-BookFlight/travel-agent-sample-01.json) from the samples provided by Microsoft)

So, we started the migration process and it did not go as planned (like always). When importing the application, we had this error message:

> BadArgument: The models: { BookFlight } already exist in the specified application version.

![](https://mohamedsahbicom.files.wordpress.com/2019/12/luismigrationdemo.gif?w=1024)

Figure 1 : Import Application

The error message does not say a lot. “The models” literally does not make any sense in this context or in the context of LUIS. **BookFlight** is the name of an intent and an entity in the imported application. That is what caused the error. The new platform does not accept same name for an intent and an entity, so we had to rename it.

A good error message can be something like this:

### You cannot assign the same name for an entity and an intent. Please use a unique name for the intent {BookFlight}

(I have no idea why we have it like that, the LUIS application is there for more than 2 years, literally before I joined my team, but this is not an excuse.)

Such a small issue took us some hours and an effort of 3 persons with troubleshooting it.

There are 2 solutions for this problem:

1. Make sure that each intent has a unique name. The name must not be used in entities or any other part of the application. **(This is the best solution)**
2. Rename the entity, but also the pattern if you are using one

To retrace the error, upload the application that is provided in this GitHub repository. An other option to retrace the error is by adding an entity with the name of an existing intent or the other way around.

![](https://mohamedsahbicom.files.wordpress.com/2019/12/image.png?w=1024)

Figure 2: Create new entity

To recap, we saw how a wrong error message looks like and how to fix the error (in case you had the same error). Check out also my blog post [Fix a gap in GitHub API v4](https://mohamedsahbi.com/2019/12/24/fix-a-gap-in-github-api-v4/). Well if you read to the end, thank you very much for your support. Wishing you a Happy New Year!
{% endraw %}
