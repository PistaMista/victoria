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
		user = lib.mkOption {
			type = lib.types.str;
			description = ''
				The user the application runs as.
			'';
			default = "victoria";
		};
		group = lib.mkOption {
			type = lib.types.str;
			description = ''
				The group the application runs as.
			'';
			default = "victoria";
		};
		databaseUrl = lib.mkOption {
			type = lib.types.str;
			description = ''
				Database URL of the database to use.
			'';
		};
	};

	config = lib.mkIf cfg.enable {
		users.users = lib.mkIf (cfg.user == "victoria") {
			victoria = {
				description = "Victoria service";
				useDefaultShell = true;
				group = cfg.group;
				isSystemUser = true;
			};
		};
		
		users.groups = lib.mkIf (cfg.group == "victoria") {
			victoria = { };
		};

		systemd.services.victoria = {
			description = "An all-purpose AI assistant server.";
			wantedBy = [ "multi-user.target" ];
			environment = {
				VICTORIA_ADDRESS = toString cfg.listenAddress;
				VICTORIA_PORT = toString cfg.listenPort;
				VICTORIA_DATABASE_URL = toString cfg.databaseUrl;
			};
			serviceConfig = {
				User = cfg.user;
				Group = cfg.group;
				ExecStart = "${victoria}/bin/victoria-backend -a ${toString cfg.listenAddress} -p ${toString cfg.listenPort}";
			};
		};
	};
}
