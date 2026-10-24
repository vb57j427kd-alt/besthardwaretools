$ErrorActionPreference = "Continue"
Set-Location "C:\Users\sy911\.accio\accounts\1740414752_598002\agents\DID-F456DA-22F456DAU1781602-5803-02360F\project\bht-site"
git add -A
git commit -m "Inject trend keywords for cabinet hardware pairing copy"
$env:GIT_SSH_COMMAND = 'ssh -o StrictHostKeyChecking=no -i "C:\Users\sy911\.ssh\id_ed25519_bht"'
git push ssh://git@ssh.github.com:443/vb57j427kd-alt/besthardwaretools.git HEAD:main
Write-Output "LOCAL  $(git rev-parse HEAD)"
