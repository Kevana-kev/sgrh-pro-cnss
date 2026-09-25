param(
    [Parameter(Mandatory = $true)]
    [string]$Path
)

$ErrorActionPreference = "Stop"
$full = (Resolve-Path $Path).Path

function Get-Roman([int]$n) {
    $map = @(
        @{ v = 10; s = "x" }, @{ v = 9; s = "ix" },
        @{ v = 5; s = "v" }, @{ v = 4; s = "iv" }, @{ v = 1; s = "i" }
    )
    $out = ""
    foreach ($m in $map) {
        while ($n -ge $m.v) { $out += $m.s; $n -= $m.v }
    }
    if ($out -eq "") { $out = "i" }
    return $out
}

function Get-Norm([string]$t) {
    if ($null -eq $t) { return "" }
    return (($t -replace "`r|`a", "") -replace "\s+", " ").Trim()
}

function Get-TocTitle([string]$raw) {
    if ($null -eq $raw) { return "" }
    $t = $raw -replace "`r|`a", ""
    $tab = $t.IndexOf("`t")
    if ($tab -ge 0) { $t = $t.Substring(0, $tab) }
    $t = (($t -replace "\s+", " ").Trim())
    $t = [regex]::Replace($t, "\s+(\.+)?\s*(- \d+ -|[ivxlcdm]+|\d+)\s*$", "")
    return $t.Trim()
}

function Get-ShownPage($para) {
    # 1 = wdActiveEndAdjustedPageNumber (numéro imprimé sur la page)
    return [int]$para.Range.Information(1)
}

function Get-Key([string]$text) {
    $m = [regex]::Match($text, "^(Figure|Tableau)\s+(\d+|[IVX]+\.\d+(?:\s+(?:bis|ter|quater|quinquies))?)")
    if (-not $m.Success) { return $null }
    return ($m.Groups[1].Value + " " + $m.Groups[2].Value)
}

function Test-H1([string]$style) {
    return ($style -like "Heading 1*") -or ($style -like "Titre 1*")
}

function Test-HAny([string]$style) {
    return ($style -like "Heading*") -or ($style -like "Titre*")
}

function Set-Dotted($para, [string]$newPage, [bool]$roman) {
    $rng = $para.Range
    $t = $rng.Text
    if ($t.EndsWith("`r")) { $t = $t.Substring(0, $t.Length - 1) }
    $tab = $t.LastIndexOf("`t")
    $left = if ($tab -ge 0) { $t.Substring(0, $tab) } else { [regex]::Replace($t, "(\s+\.+|\s+- \d+ -|\s+[ivx]+)\s*$", "") }
    $suffix = if ($roman) { $newPage } else { "- $newPage -" }
    $rng.Text = "$left`t$suffix`r"
    try {
        $para.TabStops.ClearAll()
        $para.TabStops.Add(453.6, 2, 1) | Out-Null  # 16 cm, right, dots
    } catch {}
}

Write-Host "Ouverture Word..."
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0
$doc = $word.Documents.Open($full, $false, $false)

try {
    Write-Host "Repagination..."
    $nSec = $doc.Sections.Count
    for ($s = 1; $s -le $nSec; $s++) {
        $sec = $doc.Sections.Item($s)
        $sec.PageSetup.DifferentFirstPageHeaderFooter = $false
        $sec.PageSetup.OddAndEvenPagesHeaderFooter = $false
        try {
            $pns = $sec.Headers.Item(1).PageNumbers
            if ($s -eq 1) {
                $pns.NumberStyle = 2  # lower roman
                $pns.RestartNumberingAtSection = $true
                $pns.StartingNumber = 1
            }
            else {
                $pns.NumberStyle = 0  # arabic
                $pns.RestartNumberingAtSection = $true
                $pns.StartingNumber = 1
            }
        } catch {}
    }
    $doc.Repaginate() | Out-Null

    $figPages = @{}
    $tabPages = @{}
    $headingPages = @{}
    $listFigParas = New-Object System.Collections.Generic.List[object]
    $listTabParas = New-Object System.Collections.Generic.List[object]
    $tocParas = New-Object System.Collections.Generic.List[object]

    $mode = "body"
    $count = $doc.Paragraphs.Count
    Write-Host "Paragraphes: $count"

    $i = 0
    foreach ($para in $doc.Paragraphs) {
        $i++
        $text = Get-Norm $para.Range.Text
        if ($text.Length -lt 2) { continue }

        $style = ""
        try { $style = [string]$para.Style.NameLocal } catch {}

        $isH1 = Test-H1 $style
        $isH = $isH1 -or (Test-HAny $style)

        if ($isH1 -and $text -eq "LISTE DES FIGURES") {
            $mode = "figlist"
            $headingPages[$text] = @{ s = [int]$para.Range.Information(2); p = (Get-ShownPage $para) }
            continue
        }
        if ($isH1 -and $text -eq "LISTE DES TABLEAUX") {
            $mode = "tablist"
            $headingPages[$text] = @{ s = [int]$para.Range.Information(2); p = (Get-ShownPage $para) }
            continue
        }
        if ($isH1 -and ($text -like "TABLE DES MATI*")) {
            $mode = "toc"
            $headingPages[$text] = @{ s = [int]$para.Range.Information(2); p = (Get-ShownPage $para) }
            continue
        }

        if ($isH1) {
            if ($mode -eq "figlist" -or $mode -eq "tablist") { $mode = "body" }
            elseif ($mode -eq "toc") { $mode = "body" }
            $headingPages[$text] = @{ s = [int]$para.Range.Information(2); p = (Get-ShownPage $para) }
            continue
        }
        if ($isH) {
            $headingPages[$text] = @{ s = [int]$para.Range.Information(2); p = (Get-ShownPage $para) }
            continue
        }

        if ($mode -eq "figlist") { $listFigParas.Add(@{ p = $para; t = $text }); continue }
        if ($mode -eq "tablist") { $listTabParas.Add(@{ p = $para; t = $text }); continue }
        if ($mode -eq "toc") {
            $raw = $para.Range.Text
            $tocParas.Add(@{ p = $para; t = (Get-TocTitle $raw) })
            continue
        }

        $key = Get-Key $text
        if ($key) {
            $page = Get-ShownPage $para
            if ($key.StartsWith("Figure")) { $figPages[$key] = "$page" }
            else { $tabPages[$key] = "$page" }
        }
    }

    Write-Host ("Collecte: fig={0} tab={1} headings={2}" -f $figPages.Count, $tabPages.Count, $headingPages.Count)

    foreach ($item in $listFigParas) {
        $key = Get-Key $item.t
        if ($key -and $figPages.ContainsKey($key)) { Set-Dotted $item.p $figPages[$key] $false }
    }
    foreach ($item in $listTabParas) {
        $key = Get-Key $item.t
        if ($key -and $tabPages.ContainsKey($key)) { Set-Dotted $item.p $tabPages[$key] $false }
    }
    $tocHit = 0
    $tocMiss = New-Object System.Collections.Generic.List[string]
    foreach ($item in $tocParas) {
        $title = $item.t
        if ($headingPages.ContainsKey($title) -and $headingPages[$title] -is [hashtable]) {
            $h = $headingPages[$title]
            if ([int]$h.s -le 1) { Set-Dotted $item.p (Get-Roman ([int]$h.p)) $true }
            else { Set-Dotted $item.p ([string]$h.p) $false }
            $tocHit++
        }
        else {
            $tocMiss.Add($title)
        }
    }
    Write-Host ("TOC maj={0} manque={1}" -f $tocHit, $tocMiss.Count)
    if ($tocMiss.Count -gt 0) {
        Write-Host "TOC non trouves:"
        foreach ($m in $tocMiss) { Write-Host ("  - {0}" -f $m) }
    }

    $doc.Repaginate() | Out-Null
    $doc.Save()
    $pages = $doc.ComputeStatistics(2)
    Write-Host "Pagination OK"
    Write-Host ("PAGES_WORD={0}" -f $pages)
}
finally {
    $doc.Close($true)
    $word.Quit()
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($word) | Out-Null
}
