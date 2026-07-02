{
  description = "nirviz - Visualisation tool for the Neuromorphic Intermediate Representation";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs }:
    let
      systems = [ "x86_64-linux" "aarch64-linux" "x86_64-darwin" "aarch64-darwin" ];
      forAllSystems = f: nixpkgs.lib.genAttrs systems (system: f system nixpkgs.legacyPackages.${system});
    in
    {
      packages = forAllSystems (system: pkgs:
        let
          # `nir` isn't packaged in nixpkgs, so build it here from the
          # published wheel to keep this flake self-contained.
          nir = pkgs.python312Packages.buildPythonPackage {
            pname = "nir";
            version = "1.0.5";
            format = "wheel";
            src = pkgs.fetchurl {
              url = "https://files.pythonhosted.org/packages/ef/92/ee79336f60429a4f0ced67fcdccaaa98eed53d4918ae407b3dc12cce39f7/nir-1.0.5-py3-none-any.whl";
              sha256 = "sha256-jhEtjKv/8LRAwZ2j0CTBjI1lwssgxPeUxfAhzJv0sIQ=";
            };
            propagatedBuildInputs = with pkgs.python312Packages; [ numpy h5py ];
          };

          nirviz = pkgs.python312Packages.buildPythonPackage {
            pname = "nirviz";
            version = "0.1.0";
            pyproject = true;
            src = ./.;
            build-system = with pkgs.python312Packages; [ setuptools setuptools-scm ];
            propagatedBuildInputs = with pkgs.python312Packages; [ nir graphviz pyyaml pillow ];

            pythonImportsCheck = [ "nirviz" ];
          };
        in
        {
          default = nirviz;
          inherit nirviz nir;
        });

      apps = forAllSystems (system: pkgs: {
        default = {
          type = "app";
          program = "${pkgs.writeShellScriptBin "nirviz" ''
            export PATH=${pkgs.lib.makeBinPath [ pkgs.graphviz ]}:$PATH
            exec ${pkgs.python312.withPackages (ps: [ self.packages.${system}.nirviz ])}/bin/python -m nirviz "$@"
          ''}/bin/nirviz";
        };
      });

      devShells = forAllSystems (system: pkgs: {
        default = pkgs.mkShell {
          packages = [
            (pkgs.python312.withPackages (ps: with ps; [
              self.packages.${system}.nir
              graphviz
              pyyaml
              pillow
            ]))
            pkgs.graphviz
          ];

          shellHook = ''
            export PYTHONPATH="$PWD:$PYTHONPATH"
          '';
        };
      });
    };
}
