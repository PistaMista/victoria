let
  config = {
    allowUnfree = true;
  };
  pkgs-old =
    import (fetchTarball "https://github.com/NixOS/nixpkgs/archive/refs/heads/nixos-24.05.tar.gz")
      { inherit config; };
  pkgs =
    import (fetchTarball "https://github.com/NixOS/nixpkgs/archive/refs/heads/nixos-25.05.tar.gz")
      { inherit config; };
  nvim = pkgs.writers.writeBashBin "nvim" ''
  	${pkgs.neovim}/bin/nvim -u NONE "$@"
  '';
  vscode = pkgs.vscode-with-extensions.override {
    vscodeExtensions =
      with pkgs.vscode-extensions;
      [
        eamodio.gitlens
        nonylene.dark-molokai-theme
        asvetliakov.vscode-neovim
        usernamehw.errorlens
        svelte.svelte-vscode
	pkgs-old.vscode-extensions.ms-python.python
      ]
      ++ pkgs.vscode-utils.extensionsFromVscodeMarketplace [
        {
          name = "git-graph";
          publisher = "mhutchie";
          version = "1.30.0";
          sha256 = "sHeaMMr5hmQ0kAFZxxMiRk6f0mfjkg2XMnA4Gf+DHwA=";
        }
        {
          name = "explorer";
          publisher = "vitest";
          version = "1.20.2";
          sha256 = "sGzmmziX30JS4NDDo+6Si9sTN8F/Sxqmh+WZ/C8x3ls=";
        }
      ];
  };
in
pkgs.mkShell {
  buildInputs = [
    pkgs.poetry
    pkgs.nodejs_22
    pkgs.pylyzer
    nvim
    vscode
  ];

  shellHook = ''
  	poetry install -P victoria-backend
	VENV="$(poetry env info --path -P victoria-backend 2> /dev/null)"
	source "$VENV/bin/activate"
  '';
}
