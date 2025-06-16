{ pkgs }: {
  deps = [
    pkgs.python311
    pkgs.python311Packages.streamlit
    pkgs.python311Packages.numpy
    pkgs.python311Packages.matplotlib
  ];
}