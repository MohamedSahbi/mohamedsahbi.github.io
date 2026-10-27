---
title: "Raw queries with Entity Framework Core"
date: 2019-05-22T19:10:10+01:00
description: "tl;dr In this blog post, I showcase how to migrate raw SQL query from Entity Framework 6 to EF Core 2.1 and EF Core 3.1. You can find the whole sample in GitHub . I"
tags: ["ASP.NET CORE", "C#", "EFCore", "Entity Framework Core"]
archived: true
---

## tl;dr

In this blog post, I showcase how to migrate raw SQL query from Entity Framework 6 to EF Core 2.1 and EF Core 3.1. You can find the whole sample in [GitHub](https://github.com/MohamedSahbi/RawQueryWithEFCore/).

I have been working lately on project migration form ASP.NET MVC 5 that is using Entity Framework 6 to ASP.NET Core 2.1 with Entity Framework Core 2.1. During the work, I found a raw query implemented in Entity Framework 6 as following (not really):

```csharp
public async Task<double> GetScore(int studentId)
{
    string query = @"select ((e.Grade * c.Credits)/sum(c.Credits)) as Grade
                                        from Enrollment e
                                        inner join Course c
                                        on e.CourseId = c.CourseId
                                        where studentId= @studentId
                                        group by e.Grade, c.Credits";

    var studentIdParam = new SqlParameter("@studentId", studentId);

    var gradeList = await _universityContext.Database
        .SqlQuery<int>(query, studentIdParam).ToListAsync();

    if (gradeList.Count == 0)
    {
        return 0;
    }

    return gradeList.Average();
}
```

Meanwhile, it is not possible to do so in Entity Framework core. I have to look for solutions and I found 2 of them:

The first solution is a simple implementation with ADO.NET, you can find it in my [github account](https://github.com/MohamedSahbi/RawQueryWithEFCore/blob/master/SampleWithEFCore/SampleWithEFCore/Repository/StudentRepository.cs): method `GetScoreAdoNet(int studentId)`. However, I try to avoid ADO.NET because of internal rules in our team and mainly for maintenance reasons.

So, I kept looking for another solution using Entity Framework Core. Thanks to the great community in stackoverflow, I found [this answer](https://stackoverflow.com/a/53517813/5394806) for my problem. Here is the second and better solution :

### Solution for EF Core 2.1

I will be using [Query types](https://docs.microsoft.com/en-us/ef/core/modeling/query-types) proposed by Entity Framework Core.

First, we have to create a data model that will be used as return type of the executed SQL query. Although in my sample ([here](https://github.com/MohamedSahbi/RawQueryWithEFCore/blob/master/SampleWithEFCore/EF6/Repository/StudentRepository.cs)), I just return a number (**int**), I have to create a model that has one property. The name of the property should be the same name of the column selected in the SELECT Statement.

```csharp
 public class AverageGrade
    {
        public int Grade { get; set; }
    }
```

Then, we need to configure it in the dbcontext in the method **OnModelCreating**

```csharp
modelBuilder.Query<AverageGrade>();
```

And finally we can call the raw SQL query:

```csharp
public async Task<double> GetScore(int studentId)
{
    string query = @"select ((e.Grade * c.Credits)/sum(c.Credits)) as Grade
                                        from Enrollment e
                                        inner join Course c
                                        on e.CourseId = c.CourseId
                                        where studentId= @studentId
                                        group by e.Grade, c.Credits";

    var idParam = new SqlParameter("@studentId", studentId);

    var gradeList = await _universityContext.Query<AverageGrade>()
        .FromSql(query, idParam).ToListAsync();

    return gradeList.Select(x => x.Grade).ToList().Average();
}
```

### Solution for EF Core 3.1

Starting from EF Core 3.0, the proposed solution for EF Core 2.1 is obsolete. It is part of many changes in EF Core 3.0 that you can find [here](https://docs.microsoft.com/en-us/ef/core/what-is-new/ef-core-3.0/breaking-changes#query-types-are-consolidated-with-entity-types).

A data model is needed for the output of the executed SQL query, same like in EF Core 2.1 solution.

```
public class AverageGrade
    {
        public int Grade { get; set; }
    }
```

The next step is adding the data model to the ModelBuilder in the method **OnModelCreating** :

```
modelBuilder.Entity<AverageGrade>().HasNoKey();
```

The last step is to use `DbContext.Set<>()` instead of `DbContext.Query<>()` in the method `GetScore(int studentId)`. In other words, the line number 12 (in the last code block in the Solution for EF Core 2.1) is replaced with this line of code:

```
var gradeList = await _universityContext.Set<AverageGrade>().FromSqlRaw(query, idParam).ToListAsync();
```

That's it, migration was done successfully.

***The Query Types have some limitations. In case you will be using them, please read*** ***[the official documentation](https://docs.microsoft.com/en-us/ef/core/querying/raw-sql#limitations).***

Finally, I prepared 3 projects, one with Entity Framework 6, the second with Entity Framework Core 2.1 (the first 2 projects use ASP.NET Core 2.1), and the third one with EF Core3.1. You can find the code source in [GitHub](https://github.com/MohamedSahbi/RawQueryWithEFCore/).
