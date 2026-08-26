[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$ManifestPath,

    [Parameter(Mandatory = $true)]
    [string]$AuthorizationReceiptPath
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$script:OutputRoot = $null
$script:TerminalWritten = $false
$script:HttpClient = $null
$script:RequestCount = 0
$script:TotalResponseBytes = [int64]0
$script:StartedAt = [DateTimeOffset]::UtcNow
$script:Utf8Strict = [System.Text.UTF8Encoding]::new($false, $true)
$script:Utf8NoBom = [System.Text.UTF8Encoding]::new($false)

function Throw-A0Failure {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Code,

        [Parameter(Mandatory = $true)]
        [string]$Message
    )

    throw "[$Code] $Message"
}

function Get-Sha256 {
    param([Parameter(Mandatory = $true)][string]$LiteralPath)

    return (Get-FileHash -Algorithm SHA256 -LiteralPath $LiteralPath).Hash.ToUpperInvariant()
}

function Assert-ResourceCaps {
    param([Parameter(Mandatory = $true)][object]$Caps)

    $process = Get-Process -Id $PID
    if (([DateTimeOffset]::UtcNow - $script:StartedAt).TotalSeconds -gt [int]$Caps.wall_seconds) {
        Throw-A0Failure 'ACQUISITION_WALL_CAP_EXCEEDED' "Wall-time cap exceeded."
    }
    if ($process.TotalProcessorTime.TotalSeconds -gt [int]$Caps.cpu_seconds) {
        Throw-A0Failure 'ACQUISITION_CPU_CAP_EXCEEDED' "CPU-time cap exceeded."
    }
    if ([int64]$process.PeakWorkingSet64 -gt [int64]$Caps.peak_memory_bytes) {
        Throw-A0Failure 'ACQUISITION_MEMORY_CAP_EXCEEDED' "Peak-memory cap exceeded."
    }
}

function Assert-RegularFile {
    param(
        [Parameter(Mandatory = $true)]
        [string]$LiteralPath,

        [Parameter(Mandatory = $true)]
        [string]$FailureCode
    )

    if (-not (Test-Path -LiteralPath $LiteralPath -PathType Leaf)) {
        Throw-A0Failure $FailureCode "Required file is absent: $LiteralPath"
    }

    $item = Get-Item -LiteralPath $LiteralPath -Force
    if (($item.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0) {
        Throw-A0Failure $FailureCode "Reparse-point input is forbidden: $LiteralPath"
    }
}

function Assert-UniqueJsonProperties {
    param(
        [Parameter(Mandatory = $true)]
        [System.Text.Json.JsonElement]$Element,

        [Parameter(Mandatory = $true)]
        [string]$JsonPath
    )

    if ($Element.ValueKind -eq [System.Text.Json.JsonValueKind]::Object) {
        $names = [System.Collections.Generic.HashSet[string]]::new(
            [System.StringComparer]::Ordinal
        )
        foreach ($property in $Element.EnumerateObject()) {
            if (-not $names.Add($property.Name)) {
                Throw-A0Failure 'A0_JSON_DUPLICATE_NAME' "Duplicate JSON name at $JsonPath"
            }
            Assert-UniqueJsonProperties -Element $property.Value -JsonPath "$JsonPath.$($property.Name)"
        }
    }
    elseif ($Element.ValueKind -eq [System.Text.Json.JsonValueKind]::Array) {
        $index = 0
        foreach ($item in $Element.EnumerateArray()) {
            Assert-UniqueJsonProperties -Element $item -JsonPath "$JsonPath[$index]"
            $index += 1
        }
    }
}

function Read-StrictJsonFile {
    param(
        [Parameter(Mandatory = $true)]
        [string]$LiteralPath,

        [Parameter(Mandatory = $true)]
        [string]$FailureCode
    )

    Assert-RegularFile -LiteralPath $LiteralPath -FailureCode $FailureCode
    $bytes = [IO.File]::ReadAllBytes($LiteralPath)
    if ($bytes.Length -ge 3 -and $bytes[0] -eq 0xEF -and $bytes[1] -eq 0xBB -and $bytes[2] -eq 0xBF) {
        Throw-A0Failure $FailureCode "UTF-8 BOM is forbidden: $LiteralPath"
    }

    try {
        $text = $script:Utf8Strict.GetString($bytes)
        $options = [System.Text.Json.JsonDocumentOptions]::new()
        $options.AllowTrailingCommas = $false
        $options.CommentHandling = [System.Text.Json.JsonCommentHandling]::Disallow
        $document = [System.Text.Json.JsonDocument]::Parse($text, $options)
        try {
            Assert-UniqueJsonProperties -Element $document.RootElement -JsonPath '$'
        }
        finally {
            $document.Dispose()
        }
        return ($text | ConvertFrom-Json -Depth 100)
    }
    catch {
        if ($_.Exception.Message.StartsWith('[A0_JSON_DUPLICATE_NAME]')) {
            throw
        }
        Throw-A0Failure $FailureCode "Strict JSON parse failed: $LiteralPath"
    }
}

function Write-NewBytes {
    param(
        [Parameter(Mandatory = $true)]
        [string]$LiteralPath,

        [Parameter(Mandatory = $true)]
        [byte[]]$Bytes
    )

    $parent = Split-Path -Parent $LiteralPath
    if (-not (Test-Path -LiteralPath $parent -PathType Container)) {
        [IO.Directory]::CreateDirectory($parent) | Out-Null
    }

    $stream = [IO.FileStream]::new(
        $LiteralPath,
        [IO.FileMode]::CreateNew,
        [IO.FileAccess]::Write,
        [IO.FileShare]::None
    )
    try {
        $stream.Write($Bytes, 0, $Bytes.Length)
        $stream.Flush($true)
    }
    finally {
        $stream.Dispose()
    }
}

function Write-NewJson {
    param(
        [Parameter(Mandatory = $true)]
        [string]$LiteralPath,

        [Parameter(Mandatory = $true)]
        [object]$Value
    )

    $json = $Value | ConvertTo-Json -Depth 100 -Compress
    Write-NewBytes -LiteralPath $LiteralPath -Bytes $script:Utf8NoBom.GetBytes($json)
}

function Assert-NoReparseAncestor {
    param([Parameter(Mandatory = $true)][string]$TargetPath)

    $current = [IO.Path]::GetFullPath((Split-Path -Parent $TargetPath))
    while (-not [string]::IsNullOrWhiteSpace($current)) {
        if (Test-Path -LiteralPath $current) {
            $item = Get-Item -LiteralPath $current -Force
            if (($item.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0) {
                Throw-A0Failure 'ACQUISITION_REPARSE_ANCESTOR' "Reparse ancestor is forbidden: $current"
            }
        }
        $parent = Split-Path -Parent $current
        if ([string]::IsNullOrWhiteSpace($parent) -or $parent -eq $current) {
            break
        }
        $current = $parent
    }
}

function Assert-AllowedUri {
    param(
        [Parameter(Mandatory = $true)]
        [Uri]$Uri,

        [Parameter(Mandatory = $true)]
        [System.Collections.Generic.HashSet[string]]$AllowedHosts
    )

    if (-not $Uri.IsAbsoluteUri -or $Uri.Scheme -ne 'https') {
        Throw-A0Failure 'ACQUISITION_URI_FORBIDDEN' "Only absolute HTTPS URLs are allowed."
    }
    if (-not [string]::IsNullOrEmpty($Uri.UserInfo)) {
        Throw-A0Failure 'ACQUISITION_URI_FORBIDDEN' "URL user information is forbidden."
    }
    if ($Uri.Port -ne 443) {
        Throw-A0Failure 'ACQUISITION_URI_FORBIDDEN' "Only HTTPS port 443 is allowed."
    }
    if (-not $AllowedHosts.Contains($Uri.DnsSafeHost)) {
        Throw-A0Failure 'ACQUISITION_HOST_FORBIDDEN' "Host is outside the approved allowlist."
    }
}

function Get-SelectedHeaders {
    param([Parameter(Mandatory = $true)][System.Net.Http.HttpResponseMessage]$Response)

    $selected = [ordered]@{}
    foreach ($name in @('Date', 'ETag', 'Last-Modified', 'Content-Type', 'Content-Length', 'Location')) {
        $values = $null
        if ($Response.Headers.TryGetValues($name, [ref]$values) -or
            $Response.Content.Headers.TryGetValues($name, [ref]$values)) {
            $joined = [string]::Join(', ', [string[]]$values)
            if ($joined.Length -gt 4096) {
                Throw-A0Failure 'ACQUISITION_HEADER_CAP_EXCEEDED' "Selected response header is too large."
            }
            $selected[$name] = $joined
        }
    }
    return $selected
}

function Receive-Object {
    param(
        [Parameter(Mandatory = $true)]
        [object]$ObjectSpec,

        [Parameter(Mandatory = $true)]
        [object]$Caps,

        [Parameter(Mandatory = $true)]
        [System.Collections.Generic.HashSet[string]]$AllowedHosts,

        [Parameter(Mandatory = $true)]
        [Threading.CancellationToken]$CancellationToken
    )

    $objectId = [string]$ObjectSpec.id
    if ($objectId -notmatch '^[a-z0-9][a-z0-9-]{0,63}$') {
        Throw-A0Failure 'ACQUISITION_OBJECT_ID_INVALID' "Unsafe object ID."
    }

    $currentUri = [Uri]([string]$ObjectSpec.url)
    Assert-AllowedUri -Uri $currentUri -AllowedHosts $AllowedHosts
    $redirects = [System.Collections.Generic.List[object]]::new()
    $response = $null

    for ($redirectCount = 0; $redirectCount -le [int]$Caps.redirects_per_object; $redirectCount += 1) {
        Assert-ResourceCaps -Caps $Caps
        if ($script:RequestCount -ge [int]$Caps.http_exchanges) {
            Throw-A0Failure 'ACQUISITION_REQUEST_CAP_EXCEEDED' "HTTP exchange cap reached."
        }
        $script:RequestCount += 1

        $request = [Net.Http.HttpRequestMessage]::new([Net.Http.HttpMethod]::Get, $currentUri)
        $request.Headers.UserAgent.ParseAdd('sana-e14-a1-download-only/1.0')
        try {
            $response = $script:HttpClient.SendAsync(
                $request,
                [Net.Http.HttpCompletionOption]::ResponseHeadersRead,
                $CancellationToken
            ).GetAwaiter().GetResult()
        }
        finally {
            $request.Dispose()
        }

        $status = [int]$response.StatusCode
        if ($status -in @(301, 302, 303, 307, 308)) {
            if ($redirectCount -ge [int]$Caps.redirects_per_object) {
                $response.Dispose()
                Throw-A0Failure 'ACQUISITION_REDIRECT_CAP_EXCEEDED' "Redirect cap reached."
            }
            $location = $response.Headers.Location
            if ($null -eq $location) {
                $response.Dispose()
                Throw-A0Failure 'ACQUISITION_REDIRECT_INVALID' "Redirect lacks Location."
            }
            $nextUri = if ($location.IsAbsoluteUri) { $location } else { [Uri]::new($currentUri, $location) }
            Assert-AllowedUri -Uri $nextUri -AllowedHosts $AllowedHosts
            $redirects.Add([ordered]@{
                status = $status
                from = $currentUri.AbsoluteUri
                to = $nextUri.AbsoluteUri
            })
            $response.Dispose()
            $response = $null
            $currentUri = $nextUri
            continue
        }
        break
    }

    if ($null -eq $response -or -not $response.IsSuccessStatusCode) {
        if ($null -ne $response) {
            $response.Dispose()
        }
        Throw-A0Failure 'ACQUISITION_HTTP_STATUS' "Required object did not return a successful status."
    }

    $declaredLength = $response.Content.Headers.ContentLength
    if ($null -ne $declaredLength -and $declaredLength -gt [int64]$Caps.response_bytes_per_object) {
        $response.Dispose()
        Throw-A0Failure 'ACQUISITION_SIZE_CAP_EXCEEDED' "Declared response length exceeds per-object cap."
    }

    $objectDirectory = Join-Path $script:OutputRoot 'objects'
    $partialPath = Join-Path $objectDirectory "$objectId.body.part"
    $finalPath = Join-Path $objectDirectory "$objectId.body"
    $metadataPath = Join-Path $objectDirectory "$objectId.response.json"
    $headers = Get-SelectedHeaders -Response $response
    $file = $null
    $networkStream = $null
    $objectBytes = [int64]0

    try {
        $file = [IO.FileStream]::new(
            $partialPath,
            [IO.FileMode]::CreateNew,
            [IO.FileAccess]::Write,
            [IO.FileShare]::None
        )
        $networkStream = $response.Content.ReadAsStreamAsync($CancellationToken).GetAwaiter().GetResult()
        $buffer = [byte[]]::new(65536)
        while ($true) {
            Assert-ResourceCaps -Caps $Caps
            $read = $networkStream.ReadAsync(
                $buffer,
                0,
                $buffer.Length,
                $CancellationToken
            ).GetAwaiter().GetResult()
            if ($read -eq 0) {
                break
            }
            if (($objectBytes + $read) -gt [int64]$Caps.response_bytes_per_object -or
                ($script:TotalResponseBytes + $read) -gt [int64]$Caps.total_response_bytes) {
                Throw-A0Failure 'ACQUISITION_SIZE_CAP_EXCEEDED' "Streamed response exceeds approved byte caps."
            }
            $file.Write($buffer, 0, $read)
            $objectBytes += $read
            $script:TotalResponseBytes += $read
        }
        $file.Flush($true)
    }
    finally {
        if ($null -ne $networkStream) { $networkStream.Dispose() }
        if ($null -ne $file) { $file.Dispose() }
        $response.Dispose()
    }

    [IO.File]::Move($partialPath, $finalPath)
    Assert-ResourceCaps -Caps $Caps
    $sha256 = Get-Sha256 -LiteralPath $finalPath
    if ($null -ne $ObjectSpec.expected_sha256 -and
        -not [string]::IsNullOrWhiteSpace([string]$ObjectSpec.expected_sha256) -and
        $sha256 -ne ([string]$ObjectSpec.expected_sha256).ToUpperInvariant()) {
        Throw-A0Failure 'ACQUISITION_REGISTRY_DIGEST_MISMATCH' "Approved SHA-256 mismatch for $objectId."
    }
    if ($null -ne $ObjectSpec.expected_size -and [int64]$ObjectSpec.expected_size -ge 0 -and
        $objectBytes -ne [int64]$ObjectSpec.expected_size) {
        Throw-A0Failure 'ACQUISITION_METADATA_MISMATCH' "Approved size mismatch for $objectId."
    }

    $relativeBodyPath = "objects/$objectId.body"
    $record = [ordered]@{
        schema = 'sana.e14.a1-response.v1'
        id = $objectId
        kind = [string]$ObjectSpec.kind
        requested_url = [string]$ObjectSpec.url
        final_url = $currentUri.AbsoluteUri
        status = $status
        redirects = @($redirects)
        selected_headers = $headers
        body_path = $relativeBodyPath
        body_bytes = $objectBytes
        body_sha256 = $sha256
        acquired_at_utc = [DateTimeOffset]::UtcNow.ToString('O')
        authority_effect = 'NONE'
    }
    Write-NewJson -LiteralPath $metadataPath -Value $record
    return $record
}

function Get-FileDigestBase64 {
    param(
        [Parameter(Mandatory = $true)][string]$LiteralPath,
        [Parameter(Mandatory = $true)][ValidateSet('SHA512')][string]$Algorithm
    )

    $bytes = [IO.File]::ReadAllBytes($LiteralPath)
    $digest = [Security.Cryptography.SHA512]::HashData($bytes)
    return [Convert]::ToBase64String($digest)
}

function Assert-PackageMetadata {
    param(
        [Parameter(Mandatory = $true)][object]$Manifest,
        [Parameter(Mandatory = $true)][object[]]$Records
    )

    $byId = @{}
    foreach ($record in $Records) { $byId[[string]$record.id] = $record }
    $specById = @{}
    foreach ($objectSpec in @($Manifest.objects)) { $specById[[string]$objectSpec.id] = $objectSpec }

    $nodeMetadataPath = Join-Path $script:OutputRoot ([string]$byId['node-metadata'].body_path)
    $nodeArchivePath = Join-Path $script:OutputRoot ([string]$byId['node-archive'].body_path)
    $node = Read-StrictJsonFile -LiteralPath $nodeMetadataPath -FailureCode 'ACQUISITION_METADATA_MISMATCH'
    if ([string]$node.name -ne 'canonicalize' -or [string]$node.version -ne '4.0.0') {
        Throw-A0Failure 'ACQUISITION_METADATA_MISMATCH' "npm package identity mismatch."
    }
    if ([string]$node.dist.tarball -ne [string]$specById['node-archive'].url) {
        Throw-A0Failure 'ACQUISITION_METADATA_MISMATCH' "npm tarball URL mismatch."
    }
    if ([string]$node.dist.integrity -notmatch '^sha512-[A-Za-z0-9+/]+={0,2}$') {
        Throw-A0Failure 'ACQUISITION_METADATA_MISMATCH' "npm SHA-512 SRI is absent or malformed."
    }
    $actualSri = 'sha512-' + (Get-FileDigestBase64 -LiteralPath $nodeArchivePath -Algorithm SHA512)
    if ($actualSri -cne [string]$node.dist.integrity) {
        Throw-A0Failure 'ACQUISITION_REGISTRY_DIGEST_MISMATCH' "npm SHA-512 SRI mismatch."
    }
    $actualSha1 = (Get-FileHash -Algorithm SHA1 -LiteralPath $nodeArchivePath).Hash.ToLowerInvariant()
    if ($actualSha1 -cne ([string]$node.dist.shasum).ToLowerInvariant()) {
        Throw-A0Failure 'ACQUISITION_REGISTRY_DIGEST_MISMATCH' "npm SHA-1 shasum mismatch."
    }

    $pythonMetadataPath = Join-Path $script:OutputRoot ([string]$byId['python-metadata'].body_path)
    $pythonWheelPath = Join-Path $script:OutputRoot ([string]$byId['python-wheel'].body_path)
    $python = Read-StrictJsonFile -LiteralPath $pythonMetadataPath -FailureCode 'ACQUISITION_METADATA_MISMATCH'
    if ([string]$python.info.name -ne 'rfc8785' -or [string]$python.info.version -ne '0.1.4') {
        Throw-A0Failure 'ACQUISITION_METADATA_MISMATCH' "PyPI package identity mismatch."
    }
    $matches = @($python.urls | Where-Object {
        [string]$_.filename -eq 'rfc8785-0.1.4-py3-none-any.whl'
    })
    if ($matches.Count -ne 1) {
        Throw-A0Failure 'ACQUISITION_METADATA_MISMATCH' "PyPI wheel identity is not unique."
    }
    $wheel = $matches[0]
    if ([string]$wheel.url -ne [string]$specById['python-wheel'].url -or
        [int64]$wheel.size -ne 9240 -or
        ([string]$wheel.digests.sha256).ToUpperInvariant() -ne
            '520D690B448ECF0703691C76E1A34A24DDCD4FC5BC41D589CB7C58EC651BCD48') {
        Throw-A0Failure 'ACQUISITION_METADATA_MISMATCH' "PyPI wheel metadata mismatch."
    }
    if ((Get-Sha256 -LiteralPath $pythonWheelPath) -ne
        '520D690B448ECF0703691C76E1A34A24DDCD4FC5BC41D589CB7C58EC651BCD48') {
        Throw-A0Failure 'ACQUISITION_REGISTRY_DIGEST_MISMATCH' "PyPI wheel SHA-256 mismatch."
    }

    return [ordered]@{
        node = [ordered]@{
            name = [string]$node.name
            version = [string]$node.version
            license = [string]$node.license
            archive_sha256 = Get-Sha256 -LiteralPath $nodeArchivePath
            registry_integrity = [string]$node.dist.integrity
            registry_shasum = [string]$node.dist.shasum
        }
        python = [ordered]@{
            name = [string]$python.info.name
            version = [string]$python.info.version
            wheel_sha256 = Get-Sha256 -LiteralPath $pythonWheelPath
            registry_sha256 = [string]$wheel.digests.sha256
            wheel_bytes = [int64]$wheel.size
        }
    }
}

function Get-OutputInventory {
    param([Parameter(Mandatory = $true)][string]$Root)

    $rootFull = [IO.Path]::GetFullPath($Root).TrimEnd([IO.Path]::DirectorySeparatorChar) +
        [IO.Path]::DirectorySeparatorChar
    $recordsByPath = @{}
    $paths = [System.Collections.Generic.List[string]]::new()
    foreach ($file in Get-ChildItem -LiteralPath $Root -File -Recurse) {
        if (($file.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0) {
            Throw-A0Failure 'ACQUISITION_OUTPUT_REPARSE_POINT' "Output reparse point is forbidden."
        }
        $full = [IO.Path]::GetFullPath($file.FullName)
        if (-not $full.StartsWith($rootFull, [StringComparison]::OrdinalIgnoreCase)) {
            Throw-A0Failure 'ACQUISITION_OUTPUT_ESCAPE' "Output escaped its approved root."
        }
        $relative = $full.Substring($rootFull.Length).Replace('\', '/')
        if ($recordsByPath.ContainsKey($relative)) {
            Throw-A0Failure 'ACQUISITION_OUTPUT_PATH_COLLISION' "Duplicate normalized output path."
        }
        $paths.Add($relative)
        $recordsByPath[$relative] = [ordered]@{
            path = $relative
            bytes = [int64]$file.Length
            sha256 = Get-Sha256 -LiteralPath $full
        }
    }
    $paths.Sort([StringComparer]::Ordinal)
    $inventory = [System.Collections.Generic.List[object]]::new()
    foreach ($relative in $paths) {
        $inventory.Add($recordsByPath[$relative])
    }
    return @($inventory)
}

function Write-TerminalReceipt {
    param(
        [Parameter(Mandatory = $true)][string]$State,
        [AllowNull()][string]$FailureCode,
        [AllowNull()][string]$FailureMessage,
        [AllowNull()][object]$PackageFacts,
        [Parameter(Mandatory = $true)][object]$Caps
    )

    if ($script:TerminalWritten -or [string]::IsNullOrWhiteSpace($script:OutputRoot) -or
        -not (Test-Path -LiteralPath $script:OutputRoot -PathType Container)) {
        return
    }

    $terminalPath = Join-Path $script:OutputRoot 'terminal-receipt.json'
    if (Test-Path -LiteralPath $terminalPath) {
        return
    }
    $inventory = Get-OutputInventory -Root $script:OutputRoot
    $totalBytes = [int64](($inventory | Measure-Object -Property bytes -Sum).Sum)
    if ($inventory.Count + 1 -gt [int]$Caps.output_files -or
        $totalBytes -gt [int64]$Caps.total_output_bytes) {
        $State = 'ACQUISITION_INCONCLUSIVE'
        $FailureCode = 'ACQUISITION_OUTPUT_CAP_EXCEEDED'
        $FailureMessage = 'Output inventory exceeded an approved cap.'
    }

    $terminal = [ordered]@{
        schema = 'sana.e14.a1-terminal-receipt.v1'
        state = $State
        failure_code = $FailureCode
        failure_message = $FailureMessage
        started_at_utc = $script:StartedAt.ToString('O')
        finished_at_utc = [DateTimeOffset]::UtcNow.ToString('O')
        http_exchanges = $script:RequestCount
        response_bytes = $script:TotalResponseBytes
        package_facts = $PackageFacts
        inventory = $inventory
        authority_effect = 'NONE'
        next_stage = 'UNAUTHORIZED_PENDING_G1'
    }
    Write-NewJson -LiteralPath $terminalPath -Value $terminal
    $script:TerminalWritten = $true
}

$manifest = $null
$authorization = $null

try {
    $manifestFull = [IO.Path]::GetFullPath($ManifestPath)
    $receiptFull = [IO.Path]::GetFullPath($AuthorizationReceiptPath)
    $runnerFull = [IO.Path]::GetFullPath($PSCommandPath)

    $manifest = Read-StrictJsonFile -LiteralPath $manifestFull -FailureCode 'A0_MANIFEST_INVALID'
    $authorization = Read-StrictJsonFile -LiteralPath $receiptFull -FailureCode 'A1_AUTHORIZATION_INVALID'

    if ([string]$manifest.schema -ne 'sana.e14.a0-acquisition-manifest.v1' -or
        [string]$manifest.status -ne 'REVIEW_ONLY_NOT_AUTHORIZED') {
        Throw-A0Failure 'A0_MANIFEST_INVALID' "Unexpected manifest schema or status."
    }
    if ([string]$authorization.schema -ne 'sana.e14.a1-authorization-receipt.v1' -or
        [string]$authorization.decision -ne 'APPROVE_A1_DOWNLOAD_ONLY' -or
        [string]$authorization.authority_effect -ne 'DOWNLOAD_ONLY') {
        Throw-A0Failure 'A1_AUTHORIZATION_INVALID' "Authorization receipt does not approve A1 download-only scope."
    }

    $manifestSha = Get-Sha256 -LiteralPath $manifestFull
    $runnerSha = Get-Sha256 -LiteralPath $runnerFull
    if ($manifestSha -ne ([string]$authorization.manifest_sha256).ToUpperInvariant() -or
        $runnerSha -ne ([string]$authorization.runner_sha256).ToUpperInvariant()) {
        Throw-A0Failure 'A1_AUTHORIZATION_HASH_MISMATCH' "Authorization does not bind these exact bytes."
    }
    if ($runnerSha -ne ([string]$manifest.tool.runner_sha256).ToUpperInvariant() -or
        $runnerFull -ne [IO.Path]::GetFullPath([string]$manifest.tool.runner_path)) {
        Throw-A0Failure 'A0_RUNNER_IDENTITY_MISMATCH' "Manifest runner identity mismatch."
    }

    $processPath = [IO.Path]::GetFullPath((Get-Process -Id $PID).Path)
    if ($processPath -ne [IO.Path]::GetFullPath([string]$manifest.tool.powershell_path) -or
        (Get-Sha256 -LiteralPath $processPath) -ne
            ([string]$manifest.tool.powershell_sha256).ToUpperInvariant()) {
        Throw-A0Failure 'A0_RUNTIME_IDENTITY_MISMATCH' "PowerShell runtime identity mismatch."
    }

    if ([string]$authorization.output_root -ne [string]$manifest.output_root) {
        Throw-A0Failure 'A1_AUTHORIZATION_SCOPE_MISMATCH' "Authorized output root mismatch."
    }
    if ([string]$authorization.expires_at_utc -notmatch 'Z$' -or
        [string]$authorization.issued_at_utc -notmatch 'Z$') {
        Throw-A0Failure 'A1_AUTHORIZATION_TIME_INVALID' "Authorization times must be UTC Z timestamps."
    }
    $issuedAt = [DateTimeOffset]::Parse([string]$authorization.issued_at_utc)
    $expiresAt = [DateTimeOffset]::Parse([string]$authorization.expires_at_utc)
    $now = [DateTimeOffset]::UtcNow
    if ($issuedAt -gt $now -or $expiresAt -le $now -or
        ($expiresAt - $issuedAt).TotalHours -gt 24) {
        Throw-A0Failure 'A1_AUTHORIZATION_EXPIRED' "Authorization is not currently valid or exceeds 24 hours."
    }

    $requiredIds = @(
        'node-metadata', 'node-archive', 'python-metadata', 'python-wheel',
        'rfc8785-text', 'rfc7493-text', 'rfc8785-errata-7920', 'rfc8785-errata-6292'
    )
    $actualIds = @($manifest.objects | ForEach-Object { [string]$_.id })
    if ($actualIds.Count -ne 8 -or ($actualIds | Sort-Object -Unique).Count -ne 8 -or
        (Compare-Object -ReferenceObject $requiredIds -DifferenceObject $actualIds).Count -ne 0) {
        Throw-A0Failure 'A0_MANIFEST_OBJECT_SET_INVALID' "Manifest must contain the exact eight-object set."
    }

    $allowedHosts = [System.Collections.Generic.HashSet[string]]::new(
        [System.StringComparer]::OrdinalIgnoreCase
    )
    foreach ($hostName in @($manifest.network.allowed_hosts)) {
        if (-not $allowedHosts.Add([string]$hostName)) {
            Throw-A0Failure 'A0_MANIFEST_HOST_SET_INVALID' "Duplicate host in allowlist."
        }
    }
    $expectedHosts = @(
        'registry.npmjs.org', 'pypi.org', 'files.pythonhosted.org',
        'www.rfc-editor.org', 'errata.rfc-editor.org'
    )
    if ($allowedHosts.Count -ne 5 -or
        (Compare-Object -ReferenceObject $expectedHosts -DifferenceObject @($allowedHosts)).Count -ne 0) {
        Throw-A0Failure 'A0_MANIFEST_HOST_SET_INVALID' "Manifest host allowlist is not exact."
    }

    $script:OutputRoot = [IO.Path]::GetFullPath([string]$manifest.output_root)
    Assert-NoReparseAncestor -TargetPath $script:OutputRoot
    if (Test-Path -LiteralPath $script:OutputRoot) {
        Throw-A0Failure 'ACQUISITION_ROOT_EXISTS' "Approved output root already exists."
    }
    [IO.Directory]::CreateDirectory($script:OutputRoot) | Out-Null
    [IO.Directory]::CreateDirectory((Join-Path $script:OutputRoot 'control')) | Out-Null
    [IO.Directory]::CreateDirectory((Join-Path $script:OutputRoot 'objects')) | Out-Null

    Write-NewBytes -LiteralPath (Join-Path $script:OutputRoot 'control/acquisition-manifest.json') `
        -Bytes ([IO.File]::ReadAllBytes($manifestFull))
    Write-NewBytes -LiteralPath (Join-Path $script:OutputRoot 'control/authorization-receipt.json') `
        -Bytes ([IO.File]::ReadAllBytes($receiptFull))
    Write-NewJson -LiteralPath (Join-Path $script:OutputRoot 'control/runner-identity.json') -Value ([ordered]@{
        schema = 'sana.e14.a1-runner-identity.v1'
        runner_path = $runnerFull
        runner_sha256 = $runnerSha
        powershell_path = $processPath
        powershell_sha256 = Get-Sha256 -LiteralPath $processPath
        authority_effect = 'NONE'
    })

    $handler = [Net.Http.HttpClientHandler]::new()
    $handler.AllowAutoRedirect = $false
    $handler.AutomaticDecompression = [Net.DecompressionMethods]::None
    $handler.UseCookies = $false
    $handler.UseProxy = $false
    $handler.SslProtocols = [Security.Authentication.SslProtocols]::Tls12 -bor
        [Security.Authentication.SslProtocols]::Tls13
    $script:HttpClient = [Net.Http.HttpClient]::new($handler, $true)
    $script:HttpClient.Timeout = [TimeSpan]::FromSeconds([int]$manifest.caps.wall_seconds)
    $cancellation = [Threading.CancellationTokenSource]::new(
        [TimeSpan]::FromSeconds([int]$manifest.caps.wall_seconds)
    )

    try {
        $records = [System.Collections.Generic.List[object]]::new()
        foreach ($objectSpec in @($manifest.objects)) {
            Assert-ResourceCaps -Caps $manifest.caps
            $records.Add((Receive-Object -ObjectSpec $objectSpec -Caps $manifest.caps `
                -AllowedHosts $allowedHosts -CancellationToken $cancellation.Token))
        }
        if ($records.Count -ne [int]$manifest.caps.required_successful_payloads) {
            Throw-A0Failure 'ACQUISITION_PAYLOAD_COUNT_MISMATCH' "Required payload count was not met."
        }
        $packageFacts = Assert-PackageMetadata -Manifest $manifest -Records @($records)
        Write-TerminalReceipt -State 'ACQUISITION_COMPLETE_AWAITING_G1' -FailureCode $null `
            -FailureMessage $null -PackageFacts $packageFacts -Caps $manifest.caps
    }
    finally {
        $cancellation.Dispose()
    }

    [Console]::Out.WriteLine('ACQUISITION_COMPLETE_AWAITING_G1')
    exit 0
}
catch {
    $message = $_.Exception.Message
    $failureCode = 'ACQUISITION_UNEXPECTED_FAILURE'
    if ($message -match '^\[([A-Z0-9_]+)\]') {
        $failureCode = $Matches[1]
    }
    try {
        if ($null -ne $manifest -and $null -ne $manifest.caps) {
            Write-TerminalReceipt -State 'ACQUISITION_INCONCLUSIVE' -FailureCode $failureCode `
                -FailureMessage $message -PackageFacts $null -Caps $manifest.caps
        }
    }
    catch {
        # The original failure remains decisive; terminal-write failure is reported without retry.
    }
    [Console]::Error.WriteLine($failureCode)
    exit 1
}
finally {
    if ($null -ne $script:HttpClient) {
        $script:HttpClient.Dispose()
    }
}
