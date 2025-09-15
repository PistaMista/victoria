{
  description = "An all-purpose AI assistance Ollama proxy.";
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    dev-pkgs.url = "github:NixOS/nixpkgs/nixos-25.05";
    dev-pkgs-old.url = "github:NixOS/nixpkgs/nixos-24.05";
    flake-utils.url = "github:numtide/flake-utils";

    pyproject-nix = {
      url = "github:pyproject-nix/pyproject.nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };

    uv2nix = {
      url = "github:pyproject-nix/uv2nix";
      inputs.pyproject-nix.follows = "pyproject-nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };

    pyproject-build-systems = {
      url = "github:pyproject-nix/build-system-pkgs";
      inputs.pyproject-nix.follows = "pyproject-nix";
      inputs.uv2nix.follows = "uv2nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs =
    {
      self,
      flake-utils,

      uv2nix,
      pyproject-nix,
      pyproject-build-systems,
      ...
    }@inputs:
    flake-utils.lib.eachDefaultSystem (
      system:
      let
        prod-pkgs = import inputs.nixpkgs { inherit system; };
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

        backend =
          let
            workspace = uv2nix.lib.workspace.loadWorkspace {
              workspaceRoot = ./victoria-backend;
            };
            overlay = workspace.mkPyprojectOverlay {
              sourcePreference = "wheel";
            };
            pyprojectOverrides = (
              final: prev: {
              }
            );
            python = prod-pkgs.python312;
            pkgSet =
              (prod-pkgs.callPackage pyproject-nix.build.packages {
                inherit python;
              }).overrideScope
                (
                  prod-pkgs.lib.composeManyExtensions [
                    pyproject-build-systems.overlays.default
                    overlay
                    pyprojectOverrides
                  ]
                );
            inherit (prod-pkgs.callPackages pyproject-nix.build.util { }) mkApplication;
          in
          mkApplication {
            venv = pkgSet.mkVirtualEnv "application-env" workspace.deps.default;
            package = pkgSet.victoria-backend;
          };

        frontend = prod-pkgs.buildNpmPackage {
          name = "victoria-frontend";
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
          name = "victoria-backend";

          runtimeInputs = [ ];

          text = ''
            export VICTORIA_FRONTEND_PATH="${frontend}";
            ${backend}/bin/victoria-backend "$@";
          '';
        };
      in
      {
        packages."victoria-backend" = wrapper;
        defaultPackage = self.packages.${system}."victoria-backend";
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
              dev-pkgs.uv
              dev-pkgs.nodejs_22
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
