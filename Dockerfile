FROM nixos/nix:latest
ENV NIX_CONFIG="experimental-features = nix-command flakes"

WORKDIR /app

COPY . .
RUN nix build

EXPOSE 5001
CMD ./result/bin/victoria-backend