{ pkgs }: {
  deps = [
    pkgs.python311
    pkgs.python311Packages.tkinter
    pkgs.python311Packages.matplotlib
    pkgs.python311Packages.numpy
  ];
}