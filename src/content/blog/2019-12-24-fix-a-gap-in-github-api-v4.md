---
title: "Fix a gap in GitHub API v4"
date: 2019-12-24T00:15:30+01:00
description: "In this blog post, I want to show you how I solved the problem of getting commit files content with GitHub GraphQL API (v4) and to avoid using the GitHub REST API (v3) with its"
tags: ["ASP.NET CORE", "C#", "GitHub"]
archived: true
---

In this blog post, I want to show you how I solved the problem of getting commit files content with GitHub GraphQL API (v4) and to avoid using the GitHub REST API (v3) with its crazy amount of API calls. The solution is available in this [GitHub Repository](https://github.com/MohamedSahbi/GitHubAPIDemo).

If you want the solution straight away , click [here](#solution) to skip the explanation of the problem.

![](/images/wp/2019/12/octocat.png)

GitHub Octocat (*source:* <https://github.com/logos>)

GitHub is the most famous code-hosting platform for version control and collaboration. It is essential for all IT people. One of the best features of GitHub is the offered APIs to manipulate the content and integrate GitHub in a workflow such as CI pipeline. It offers two versions of API: GitHub API v3, which is a REST API and GitHub GraphQL API v4. These are the current two stables API versions. (If you are wondering about the previous versions, you can get some information in [GitHub documentation](https://developer.github.com/v3/versions).

The GitHub REST API v3 covers “all” (or almost, I am not sure) areas. However, tons of API calls need to be made in order to satisfy a workflow job. Therefore, GitHub decided to replace REST API with GraphQL in the version 4 and this is why:

> GitHub chose GraphQL for our API v4 because it offers significantly more flexibility for our integrators. The ability to define precisely the data you want—and only the data you want—is a powerful advantage over the REST API v3 endpoints. GraphQL lets you replace multiple REST requests with a single call to fetch the data you specify.
>
> GitHub documentation, <https://developer.github.com/v4>

However, the new API (GraphQL API v4) did not solve the problem 100%. It still has some gaps and it does not cover all areas. You may need to go back to the version 3 to satisfy a given job.

***Disclaimer: I was novice to GitHub API and GraphQL when I started working in this project.***

I was working in a project that integrates GitHub in one of its processes. I chose the GraphQL API v4. Everything was going smooth until I had to get the content of the last commit.  Google helped a bit sometimes and [github.community](https://github.community/) forums too (not well referenced in Google). I looked for a way to get the content of a given commit with GraphQL, I thought that it was an obvious thing; I managed to create this graph with the provided documentation.

*If you are novice to GraphQL, you can start your learning journey here [graphql.org/learn](https://graphql.org/learn/) and I recommend the query editor GraphiQL : the GitHub repository [github.com/skevy/graphiql-app](https://github.com/skevy/graphiql-app) / download page [electronjs.org/apps/graphiql](https://electronjs.org/apps/graphiql)*

```
{
   rateLimit{
    cost
    remaining
  }
  repository(name: "GitHubAPIDemo", owner: "MohamedSahbi") {
    ref(qualifiedName: "master") {
      name
      id
      target {
        ... on Commit {
          id
          history(first: 1) {
            pageInfo {
              hasNextPage
            }
            totalCount
            edges {
              node {
                author {
                  name
                  date
                }
                changedFiles
                commitResourcePath
                oid
                abbreviatedOid
                tree {
                  entries {
                    name
                    type
                    oid
                    object {
                      #This is a fragment
                      ...GetAllFiles
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}

fragment GetAllFiles on Tree {
  ... on Tree {
    entries {
      name
      type
      oid
      object {
        ... on Tree {
          entries {
            name
            type
            oid
            object {
              ... on Blob {
                text
              }
            }
          }
        }
      }
    }
  }
}
```

This graph query returns by order:

- The cost of my request in the rate limit section. This is important because every user has a limited credit of 5000 request per hour, but a single GraphQL call can cost 1 credit, 100 credits or more than 5000 credits. For more details, see the explanation provided by [GitHub](https://developer.github.com/apps/building-github-apps/understanding-rate-limits-for-github-apps/).
- The most recent commit details since we choose “history (first:1)”
- The repository content that we chose to get in the section:

```
                tree {
                  entries {
                    name
                    type
                    oid
                    object {
                      #This is a fragment
                      ...GetAllFiles
                    }
                  }
                }
```

What I found it that the commit history does not include the changed files URLs that are provided using the REST API v3. I kept looking for a way to fix my query. I was still believing that it is provided out-of-the-box, but since I am not experienced with GraphQL, I thought I made a mistake in my query.

Then, I lost hope for a while. I decided to query the GitHub repository with REST API v3. To go the content of each file I have to:

- First, call the API endpoint <https://api.github.com/repos/MohamedSahbi/GitHubAPIDemo/commits> which returns a JSON array that contains all the commits. Also, it is possible to return commits starting from a given date using the parameter “since” e.g. <https://api.github.com/repos/MohamedSahbi/GitHubAPIDemo/commits?since=2019-12-22T19:26:44Z> . For more details about this API endpoint, see the official documentation [here](https://developer.github.com/v3/repos/commits/).
- Second, call the same endpoint by specifying the commit hash that we get from the first endpoint call like this: [https://api.github.com/repos/MohamedSahbi/GitHubAPIDemo/commits/<commitHash>](https://api.github.com/repos/MohamedSahbi/GitHubAPIDemo/commits/commitHash). It returns JSON object that includes a precious array `files`that we need for the next endpoint call. However, it includes also data that we already had from the first call, that is the kind of duplicate information that I wanted to avoid with GraphQL query.

```
"files": [
    {
      "sha": "9907549076a9271ee4948e909eb0669d3ba4875b",
      "filename": "LICENSE",
      "status": "added",
      "additions": 21,
      "deletions": 0,
      "changes": 21,
      "blob_url": "https://github.com/MohamedSahbi/GitHubAPIDemo/blob/5f4538bce768c67bcfd3e71cb05a14614657f68f/LICENSE",
      "raw_url": "https://github.com/MohamedSahbi/GitHubAPIDemo/raw/5f4538bce768c67bcfd3e71cb05a14614657f68f/LICENSE",
      "contents_url": "https://api.github.com/repos/MohamedSahbi/GitHubAPIDemo/contents/LICENSE?ref=5f4538bce768c67bcfd3e71cb05a14614657f68f",
      "patch": "@@ -0,0 +1,21 @@\n+MIT License\n+\n+Copyright (c) 2019 Mohamed Sahbi\n+\n+Permission is hereby granted, free of charge, to any person obtaining a copy\n+of...."
    },
    {
      "sha": "7b9e8fe3adf9f784749834da35fecda8a5392bd3",
      "filename": "README.md",
      "status": "added",
      "additions": 2,
      "deletions": 0,
      "changes": 2,
      "blob_url": "https://github.com/MohamedSahbi/GitHubAPIDemo/blob/5f4538bce768c67bcfd3e71cb05a14614657f68f/README.md",
      "raw_url": "https://github.com/MohamedSahbi/GitHubAPIDemo/raw/5f4538bce768c67bcfd3e71cb05a14614657f68f/README.md",
      "contents_url": "https://api.github.com/repos/MohamedSahbi/GitHubAPIDemo/contents/README.md?ref=5f4538bce768c67bcfd3e71cb05a14614657f68f",
      "patch": "@@ -0,0 +1,2 @@\n+# GitHubAPIDemo\n+This repository contains a sample demo for my blog post"
    }
  ]
```

- Third, we loop over the files array and each time we have to:
  - Call the endpoint that is giving in the attribute `contents_url`
  - The previous call returns a JSON object that contains the attribute `download_url`, which is the last API endpoint that we have to call to get the file content (Finally!!!).

Imagine you want to get the updated files in the last commit without knowing the commit hash, that is:

**2 API calls + (2 * number of updated files) API calls >= 4 API calls**

The duplicate data, the useless extra information in the JSON responses, and the huge number of endpoint calls to get files content pushed me to keep looking further for a better solution. I kept looking until I found [this post](https://github.community/t5/GitHub-API-Development-and/GraphQL-API-get-list-of-files-related-to-commit/m-p/24666#M1850) about the same problem that I am facing. It convinced me that I have to fix it myself since there is no out-of-the-box solution.

Suddenly, I found [this great post](https://medium.com/atheros/graphql-quick-tip-aliases-567303a9ddc5) about the GraphQL aliases. I should have paid more attention when learning GraphQL or spend some extra hours learning. And yeah I do not how I end up finding about aliases when I was solving the problem.

I guess you know where I am going here. Alias is the best way to avoid the **2*number of updated files** API calls that I had to do using the REST API v3.  The solution is to profit from the best features of both GitHub API v3 and v4.

### Solution

The final process looks like this:

1. Get the commits using REST API v3
2. Get the commit content also using REST API v3
3. Generate a single GraphQL query with aliases to get the files content.

I created a sample project in GitHub with a [GitHub Service](https://github.com/MohamedSahbi/GitHubAPIDemo/blob/master/GitHubAPIDemo/Services/GitHubService.cs) that you can reuse easily. The are 2 main methods offered by this service:

- `GetLastCommitFilesContent(string directory, DateTime? startingFrom = null)` : it gets the last commit, look for its content and then generate a graphQL query and retrieve the files by calling GraphQL API. It returns an object of type `GitHubServiceOutput`.
- `GetCommitFilesContent(string commitHash, string directory)` : a similar method to the previous one, but it takes commit hash as parameter. The output is like the previous method's output.

You will find the details about the code sample and the used libraries in the GitHub repository.
