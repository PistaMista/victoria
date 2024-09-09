{ config, lib, victoria, ... }:
let
	cfg = config.services.victoria;
in
{
	options.services.victoria = {
		enable = lib.mkEnableOption "Whether to enable Victoria, an AI assistance server.";
		listenAddress = lib.mkOption {
			type = lib.types.str;
			description = ''
				The address to listen on.
			'';
			default = "0.0.0.0";
		};
		listenPort = lib.mkOption {
			type = lib.types.int;
			description = ''
				The port to listen on.
			'';
			default = 5001;
		};
	};

	config = lib.mkIf cfg.enable {
		systemd.services.victoria = {
			description = "An all-purpose AI assistant server.";
			wantedBy = [ "multi-user.target" ];
			serviceConfig = {
				ExecStart = "${victoria}/bin/victoria-backend -a ${toString cfg.listenAddress} -p ${toString cfg.listenPort}";
			};
		};
	};
}
