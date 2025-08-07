{ pkgs ? import <nixpkgs> {} }:
pkgs.mkShell {
  buildInputs = with pkgs.python313Packages; [
    tkinter
    pillow
  ];

  shellHook = ''
    python3 main.py
  '';
}