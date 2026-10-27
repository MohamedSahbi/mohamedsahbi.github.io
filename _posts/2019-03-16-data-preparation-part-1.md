---
title: "Data preparation (part 1)"
date: 2019-03-16 16:35:30 +0100
description: "Data preparation is the most time consuming phase in any data related cycle whether you are preparing the data for machine learning model or data mining or BI. I will explain how to prepare the"
tags: [data, datapreparation, DataSerie]
archived: true
---

{% raw %}
Data preparation is the most time consuming phase in any data related cycle whether you are preparing the data for machine learning model or data mining or BI.

I will explain how to prepare the data efficiently by following different steps.

Many people who are starting their career in the data field forget about an important step. They ask for the data and start preparing it straight away.

But before that, you should do some pre-preparation.

First, you need to understand the business logic. Every data analysis task is related to business task.

Ask for explanation and read the available documentation. In addition, meetings with a business analyst in that organization or service/product owners may be required. You gained a lot of time with this step (you would find out that some data are missing afterwards if you skip it or the data structure does not make sense and many random problems)

****Don’t let them convince you that the data is self explanatory.***

Business understanding does not have a simple method to use. You just need to figure out how the business works and most importantly how the data was generated. After finishing this step, ask for the   
needed data to the given task.

Now, we can start the data preparation. To do so we need the metadata.

Collect the metadata

Metadata is the data that describes the data. Having the metadata is a must, if it not accessible you should create it with the help of the data owner.

Metadata helps with identifying the attributes of the data-set, the type of each attribute and sometimes even the values assigned for a concrete attribute.

Data profiling

Data profiling is important to better understand the data. It “is the process of examining the data available from an existing information source (e.g. a database or a file) and collecting statistics or informative summaries about that data”.  Data profiling includes structure discovery, content discovery and relationship discovery. This step makes it easier to discover and choose the needed data. **Also, if similar data are needed for next iterations, you know already how to deal with it and the whole data preparation process becomes more easier.**

Define data preparation rules (optional)

This step applies for big data. Data preparation rules are
the methods of cleansing and transforming the data.

**Why**? Cleaning big data is not a simple task and it’s time consuming. Imagine you delete rows using the value of an attribute as condition, than you find out that the condition is missing something and the size of your data-set is 5TB. That will take you forever to figure out the right condition.

**How**? We use a random sample from our data-set, we cleanse it and transform it. The script that was used to prepare the   
random data sample will be used for the whole data-set.

**The random sample must be valid.** I will write a blog post about generating a correct and valid random sample.

Iterative preparation

Start with the basic cleansing steps that apply for any
dataset. After that you tackle the challenging steps such as dealing with
missing data. Let the data transformation to the end.

In the part 2, we will understand how to deal with missing values and how to get better quality data.
{% endraw %}
