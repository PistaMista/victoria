{ config, lib, victoria, ... }:
let
	cfg = config.services.victoria;
in
{
	options.services.victoria = {
		enable = lib.mkEnableOption "Whether to enable Victoria, an AI assistance server.";
	};

	config = lib.mkIf cfg.enable {
		systemd.services.victoria = {
			description = "An all-purpose AI assistant server.";
			wantedBy = [ "multi-user.target" ];
			serviceConfig = {
				ExecStart = "${victoria}/bin/victoria-backend";
			};
		};
	};
}
