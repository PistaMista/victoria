{ config, lib, ... }:
{
	options.veronica = {
		enable = lib.mkEnableOption "Whether to enable Veronica, an AI assistance server.";
	};

	config = lib.mkIf config.options.services.veronica.enable {
	};
}
