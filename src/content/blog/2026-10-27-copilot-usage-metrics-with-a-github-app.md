---
title: "Copilot usage metrics with a GitHub App, no PAT needed"
date: 2026-10-27T15:00:00+01:00
description: "How to pull GitHub Copilot usage metrics reports at enterprise and organization level with a GitHub App installation token instead of a personal access token, in plain PowerShell."
tags: ["GitHub Copilot", "GitHub Apps", "PowerShell"]
---
If you report on GitHub Copilot adoption, sooner or later you'll automate pulling the usage metrics. The quick way is a personal access token. The problem is that a PAT belongs to a person: it carries their access, it expires on their schedule, and it breaks when they change roles.

A **GitHub App** is a better fit for automation. You keep a private key, sign a short-lived JWT on every run, and swap it for an installation token that expires after an hour. Nothing is tied to a person.

Here's the flow I use, in plain PowerShell 7 with no modules. The full guide, with every step and a troubleshooting table, is in [this gist](https://gist.github.com/MohamedSahbi/d3415db277dbb2ef0deec609c12d26b3).

## How it works

```
Private key (.pem)  ──sign──►  JWT (max 10 min)
JWT  ──►  GET /enterprises/{ent}/installation  (or /orgs/{org}/installation)  ──►  installation id
JWT  ──►  POST /app/installations/{id}/access_tokens  ──►  installation token (1 h)
Installation token  ──►  GET .../copilot/metrics/reports/...  ──►  signed download links (NDJSON)
```

## Setup checklist

1. **Policy.** In *Enterprise → Policies → Copilot*, set **Copilot usage metrics** to *Enabled everywhere*. If you skip this, the endpoints return 403 or 404.
2. **Permissions.** Give the app **Enterprise Copilot metrics: Read** and/or **Organization Copilot metrics: Read**.
3. **Install it where you query.** An enterprise installation only covers `/enterprises/...` endpoints. For org-level reports, install the app on **each organization**.
4. **Approve permission changes.** If you add a permission later, an owner has to accept it, and you need a **new** token afterwards.
5. **Private key.** Generate one under *App settings → Private keys*. In automation, keep it in Key Vault and sign a fresh JWT on every run. You don't need a client secret.

## Sign the JWT

```powershell
$clientId = "<CLIENT_ID>"   # or App ID
$pem      = Get-Content ".\<APP_NAME>.private-key.pem" -Raw

function ConvertTo-B64Url([byte[]]$b) {
    [Convert]::ToBase64String($b).TrimEnd('=').Replace('+','-').Replace('/','_')
}

$now     = [DateTimeOffset]::UtcNow.ToUnixTimeSeconds()
$header  = @{ alg = 'RS256'; typ = 'JWT' } | ConvertTo-Json -Compress
$payload = @{ iat = $now - 60; exp = $now + 540; iss = $clientId } | ConvertTo-Json -Compress

$unsigned = (ConvertTo-B64Url ([Text.Encoding]::UTF8.GetBytes($header))) + '.' +
            (ConvertTo-B64Url ([Text.Encoding]::UTF8.GetBytes($payload)))

$rsa = [System.Security.Cryptography.RSA]::Create()
$rsa.ImportFromPem($pem)
$sig = $rsa.SignData([Text.Encoding]::UTF8.GetBytes($unsigned),
        [Security.Cryptography.HashAlgorithmName]::SHA256,
        [Security.Cryptography.RSASignaturePadding]::Pkcs1)

$jwt = "$unsigned." + (ConvertTo-B64Url $sig)
$h = @{ Authorization = "Bearer $jwt"; Accept = "application/vnd.github+json"; "X-GitHub-Api-Version" = "2026-03-10" }
```

`iat` is set 60 seconds in the past to absorb clock skew, and `exp` stays under GitHub's 10-minute limit. `RSA.ImportFromPem` needs .NET 5 or newer, which is why this requires PowerShell 7.

## Get a token and the report

```powershell
$inst = Invoke-RestMethod "https://api.github.com/enterprises/<ENTERPRISE_SLUG>/installation" -Headers $h
$tok  = Invoke-RestMethod -Method Post "https://api.github.com/app/installations/$($inst.id)/access_tokens" -Headers $h

$h.Authorization = "Bearer $($tok.token)"
$r = Invoke-RestMethod "https://api.github.com/enterprises/<ENTERPRISE_SLUG>/copilot/metrics/reports/enterprise-1-day?day=<YYYY-MM-DD>" -Headers $h

# The download links are pre-signed: don't send the Authorization header
$records = $r.download_links | ForEach-Object {
    (Invoke-RestMethod -Uri $_ | Out-String) -split '\r?\n' | Where-Object { $_.Trim() }
} | ForEach-Object { $_ | ConvertFrom-Json }
```

For org-level, user-level reports, swap in `/orgs/<ORG>/installation` and `/orgs/<ORG>/copilot/metrics/reports/users-1-day`.

Full guide with troubleshooting: [gist](https://gist.github.com/MohamedSahbi/d3415db277dbb2ef0deec609c12d26b3) · API reference: [Copilot usage metrics](https://docs.github.com/rest/copilot/copilot-usage-metrics)

*I wrote this post with help from [Claude](https://claude.ai), based on my own guide and scripts.*
