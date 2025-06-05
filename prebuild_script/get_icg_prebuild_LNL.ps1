param ([int] $ver)

$workspace = (Get-location).path
$Codebase_Source = 'C:\Users\mandyhsi\workspace\vieddrv-github\w\camerasw\Source'
Set-Location -Path $Codebase_Source
write-host 'codebase source : ' $Codebase_Source
write-host 'pwd : '$workspace

$invokeGit= {
    Param (
        [Parameter(
            Mandatory=$true
        )]
        [string]$Reason,
        [Parameter(
            Mandatory=$true
        )]
        [string[]]$ArgumentsList
    )
    try
    {
        $gitPath=& "C:\Windows\System32\where.exe" git
        $gitErrorPath=Join-Path $env:TEMP "stderr.txt"
        $gitOutputPath=Join-Path $env:TEMP "stdout.txt"
        if($gitPath.Count -gt 1)
        {
            $gitPath=$gitPath[0]
        }

        Write-Verbose "[Git][$Reason] Begin"
        Write-Verbose "[Git][$Reason] gitPath=$gitPath"
        Write-Host "git $arguments"
        $process=Start-Process $gitPath -ArgumentList $ArgumentsList -NoNewWindow -PassThru -Wait -RedirectStandardError $gitErrorPath -RedirectStandardOutput $gitOutputPath
        $outputText=(Get-Content $gitOutputPath)
        $outputText | ForEach-Object {Write-Host $_}

        Write-Verbose "[Git][$Reason] process.ExitCode=$($process.ExitCode)"
        if($process.ExitCode -ne 0)
        {
            Write-Warning "[Git][$Reason] process.ExitCode=$($process.ExitCode)"
            $errorText=$(Get-Content $gitErrorPath)
            $errorText | ForEach-Object {Write-Host $_}

            if($errorText -ne $null)
            {
                exit $process.ExitCode
            }
        }
        return $outputText
    }
    catch
    {
        Write-Error "[Git][$Reason] Exception $_"
    }
    finally
    {
        Write-Verbose "[Git][$Reason] Done"
    }
}

## 'git.exe describe --abbrev=0'
$arguments=@(
  "describe"
  "--tags"
  " --abbrev=0"
)
$last_tag = Invoke-Command -ScriptBlock $invokeGit -ArgumentList "Tag",$arguments
write-host "last_tag : " $last_tag

$arguments=@(
  "branch"
  "--show-current"
)
$cur_branch = Invoke-Command -ScriptBlock $invokeGit -ArgumentList "branch",$arguments
write-host "current branch : " $cur_branch

if ($cur_branch -eq 'ice_master') {
	$branch = 'master'
	write-host 'branch =' $branch
} elseif ($cur_branch -eq 'ice_lnl') {
	$branch = 'stable_lnl_pv_20240416'
	write-host 'branch =' $branch
} elseif ($cur_branch -eq 'ice_mtl') {
	$branch = 'stable_mtl_20221221'
	write-host 'branch =' $branch
} else {
    write-host "can not find matched branch name"
}

pause


$branch = 'stable_lnl_pv_20240416'
#$ver = $last_tag

if ($ver -eq 0) {
	$ver = read-host -Prompt "Please enter prebuld ver" 
	write-host "prebuild ver : $($ver)"
} 

if ($branch -eq '') {
	$branch = read-host -Prompt "Please enter branch name" 
	write-host "prebuild branch : $($branch)"
}

Set-Location -Path $workspace
Get-Location

#$branch = 'stable_adlp_pv_cobalt_20210914'
#$branch = 'master'


write-host ">> branch : " $branch
write-host ">> ver : " $ver

$Prebuild_path = '\\ccr.corp.intel.com\ec\proj\iag\peg\icgbj\OSimages\Artifacts\Scheduled\CameraSW\'+ $branch
$Target_ver=''

if ($ver -eq -1){
	write-host "get lastet version..."
	$Lastet_build = Get-ChildItem $Prebuild_path -name | Sort -desc | select -first 1
	Write-Host 'Last build from ICG : ' $Lastet_build
	$Target_ver=$Lastet_build
} else {
	write-host ">> Get Prebuild from $($Prebuild_path)"
    write-host $branch $ver
	$Target_ver = Get-ChildItem $Prebuild_path\* -include "$ver*" -name
}


Write-Host 'Prebuild from ICG : ' $Target_ver
## ctrl c !!!


# parse build version
function SplitPrebuildName {
    param(
        [string]$Text,
        [int] $Index
    )
    if ($Index -lt 0 -or $Index -gt 80){
        return $false
    }
    $_ -match '_'
}

$Icg_ver, $build_date = ($Target_ver -split $function:SplitPrebuildName)[0, 6]
Write-Host 'build_ver :  ' $Icg_ver
Write-Host 'build date : '  $build_date
$Prebuild_local = 'prebuild_' + $Icg_ver

# check if prebuild local exist 
Write-Host 'Check if prebuild local [$Prebuild_local]  exists :'
if (Test-Path -Path $Prebuild_local) {
   Write-Host $Prebuild_local 'already exists! Do nothing.'
	Exit 1
} else {
    Write-Host $Prebuild_local " doesn't exist."
}

# create build dir 
Write-Host 'dest folder : ' $Prebuild_local
New-Item -ItemType directory $Prebuild_local

# copy libs 
Write-Host 'Copy Prebuild librarys ... ' 
$include = @('Intel3A*','lib*.zip','LNL_*.zip','StaticGraph_LNL.zip','lnl_isp_package.zip')
$source = $Prebuild_path + '/' + $Target_ver
Write-Host $source
$childs = Get-ChildItem $source\* -Recurse -Include $include
Write-Host $childs
$childs | Copy-Item -Destination {Join-Path $Prebuild_local $_.FullName.Substring($source.length)} 
Write-Host "copy completed"
pause
#Copy-Item -Path $Prebuild_path\$Target_ver\* -Include $include -Recurse -Destination $Prebuild_local
#Get-ChildItem $Prebuild_local -Name

