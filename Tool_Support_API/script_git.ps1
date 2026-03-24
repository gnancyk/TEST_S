param (
    [string]$CommitMessage,
    [ValidateSet("o", "n")]
    [string]$DejaFaitGitPull
)

# Si les paramètres ne sont pas fournis, les demander à l'utilisateur
if (-not $CommitMessage) {
    $CommitMessage = Read-Host "Entrez le message du commit"
}

if (-not $DejaFaitGitPull) {
    $DejaFaitGitPull = Read-Host "Avez-vous fait un git pull ? Entrez 'o' pour oui ou 'n' pour non"
}

switch ($DejaFaitGitPull) {
    "n" {
        git pull 
        # origin develop
    }
    "o" {
        Write-Host "Ok, on continue sans faire de git pull."
    }
    Default {
        Write-Host "Réponse invalide. Veuillez entrer 'o' ou 'n'." -ForegroundColor Red
        exit 1
    }
}

git add .
git commit -m "$CommitMessage"
git push 
# origin develop
