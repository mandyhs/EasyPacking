param (
    [Parameter(Mandatory, HelpMessage="usage:  .\extract_prebuild_LNL.ps1 [prebuild_path]") ]
    [string]$prebuild
 )
 
 # modify the code root to your local path
 $code_root = "C:\\Users\\mandyhsi\\workspace\\vieddrv-github\\w\\camerasw\\Master_Sor"
 $workspace = (Get-location).path

$CAMERA_SRC_PATH = $code_root

Set-Location $prebuild
$ICE_PREBUILD_PATH = (Get-location).path

Write-Host 'copy prebuild for LNL'
Write-Host 'from  : '$ICE_PREBUILD_PATH
Write-Host 'to    : '$CAMERA_SRC_PATH

if (Test-Path -Path $ICE_PREBUILD_PATH) {
    Write-Host 'prebuild exists.'
} else {
    Write-Error 'prebuild dose not exists! '$ICE_PREBUILD_PATH
    exit 1
}

Set-Location -Path $CAMERA_SRC_PATH

# create path
new-item -itemtype directory -path ".\\Camera\\Platform\\LNL\\MFTPlugin\\LNL\\Intel3AUniversal" -Verbose -Force
#new-item -itemtype directory -path ".\\Camera\\Platform\\LNL\\MFTPlugin\\LNL\\libsubway\\x64\\LNL" -Verbose -Force
new-item -itemtype directory -path ".\\Camera\\xos\\lnl_isp_package" -Verbose -Force

# extract prebuild
Expand-Archive -Path "$ICE_PREBUILD_PATH\Intel3A_*.zip" -DestinationPath ".\\Camera\\MFTPlugin"  -Verbose -Force
Expand-Archive -Path "$ICE_PREBUILD_PATH\libburstisp_*.zip" -DestinationPath ".\\Camera\\MFTPlugin"  -Verbose -Force
Expand-Archive -Path "$ICE_PREBUILD_PATH\libevcp_*.zip" -DestinationPath ".\\Camera\\MFTPlugin"  -Verbose -Force
Expand-Archive -Path "$ICE_PREBUILD_PATH\libface_*.zip" -DestinationPath ".\\Camera\\MFTPlugin"  -Verbose -Force
Expand-Archive -Path "$ICE_PREBUILD_PATH\libtnr_*.zip" -DestinationPath ".\\Camera\\MFTPlugin"  -Verbose -Force
Expand-Archive -Path "$ICE_PREBUILD_PATH\libexpat_*.zip" -DestinationPath ".\\Camera\\MFTPlugin"  -Verbose -Force
Expand-Archive -Path "$ICE_PREBUILD_PATH\libiacss_*.zip" -DestinationPath ".\\Camera\\MFTPlugin"  -Verbose -Force

# LNL prebuild
Expand-Archive -Path "$ICE_PREBUILD_PATH\LNL_Intel3AUniversal_*.zip" -DestinationPath ".\\Camera\\Platform\\LNL\\MFTPlugin\\LNL\\Intel3AUniversal"  -Verbose -Force
Expand-Archive -Path "$ICE_PREBUILD_PATH\LNL_libsubway_*.zip" -DestinationPath ".\\Camera\\Platform\\LNL\\MFTPlugin\\libsubway\\x64\\LNL"  -Verbose -Force
Expand-Archive -Path "$ICE_PREBUILD_PATH\lnl_isp_package.zip"  -DestinationPath ".\\Camera\\xos\\lnl_isp_package"  -Verbose -Force
Expand-Archive -Path "$ICE_PREBUILD_PATH\StaticGraph_LNL.zip" -DestinationPath ".\\Camera\\xos\\static_graph"  -Verbose -Force

# Remove-Item  '.\\Camera\\Platform\\LNL\\iacamera\\CmdQueueBased\\PSysCtl\\StaticGraphAutogen' -Recurse -Force -Confirm:$false
# Move-Item -Path ".\\Camera\\xos\\static_graph\\StaticGraphAutogen\\"-Destination ".\\Camera\\Platform\\LNL\\iacamera\\CmdQueueBased\\PSysCtl" -Verbose -Force
robocopy ".\\Camera\\xos\\static_graph\\StaticGraphAutogen\\LNL\\" ".\\Camera\\Platform\\LNL\\iacamera\\CmdQueueBased\\PSysCtl\\StaticGraphAutogen\\LNL\\" /mir /v
Remove-Item  '.\\Camera\\xos\\static_graph\\StaticGraphAutogen' -Recurse -Force -Confirm:$false

Set-Location -Path  $workspace
Write-Host 'copy prebuild : done!'

pause
