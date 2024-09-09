let
	config = {
		allowUnfree = true;
	};
	pkgs = import (fetchTarball "https://nixos.org/channels/nixos-unstable/nixexprs.tar.xz") { inherit config; };
	vscode = pkgs.vscode-with-extensions.override {
		vscodeExtensions = with pkgs.vscode-extensions;
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
		];
	};
in pkgs.mkShell {
	packages = [
		pkgs.poetry
		pkgs.nodejs_22
		vscode
		(pkgs.python3.withPackages (ps: [ps.flask ps.waitress ps.langchain]))
	];
}
