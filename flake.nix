{
  description = "An all-purpose AI assistance Ollama proxy.";
  inputs = {
    prod-pkgs.url = "github:NixOS/nixpkgs/nixos-24.05";
    dev-pkgs.url = "github:NixOS/nixpkgs/nixos-25.05";
    dev-pkgs-old.url = "github:NixOS/nixpkgs/nixos-24.05";
    poetry2nix.url = "github:nix-community/poetry2nix";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs =
    {
      self,
      poetry2nix,
      flake-utils,
      ...
    }@inputs:
    flake-utils.lib.eachDefaultSystem (
      system:
      let
        inherit (poetry2nix.lib.mkPoetry2Nix { pkgs = prod-pkgs; })
          mkPoetryApplication
          defaultPoetryOverrides
          ;
        backendName = "victoria-backend";
        frontendName = "victoria-frontend";

        prod-pkgs = import inputs.prod-pkgs { inherit system; };
        dev-pkgs = import inputs.dev-pkgs {
          inherit system;
          config = {
            allowUnfreePredicate =
              pkg:
              builtins.elem (prod-pkgs.lib.getName pkg) [
                "vscode"
                "vscode-with-extensions"
              ];
          };
        };
        dev-pkgs-old = import inputs.dev-pkgs-old { inherit system; };

        poetryOverrides = defaultPoetryOverrides.extend (
          final: prev: {
            langchain-ollama = prev.langchain-ollama.overridePythonAttrs (old: {
              buildInputs = (old.buildInputs or [ ]) ++ [ prev.poetry ];
            });
            argparse = prev.argparse.overridePythonAttrs (old: {
              buildInputs = (old.buildInputs or [ ]) ++ [ prev.setuptools ];
            });
          }
        );

        backend = mkPoetryApplication {
          projectDir = ./victoria-backend;
          overrides = poetryOverrides;
          preferWheels = true;

          # Copy database migration scripts
          postInstall = ''
            mkdir -p $out/share/victoria-backend
            cp -r ${./victoria-backend/alembic} $out/lib/python3.11/site-packages/alembic
          '';
        };

        frontend = prod-pkgs.buildNpmPackage {
          name = frontendName;
          src = ./victoria-frontend;
          npmDepsHash = "sha256-3+hHRpk7isnvp2730/SXkjZaXWW5meNWHMR/1aK7bis=";

          buildInputs = with prod-pkgs; [
            nodejs_22
          ];

          installPhase = ''
            cp -r build $out;
          '';
        };

        wrapper = prod-pkgs.writeShellApplication {
          name = backendName;

          runtimeInputs = [ ];

          text = ''
            export VICTORIA_FRONTEND_PATH="${frontend}";
            ${backend}/bin/victoria-backend "$@";
          '';
        };
      in
      {
        packages.${backendName} = wrapper;
        defaultPackage = self.packages.${system}.${backendName};
        devShell =
          let
            nvim = dev-pkgs.writers.writeBashBin "nvim" ''
              ${dev-pkgs.neovim}/bin/nvim -u NONE "$@"
            '';
            vscode = dev-pkgs.vscode-with-extensions.override {
              vscodeExtensions =
                with dev-pkgs.vscode-extensions;
                [
                  eamodio.gitlens
                  nonylene.dark-molokai-theme
                  asvetliakov.vscode-neovim
                  usernamehw.errorlens
                  svelte.svelte-vscode
                  dev-pkgs-old.vscode-extensions.ms-python.python
                  dev-pkgs-old.vscode-extensions.ms-python.debugpy
                ]
                ++ dev-pkgs.vscode-utils.extensionsFromVscodeMarketplace [
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
          dev-pkgs.mkShell {
            buildInputs = [
              dev-pkgs.poetry
              dev-pkgs.nodejs_22
              nvim
              vscode
            ];

            shellHook = ''
              export DB_USER="user"
              export DB_PASS="pass"
              # FOR USE IN TESTING, NOT PRODUCTION!
              export VICTORIA_JWT_SECRET="d2e74cd1a54c4b8b90f215f5bcd057fbb10b2c23a1615ca49edeee0415f5b055"
            '';
          };
      }
    )
    // {
      nixosModules.victoria =
        {
          config,
          lib,
          pkgs,
          ...
        }:
        import ./nixos.nix {
          inherit config lib;
          victoria = (self.packages.${pkgs.system}.victoria-backend);
        };
    };
}
