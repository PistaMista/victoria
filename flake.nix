{
	description = "An all-purpose AI assistance Ollama proxy.";
	inputs = {
		nixpkgs.url =  "github:NixOS/nixpkgs/nixos-24.05";
		poetry2nix.url = "github:nix-community/poetry2nix";
		flake-utils.url = "github:numtide/flake-utils";
	};

	outputs = {self, nixpkgs, poetry2nix, flake-utils }: 
		flake-utils.lib.eachDefaultSystem (system:
			let
				inherit (poetry2nix.lib.mkPoetry2Nix { inherit pkgs; }) mkPoetryApplication defaultPoetryOverrides;
				backendName = "victoria-backend";
				frontendName = "victoria-frontend";

				pkgs = nixpkgs.legacyPackages.${system};

				poetryOverrides = defaultPoetryOverrides.extend
						(final: prev: {
							langchain-ollama = prev.langchain-ollama.overridePythonAttrs (
								old: {
									buildInputs = (old.buildInputs or [ ]) ++ [ prev.poetry ];
								}
							);
							argparse = prev.argparse.overridePythonAttrs (
								old: {
									buildInputs = (old.buildInputs or [ ]) ++ [ prev.setuptools ];
								}
							);
						});


				backend = mkPoetryApplication {
					projectDir = ./victoria-backend;
					overrides = poetryOverrides;
					preferWheels = true;
				};

				frontend = pkgs.buildNpmPackage {
					name = frontendName;
					src = ./victoria-frontend;
					npmDepsHash = "sha256-yTGs9XbXr7itsA/ukspfDv5ig6mQX262PIf/pqYvb5c=";

					buildInputs = with pkgs; [
						nodejs_22
					];

					installPhase = ''
						cp -r build $out;
					'';
				};

				wrapper = pkgs.writeShellApplication {
					name = backendName;

					runtimeInputs = [ ];

					text = ''
						export FRONTEND_PATH="${frontend}";
						${backend}/bin/victoria-backend "$@";
					'';
				};
			in
			{
				packages.${backendName} = wrapper;
				defaultPackage = self.packages.${system}.${backendName};
				devShell = pkgs.mkShell {
					buildInputs = with pkgs; [ poetry ];
					inputsFrom = builtins.attrValues self.packages.${system};
				};
			}
		) // {
			nixosModules.victoria = {config, lib, pkgs, ... }: import ./nixos.nix { 
				inherit config lib; 
				victoria = (self.packages.${pkgs.system}.victoria-backend);
			}; 
		};
}
