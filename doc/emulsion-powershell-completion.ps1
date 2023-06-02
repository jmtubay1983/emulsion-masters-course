# Script de complétion pour la commande "emulsion"


#import subprocess
#
## Vérifier si un profil de démarrage PowerShell existe déjà
#command_check_profile = 'Test-Path $PROFILE'
#result = subprocess.run(['powershell.exe', '-Command', command_check_profile], capture_output=True, text=True)
#profile_exists = result.stdout.strip() == 'True'
#
## Chemin du script à ajouter au profil de démarrage
#script_path = r'C:\chemin\vers\monscript.ps1'  # Remplacez par le chemin d'accès réel de votre script
#
#if not profile_exists:
## Créer un nouveau profil de démarrage
#command_create_profile = 'New-Item -Path $PROFILE -ItemType File -Force'
#subprocess.run(['powershell.exe', '-Command', command_create_profile])
#
## Ajouter le script au profil de démarrage
#command_add_to_profile = f'Add-Content -Path $PROFILE -Value \'& "{script_path}"\''
#subprocess.run(['powershell.exe', '-Command', command_add_to_profile])
#
#print("La configuration du profil de démarrage de PowerShell est terminée.")

## activer le script de complétion quand on active l'environnement conda où est installé EMULSION
## -> script .bat dans miniconda3/envs/myenv/etc/conda/activate.d

function TabComplete-Emulsion {
    [CmdletBinding()]
    param (
        [String]$command,
        [String]$cur,
        [String]$prev
    )

    $cmds = "run", "show", "describe", "diagrams", "plot", "generate"
    $opts = "-r", "-t", "--runs", "--time", "--aggregate", "--detail", "--level", "--seed", "--save", "--load", "--start-id", "--show-seed", "--table-params", "--no-count", "-p", "--param", "--log-params", "--view-model", "--output-dir", "--input-dir", "--figure-dir", "--code-path", "--format", "--silent", "--echo", "--deterministic", "--test", "--init"
    $has_p = $false

    # First argument: command or help or version
    if ($prev -eq $null) {
        $compWords = $cmds + "-V", "--version", "-L", "--license", "-h", "--help"
        $matches = $compWords -like "$cur*"
        $matches
        return
    }

    # Second argument: discard if version/help
    if ($prev -in ("-V", "--version", "-h", "--help", "-L", "--license")) {
        return
    }

    # Identify command
    $command = $command.ToLower()

    # Check if -p|--param already used
    for ($i = 0; $i -lt $prev.Length; $i++) {
        if ($prev[$i] -in ("-p", "--param")) {
            $has_p = $true
        }
    }

    # Some commands accept fewer options
    switch ($command) {
        "generate", "describe" {
            $opts = ""
            break
        }
        "diagrams" {
            $opts = "--output-dir", "--figure-dir", "--format"
            break
        }
        "show" {
            $opts = "--modifiable", "-p", "--param"
            break
        }
        default {
            if ($has_p) {
                $opts = "-p", "--param"
            }
            break
        }
    }

    # Handle MODEL and OPTIONS
    switch ($prev) {
    { $_ -like "*.yaml" } {
    $opts
    break
    }
    "-r", "--runs", "-t", "--time", "--level", "--seed", "--start-id" {
    break
    }
    "--format" {
    $compWords = "png", "pdf", "jpg", "svg"
    $matches = $compWords -like "$cur*"
    $matches
    break
    }
    "-p", "--param" {
    $model = $null
    if ($COMP_WORDS[2] -eq "--plot") {
    $model = $COMP_WORDS[3]
    }
    else {
    $model = $COMP_WORDS[2]
    }

    if ($model) {
    if ($prevModel -eq $null -or $model -ne $prevModel) {
    $prevModel = $model
    $emulsionModelParams = &(emulsion show $model --modifiable)
    }
    }

    $matches = $emulsionModelParams -like "$cur*"
    $matches
    break
    }
    "--output-dir", "--input-dir", "--figure-dir" {
    $compOptions = Get-ChildItem -Directory -Path "." -Filter "$cur*"
    $compOptions.Name
    break
    }
    "--load", "--save" {
    $compOptions = Get-ChildItem -Path "." -Filter "$cur*"
    $compOptions.Name
    break
    }
}

# If at least 3 arguments (command [--plot] model) propose options
if ($prev.Length -ge 3) {
    $matches = $opts -like "$cur*"
    $matches
    return
}

if ($command) {
    $files = Get-ChildItem -Filter "*.yaml" -Name
    if (-not $files) {
        return
    }
    else {
        if ($command -eq "run" -and $prev -ne "--plot") {
            $compWords = "--plot", $files
            $matches = $compWords -like "$cur*"
            $matches
            return
        }
        else {
            $matches = $files -like "$cur*"
            $matches
            return
        }
    }
}
}

Register-ArgumentCompleter -Native -CommandName "emulsion" -ScriptBlock {
param (
[String]$command,
[String]$wordToComplete,
[String]$cursorPosition
)

$wordToComplete = $wordToComplete.Trim()
$cursorPosition = $cursorPosition.Trim()

$commandArray = $wordToComplete.Split()
$currentWordIndex = ($cursorPosition.Split() | Select-Object -Last 1).Trim().Length

$currentWord = $commandArray[$currentWordIndex]

$previousWordIndex = $currentWordIndex - 1
$previousWord = $null
if ($previousWordIndex -ge 0) {
$previousWord = $commandArray[$previousWordIndex]
}

TabComplete-Emulsion -command $command -cur $currentWord -prev $previousWord
}
