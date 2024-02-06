# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

# This script is specifically used on Windows Server Core based docker images

# Set TLS to 1.2 so SSL/TLS can be enabled for downloading artifacts
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

# Install Scoop as Administrator User here
iex "& {$(irm get.scoop.sh)} -RunAsAdmin"

# Disable "current" alias directory as it is not preserved after AMI creation
# Use static path in environment variable
scoop config no_junction true

# Install git
scoop install git
git --version
# Path for git windows usr bin
$fileName = 'nohup.exe'
$fileDir = 'C:\\Users\\ContainerAdministrator\\scoop\\apps\\git'
$fileFound = (Get-ChildItem -Path $fileDir -Filter $fileName -Recurse | %{$_.FullName} | select -first 1)
$fileFound
$gitPathFound = $fileFound.replace("$fileName", '')
$gitPathFound
# Add to EnvVar
$userenv = [System.Environment]::GetEnvironmentVariable("Path", [System.EnvironmentVariableTarget]::User)
[System.Environment]::SetEnvironmentVariable("PATH", $userenv + ";$gitPathFound", [System.EnvironmentVariableTarget]::User)
# Make sure mem size are set to avoid "Out of memory, malloc failed" issues on Windows
git config --system core.packedGitLimit 128m
git config --system core.packedGitWindowSize 128m
git config --system core.longPaths true
git config --system pack.deltaCacheSize 128m
git config --system pack.packSizeLimit 128m
git config --system pack.windowMemory 128m
git config --system pack.window 0
git config --system pack.threads 1
git config --system core.compression 0
git config --system protocol.version 1
git config --system --list
# Rename system32 find.exe in case it gets conflicted with POSIX find
bash.exe -c "mv -v 'C:\\Windows\\System32\\find.exe' 'C:\\Windows\\System32\\find_windows.exe'"

# Add some sleep due to a potential race condition
Start-Sleep -Seconds 5

# Setup Repos (This has to happen after git is installed or will error out)
scoop bucket add java
scoop bucket add versions
scoop bucket add extras
scoop bucket add github-gh https://github.com/cli/scoop-gh.git

# Install mingw for k-NN specific requirements with renaming
# Try to lock on to 12.2.0-rt_v10-rev1 as the newer versions on scoop pointed to the ucrt version to replace legacy msvcrt
# https://github.com/opensearch-project/k-NN/issues/829#issuecomment-1499846457
scoop install https://raw.githubusercontent.com/ScoopInstaller/Main/dad0cee42bb2c0be7acf9f341fba2a55e415e0f2/bucket/mingw.json
$libName = 'libgfortran-5.dll'
$libNameRequired = 'libgfortran-3.dll'
$libDir = 'C:\\Users\\ContainerAdministrator\\scoop\\apps\\mingw'
$libFound = (Get-ChildItem -Path $libDir -Filter $libName -Recurse | %{$_.FullName} | select -first 1)
$libFound
$libPathFound = $libFound.replace("$libName", '')
$libPathFound
mv -v "$libFound" "$libPathFound\\$libNameRequired"
# Add MINGW_BIN path to User Env Var for k-NN to retrieve libs
[System.Environment]::SetEnvironmentVariable("MINGW_BIN", "$libPathFound", [System.EnvironmentVariableTarget]::User)

# Install zlib for k-NN compilation requirements
scoop install zlib
# Reg PEP
$zlibVersionInfo = (scoop info zlib | out-string -stream | Select-String 'Version.*:')
$zlibVersionNumber = ($zlibVersionInfo -split ':' | select -last 1)
$zlibVersionNumber = $zlibVersionNumber.Trim()
$zlibHome = "C:\\Users\\ContainerAdministrator\\scoop\\apps\\zlib\\$zlibVersionNumber"
$zlibRegFilePath = "$zlibHome\\register.reg"
$zlibRegFilePath
regedit /s $zlibRegFilePath

# Install jdk
# Temurin jdk does not have all the versions supported on scoop, especially version 14, 20, and above
# As of now we will mix temurin and openjdk as temurin for production has support policies for fixes and patches
# We need to make sure we do not mis-install temurin and openjdk with the same version or the distribution build code will have issues
$jdkVersionList = "temurin8-jdk JAVA8_HOME", "temurin11-jdk JAVA11_HOME", "openjdk14 JAVA14_HOME", "temurin17-jdk JAVA17_HOME", "temurin19-jdk JAVA19_HOME", "openjdk20 JAVA20_HOME", "temurin21-jdk JAVA21_HOME"
Foreach ($jdkVersion in $jdkVersionList)
{
    $jdkVersion
    $jdkArray = $jdkVersion.Split(" ")
    $jdkArray[0]
    $jdkArray[1]
    scoop install $jdkArray[0]
    $JAVA_HOME_TEMP = [System.Environment]::GetEnvironmentVariable("JAVA_HOME", [System.EnvironmentVariableTarget]::User).replace("\", "/")
    $JAVA_HOME_TEMP
    [System.Environment]::SetEnvironmentVariable($jdkArray[1], "$JAVA_HOME_TEMP", [System.EnvironmentVariableTarget]::User)
    java -version
}
# Switch to temurin11-jdk as it is the widest supported version to build OpenSearch
scoop reset temurin11-jdk
$JAVA_HOME_TEMP = [System.Environment]::GetEnvironmentVariable("JAVA_HOME", [System.EnvironmentVariableTarget]::User).replace("\", "/")
$JAVA_HOME_TEMP
[System.Environment]::SetEnvironmentVariable('JAVA_HOME', "$JAVA_HOME_TEMP", [System.EnvironmentVariableTarget]::User)
java -version

# Install python and lock onto 3.9.13 now
scoop install https://raw.githubusercontent.com/ScoopInstaller/Versions/cadc6e36c880e99965d4b8e1f1bf81e91421ec97/bucket/python39.json
python --version
# Reg PEP
$versionInfo = (scoop info python39 | out-string -stream | Select-String 'Version.*:')
$versionInfo
$versionNumber = ($versionInfo -split ':' | select -last 1)
$versionNumber
$versionNumber = $versionNumber.Trim()
$versionNumber
$pythonHome = "C:\\Users\\ContainerAdministrator\\scoop\\apps\\python39\\$versionNumber"
$pythonHome
$pythonLibHome = "$pythonHome\\Lib"
$pythonLibHome
$regFilePath = "$pythonHome\\install-pep-514.reg"
$regFilePath
regedit /s $regFilePath
# Windows AMI does not preserve alias directory, copy all the files to an actual directory
New-Item -Path "$pythonHome\\Scripts_temp" -ItemType Directory
Copy-Item -Path "$pythonHome\\Scripts\\*" -Destination "$pythonHome\\Scripts_temp\\"
Remove-Item "$pythonHome\\Scripts" -Force -Recurse
Rename-Item "$pythonHome\\Scripts_temp" "$pythonHome\\Scripts"
# Same as above but different dir
New-Item -Path "$pythonLibHome\\site-packages_temp" -ItemType Directory
Copy-Item -Path "$pythonLibHome\\site-packages\\*" -Destination "$pythonLibHome\\site-packages_temp\\"
Remove-Item "$pythonLibHome\\site-packages" -Force -Recurse
Rename-Item "$pythonLibHome\\site-packages_temp" "$pythonLibHome\\site-packages"

# Install maven
scoop install maven
mvn --version

# Install jq 1.6
scoop install https://raw.githubusercontent.com/ScoopInstaller/Main/96316b49652d5c9672960b39db141962ad4210b0/bucket/jq.json
jq --version

# Install yq 4.34.2
scoop install https://raw.githubusercontent.com/ScoopInstaller/Main/1e9c8b3dfa5ebe7a8c270daf7355aa1db9926e00/bucket/yq.json
yq --version

# Install volta to replace nvm on Windows as Windows is not able to handle symlink after AMI creation
# While Volta is using a fixed location and switch binary version automatically for the Windows Agent
# As of now, volta is locked to version 1.0.8 due to issues installing yarn within docker container
# https://github.com/opensearch-project/opensearch-ci/issues/281#issuecomment-1654424423
scoop install https://raw.githubusercontent.com/ScoopInstaller/Main/49d6f71e5bd7096d49b3286ad02d5d482726b467/bucket/volta.json
volta --version
$nodeVersionList = "10.24.1","14.19.1","14.20.0", "14.20.1", "14.21.3", "16.20.0", "18.16.0"
Foreach ($nodeVersion in $nodeVersionList)
{
    $nodeVersion
    volta install "node@$nodeVersion"
    node -v
}
$ref = "main"
$JSON_BASE = "https://raw.githubusercontent.com/opensearch-project/OpenSearch-Dashboards/$ref/package.json"
$yarnVersion = (curl.exe -s -o- $JSON_BASE | yq.exe -r '.engines.yarn')
$yarnVersion
volta install yarn@$yarnVersion
yarn --version
# Temporarily comment out cypress caching due to performance issues on Windows startup
# The opensearch-dashboards-functional-test repo can still run tests
# as cypress will be installed globally by `npm install` when running integtest.sh
# https://github.com/opensearch-project/opensearch-ci/issues/297
# $cypressVersionList = "5.6.0", "9.5.4", "12.13.0"
# Foreach ($cypressVersion in $cypressVersionList)
# {
#     $cypressVersion
#     volta install "cypress@$cypressVersion"
#     cypress --version
# }
$userenv2 = [System.Environment]::GetEnvironmentVariable("Path", [System.EnvironmentVariableTarget]::User)
$nodePathFixed = "C:\\Users\\ContainerAdministrator\\scoop\\persist\\volta\\appdata\\bin"
[System.Environment]::SetEnvironmentVariable("PATH", $userenv2 + ";$nodePathFixed", [System.EnvironmentVariableTarget]::User)

# Install chromium (internally it is chrome.exe in app directory)
# Lock chromium to v114.0.5735.134-r1135570 due to https://github.com/opensearch-project/opensearch-build/issues/4241
scoop install https://raw.githubusercontent.com/ScoopInstaller/Extras/6befedcb5296cacbb0428e76baab7368609b6006/bucket/chromium.json
$chromiumName = 'chrome.exe'
$chromiumDir = 'C:\\Users\\ContainerAdministrator\\scoop\\apps\\chromium'
$chromiumFound = (Get-ChildItem -Path $chromiumDir -Filter $chromiumName -Recurse | %{$_.FullName} | select -first 1)
$chromiumFound
# Add BROWSER_PATH path to User Env Var for cypress test to retrieve chromium.exe path
[System.Environment]::SetEnvironmentVariable("BROWSER_PATH", "$chromiumFound", [System.EnvironmentVariableTarget]::User)

# Install fonts for the chromium-based browsers: https://github.com/opensearch-project/opensearch-build/issues/4416
# Based on this repo: https://github.com/gantrior/docker-chrome-windows
# From this issue: https://github.com/docker/for-win/issues/3438
curl.exe -SLO https://ci.opensearch.org/ci/dbc/tools/FontsToAdd.tar
tar -xvf FontsToAdd.tar
.\\Add-Font.ps1 Fonts
rm -v FontsToAdd.tar
rm -v Add-Font.ps1
rm -v -r -force Fonts

# Install ruby24
scoop install ruby24
ruby --version

# Install gh
scoop install gh
gh version

# Install dev tools
# Lock to 3.23.3
scoop install https://raw.githubusercontent.com/ScoopInstaller/Main/56eed69c3bf04110e306f77ad45cfc8c1c5bb9bc/bucket/cmake.json
cmake --version

# Install zip
scoop install zip
scoop install unzip

# Install docker
# Lock Docker 24.0.7
# Lock Docker-Compose 2.23.0
# https://github.com/opensearch-project/opensearch-build/issues/4126
scoop install https://raw.githubusercontent.com/ScoopInstaller/Main/f7cf8513558307e90b483ddff2394a023e894ccf/bucket/docker.json
scoop install https://raw.githubusercontent.com/ScoopInstaller/Main/a6a7d8e2a7eecb13fb7200952c9bcea4eaeeb994/bucket/docker-compose.json

# Scoop cleanup
scoop cache rm *

# Pip
wget https://bootstrap.pypa.io/get-pip.py -OutFile get-pip.py
python get-pip.py
pip --version
# Install pipenv
pip install pipenv==2023.6.12
pipenv --version
# Install awscli
pip install awscli==1.32.17
aws --version
# Cleanup
pip cache remove * 
Remove-Item 'get-pip.py' -Force

# Refresh env vars
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

# Enable Long Path
set-ItemProperty -Path HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem LongPathsEnabled -Type DWORD -Value 1 -Force

