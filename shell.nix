let 
	pkgs = import <nixpkgs> {};
in
pkgs.mkShell {
	buildInputs = with pkgs; [
		(python312.withPackages (pp: [
			pp.langchain		
		]))
	];
}


