{
	description = "My testing Python app with Flakes";
	inputs = {
		nixpkgs.url =  "github:NixOS/nixpkgs/release-24.05";
	};

	outputs = {self, nixpkgs }: {
		defaultPackages.x86_64-linux = with import nixpkgs { system = "x86_64-linux"; }; hello;

	};
}
