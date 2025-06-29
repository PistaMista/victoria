let
  config = {
    allowUnfree = true;
  };
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
        ms-python.python

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
  packages = [
    pkgs.poetry
    pkgs.nodejs_22
    nvim
    vscode
    (pkgs.python3.withPackages (ps: [
      ps.flask
      ps.waitress
      ps.langchain
    ]))
  ];
}
