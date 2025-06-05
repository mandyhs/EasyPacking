param (
    [Parameter(Mandatory, HelpMessage="usage:  .\extract_prebuild_PTL.ps1 [prebuild_path]") ]
    [string]$prebuild
 )
 
 # modify the code root to your local path
 $code_root = "C:\\Users\\mandyhsi\\workspace\\vieddrv-github\\w\\camerasw\\Master_Sor"
 $workspace = (Get-location).path

$CAMERA_SRC_PATH = $code_root

Set-Location $prebuild
$ICE_PREBUILD_PATH = (Get-location).path

Write-Host 'copy prebuild for PTL'
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
new-item -itemtype directory -path ".\\Camera\\xos\\ptl_isp_package" -Verbose -Force
new-item -itemtype directory -path ".\\Camera\\MFTPlugin\\libUtility" -Verbose -Force

# extract prebuild
Expand-Archive -Path "$ICE_PREBUILD_PATH\Intel3A_*.zip" -DestinationPath ".\\Camera\\MFTPlugin"  -Verbose -Force
# Expand-Archive -Path "$ICE_PREBUILD_PATH\libburstisp_*.zip" -DestinationPath ".\\Camera\\MFTPlugin"  -Verbose -Force
# Expand-Archive -Path "$ICE_PREBUILD_PATH\libevcp_*.zip" -DestinationPath ".\\Camera\\MFTPlugin"  -Verbose -Force

Expand-Archive -Path "$ICE_PREBUILD_PATH\libUtility_*.zip" -DestinationPath ".\\Camera\\MFTPlugin\\libUtility"  -Verbose -Force
Expand-Archive -Path "$ICE_PREBUILD_PATH\libface_*.zip" -DestinationPath ".\\Camera\\MFTPlugin"  -Verbose -Force
Expand-Archive -Path "$ICE_PREBUILD_PATH\libtnr_*.zip" -DestinationPath ".\\Camera\\MFTPlugin"  -Verbose -Force
# Expand-Archive -Path "$ICE_PREBUILD_PATH\libexpat_*.zip" -DestinationPath ".\\Camera\\MFTPlugin"  -Verbose -Force
# Expand-Archive -Path "$ICE_PREBUILD_PATH\libiacss_*.zip" -DestinationPath ".\\Camera\\MFTPlugin"  -Verbose -Force

# PTL prebuild
Expand-Archive -Path "$ICE_PREBUILD_PATH\PTL_Intel3AUniversal_*.zip" -DestinationPath ".\\Camera\\MFTPlugin\\PTL\\Intel3AUniversal"  -Verbose -Force
#Expand-Archive -Path "$ICE_PREBUILD_PATH\PTL_libsubway_*.zip" -DestinationPath ".\\Camera\\Platform\\LNL\\MFTPlugin\\libsubway\\x64\\PTL"  -Verbose -Force
Expand-Archive -Path "$ICE_PREBUILD_PATH\ptl_isp_package.zip"  -DestinationPath ".\\Camera\\xos\\ptl_isp_package"  -Verbose -Force
Expand-Archive -Path "$ICE_PREBUILD_PATH\StaticGraph_PTL.zip" -DestinationPath ".\\Camera\\xos\\static_graph"  -Verbose -Force

#Expand-Archive -Path "$ICE_PREBUILD_PATH\PTL_Intel3AUniversal_*.zip" -DestinationPath ".\\Camera\\MFTPlugin\\PTL\\Intel3AUniversal"  -Verbose -Force
Expand-Archive -Path "$ICE_PREBUILD_PATH\PTL_libsubway_*.zip" -DestinationPath ".\\Camera\\MFTPlugin\\libsubway\\x64\\PTL"  -Verbose -Force
#Expand-Archive -Path "$ICE_PREBUILD_PATH\ptl_isp_package.zip"  -DestinationPath ".\\Camera\\xos\\ptl_isp_package"  -Verbose -Force
#Expand-Archive -Path "$ICE_PREBUILD_PATH\StaticGraph_PTL.zip" -DestinationPath ".\\Camera\\xos\\static_graph"  -Verbose -Force

# Remove-Item  '.\\Camera\\Platform\\LNL\\iacamera\\CmdQueueBased\\PSysCtl\\StaticGraphAutogen' -Recurse -Force -Confirm:$false
# Move-Item -Path ".\\Camera\\xos\\static_graph\\StaticGraphAutogen\\"-Destination ".\\Camera\\Platform\\LNL\\iacamera\\CmdQueueBased\\PSysCtl" -Verbose -Force
robocopy ".\\Camera\\xos\\static_graph\\StaticGraphAutogen\\PTL\\" ".\\Camera\\iacamera\\CmdQueueBased\\PSysCtl\\StaticGraphAutogen\\PTL\\" /mir /v
Remove-Item  '.\\Camera\\xos\\static_graph\\StaticGraphAutogen' -Recurse -Force -Confirm:$false

Set-Location -Path  $workspace
Write-Host 'copy prebuild : done!'

pause
