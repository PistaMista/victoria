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
				pkgs = nixpkgs.legacyPackages.${system};
				packageName = "victoria";
				inherit (poetry2nix.lib.mkPoetry2Nix { inherit pkgs; }) mkPoetryApplication defaultPoetryOverrides;

				app = mkPoetryApplication {
					projectDir = ./.;
					overrides = defaultPoetryOverrides.extend
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
				};
			in
			{
				packages.${packageName} = app;
				defaultPackage = self.packages.${system}.${packageName};
				devShell = pkgs.mkShell {
					buildInputs = with pkgs; [ poetry ];
					inputsFrom = builtins.attrValues self.packages.${system};
				};
			}
		) // {
			nixosModules.victoria.imports = [ ./nixos.nix ];
		};
}
