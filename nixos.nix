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
		ollamaAddress = lib.mkOption {
			type = lib.types.str;
			description = ''
				Address of the Ollama server to use.
			'';
			default = "http://localhost:11434";
		};
		ollamaModel = lib.mkOption {
			type = lib.types.str;
			description = ''
				The language model to use with Ollama.
			'';
			default = "llama-3.1";
		};
	};

	config = lib.mkIf cfg.enable {
		systemd.services.victoria = {
			description = "An all-purpose AI assistant server.";
			wantedBy = [ "multi-user.target" ];
			environment = {
				VICTORIA_ADDRESS = toString cfg.listenAddress;
				VICTORIA_PORT = toString cfg.listenPort;
				VICTORIA_OLLAMA_ADDRESS = toString cfg.ollamaAddress;
				VICTORIA_OLLAMA_MODEL = toString cfg.ollamaModel;
			};
			serviceConfig = {
				ExecStart = "${victoria}/bin/victoria-backend -a ${toString cfg.listenAddress} -p ${toString cfg.listenPort}";
			};
		};
	};
}
