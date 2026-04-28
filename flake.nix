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
        python = prod-pkgs.python313;
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
        prod-venv = pkgSet.mkVirtualEnv "application-env" workspace.deps.default;
        dev-venv = pkgSet.mkVirtualEnv "dev-env" {
          victoria-backend = [ "dev" ];
        };

        backend =
          let
            inherit (prod-pkgs.callPackages pyproject-nix.build.util { }) mkApplication;
          in
          mkApplication {
            venv = prod-venv;
            package = pkgSet.victoria-backend;
          };

        frontend = prod-pkgs.buildNpmPackage {
          name = "victoria-frontend";
          src = ./victoria-frontend;
          npmDepsHash = "sha256-9vBmco/7bk88jQFqRgDpLvpAI1hi4sHgXBirRbVrgG4=";

          buildInputs = with prod-pkgs; [
            nodejs_22
          ];

          installPhase = ''
            cp -r build $out;
          '';
        };

        wrapper = prod-pkgs.writeShellApplication {
          name = "victoria-backend";

          runtimeInputs = [
            # Needed by GitPython
            prod-pkgs.git
          ];

          text = ''
            export VICTORIA_FRONTEND_PATH="${frontend}";
            ${backend}/bin/victoria-backend "$@";
          '';
        };
      in
      {
        packages."victoria-backend" = wrapper;
        defaultPackage = self.packages.${system}."victoria-backend";
        devShell = dev-pkgs.mkShell {
          buildInputs = [
            dev-venv
            dev-pkgs.uv
            dev-pkgs.nodejs_22
          ];

          shellHook = ''
                                                export PATH="${dev-venv}/bin:$PATH"
            export PYTHONPATH="$(${dev-pkgs.git}/bin/git rev-parse --show-toplevel)/victoria-backend"
            export VIRTUAL_ENV="${dev-venv}"
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
          victoria = (self.packages.${pkgs.stdenv.hostPlatform.system}.victoria-backend);
        };
    };
}
